

import logging

from app.modules.logger import get_logger


class BaseDetector:
    """
    BaseDetector class to handle common functionality like loading a model and image preprocessing.
    """
    logger: logging.Logger

    def __init__(self):
        self.logger = get_logger()

    def load_model_and_prepare(self):
        pass

    def preprocess_image(self, image):
        pass

    def detect_image(self, image):
        pass
    
    __call__ = detect_image
