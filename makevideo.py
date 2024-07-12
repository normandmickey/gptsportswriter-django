from mutagen.mp3 import MP3 
from PIL import Image 
from pathlib import Path 
import os, math
import imageio 
from moviepy import editor
import numpy

audio_path = os.path.join(os.getcwd(), "c:/users/norma/documents/github/gptsportswriter-django/speech.mp3") 
video_path = os.path.join(os.getcwd(), "videos") 
images_path = os.path.join(os.getcwd(), "images") 
audio = MP3(audio_path) 
audio_length = audio.info.length 

path = "c:/users/norma/documents/github/gptsportswriter-django/images/"
dirs = os.listdir( path )

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((1024,1024), Image.LANCZOS)
            imResize.save(f + "_resized.jpg", 'JPEG', quality=90)


list_of_images = [] 
for image_file in os.listdir(images_path): 
    if image_file.endswith('.jpg'): 
        image_path = os.path.join(images_path, image_file) 
        image = Image.open(image_path)
        list_of_images.append(image) 

resize()

duration = audio_length/len(list_of_images) 
imageio.mimsave('images.gif', list_of_images, fps=1/duration) 
 
video = editor.VideoFileClip("images.gif") 
audio = editor.AudioFileClip(audio_path) 
final_video = video.set_audio(audio) 
os.chdir(video_path) 
final_video.write_videofile(fps=1, codec="libx264", filename="video.mp4")