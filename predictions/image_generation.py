import os, requests
from io import BytesIO
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont

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
    #messages=[
    #    {
    #    "role": "user",
    #    "content": "create an image prompt to display the following text" + text
    #    }
    #],
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

def generate_image3(title, filename):
    # 1. Create a new image
    img = Image.new('RGB', (1024, 1024), color=(73, 109, 137)) # Blue background

    # 2. Create a drawing object
    d = ImageDraw.Draw(img)

    # 3. Load a font (replace 'arial.ttf' with a font available on your system)
    try:
        fnt = ImageFont.truetype('arial.ttf', 50)
        fnt2 = ImageFont.truetype('arial.ttf', 30)
    except IOError:
        print("Arial font not found. Using default font.")
        fnt = ImageFont.load_default() # Fallback to default font
        fnt2 = ImageFont.load_default()

    # 4. Add text
    text_to_add = "www.GPTSportsWriter.com"
    text_color = (255, 255, 0) # Yellow color
    d.text((50, 80), text_to_add, font=fnt, fill=text_color)
    d.text((50, 160), title, font=fnt2, fill=text_color)
    
    # 5. Save the image
    img.save(filename)

    print("Image 'image_with_text.png' created successfully.")

def addWatermark(title, filename):
    # 1. Create a new image
    title = title.split(":", 1)[1]
    img = Image.open(filename)

    # 2. Create a drawing object
    d = ImageDraw.Draw(img)

    # 3. Load a font (replace 'arial.ttf' with a font available on your system)
    try:
        fnt = ImageFont.truetype('arial.ttf', 50)
        fnt2 = ImageFont.truetype('arial.ttf', 30)
    except IOError:
        print("Arial font not found. Using default font.")
        fnt = ImageFont.load_default() # Fallback to default font
        fnt2 = ImageFont.load_default()
        
    # 4. Add text
    text_to_add = "www.GPTSportsWriter.com"
    text_color = (255, 255, 255) # Yellow color
    d.text((10, 20), text_to_add, font=fnt, fill='white', stroke_width=2, stroke_fill='black')
    d.text((10, 80), title, font=fnt2, fill='white', stroke_width=2, stroke_fill='black')
    
    # 5. Save the image
    img.save(filename)

    print("Image 'image_with_text.png' created successfully.")

