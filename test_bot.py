import unittest
from app import app, get_bot_response

class TestChatBot(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_greeting(self):
        reply = get_bot_response("Hello")
        self.assertIn(reply, [
            "Hello! How can I assist you with your studies or campus info today?",
            "Hi there! Ask me anything about courses, exams, or campus facilities."
        ])

    def test_library(self):
        reply = get_bot_response("When does the library open?")
        self.assertIn("Central Library", reply)

    def test_exam(self):
        reply = get_bot_response("When are the exams?")
        self.assertIn("Midterm exams", reply)

    def test_wifi(self):
        reply = get_bot_response("Campus Wi-Fi")
        self.assertIn("Campus-Student", reply)

    def test_unknown(self):
        reply = get_bot_response("asdkjhfasdjkfasdf")
        self.assertIn("I'm not quite sure I understand", reply)

    def test_chat_endpoint_success(self):
        res = self.client.post("/chat", json={"message": "Hey"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(len(data.get("reply", "")) > 0)

    def test_chat_endpoint_empty(self):
        res = self.client.post("/chat", json={"message": ""})
        self.assertEqual(res.status_code, 400)

    def test_home_route(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Campus AI Assistant", res.data)

if __name__ == "__main__":
    unittest.main()
