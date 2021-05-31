import unittest
from client import msg_user_to_user, createParser, create_quick_chat, msg_to_chat
import argparse
import time


"""
Тест клиентской функции с помощью unittest
"""


class TestClient(unittest.TestCase):
    def test_create_parser(self):
        parser = argparse.ArgumentParser()
        self.assertEqual(type(createParser()), type(parser))

    def test_msg_user_to_user(self):
        self.assertEqual(msg_user_to_user(testing=True)["message"], "Hi")

    def test_create_quick_chat(self):
        self.assertEqual(create_quick_chat(testing=True)["chat_name"], "Test_chat")

    def test_msg_to_chat(self):
        self.assertEqual(
            msg_to_chat(chat_name="Chat_1", sock=[], testing=True)["message"],
            "Test",
        )


if __name__ == "__main__":
    unittest.main()
