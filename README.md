# Image Tampering Detection Using ELA and Metadata Analysis

Detecting alterations in digital images has become a significant area of study in recent years, as the authenticity of digital photos is increasingly important in a world where more than 3.2 billion images are uploaded to the internet daily. Image forgery is a very significant problem because it can be used to spread misinformation, sway public opinion, and even perpetrate crimes. Image forgery detection algorithms are a useful tool for identifying and preventing the spread of tampered images, and for protection against the negative impacts of image forgery. It is also more cost-effective than hiring additional staff or contracting with external experts to manually inspect images.

The proposed method exploits metadata analysis to give more insight into the authenticity of an image. Extracted metadata is used to get the weather at a given date and time of a location image is tagged with. Trained Weather Classifier CNN predicts the weather in an image, which now can be cross-checked with the original weather condition obtained using metadata. The system overview is depicted in Fig. 1. 

[!alt] <fig1>

## ELA of Real and Tampered image:

[!alt] <real>

[!alt] <tampered>

Dataset of real and tampered images(CASIA 2.0) have been preprocessed for Error Level Analysis, obtaining new processed dataset of 10091 training and 2k of validation.
<br>Achieved maximum accuracy of 95.12%. (Training)
<br>Test accuracy attained using the model was 87.24%. 

## Metadata based Weather Classifier CNN

Trained for total of 1804 training images and 451 for validation images, weather model classifies a outdoor scene into following weather conditions:
<ul>
<li> Lighting
<li> rainy
<li> cloudy
<li> sunny
</ul>

Test Accuracy attained using the model was 73.4%.
