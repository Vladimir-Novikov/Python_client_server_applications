import pickle
from socket import socket, AF_INET, SOCK_STREAM
import time
import sys
from select import select
import argparse
import logging
from logs._server_log_decorator import log


# from logs import _server_log_config

"""Раскомментировать этот код в случае применения _client_log_config (без декораторов)"""
# logger = logging.getLogger("app.server")
# logger.info("app start")


"""
декоратор mockable тестируется на функциях: authenticate(), quit_s(), presence()
для этого DEBUG = TRUE и запуск модуля server.py
в консоли выйдyт сообщения response 
"""
DEBUG = False
test_data = {
    "user": {"account_name": "user_mock", "password": "123"},
}


def mockable(func):
    def wrap(*args, **kwargs):
        result = func(**test_data) if DEBUG else func(*args, **kwargs)
        if DEBUG:
            print(result)
        return result

    return wrap


@log()
# обработка командной строки с параметрами
def createParser():
    # logger.info("parser start")
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default="7777")
    parser.add_argument("-a", "--addr", default="0.0.0.0")
    parser.error = myerror
    return parser


@log(level="error")
def myerror(message):
    # logger.error(f"parser wrong argument: {message}")
    # print(f"Применен недопустимый аргумент {message}")
    return f"Применен недопустимый аргумент {message}"


@log(level="info", return_values=2)
def checking_data(message):
    if len(message) > 640:  # проверка длины пакета
        # logger.error("Длина пакета больше 640")
        return {
            "response": 400,
            "time": time.time(),
            "error": "Длина объекта больше 640 символов",
        }  # неправильный запрос/JSON-объект;

    dict_of_commands = {
        "authenticate": authenticate,
        "presence": presence,
        "msg": msg,
        "quit": quit_s,  # т.к. в python есть ф-ция quit - определил для ф-ции другое имя
        "join": join,
        "leave": leave,
        "create": create,
    }
    data = pickle.loads(message)
    action = data["action"]
    if action not in dict_of_commands:
        # logger.error("wrong command in message")
        return {"response": 404, "time": time.time(), "error": f"Неизвестная команда {action}"}
    processing_the_action = dict_of_commands[action]  # находим в словаре обработчик и присваиваем его переменной
    # logger.info(f"processing {action}")
    return processing_the_action(**data)  # выполняем нужную функцию


authorized_users = ["all"]
chat_rooms = {}


@log(level="info", return_values=2)
@mockable
def authenticate(**kwargs):  # пароль не запрашивается на данном этапе разработки
    user_name = kwargs["user"]["account_name"]
    if user_name in authorized_users:
        # logger.warning(f"уже имеется подключение с указанным логином {user_name}")
        return {
            "response": 409,
            "time": time.time(),
            "alert": f"уже имеется подключение с указанным логином {user_name} ",
        }
    authorized_users.append(user_name)
    # logger.info(f"Пользователь {user_name} успешно авторизован")
    return {"response": 200, "time": time.time(), "alert": f"Пользователь {user_name} успешно авторизован"}


@log(level="info", return_values=2)
@mockable
def presence(**kwargs):
    user_name = kwargs["user"]["account_name"]
    if user_name in authorized_users:
        # logger.info(f"presence {user_name} присутсвует в списке подключенных пользователей")
        return {
            "response": 200,
            "time": time.time(),
            "alert": f"Хорошо, {user_name} присутсвует в списке подключенных пользователей",
        }
    # logger.error(f"response 404 пользователь {user_name} отсутствует на сервере")
    return {"response": 404, "time": time.time(), "error": f"пользователь {user_name} отсутствует на сервере"}


@log(level="info", return_values=2)
def msg(**kwargs):
    from_user = kwargs["from"]
    to_user = kwargs["to"]
    message = kwargs["message"]
    if from_user not in authorized_users:
        # logger.error(f"response 401 Пользователь {from_user} не авторизован")
        return {"response": 401, "time": time.time(), "alert": f"Пользователь {from_user} не авторизован"}

    if to_user[0] == "#":
        chat = to_user[1:]
        if chat not in chat_rooms:
            # logger.error(f"response 404 error Чат {chat} пока не создан")
            return {"response": 404, "time": time.time(), "error": f"Чат {chat} пока не создан"}
        # logger.info(f"Сообщение от {from_user} успешно доставлено в чат {chat}")
        return {
            "response": 200,
            "time": time.time(),
            "alert": f"Сообщение от {from_user} успешно доставлено в чат {chat}",
        }
    if to_user not in authorized_users:
        # logger.error(f"response 404 Пользователь {to_user} на сервере не зарегистрирован")
        return {"response": 404, "time": time.time(), "alert": f"Пользователь {to_user} на сервере не зарегистрирован"}

    # return {"response": 200, "time": time.time(), "alert": f"Сообщение от {from_user} успешно доставлено {to_user}"}
    # logger.info(f"Сообщение от {from_user} успешно доставлено {to_user}")
    return {
        "response": 200,
        "time": time.time(),
        "alert": f"Сообщение от {from_user} успешно доставлено {to_user}",
        "msg": f"{message}",
    }


@log(level="info", return_values=2)
@mockable
def quit_s(**kwargs):
    user_name = kwargs["user"]["account_name"]
    if user_name in authorized_users:
        authorized_users.remove(user_name)
        # logger.info(f"Пользователь {user_name} успешно отключен от сервера")
        return {"response": 200, "time": time.time(), "alert": f"Пользователь {user_name} успешно отключен от сервера"}
    # logger.error(f"response 404 Пользователь {user_name} на сервере не зарегистрирован")
    return {"response": 404, "time": time.time(), "error": f"Пользователь {user_name} на сервере не зарегистрирован"}


@log(level="info", return_values=2)
def join(**kwargs):
    chat_name = kwargs["chat_name"]
    user = kwargs["from"]
    if user not in authorized_users:
        # logger.error(f"response 404 пользователь {user} отсутствует на сервере")
        return {"response": 404, "time": time.time(), "error": f"пользователь {user} отсутствует на сервере"}
    if chat_name in chat_rooms:
        if user not in chat_rooms[chat_name]:
            chat_rooms[chat_name].append(user)
            # logger.info(f"Пользователь {user} добавлен в {chat_name}")
            return {
                "response": 200,
                "time": time.time(),
                "alert": f"Пользователь {user} добавлен в {chat_name} ",
            }
        # logger.error(f"response 409 Пользователь {user} уже присутствует в чате {chat_name}")
        return {
            "response": 409,
            "time": time.time(),
            "error": f"Пользователь {user} уже присутствует в чате {chat_name}  ",
        }
    # logger.error(f"response 409 Чат {chat_name} пока не создан")
    return {
        "response": 409,
        "time": time.time(),
        "error": f"Чат {chat_name} пока не создан",
    }


@log(level="info", return_values=2)
def leave(**kwargs):
    chat_name = kwargs["chat_name"]
    user = kwargs["from"]
    if user not in authorized_users:
        # logger.error(f"response 404 пользователь {user} отсутствует на сервере")
        return {"response": 404, "time": time.time(), "error": f"пользователь {user} отсутствует на сервере"}
    if chat_name in chat_rooms:
        if user in chat_rooms[chat_name]:
            chat_rooms[chat_name].remove(user)
            # logger.info(f"Пользователь {user} удален из {chat_name}")
            return {
                "response": 200,
                "time": time.time(),
                "alert": f"Пользователь {user} удален из {chat_name} ",
            }
        # logger.error(f"response 409 Пользователя {user} нет в чате {chat_name}")
        return {
            "response": 409,
            "time": time.time(),
            "error": f"Пользователя {user} нет в чате {chat_name}  ",
        }
    # logger.error(f"response 409 Чат {chat_name} пока не создан")
    return {
        "response": 409,
        "time": time.time(),
        "error": f"Чат {chat_name} пока не создан",
    }


@log(level="info", return_values=2)
def create(**kwargs):
    chat_name = kwargs["chat_name"]
    user = kwargs["from"]
    if user not in authorized_users:
        # logger.error(f"response 404 пользователь {user} отсутствует на сервере")
        return {"response": 404, "time": time.time(), "error": f"пользователь {user} отсутствует на сервере"}
    if chat_name in chat_rooms:
        # logger.error(f"response 409 уже имеется чат с указанным названием {chat_name}")
        return {
            "response": 409,
            "time": time.time(),
            "alert": f"уже имеется чат с указанным названием {chat_name} ",
        }
    chat_rooms[chat_name] = [user]  # создаем чат и список его участников
    # logger.info(f"Чат {chat_name} успешно создан")
    return {"response": 200, "time": time.time(), "alert": f"Чат {chat_name} успешно создан"}


@log(level="info", return_values=1)
def read_requests(r_clients, all_clients):
    """ Чтение запросов из списка клиентов"""
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}
    for sock in r_clients:
        try:
            data = sock.recv(1024)
            responses[sock] = data
        except:
            print("Клиент {} {} отключился".format(sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)
        return responses


@log(level="info", return_values=1)
def write_responses(requests, w_clients, all_clients):
    for sock in w_clients:
        if sock in requests:
            try:
                # Подготовить и отправить ответ сервера
                resp = requests[sock]
                response = checking_data(resp)
                if "msg" in response:
                    for s_client in w_clients:
                        try:
                            s_client.send(pickle.dumps(response))
                        except:
                            pass

                sock.send(pickle.dumps(response))
            except:  # Сокет недоступен, клиент отключился
                print("Клиент {} {} отключился".format(sock.fileno(), sock.getpeername()))
                sock.close()
                all_clients.remove(sock)


@log(level="info", return_values=1)
def main():
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    clients = []
    with socket(AF_INET, SOCK_STREAM) as s:  # Создает сокет TCP
        s.bind((namespace.addr, int(namespace.port)))  # Присваивает порт
        s.listen(5)  # Переходит в режим ожидания запросов Одновременно обслуживает не более 5 запросов.
        s.settimeout(0.2)
        while True:
            try:
                conn, addr = s.accept()  # Проверка подключений
            except OSError as e:
                pass  # timeout вышел
            else:
                print("Получен запрос на соединение от %s" % str(addr))
                clients.append(conn)
            finally:
                # Проверить наличие событий ввода-вывода
                wait = 10
                r = []
                w = []
                try:
                    r, w, e = select(clients, clients, [], wait)
                except:
                    pass  # Ничего не делать, если какой-то клиент отключился

                requests = read_requests(r, clients)  # Сохраним запросы клиентов
                if requests:
                    write_responses(requests, w, clients)  # Выполним отправку ответов клиентам


if __name__ == "__main__":
    if not DEBUG:
        try:
            main()
        except Exception as er:
            pass

    if DEBUG:
        authenticate()
        quit_s()
        presence()

"""
команды quit, presence, authenticate принимают словарь такого вида
{
    "action": "presence",
    "time": <unix timestamp>,
    "type": "status",
    "user": {
        "account_name": "C0deMaver1ck",
        "status": "Yep, I am here!"
        }
}
т.е. со вложенным словарем

в дальнейшем хочу оставить такой вид только для authenticate

остальные команды используют такую форму
{
    "action": "msg",
    "time": <unix timestamp>,
    "to": "account_name",
    "from": "account_name",
    "encoding": "ascii",
    "message": "message"
}

"""
