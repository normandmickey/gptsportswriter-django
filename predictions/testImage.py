from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji

def wrap_text(text, font, max_width):
    lines = []
    words = text.split(' ')
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        text_width = font.getlength(test_line)
        if text_width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

# Create a blank image
image = Image.new("RGB", (1024, 1024), color=(255, 255, 255))
draw = ImageDraw.Draw(image)

# Load the font
try:
    font = ImageFont.truetype("arial.ttf", 20)  # Replace with your font path
except IOError:
    font = ImageFont.load_default()  # Fallback if the specified font is not found

# Text and settings
long_text = "Chicago White Sox VS Toronto Blue Jays 2025-06-22 Blue Jays favored like they're the Avengers, but Houser's pitching like Thanos. White Sox at +215? Might be the snap they need! ⚾️💥 #UnderdogMagic #BetTheSox @BlueJays @whitesox Want more? Visit https://www.gptsportswriter.com/prediction-detail/prediction-chicago-white-sox-vs-toronto-blue-jays-2025-06-22/"
max_width = 800  # Maximum width for the text block
x_position = 20
y_position = 20
line_spacing = 10  # Pixels between lines
fill_color = (0, 0, 0)  # Black color

# Wrap the text and draw each line
wrapped_lines = wrap_text(long_text, font, max_width)
for line in wrapped_lines:
    #draw.text((x_position, y_position), line, font=font, fill=fill_color)
    with Pilmoji(image) as pilmoji:
        pilmoji.text((x_position, y_position), long_text.strip(), (0, 0, 0), font)
        y_position += font.size + line_spacing  # Use font size for line height

# Save the result
image.save("wrapped_text_image.png")