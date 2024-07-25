import os 
import cv2
from PIL import Image, ImageChops, ImageEnhance
import numpy as np

def convert_to_ela_image(path, quality):
    temp_filename = 'temp_file_name.jpg'
    ela_filename = 'temp_ela.png'
    image = Image.open(path).convert('RGB')
    image.save(temp_filename, 'JPEG', quality = quality)
    temp_image = Image.open(temp_filename)

    ela_image = ImageChops.difference(image, temp_image)

    extrema = ela_image.getextrema()
    max_diff = sum([ex[1] for ex in extrema])/3
    if max_diff == 0:
        max_diff = 1

    scale = 255.0 / max_diff
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    
    return ela_image

def prepare_image_for_ela(image_path):
    ela_img = convert_to_ela_image(image_path, 90)
    img = np.array(ela_img.resize((128,128))).flatten() / 255.0
    img = img.reshape(128,128,3)
    return np.expand_dims(img, axis=0),ela_img

def prerpare_img_for_weather(image_path):
    img = np.array(Image.open(image_path).convert('RGB').resize((128,128)))/255.0
    img = img.reshape(128,128,3)
    return np.expand_dims(img, axis=0)
