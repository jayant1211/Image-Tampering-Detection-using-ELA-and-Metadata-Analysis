import cv2
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
from keras.models import load_model
from helper import prepare_image_for_ela, prerpare_img_for_weather
import numpy as np
from fetchOriginal import image_coordinates, get_weather

class_weather = ['Lightning','Rainy','Snow','Sunny']
class_ELA = ['Real','Tampered']

img_name = input("Please enter .jpg/.jpeg image path: ")

#make sure image is lossy compression
if not (img_name.endswith('.jpeg') or img_name.endswith('.jpg')):
    while not (img_name.endswith('.jpeg') or img_name.endswith('.jpg')):
        img_name = input("Invalid Input! Please enter .jpg/.jpeg image path: ")

#Display image to user to set weather-flag
def check_img(image_name):
    img = cv2.resize(cv2.imread(image_name),(400,400))
    cv2.imshow("Image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    flag = input("Was the image an Outdoor image?(y/n/recheck): ")
    if flag == 'recheck':
        check_img(image_name)
    else:
        return str(flag)

flag = check_img(img_name)

def detect_ELA(img_name):
    #preparing img for ELA_model()
    np_img_input = prepare_image_for_ela(img_name)
   
    #load model
    ELA_model = load_model('ELA_Training/ELA_model.h5')

    #test image
    Y_predicted = ELA_model.predict(np_img_input, verbose=0 )

    print("\n***RESULTS***\n1. Model shows ",round(np.max(Y_predicted[0])*100,3),"% Accuracy of Image being ",class_ELA[np.argmax(Y_predicted[0])])
    
#detect_ELA('MetaData/img.jpg')
def detect_weather(img_name):
    np_img_input = prerpare_img_for_weather(img_name)

    model_Weather = load_model('WeatherCNNTraining/Weather_Model.h5')

    #test image
    Y_predicted = model_Weather.predict(np_img_input, verbose=0)

    print("\n3. Model shows weather in Image is ",class_weather[np.argmax(Y_predicted[0])])

def org_weather(img_name):
    date_time,lat,long = image_coordinates(img_name)
    print("\n2. Weather originally was: ",get_weather(date_time,lat,long))

detect_ELA(img_name)

if flag == 'y':
    org_weather(img_name)
    detect_weather(img_name)
