import os
import io
import requests
import matplotlib.pyplot as plt
from PIL import Image
from urllib.request import urlopen

ALLOWED_EXTENSIONS = {".png", '.jpg', '.jpeg', '.webp', '.gif'}

#Tools functions
def process_image(image_link_or_path):
    try:
        urlopen(image_link_or_path)
        image_data = requests.get(image_link_or_path, stream=True).raw
    except : 
        image_data = image_link_or_path
    finally:
        image = Image.open(image_data)
        return image
    

def allowed_file(filename):
    return os.path.splitext(os.path.basename(filename))[1].lower() in ALLOWED_EXTENSIONS

def plot_to_IOBytes(figure):
  picture = io.BytesIO()
  figure.savefig(picture, format='png', dpi=1000,  transparent=True)
  picture.seek(0)
  return picture