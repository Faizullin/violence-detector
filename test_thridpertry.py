import base64
from openai import OpenAI

API_KEY = "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"
client = OpenAI(
    api_key=API_KEY
)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "./violence-detection/data/0_Wrexham-brawl1.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What is in this image?",
        },
        # {
        #   "type": "image_url",
        #   "image_url": {
        #     "url":  f"data:image/jpeg;base64,{base64_image}"
        #   },
        # },
      ],
    }
  ],
)
