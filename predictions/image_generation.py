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
    print(title)
    match = title.split(":")[1]
    away_team = match.split("VS")[0]
    home_team = match.split('VS')[1][:-11]
    match_date = match.split('VS')[1][-11:]
    # 1. Create a new image
    img_width, img_height = 1024, 1024
    img = Image.new('RGB', (img_width, img_height), color=(73, 109, 137))  # Blue background

    # 2. Create a drawing object
    d = ImageDraw.Draw(img)

    # 3. Load a font (replace 'arial.ttf' with a font available on your system)
    try:
        fnt = ImageFont.truetype('arial.ttf', 80)
        fnt2 = ImageFont.truetype('arial.ttf', 50)
    except IOError:
        print("Arial font not found. Using default font.")
        fnt = ImageFont.load_default(size=80) # Fallback to default font
        fnt2 = ImageFont.load_default(size=50)

    # 4. Add text
    text_to_add = "www.GPTSportsWriter.com"
    text_color = (255, 255, 0) # Yellow color
    d.text((20, 80), text_to_add, font=fnt, fill=text_color)
    d.text(((img_width - (len(away_team) * 27.5)) / 2, 190), away_team, font=fnt2, fill=text_color)
    d.text(((img_width - 55) / 2, 250), "VS", font=fnt2, fill=text_color)
    d.text(((img_width - (len(home_team) * 27.5)) / 2, 310), home_team, font=fnt2, fill=text_color)
    d.text(((img_width - (len(match_date) * 27.5)) / 2, 430), match_date, font=fnt2, fill=text_color)
    
    # 5. Save the image
    img.save(filename)

    #print("Image 'image_with_text.png' created successfully.")

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
        fnt = ImageFont.load_default(size=50) # Fallback to default font
        fnt2 = ImageFont.load_default(size=30)

    # 4. Add text
    text_to_add = "www.GPTSportsWriter.com"
    text_color = (0, 255, 0) # Florescent Green Color
    d.text((10, 884), text_to_add, font=fnt, fill=text_color, stroke_width=2, stroke_fill='black')
    d.text((10, 944), title, font=fnt2, fill=text_color, stroke_width=2, stroke_fill='black')
    
    # 5. Save the image
    img.save(filename)

    #print("Image 'image_with_text.png' created successfully.")

