import os, requests
from io import BytesIO
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def createImagePrompt(text):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "user",
        "content": "create a prompt to create a meme like image in the style of digital art.  Find the mascot for the teams mentioned in the text and create an image of a game between them, include references to the cities or colleges and teams or mascots mentioned in the text with emphasis the home team, be creative, fun and whimsical. If there are no teams mentioned then use the subject of text as your inspiration. Make sure the image is relevant to the sport mentioned." + text
        }
    ],
    temperature=0.5,
    max_tokens=800,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    return response.choices[0].message.content


def generate_image(text_prompt):
    image_url = ""
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=text_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
    except:
        image_url = ""
    return image_url

def generate_image2(text_prompt):
    image_url = ""
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=text_prompt,
            size="512x512",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        image_data = requests.get(image_url).content
    except:
        image_data = ""
    return image_data

#def generate_image(prompt):
#    response = openai.images.generate(prompt=prompt[:1000], n=1, size="512x512")
#    image_url = response.data[0].url
#    print(image_url)
#    image_data = requests.get(image_url).content
#    return BytesIO(image_data)



