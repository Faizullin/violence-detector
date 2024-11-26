import json
import queue
import threading
import time

import cv2
import requests


class ApiRequester(threading.Thread):
    """Handles sending API requests for detection events."""
    save_to_server: bool = False

    def __init__(self, queue, api_device_id, api_key, api_url, interval=60):
        super().__init__(daemon=True)
        self.api_device_id = api_device_id
        self.api_key = api_key
        self.api_url = api_url
        self.interval = interval
        self.last_request_time = 0
        self.queue = queue

    def can_send_request(self):
        """Check if enough time has passed to send another request."""
        return (time.time() - self.last_request_time) >= self.interval

    def send_request_api(self, data, image):
        _, img_encoded = cv2.imencode('.jpg', image)
        files = {
            "image": ("image.jpg", img_encoded.tobytes(), "image/jpeg"),
        }
        headers = {
            "Authorization": f"Api-key {self.api_key}"
        }
        print("Request", headers, dict(data), files.keys())
        try:
            response = requests.post(
                self.api_url, data=data, files=files, headers=headers)
            if response.status_code == 200:
                print("\nAPI Request Successful")
            else:
                print("\nAPI Request Failed {} {}".format(
                    response.status_code, response.text))
            return response
        except requests.RequestException as e:
            print(f"\nAPI Request Error: {e}")
            return e.response

    def send_request(self, result_data, image):
        """Send a POST request to the specified API URL."""
        if self.can_send_request():
            data = {
                "prediction1": json.dumps({

                    "prediction": result_data
                }),
                "device_id": self.api_device_id,
                "save_to_server": self.save_to_server,
            }
            res = self.send_request_api(data, image,)
            self.last_request_time = time.time()
            return res

    def run(self):
        """Continuously monitor the queue and send API requests."""
        while True:
            try:
                data: dict = self.queue.get(
                    timeout=1)  # Get item from queue
                print("queue", data['result'])
                self.send_request(data['result'], data['image'])
            except queue.Empty:
                time.sleep(1)
                continue  # No items to process, continue t
