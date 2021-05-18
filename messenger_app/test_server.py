import pickle
from server import checking_data, authenticate, presence, msg, quit_s, join, leave, create, createParser
import time
import pytest
import server  # импортируем переменные, т.к. во время выполнения тестов функции операются на эти данные

"""
Функции сервера тестируются с помощью pytest
"""


data_authenticate = {"action": "authenticate", "user": {"account_name": "user_1", "password": "123"}}
data_create = {
    "action": "create",
    "time": time.time(),
    "from": "user_1",
    "chat_name": "My_chat",
}
data_len = {i: i for i in range(250)}

data_bad_com = {"action": "test_com", "user": {"account_name": "user_1", "password": "123"}}

data_join_1 = {
    "action": "join",
    "time": time.time(),
    "from": "user_1",
    "chat_name": "My_chat",
}

data_join_2 = {
    "action": "join",
    "time": time.time(),
    "from": "user_1",
    "chat_name": "New_chat",
}

data_join_3 = {
    "action": "join",
    "time": time.time(),
    "from": "user_2",
    "chat_name": "New_chat",
}

data_join_4 = {
    "action": "join",
    "time": time.time(),
    "from": "user_3",
    "chat_name": "My_chat",
}
data_authenticate_user_3 = {"action": "authenticate", "user": {"account_name": "user_3", "password": "123"}}


data_msg_1 = {
    "action": "msg",
    "time": time.time(),
    "to": "user_1",
    "from": "user_0",
    "encoding": "ascii",
    "message": "message",
}

data_msg_2 = {
    "action": "msg",
    "time": time.time(),
    "to": "user_0",
    "from": "user_1",
    "encoding": "ascii",
    "message": "message",
}

data_msg_3 = {
    "action": "msg",
    "time": time.time(),
    "to": "user_3",
    "from": "user_1",
    "encoding": "ascii",
    "message": "message",
}

data_msg_chat_1 = {
    "action": "msg",
    "time": time.time(),
    "to": "#New_chat",
    "from": "user_1",
    "encoding": "ascii",
    "message": "message",
}

data_msg_chat_2 = {
    "action": "msg",
    "time": time.time(),
    "to": "#My_chat",
    "from": "user_1",
    "encoding": "ascii",
    "message": "message",
}

data_leave_chat_1 = {
    "action": "leave",
    "time": time.time(),
    "from": "user_0",
    "chat_name": "My_chat",
}

data_leave_chat_2 = {
    "action": "leave",
    "time": time.time(),
    "from": "user_1",
    "chat_name": "New_chat",
}

data_leave_chat_3 = {
    "action": "leave",
    "time": time.time(),
    "from": "user_1",
    "chat_name": "My_chat",
}

data_quit = {
    "action": "quit",
    "time": time.time(),
    "type": "status",
    "user": {"account_name": "user_1", "status": "I am here!"},
}

""" 
серия тестов на аутентификацию и присутствие пользователя
тестируемые функции authenticate и presence
"""


def test_authenticate_1():
    assert authenticate(**data_authenticate) == {
        "alert": "Пользователь user_1 успешно авторизован",
        "response": 200,
        "time": time.time(),
    }


def test_authenticate_2():
    assert authenticate(**data_authenticate) == {
        "response": 409,
        "time": time.time(),
        "alert": "уже имеется подключение с указанным логином user_1 ",
    }


def test_presence_1():
    assert presence(**data_authenticate) == {
        "response": 200,
        "time": time.time(),
        "alert": "Хорошо, user_1 присутсвует в списке подключенных пользователей",
    }


def test_presence_2():
    server.authorized_users = []  # очистили список пользователей
    assert presence(**data_authenticate) == {
        "response": 404,
        "time": time.time(),
        "error": "пользователь user_1 отсутствует на сервере",
    }


""" 
серия тестов на создание чата и выход пользователей из чата
тестируемые функции create и leave
"""


def test_create_1():
    assert create(**data_create) == {
        "response": 404,
        "time": time.time(),
        "error": "пользователь user_1 отсутствует на сервере",
    }


def test_create_2():
    server.authorized_users = ["user_1"]  # добавили пользователей
    assert create(**data_create) == {"response": 200, "time": time.time(), "alert": "Чат My_chat успешно создан"}


def test_create_3():
    assert create(**data_create) == {
        "response": 409,
        "time": time.time(),
        "alert": "уже имеется чат с указанным названием My_chat ",
    }


def test_leave_1():
    assert leave(**data_create) == {
        "response": 200,
        "time": time.time(),
        "alert": "Пользователь user_1 удален из My_chat ",
    }


def test_leave_2():
    assert leave(**data_create) == {
        "response": 409,
        "time": time.time(),
        "error": "Пользователя user_1 нет в чате My_chat  ",
    }


def test_leave_3():
    server.chat_rooms = {}  # сбросили все чаты
    assert leave(**data_create) == {
        "response": 409,
        "time": time.time(),
        "error": "Чат My_chat пока не создан",
    }


def test_leave_4():
    server.authorized_users = []
    assert leave(**data_create) == {
        "response": 404,
        "time": time.time(),
        "error": "пользователь user_1 отсутствует на сервере",
    }


"""
Далее, чтобы не дублировать тесты, тестирование идет через функцию checking_data, которая запускает другие функции
Тестируемые функции: checking_data, authenticate, join
"""

# здесь получилось дублирование теста ф-ции authenticate, но через ф-цию checking_data


def test_checking_data_1():
    assert checking_data(pickle.dumps(data_authenticate)) == {
        "alert": "Пользователь user_1 успешно авторизован",
        "response": 200,
        "time": time.time(),
    }


def test_checking_data_2():
    assert checking_data(pickle.dumps(data_authenticate)) == {
        "response": 409,
        "time": time.time(),
        "alert": "уже имеется подключение с указанным логином user_1 ",
    }


# проверка длины сообщения


def test_checking_data_3():
    assert checking_data(pickle.dumps(data_len)) == {
        "response": 400,
        "time": time.time(),
        "error": "Длина объекта больше 640 символов",
    }


def test_checking_data_4():
    assert checking_data(pickle.dumps(data_bad_com)) == {
        "response": 404,
        "time": time.time(),
        "error": "Неизвестная команда test_com",
    }


# создание чата через checking data


def test_checking_data_5():
    assert checking_data(pickle.dumps(data_create)) == {
        "response": 200,
        "time": time.time(),
        "alert": "Чат My_chat успешно создан",
    }


# тестирование ф-ции join через checking_data


def test_checking_data_6():
    assert checking_data(pickle.dumps(data_join_1)) == {
        "response": 409,
        "time": time.time(),
        "error": "Пользователь user_1 уже присутствует в чате My_chat  ",
    }


def test_checking_data_7():  #
    assert checking_data(pickle.dumps(data_join_2)) == {
        "response": 409,
        "time": time.time(),
        "error": "Чат New_chat пока не создан",
    }


def test_checking_data_8():  #
    assert checking_data(pickle.dumps(data_join_3)) == {
        "response": 404,
        "time": time.time(),
        "error": "пользователь user_2 отсутствует на сервере",
    }


# добавление еще одного пользователя для дальнейших тестов


def test_checking_data_9():  #
    assert checking_data(pickle.dumps(data_authenticate_user_3)) == {
        "response": 200,
        "time": time.time(),
        "alert": "Пользователь user_3 успешно авторизован",
    }


def test_checking_data_10():  #
    assert checking_data(pickle.dumps(data_join_4)) == {
        "response": 200,
        "time": time.time(),
        "alert": "Пользователь user_3 добавлен в My_chat ",
    }


"""
тестирование ф-ции msg через checking_data
"""


def test_checking_data_11():  #
    assert checking_data(pickle.dumps(data_msg_1)) == {
        "response": 401,
        "time": time.time(),
        "alert": "Пользователь user_0 не авторизован",
    }


def test_checking_data_12():  #
    assert checking_data(pickle.dumps(data_msg_2)) == {
        "response": 404,
        "time": time.time(),
        "alert": "Пользователь user_0 на сервере не зарегистрирован",
    }


def test_checking_data_13():  #
    assert checking_data(pickle.dumps(data_msg_3)) == {
        "response": 200,
        "time": time.time(),
        "alert": "Сообщение от user_1 успешно доставлено user_3",

        "msg": "message",


    }


def test_checking_data_14():  #
    assert checking_data(pickle.dumps(data_msg_chat_1)) == {
        "response": 404,
        "time": time.time(),
        "error": "Чат New_chat пока не создан",
    }


def test_checking_data_15():  #
    assert checking_data(pickle.dumps(data_msg_chat_2)) == {
        "response": 200,
        "time": time.time(),
        "alert": "Сообщение от user_1 успешно доставлено в чат My_chat",
    }


"""
тестирование ф-ции leave через checking_data
"""


def test_checking_data_16():  #
    assert checking_data(pickle.dumps(data_leave_chat_1)) == {
        "response": 404,
        "time": time.time(),
        "error": "пользователь user_0 отсутствует на сервере",
    }


def test_checking_data_17():  #
    assert checking_data(pickle.dumps(data_leave_chat_2)) == {
        "response": 409,
        "time": time.time(),
        "error": "Чат New_chat пока не создан",
    }


def test_checking_data_18():  #
    assert checking_data(pickle.dumps(data_leave_chat_3)) == {
        "response": 200,
        "time": time.time(),
        "alert": "Пользователь user_1 удален из My_chat ",
    }


def test_checking_data_19():  #
    assert checking_data(pickle.dumps(data_leave_chat_3)) == {
        "response": 409,
        "time": time.time(),
        "error": "Пользователя user_1 нет в чате My_chat  ",
    }


"""
тестирование ф-ции quit_s через checking_data
"""


def test_checking_data_20():  #
    assert checking_data(pickle.dumps(data_quit)) == {
        "response": 200,
        "time": time.time(),

        "alert": "Пользователь user_1 успешно отключен от сервера",

    }


def test_checking_data_21():  #
    assert checking_data(pickle.dumps(data_quit)) == {
        "response": 404,
        "time": time.time(),
        "error": "Пользователь user_1 на сервере не зарегистрирован",
    }


"""
Функцию createParser протестировать не удалось. Данные совпадают, но выдает ошибку
"""

# def test_create_parser():  #
#     assert (
#         createParser()
#         == "ArgumentParser(prog='pytest', usage=None, description=None, formatter_class=<class 'argparse.HelpFormatter'>, conflict_handler='error', add_help=True)"
#     )


"""
Через передачу нескольких параметров также не удалось протестировать, т.к. не совпадает время (отличия на доли секунды - видимо работа декоратора)
"""


# @pytest.mark.parametrize(
#     "i,value",
#     [
#         (
#             data_1,
#             {
#                 "alert": "Пользователь user_1 успешно авторизован",
#                 "response": 200,
#                 "time": time.time(),
#             },
#         )
#     ],
# )
