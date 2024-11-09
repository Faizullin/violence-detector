import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load your trained model
# Update with the actual path to your trained model
model = load_model('modelnew.h5')


def preprocess_image(image_path, img_size=128):
    """
    Preprocess the image to match the input shape of the model.
    """
    # Load the image and resize
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
    image = cv2.resize(image, (img_size, img_size))
    image = image / 255.0  # Normalize pixel values
    return np.expand_dims(image, axis=0)  # Add batch dimension


def detect_image(model, image_path):
    """
    Use the loaded model to detect features in the provided image.
    """
    # Preprocess the image
    processed_image = preprocess_image(image_path)

    # Predict using the model
    prediction = model.predict(processed_image)

    # Interpret the result (adjust based on binary or multi-class classification)
    if prediction >= 0.5:
        return "Violence Detected"  # Adjust based on your model's classes
    else:
        return "Non-Violence Detected"


# Example usage
image_path = 'path_to_image.jpg'  # Update with the actual path to your image
result = detect_image(model, image_path)
print(result)
