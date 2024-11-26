import threading
import time
from queue import Queue

import cv2

from .model import Model
from .requester import ApiRequester


class DetectionApp:
    cap: cv2.VideoCapture = None
    queue: Queue = None
    model: Model = None
    api_requester: ApiRequester = None
    frame_thread: threading.Thread = None

    def __init__(self, queue, model, api_requester):
        # Initialize the model and video capture
        self.model = model
        self.api_requester = api_requester
        self.queue = queue  # Queue to communicate with the main app

        # Detection settings
        self.detection_on = False
        self.model_processing_on = False
        self.consecutive_detections = 0
        self.detection_result = "Detection: Off"

        # Start the detection thread
        self.detection_thread = threading.Thread(
            target=self._detection_thread, daemon=True)
        self.detection_thread.start()

    def toggle_detection(self, state=None):
        """Toggle detection on or off."""
        if state is not None:
            self.detection_on = state
        else:
            self.detection_on = not self.detection_on
        if not self.detection_on:
            self.model_processing_on = False
        print(f"\n{'Detection on' if self.detection_on else 'Detection off'}")

    def toggle_model_processing(self, state=None):
        """Enable or disable model processing."""
        if not self.detection_on:
            print("Cannot toggle model processing without camera running.")
            return
        if state is not None:
            self.model_processing_on = state
        else:
            self.model_processing_on = not self.model_processing_on
            print(
                f"\n{'Model Processing Enabled' if self.model_processing_on else 'Model Processing Disabled'}")

    def detect_from_image(self, image):
        result = self.model.predict(image)
        return result

    def trigger_detection_result(self, result):
        prediction_keywords = ["violence", "fire", "fight", "crash"]

        # Check if the model detects a relevant event (e.g., violence, crash)
        detection_detected = False
        for keyword in prediction_keywords:
            if keyword in result["label"]:
                detection_detected = True
                break
        return detection_detected

    def _run_detection(self, frame):
        """Run the model prediction and handle detection result."""
        result = self.detect_from_image(frame)
        detection_detected = self.trigger_detection_result(result)

        # Consecutive detection logic
        if detection_detected and result["confidence"] > 0.2:
            self.consecutive_detections += 1
        else:
            self.consecutive_detections = 0

        # Update the detection result
        self.detection_result = f"Detection: {result}"

        # Send to request queue if there are 4 consecutive detections
        if self.consecutive_detections >= 4 and self.api_requester.can_send_request():
            print("Raise", self.detection_result)
            self.queue.put({
                "result": result,
                "image": frame,
            })
            self.consecutive_detections = 0  # Reset after sending

    def _detection_thread(self):
        """Thread function to handle detection independently."""
        while True:
            if self.detection_on and self.cap:
                ret, frame = self.cap.read()
                if ret and self.model_processing_on:
                    self._run_detection(frame)
            time.sleep(0.1)

    def start_frame(self):
        if self.frame_thread and self.frame_thread.is_alive():
            return
        self.frame_thread = threading.Thread(target=self.run, daemon=True)
        self.frame_thread.start()

    def display_frame(self):
        """Display frames and detect key events."""
        while True:
            if not self.detection_on:
                break

            ret, frame = self.cap.read()
            if not ret:
                print("camera read error")
                break

            # Show the frame with detection results
            cv2.imshow("Real-Time Capture", frame)
            cv2.putText(frame, self.detection_result, (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Wait for key press
            key = cv2.waitKey(1) & 0xFF
            if cv2.getWindowProperty("Real-Time Capture", cv2.WND_PROP_VISIBLE) < 1:
                break

            # Toggle detection with 'b'
            if key == ord('b'):
                self.toggle_detection()

            # Enable/Disable model processing with 'm'
            elif key == ord('m'):
                self.toggle_model_processing()

            # Exit with ESC
            elif key == 27:  # ESC
                break

        self.cap.release()
        self.detection_on = False
        self.model_processing_on = False
        cv2.destroyAllWindows()

    def run(self):
        """Start the main loop to display frames."""
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.cap = cv2.VideoCapture(0)
        self.display_frame()
