from socket import socket, AF_INET, SOCK_STREAM
import time
import sys

import argparse
import pickle


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default="7777")
    parser.add_argument("-a", "--addr", default="localhost")
    parser.error = myerror

    return parser


def myerror(message):
    print(f"Применен недопустимый аргумент {message}")


parser = createParser()
namespace = parser.parse_args(sys.argv[1:])


s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
s.connect((namespace.addr, int(namespace.port)))  # Соединиться с сервером


"""insert message here"""

msg = {
    "action": "authenticate",
    "time": time.time(),
    "user": {"account_name": "user_1", "password": "CorrectHorseBatteryStaple"},
}


s.send(pickle.dumps(msg))
data = s.recv(1024)
print("Сообщение от сервера: ", pickle.loads(data), ", длиной ", len(data), "байт")
s.close()


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
