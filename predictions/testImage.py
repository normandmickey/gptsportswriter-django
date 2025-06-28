from PIL import Image, ImageDraw, ImageFont

def generate_image3(title, filename):
    """
    Generate an image with a blue background and text.

    Args:
    title (str): The title to display on the image, e.g., "Prediction: South Africa VS Zimbabwe2025-06-28".
    filename (str): The filename to save the image as.

    Returns:
    None
    """

    # Parse the title
    match = title.split(":")[1]
    away_team = match.split("VS")[0]
    home_team = match.split('VS')[1][:-10]
    match_date = match.split('VS')[1][-10:]


    # Create a new image
    img_width, img_height = 1024, 1024
    img = Image.new('RGB', (img_width, img_height), color=(73, 109, 137))  # Blue background

    # Create a drawing object
    d = ImageDraw.Draw(img)

    # Load a font (replace 'arial.ttf' with a font available on your system)
    try:
        fnt = ImageFont.truetype('arial.ttf', 80)
        fnt2 = ImageFont.truetype('arial.ttf', 50)
    except IOError:
        print("Arial font not found. Using default font.")
        fnt = ImageFont.load_default(size=80)  # Fallback to default font
        fnt2 = ImageFont.load_default(size=50)

    # Add text
    text_to_add = "www.GPTSportsWriter.com"
    text_color = (255, 255, 0)  # Yellow color
    print(img_width)
    d.text((20, 80), text_to_add, font=fnt, fill=text_color)
    d.text(((img_width - (len(away_team) * 27.5)) / 2, 190), away_team, font=fnt2, fill=text_color)
    d.text(((img_width - 55) / 2, 250), "VS", font=fnt2, fill=text_color)
    d.text(((img_width - (len(home_team) * 27.5)) / 2, 310), home_team, font=fnt2, fill=text_color)
    d.text(((img_width - (len(match_date) * 27.5)) / 2, 430), match_date, font=fnt2, fill=text_color)
    

    # Save the image
    img.save(filename)

generate_image3("Prediction: Washington Nationals VS Los Angeles Angels 2025-06-28", "test.png")