import streamlit as st
import cv2
import os
import numpy as np
from keras.models import load_model
from helper import prepare_image_for_ela, prerpare_img_for_weather
from fetchOriginal import image_coordinates, get_weather
from PIL import Image as PILImage
import io

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
st.title("Image Tampering Detection Using ELA and Metadata Analysis")

st.markdown(""" 
            ### Welcome to the Image Tampering Detector!
            **What This Project Does:**
            This tool helps you determine whether an image has been altered or manipulated. Try it out and see if your images hold up under scrutiny!
            """)
with st.expander("How it Works?"):
    st.markdown("""
There are two parallels that are being used to identify an image's authenticity:

1. **Error Level Analysis (ELA):**
   - Images that are edited often show different compression artifacts compared to the original ones. ELA highlights these discrepancies, making tampering visible.
""")

    # Create columns for horizontal layout
    col1, col2 = st.columns(2)

    # Display ELA images in columns
    with col1:
        st.image("rsc/real.jpg", caption="ELA of a Real Image", use_column_width=True)

    with col2:
        st.image("rsc/fake.jpg", caption="ELA of a Tampered Image", use_column_width=True)

    st.markdown("""
    Notice how ELA on real image shows consistency across the image but on fake image, ELA shows discrepancy across some regions.
                
    2. **Weather Validation:**
        - **Purpose:** Weather Validation examines the metadata embedded in the image to cross-check if the depicted weather conditions are consistent with historical weather data from the image's recorded location and time.
        - **How?:**
            Images often contain metadata that includes information about the location, date, and time when the image was taken.
            Using this metadata, historical weather databases are queried to retrieve the weather conditions for the recorded location and date.
            Then actual weather conditions in the image are compared (as identified by a Weather CNN model) with the historical data to determine if they match.
        - **Why It Matters:** This helps in verifying the authenticity of outdoor images by ensuring that the weather depicted matches what was recorded historically for that location and time. Discrepancies can indicate tampering or misrepresentation.
""")
with st.expander("How to use it?"):
    st.markdown("""
    1. **Upload an Image:** Choose an image to analyze.
    2. **Select the Outdoor Option:** Indicate whether the image is taken outdoors.
    3. **View Results:** Get insights into the image’s authenticity with detailed analysis.

    """)

with st.expander("Got a Query?"):
    st.markdown("""
Hi, I'm Jayant
                
If you have any questions, feedback, suggestions, or just want to chat, feel free to reach out!

- [Linkedin](https://www.linkedin.com/in/jayantmeshram/)
- [Github](https://github.com/jayant1211)

you can also email me at jayantmeshram398@gmail.com.
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
        # Display ELA result image
        st.image(ela_result, caption="ELA Analysis")

        #TODO ela img goes away, add session step here
        
        # Save ELA result image to a BytesIO object
        buffer = io.BytesIO()
        ela_result.save(buffer, format="JPEG")  # ela_result should be a PIL Image
        buffer.seek(0)
        
        # Add a download button for the ELA result image
        st.download_button(
            label="Save ELA Result Image",
            data=buffer,
            file_name="ela_result.jpg",
            mime="image/jpeg"
        )

    # Button to reset the session state and allow new image upload
    if st.button("Try New Image"):
        st.session_state.step = 0
        #st.experimental_rerun() is not working
        st.rerun()
