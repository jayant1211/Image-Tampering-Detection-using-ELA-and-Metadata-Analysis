import streamlit as st
import cv2
import os
import numpy as np
from keras.models import load_model
from helper import prepare_image_for_ela, prerpare_img_for_weather
from fetchOriginal import image_coordinates, get_weather
from PIL import Image as PILImage

# Constants
class_weather = ['Lightning', 'Rainy', 'Snow', 'Sunny']
class_ELA = ['Real', 'Tampered']

# Functions
def check_img(image_name):
    img = cv2.resize(cv2.imread(image_name), (750, 750))
    return img

def detect_ELA(img_name):
    global ela_result
    np_img_input, ela_result = prepare_image_for_ela(img_name)
    ELA_model = load_model('ELA_Training/model_ela.h5')
    Y_predicted = ELA_model.predict(np_img_input, verbose=0)
    return "Model shows {}% accuracy of image being {}".format(round(np.max(Y_predicted[0]) * 100), class_ELA[np.argmax(Y_predicted[0])])

def detect_weather(img_name):
    np_img_input = prerpare_img_for_weather(img_name)
    model_Weather = load_model('WeatherCNNTraining/Weather_Model.h5')
    Y_predicted = model_Weather.predict(np_img_input, verbose=0)
    return "Model shows weather in Image is {}".format(class_weather[np.argmax(Y_predicted[0])])

def org_weather(img_name):
    date_time, lat, long = image_coordinates(img_name)
    location, date, weather = get_weather(date_time, lat, long)
    return "The Image was taken at {} and weather there on {} was {}".format(location, date, weather)

# Streamlit Interface
st.title("Image Tampering Detection and Weather Classification")

# Introductory Text
st.markdown("""
### Welcome to the Image Tampering Detector!

**What This Project Does:**
This tool helps you determine whether an image has been altered or manipulated. Using advanced technologies, we analyze images to reveal their authenticity.

**How It Works:**
1. **Error Level Analysis (ELA):**
   - Images that are edited often show different compression artifacts compared to original ones. We use ELA to highlight these discrepancies, making tampering visible.
   - **Real vs. Tampered Images:**
    ![Real](rsc/ela.jpg)
    ![Tampered Image](rsc/fake.jpg)
         
2. **Weather Validation:**
   - By examining the metadata of the image, we check if the weather depicted matches historical data from the image’s recorded location and time.
   

**How To Use It:**
1. **Upload an Image:** Choose an image to analyze.
2. **Select the Outdoor Option:** Indicate whether the image is taken outdoors.
3. **View Results:** Get insights into the image’s authenticity with detailed analysis.

Try it out and see if your images hold up under scrutiny!
""")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 0

# Handle file upload
uploaded_file = st.file_uploader("Choose a .jpg/.jpeg image...", type=["jpg", "jpeg"])

if uploaded_file is not None:
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    flag = st.radio("Was the image an Outdoor image?", ('Yes', 'No'))

    if st.button("Proceed") and st.session_state.step == 0:
        st.session_state.step = 1

# Show results if step > 0
if st.session_state.step > 0:
    org = check_img("temp.jpg")
    res1 = detect_ELA("temp.jpg")
    res2, res3 = '', ''
    if flag == 'Yes':
        res2 = org_weather("temp.jpg")
        res3 = detect_weather("temp.jpg")

    st.write("### Results:")
    st.write("1. " + res1)
    if flag == 'Yes':
        st.write("2. " + res2)
        st.write("3. " + res3)

    if st.button("Show Error Level Analysis") and st.session_state.step == 1:
        st.image(ela_result, caption="ELA Analysis")

    # Button to reset the session state and allow new image upload
    if st.button("Try New Image"):
        st.session_state.step = 0
        st.experimental_rerun()
