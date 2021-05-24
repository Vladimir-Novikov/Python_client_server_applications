from socket import socket, AF_INET, SOCK_STREAM
import time
import sys
import argparse
import pickle
import logging
from select import select

# from logs import _client_log_config
from logs._client_log_decorator import log

"""Раскомментировать этот код в случае применения _client_log_config (без декораторов)"""
# logger = logging.getLogger("app.client")
# logger.info("app start")


@log()
def createParser():
    # logger.info("parser start")
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default="7777")
    parser.add_argument("-a", "--addr", default="localhost")
    parser.error = myerror

    return parser


@log("error")
def myerror(message):
    # print(f"Применен недопустимый аргумент {message}")
    return f"Применен недопустимый аргумент {message}"


@log()
def message_processing(data):
    # return data
    if len(data) == 0:
        return "Empty"
    if "msg" in data:
        return data["msg"]
    if data["response"] > 200:
        # logger.warning(data)
        return data
    # logger.info(data)
    return data


user_name = ""


@log()
def user_registration(testing=False):
    global user_name
    if testing:
        user_name = "Test_name"
    else:
        while len(user_name) < 2:
            user_name = input("Введите ваше имя: ").strip()
    msg = {
        "action": "authenticate",
        "time": time.time(),
        "user": {"account_name": user_name, "password": "123"},
    }
    return msg


@log()
def main():
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
    s.connect((namespace.addr, int(namespace.port)))  # Соединиться с сервером
    s.send(pickle.dumps(user_registration()))
    data = s.recv(1024)
    print("Сообщение от сервера: ", message_processing(pickle.loads(data)), ", длиной ", len(data), "байт")
    s.settimeout(0.2)
    while True:
        msg = input("Ваше сообщение: ")
        if msg == "exit":
            s.close()
            break
        msg = {
            "action": "msg",
            "time": time.time(),
            "to": "all",
            "from": user_name,
            "encoding": "ascii",
            "message": msg,
        }
        s.send(pickle.dumps(msg))
        data = s.recv(1024)
        print("Сообщение из чата", message_processing(pickle.loads(data)))


if __name__ == "__main__":
    try:
        main()
    except Exception as er:
        pass


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
