from flask import Flask, request, render_template
from PIL import Image
import numpy as np

app = Flask(__name__)

ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width / 1.65  
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayscale_image(image):
    return image.convert("L")

def image_to_ascii(image):
    pixels = np.array(image)
    ascii_str = ""
    for pixel_value in pixels:
        ascii_str += ASCII_CHARS[pixel_value // 32]
    return ascii_str

def convert_to_ascii(image):
    image = resize_image(image)
    image = grayscale_image(image)
    
    ascii_str = ""
    for y in range(image.height):
        for x in range(image.width):
            ascii_str += ASCII_CHARS[image.getpixel((x, y)) // 32]
        ascii_str += "\n"
    
    return ascii_str

@app.route('/')
def loading():
    return render_template('loading.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return "No image part"
    
    file = request.files['image']
    
    if file.filename == '':
        return "No selected file"
    
    if file:
        image = Image.open(file.stream)
        ascii_art = convert_to_ascii(image)
        return ascii_art

if __name__ == "__main__":
    app.run(debug=True)
