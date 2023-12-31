import os

from openai import OpenAI

client = OpenAI(api_key=os.environ['GPT_KEY'])

response = client.images.generate(
  model="dall-e-3",
  prompt="I want logo for dentistry clinic called Mint Dent",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
print(image_url)