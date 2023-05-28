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
    img = cv2.resize(cv2.imread(image_name),(750,750))
    cv2.imshow("Image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    flag = input("Was the image an Outdoor image?(y/n/recheck): ")
    if flag == 'recheck':
        check_img(image_name)
    else:
        return img, str(flag)

org, flag = check_img(img_name)

def detect_ELA(img_name):
    res1 = ''
    #preparing img for ELA_model()
    np_img_input = prepare_image_for_ela(img_name)
   
    #load model
    ELA_model = load_model('ELA_Training/ELA_model.h5')

    #test image
    Y_predicted = ELA_model.predict(np_img_input, verbose=0 )

    res1 += "1. Model shows {}% accuracy of image being {}".format(round(np.max(Y_predicted[0])*100),class_ELA[np.argmax(Y_predicted[0])])
    return res1

#detect_ELA('MetaData/img.jpg')
def detect_weather(img_name):
    res3 = ''
    np_img_input = prerpare_img_for_weather(img_name)

    model_Weather = load_model('WeatherCNNTraining/Weather_Model.h5')

    #test image
    Y_predicted = model_Weather.predict(np_img_input, verbose=0)

    res3 += "3. Model shows weather in Image is {}".format(class_weather[np.argmax(Y_predicted[0])])
    return res3

def org_weather(img_name):
    res2 = ''
    date_time,lat,long = image_coordinates(img_name)
    res2 += "2. Weather originally was {}".format(get_weather(date_time,lat,long))
    return res2

res1 = detect_ELA(img_name)
res2 = ''
res3 = ''
if flag == 'y':
    res2 = org_weather(img_name)
    res3 = detect_weather(img_name)

print("RESULTS:\n{}\n{}\n{}".format(res1,res2,res3))

blank = np.zeros((750,750,3),np.uint8)

cv2.putText(blank,res1,(10,20),cv2.FONT_HERSHEY_SIMPLEX,.7,(255,255,255),1)
cv2.putText(blank,res2,(10,70),cv2.FONT_HERSHEY_SIMPLEX,.7,(255,255,255),1)
cv2.putText(blank,res3,(10,120),cv2.FONT_HERSHEY_SIMPLEX,.7,(255,255,255),1)

final_res = np.concatenate((org,blank), axis=1)
cv2.imwrite('res/org1.jpg',final_res)
cv2.imshow("Result",final_res)
cv2.waitKey(0)
cv2.destroyAllWindows()