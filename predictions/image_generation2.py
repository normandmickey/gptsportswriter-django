import os
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def createImagePrompt(text):
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "user",
        "content": "create a prompt to create a meme like image in the style of digital art." + text
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
        prompt="create a banner image for a website called GPTSportsWriter.com.  The site provides AI powered sports betting predictions and advice.",
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return image_url

print(generate_image(""))

