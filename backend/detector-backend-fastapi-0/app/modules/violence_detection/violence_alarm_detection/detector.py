import cv2
import numpy as np
from tensorflow.keras.models import load_model

from app.modules.violence_detection.base_detector import BaseDetector
from app.modules.storage import storage


class ViolenceAlarmDetector(BaseDetector):

    def preprocess_image(self, image, img_size=128):
        """
        Preprocess the image to match the input shape of the model.
        """
        c_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
        c_image = cv2.resize(c_image, (img_size, img_size))
        c_image = c_image / 255.0  # Normalize pixel values
        return np.expand_dims(c_image, axis=0)  # Add batch dimension

    def detect_image(self, image):
        processed_image = self.preprocess_image(image)
        prediction = self.model.predict(processed_image)
        threshold = 0.5
        v = prediction >= threshold
        return [
            {
                "prediction": prediction,
                "result": v,
                "message": "Violence" if v else "Non-Violence"
            }
        ]

    def load_model_and_prepare(self):

        self.logger.info(
            f"ViolenceAlarmDetector ({self}): Loading model and preparing")
        model_path = storage.get_model_weights_dir_path().joinpath('modelnew.h5')
        self.model = load_model(model_path)

        self.logger.info(
            f"ViolenceAlarmDetector ({self}): Model loaded and prepared")
