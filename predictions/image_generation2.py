import os
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def createImagePrompt(text):
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "user",
        "content": "you are a grapic designer" + text
        }
    ],
    temperature=0.3,
    max_tokens=300,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    return response.choices[0].message.content


def generate_image(text_prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt="create an image for a chat bot called TLDR the image should be warm and appealing",
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return image_url

print(generate_image(""))

