from pathlib import Path

from ..base_detector import BaseDetector


class ViolenceBasicDetector(BaseDetector):
    """
    A class that extends BaseDetector for detecting violence in images.
    """

    model = None

    def detect_image(self, image):
        """
        Use the loaded model to detect features in the provided image.
        """

        prediction = self.model.predict(image=image)
        return [
            {
                "type": "basic",
                "prediction": prediction,
                "message": prediction["label"].title()
            }
        ]

    def load_model_and_prepare(self):
        self.logger.info(f"ViolenceBasicDetector ({self}): Loading model and preparing")
        from .model import Model
        settings_path = Path(__file__).parent.joinpath("settings.yaml")
        self.model = Model(settings_path=str(settings_path))
        self.logger.info(f"ViolenceBasicDetector ({self}): Model loaded and prepared")
