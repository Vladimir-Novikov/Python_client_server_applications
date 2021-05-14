import pickle
from socket import socket, AF_INET, SOCK_STREAM
import time
import sys

import argparse

# обработка командной строки с параметрами
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default="7777")
    parser.add_argument("-a", "--addr", default="0.0.0.0")
    parser.error = myerror

    return parser


def myerror(message):
    print(f"Применен недопустимый аргумент {message}")


parser = createParser()
namespace = parser.parse_args(sys.argv[1:])


def checking_data(message):
    if len(message) > 640:  # проверка длины пакета
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
        return {"response": 404, "time": time.time(), "error": f"Неизвестная команда {action}"}
    processing_the_action = dict_of_commands[action]  # находим в словаре обработчик и присваиваем его переменной
    return processing_the_action(**data)  # выполняем нужную функцию


authorized_users = []
chat_rooms = {}


def authenticate(**kwargs):  # пароль не запрашивается на данном этапе разработки
    user_name = kwargs["user"]["account_name"]
    if user_name in authorized_users:
        return {
            "response": 409,
            "time": time.time(),
            "alert": f"уже имеется подключение с указанным логином {user_name} ",
        }
    authorized_users.append(user_name)
    return {"response": 200, "time": time.time(), "alert": f"Пользователь {user_name} успешно авторизован"}


def presence(**kwargs):
    user_name = kwargs["user"]["account_name"]
    if user_name in authorized_users:
        return {
            "response": 200,
            "time": time.time(),
            "alert": f"Хорошо, {user_name} присутсвует в списке подключенных пользователей",
        }
    return {"response": 404, "time": time.time(), "error": f"пользователь {user_name} отсутствует на сервере"}


def msg(**kwargs):
    from_user = kwargs["from"]
    to_user = kwargs["to"]
    if from_user not in authorized_users:
        return {"response": 401, "time": time.time(), "alert": f"Пользователь {from_user} не авторизован"}

    if to_user[0] == "#":
        chat = to_user[1:]
        if chat not in chat_rooms:
            return {"response": 404, "time": time.time(), "error": f"Чат {chat} пока не создан"}
        return {
            "response": 200,
            "time": time.time(),
            "alert": f"Сообщение от {from_user} успешно доставлено в чат {chat}",
        }
    if to_user not in authorized_users:
        return {"response": 404, "time": time.time(), "alert": f"Пользователь {to_user} на сервере не зарегистрирован"}

    return {"response": 200, "time": time.time(), "alert": f"Сообщение от {from_user} успешно доставлено {to_user}"}


def quit_s(**kwargs):
    user_name = kwargs["user"]["account_name"]
    if user_name in authorized_users:
        authorized_users.remove(user_name)
        return {"response": 200, "time": time.time(), "alert": f"Пользователь {user_name} оключен от сервера"}
    return {"response": 404, "time": time.time(), "error": f"Пользователь {user_name} на сервере не зарегистрирован"}


def join(**kwargs):
    chat_name = kwargs["chat_name"]
    user = kwargs["from"]
    if user not in authorized_users:
        return {"response": 404, "time": time.time(), "error": f"пользователь {user} отсутствует на сервере"}
    if chat_name in chat_rooms:
        if user not in chat_rooms[chat_name]:
            chat_rooms[chat_name].append(user)
            return {
                "response": 200,
                "time": time.time(),
                "alert": f"Пользователь {user} добавлен в {chat_name} ",
            }
        return {
            "response": 409,
            "time": time.time(),
            "error": f"Пользователь {user} уже присутствует в чате {chat_name}  ",
        }

    return {
        "response": 409,
        "time": time.time(),
        "error": f"Чат {chat_name} пока не создан",
    }


def leave(**kwargs):
    chat_name = kwargs["chat_name"]
    user = kwargs["from"]
    if user not in authorized_users:
        return {"response": 404, "time": time.time(), "error": f"пользователь {user} отсутствует на сервере"}
    if chat_name in chat_rooms:
        if user in chat_rooms[chat_name]:
            chat_rooms[chat_name].remove(user)
            return {
                "response": 200,
                "time": time.time(),
                "alert": f"Пользователь {user} удален из {chat_name} ",
            }
        return {
            "response": 409,
            "time": time.time(),
            "error": f"Пользователя {user} нет в чате {chat_name}  ",
        }

    return {
        "response": 409,
        "time": time.time(),
        "error": f"Чат {chat_name} пока не создан",
    }


def create(**kwargs):
    chat_name = kwargs["chat_name"]
    user = kwargs["from"]
    if user not in authorized_users:
        return {"response": 404, "time": time.time(), "error": f"пользователь {user} отсутствует на сервере"}
    if chat_name in chat_rooms:
        return {
            "response": 409,
            "time": time.time(),
            "alert": f"уже имеется чат с указанным названием {chat_name} ",
        }
    chat_rooms[chat_name] = [user]  # создаем чат и список его участников
    return {"response": 200, "time": time.time(), "alert": f"Чат {chat_name} успешно создан"}


if __name__ == "__main__":
    s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
    s.bind((namespace.addr, int(namespace.port)))  # Присваивает порт 8888
    s.listen(5)  # Переходит в режим ожидания запросов Одновременно обслуживает не более 5 запросов.
    while True:

        client, addr = s.accept()
        message = client.recv(1024)
        print("Сообщение: ", pickle.loads(message), ", было отправлено клиентом: ", addr)
        response = checking_data(message)
        client.send(pickle.dumps(response))
        client.close()

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
