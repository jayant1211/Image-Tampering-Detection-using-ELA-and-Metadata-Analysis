# Image Tampering Detection Using ELA and Metadata Analysis

Image Forensics has become a significant area of study in recent years. The authenticity of digital photos is increasingly important in a world where more than 3.2 billion images are uploaded to the internet daily.

Image forgery is a very significant problem because it can be used to spread misinformation, sway public opinion, and even perpetrate crimes. We all know at least one example, say of a friend or on a more widespread level, which was fueled by a fake image. How can one tell if an image is digitally manipulated? With advanced image editing software in the hands of the general public, everyone and their cat can create a morphed image.

Well, image forgery is a field where a user or organization uses detection algorithms for identifying and preventing the spread of tampered images, and for protection against the negative impacts of image forgery. It is also more cost-effective than hiring additional staff or contracting with external experts to manually inspect images.

We propose a multi-modal method, which uses a deep convolution network with error level analysis and metadata of an image linked with historical weather data to give insight into the authenticity of an image.

[!alt] <fig1>

## Error Level Analysis - ELA
  
The CNN part is easy - take two classes, real and fake, and train. This can work for most cases, but Error Level Analysis is a technique that highlights the edited areas with a weird blue-red tint.
  
[!alt] <real>

[!alt] <tampered>

So, before training the model, if every image is preprocessed with Error Level Analysis, it helps the model learn much better to classify among the ELA of real and fake images. The dataset of real and tampered images (CASIA 2.0) has been preprocessed for Error Level Analysis, obtaining a new processed dataset of 10,091 training images and 2,000 for validation. 
  
<br>We achieved a maximum accuracy of 95.12% during training.
<br>The test accuracy attained using the model was 87.24%.
  
## Metadata-based Weather Classifier CNN

The weather part is mostly helpful in outdoor images. For obvious reasons, we cannot infer the weather in an indoor scenario. We extract the metadata of the image to get the date, time, and location the image is tagged with (most digital cameras tag longitude and latitude of the location and time of the image captured). Additionally, we have our custom weather model trained for weather classification, which predicts the weather in an image. We can predict the weather in the image using the weather model and cross-check it with the actual weather of that location at that certain point in time the image is tagged with.
  

We have collected a total of 1,804 training images and 451 validation images, and the categories we narrowed down for the classification are the following:
<ul>
<li> Lighting
<li> rainy
<li> cloudy
<li> sunny
</ul>

Test Accuracy attained using the model was 73.4%.
  
## Results
  
So its upto user at end to infer authencity by looking at the result of an image. The insight with ELA model confidence along with Weather Model result is shown as:
[!alt] <real>
