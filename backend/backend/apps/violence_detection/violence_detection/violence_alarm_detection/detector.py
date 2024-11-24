from pathlib import Path
from typing import List, Dict, Any

import cv2
import numpy as np
from django.conf import settings
from tensorflow.keras.models import load_model

from ..base_detector import BaseDetector


class ViolenceAlarmDetector(BaseDetector):
    model = None

    def preprocess_image(self, image, img_size=128):
        """
        Preprocess the image to match the input shape of the model.
        """
        c_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
        c_image = cv2.resize(c_image, (img_size, img_size))
        c_image = c_image / 255.0  # Normalize pixel values
        return np.expand_dims(c_image, axis=0)  # Add batch dimension

    def detect_image(self, image) -> List[Dict[str, Any]]:
        processed_image = self.preprocess_image(image)
        prediction = self.model.predict(processed_image)
        threshold = 0.5
        v = bool(prediction >= threshold)
        return [
            {
                "type": "alarm",
                "prediction": float(prediction),
                "result": v,
                "message": "Violence" if v else "Non-Violence"
            }
        ]

    def load_model_and_prepare(self):
        self.logger.info(f"ViolenceAlarmDetector ({self}): Loading model and preparing")
        model_path: Path = Path(settings.BASE_DIR)
        model_path = model_path.joinpath('api-weights').joinpath("modelnew.h5")
        self.model = load_model(str(model_path))
        self.logger.info(
            f"ViolenceAlarmDetector ({self}): Model loaded and prepared")
