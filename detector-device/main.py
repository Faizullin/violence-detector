import os
import queue
import sys
import threading
import time

import cv2
import requests
from dotenv import load_dotenv

from model import Model

# Load environment variables from .env file
load_dotenv()
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
API_DEVICE_ID = os.getenv("API_DEVICE_ID")


class ApiRequester(threading.Thread):
    """Handles sending API requests for detection events."""

    def __init__(self, api_url, interval=60):
        super().__init__(daemon=True)
        self.api_url = api_url
        self.interval = interval
        self.last_request_time = 0
        self.queue = queue.Queue()  # Queue for detection data

    def can_send_request(self):
        """Check if enough time has passed to send another request."""
        return (time.time() - self.last_request_time) >= self.interval

    def send_request(self, message, image):
        """Send a POST request to the specified API URL."""
        if self.can_send_request():
            # Prepare data to be sent
            _, img_encoded = cv2.imencode('.jpg', image)
            data = {
                "message": message,
                "device_id": API_DEVICE_ID,
            }
            files = {
                "image": ("image.jpg", img_encoded.tobytes(), "image/jpeg"),
            }
            headers = {
                "Authorization": f"Api-key {API_KEY}"
            }

            try:
                response = requests.post(
                    self.api_url, data=data, files=files,  headers=headers)
                if response.status_code == 200:
                    print("\nAPI Request Successful")
                else:
                    print("\nAPI Request Failed {} {}".format(
                        response.status_code, response.text))
                self.last_request_time = time.time()
            except requests.RequestException as e:
                print(f"\nAPI Request Error: {e}")

    def run(self):
        """Continuously monitor the queue and send API requests."""
        while True:
            try:
                message, image = self.queue.get(
                    timeout=1)  # Get item from queue
                self.send_request(message, image)
            except queue.Empty:
                continue  # No items to process, continue the loop


class DetectionApp:
    def __init__(self, api_requester):
        # Initialize the model and video capture
        self.model = Model()
        self.cap = cv2.VideoCapture(0)
        self.api_requester = api_requester

        # Detection and request settings
        self.detection_on = False
        self.consecutive_detections = 0
        self.detection_result = "Detection: Off"

        # Start the detection thread
        self.detection_thread = threading.Thread(
            target=self._detection_thread, daemon=True)
        self.detection_thread.start()

    def toggle_detection(self):
        """Toggle detection on or off."""
        self.detection_on = not self.detection_on
        print(f"\n{'Detection on' if self.detection_on else 'Detection off'}")

    def _run_detection(self, frame):
        """Run the model prediction and handle detection result."""
        result = self.model.predict(frame)
        prediction1_keywords = ["violence", "fire", "fight", "crash"]

        tt = False
        for i in prediction1_keywords:
            if i in result["label"]:
                tt = True
                break

        # Check if result indicates a detection
        if tt and result["confidence"] > 0.2:
            self.consecutive_detections += 1
        else:
            self.consecutive_detections = 0

        # Update detection result for display
        self.detection_result = f"Detection: {result}"

        # Check for 4 consecutive detections and add to request queue
        if self.consecutive_detections >= 4 and self.api_requester.can_send_request():
            self.api_requester.queue.put(("Detection occurred", frame))
            self.consecutive_detections = 0  # Reset after sending to the queue

    def _detection_thread(self):
        """Thread function for handling detection independently."""
        while True:
            if self.detection_on:
                ret, frame = self.cap.read()
                if ret:
                    self._run_detection(frame)
            time.sleep(0.1)

    def display_frame(self):
        """Main loop to display frames and handle key events."""
        print("Press 'b' to toggle detection on/off. Press 'ESC' to quit.")

        while True:
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture image")
                break

            # Display the resulting frame
            cv2.imshow("Real-Time Capture", frame)

            # Print detection result in the same place using stdout
            sys.stdout.write("\r" + self.detection_result)
            sys.stdout.flush()

            # Wait for a key press and check for window close
            key = cv2.waitKey(1) & 0xFF
            if cv2.getWindowProperty("Real-Time Capture", cv2.WND_PROP_VISIBLE) < 1:
                break

            # Toggle detection on/off if 'b' is pressed
            if key == ord('b'):
                self.toggle_detection()

            # Exit if 'ESC' is pressed
            elif key == 27:  # ESC key
                break

        # Release the capture and close windows
        self.cap.release()
        cv2.destroyAllWindows()

    def run(self):
        """Run the main display loop."""
        self.display_frame()


# To run the application:
if __name__ == "__main__":
    # Initialize the ApiRequester with the API URL from the .env file
    api_requester = ApiRequester(api_url=API_URL, interval=60)
    api_requester.start()  # Start the API requester thread

    # Initialize and run the DetectionApp
    app = DetectionApp(api_requester)
    app.run()
