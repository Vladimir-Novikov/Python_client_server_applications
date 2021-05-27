import unittest
from client import msg_user_to_user, createParser
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
        self.assertEqual(
            msg_user_to_user(testing=True),
            {
                "action": "msg",
                "time": time.time(),
                "to": "User_1",
                "from_user": "Me",
                "encoding": "ascii",
                "message": "Hi",
            },
        )


if __name__ == "__main__":
    unittest.main()
