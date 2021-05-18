import unittest
from client import message_processing, createParser
import argparse


"""
Тест клиентской функции с помощью unittest
"""


class TestClient(unittest.TestCase):
    def test_create_parser(self):
        parser = argparse.ArgumentParser()
        self.assertEqual(type(createParser()), type(parser))

    def test_message_processing_response_400(self):
        self.assertEqual(
            message_processing(
                {
                    "response": 409,
                    "alert": "уже имеется подключение с указанным логином user_1 ",
                }
            ),
            {
                "response": 409,
                "alert": "уже имеется подключение с указанным логином user_1 ",
            },
        )

    def test_message_processing_message(self):
        self.assertEqual(
            message_processing({"msg": "Hi"}),
            "Hi",
        )

    def test_message_processing_empty(self):
        self.assertEqual(
            message_processing({}),
            "Empty",
        )

    def test_message_processing_response_200(self):
        self.assertEqual(
            message_processing(
                {
                    "response": 200,
                }
            ),
            {
                "response": 200,
            },
        )


if __name__ == "__main__":
    unittest.main()
