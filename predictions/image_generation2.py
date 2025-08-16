import os
from openai import OpenAI
client = OpenAI(api_key="")


def createImagePrompt(text):
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "user",
        "content": "you are a grapic designer create a prompt for dall-e-3 based on the follwoing " + text
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
        prompt=text_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return image_url

print(generate_image(createImagePrompt("Create an image that shows references to sports betting")))
#print(createImagePrompt)


