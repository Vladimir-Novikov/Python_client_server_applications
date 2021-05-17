import unittest
from client import message_processing

"""
Тест клиентской функции с помощью unittest
"""


class TestClient(unittest.TestCase):
    def test_response(self):
        self.assertEqual(
            message_processing(
                {
                    "response": 409,
                    "time": 1620822218.6663346,
                    "alert": "уже имеется подключение с указанным логином user_1 ",
                }
            ),
            {
                "response": 409,
                "time": 1620822218.6663346,
                "alert": "уже имеется подключение с указанным логином user_1 ",
            },
        )

    def test_message(self):
        self.assertEqual(
            message_processing({"message": "Hi"}),
            "Hi",
        )

    def test_message_empty(self):
        self.assertEqual(
            message_processing({}),
            "Empty",
        )


if __name__ == "__main__":
    unittest.main()
