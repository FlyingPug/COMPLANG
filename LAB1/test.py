import unittest
import requests
from datetime import datetime, timedelta
import pytz


class TestWebApp(unittest.TestCase):
    BASE_URL = "http://localhost:8000"

    def test_get_root(self):
        response = requests.get(f"{self.BASE_URL}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Current Server Time:", response.text)

        time_text = response.text.split("Current Server Time: ")[1].split("</h1>")[0]
        server_time = datetime.strptime(time_text, "%Y-%m-%d %H:%M:%S")
        self.assertTrue(datetime.utcnow() - timedelta(seconds=5) <= server_time <= datetime.utcnow())

    def test_get_timezone(self):
        tz_name = "Europe/Moscow"
        response = requests.get(f"{self.BASE_URL}/{tz_name}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(f"Current Time in {tz_name}:", response.text)

        tz = pytz.timezone(tz_name)
        local_time = datetime.now(tz)
        time_text = response.text.split(f"Current Time in {tz_name}: ")[1].split("</h1>")[0]
        server_time = tz.localize(datetime.strptime(time_text, "%Y-%m-%d %H:%M:%S"))
        self.assertTrue(local_time - timedelta(seconds=5) <= server_time <= local_time)

    def test_post_api_time(self):
        response = requests.post(f"{self.BASE_URL}/api/v1/time", data={"tz": "UTC"})
        self.assertEqual(response.status_code, 200)
        server_time = datetime.fromisoformat(response.json()["time"])
        self.assertTrue(datetime.now(pytz.UTC) - timedelta(seconds=5) <= server_time <= datetime.now(pytz.UTC))

    def test_post_api_date(self):
        response = requests.post(f"{self.BASE_URL}/api/v1/date", data={"tz": "UTC"})
        self.assertEqual(response.status_code, 200)
        server_date = datetime.strptime(response.json()["date"], "%Y-%m-%d").date()
        self.assertEqual(server_date, datetime.utcnow().date())

    def test_post_api_datediff(self):
        payload = {"start": "12.20.2021 22:21:05", "end": "12.21.2021 22:21:05", "tz": "UTC"}
        response = requests.post(f"{self.BASE_URL}/api/v1/datediff", data=payload)
        self.assertEqual(response.status_code, 200)
        server_difference = response.json()["difference"]
        self.assertEqual(server_difference, "1 day, 0:00:00")


if __name__ == "__main__":
    unittest.main()