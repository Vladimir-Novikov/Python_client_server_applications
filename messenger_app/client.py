from socket import socket, AF_INET, SOCK_STREAM
import time
import sys

import argparse
import pickle
import logging

from logs import _client_log_config


logger = logging.getLogger("app.client")
logger.info("app start")


def createParser():
    logger.info("parser start")
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default="7777")
    parser.add_argument("-a", "--addr", default="localhost")
    parser.error = myerror

    return parser


def myerror(message):
    logger.error(f"parser wrong argument: {message}")
    # print(f"Применен недопустимый аргумент {message}")


def message_processing(data):
    if len(data) == 0:
        return "Empty"
    if "msg" in data:
        return data["msg"]
    if data["response"] > 200:
        logger.warning(data)
        return data
    logger.info(data)
    return data


def command_processing():
    user_name = ""  # имя пользователя
    while len(user_name) < 2:
        user_name = input("Введите ваше имя (минимум 2 знака): ").strip()
        msg = {
            "action": "authenticate",
            "time": time.time(),
            "user": {"account_name": f"{user_name}", "password": "123"},
        }
        s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
        s.connect((namespace.addr, int(namespace.port)))  # Соединиться с сервером
        s.send(pickle.dumps(msg))
        data = s.recv(1024)
        print("Сообщение от сервера: ", message_processing(pickle.loads(data)), ", длиной ", len(data), "байт")
    while True:
        command = input("Введите q для выхода, s для отправки сообщения, n для регистрации \n--> ")
        try:
            # if command == "n":

            if command == "s":
                to = input("Кому: ")
                text = input("Сообщение: ")
                msg = {
                    "action": "msg",
                    "time": time.time(),
                    "to": f"{to}",
                    "from": f"{user_name}",
                    "encoding": "ascii",
                    "message": f"{text}",
                }
                s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
                s.connect((namespace.addr, int(namespace.port)))  # Соединиться с сервером
                s.send(pickle.dumps(msg))
                data = s.recv(1024)
                print("Сообщение от сервера: ", message_processing(pickle.loads(data)), ", длиной ", len(data), "байт")

            if command == "q":
                logger.info("exit")
                try:
                    s.close()
                except NameError as er:  # сокет не создавался
                    logger.error("Сокет не создавался, клиент вышел")
                break

        except ConnectionRefusedError as er:  # сервер отклонил подключение
            logger.error(er)


if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    command_processing()


"""
образцы сообщений для тестирования
msg = {
    "action": "authenticate",
    "time": time.time(),
    "user": {"account_name": "C0deMaver1ck", "password": "CorrectHorseBatteryStaple"},
}


msg = {
    "action": "quit",
    "time": time.time(),
    "type": "status",
    "user": {"account_name": "C0deMaver1ck", "status": "Yep, I am here!"},
}

msg = {
    "action": "presence",
    "time": time.time(),
    "type": "status",
    "user": {"account_name": "C0deMaver1ck", "status": "Yep, I am here!"},
}


msg = {
    "action": "msg",
    "time": time.time(),
    "to": "C0deMaver1ck",
    "from": "User_1",
    "encoding": "ascii",
    "message": "message"
}

msg = {
    "action": "create",
    "time": time.time(),
    "from": "C0deMaver1ck",
    "chat_name": "My_chat",
}

msg = {
    "action": "join",
    "time": time.time(),
    "from": "User_1",
    "chat_name": "My_chat",
}

msg = {
    "action": "leave",
    "time": time.time(),
    "from": "User_1",
    "chat_name": "My_chat",
}


"""