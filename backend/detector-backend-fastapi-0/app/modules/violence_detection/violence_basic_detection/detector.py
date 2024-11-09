from pathlib import Path

import cv2
import numpy as np

from app.modules.violence_detection.base_detector import BaseDetector


class ViolenceBasicDetector(BaseDetector):
    """
    A class that extends BaseDetector for detecting violence in images.
    """

    def preprocess_image(self, image, img_size=128):
        """
        Preprocess the image to match the input shape of the model.
        """
        c_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
        c_image = cv2.resize(c_image, (img_size, img_size))
        c_image = c_image / 255.0  # Normalize pixel values
        return np.expand_dims(c_image, axis=0)  # Add batch dimension

    def detect_image(self, image):
        """
        Use the loaded model to detect features in the provided image.
        """

        prediction = self.model.predict(image=image)
        v = 1
        return [
            {
                "prediction": prediction,
                "result": v,
                "message": prediction["label"].title()
            }
        ]

    def load_model_and_prepare(self):
        self.logger.info(f"ViolenceBasicDetector ({self}): Loading model and preparing")
        from .model import Model
        settings_path = Path(__file__).parent.joinpath("settings.yaml")
        model = Model(settings_path=settings_path)
        self.model = model
        self.logger.info(f"ViolenceBasicDetector ({self}): Model loaded and prepared")
