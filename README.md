# Image Tampering Detection Using ELA and Metadata Analysis

Image forensics has witnessed significant growth in recent years, driven by advancements in computer vision and the surge of digital data. Ensuring the authenticity of images has become a top priority, as sophisticated manipulation techniques continue to emerge. We propose a multi-modal approach to gain insight on image's authenticity.

### Setup
Clone the repo<br>
<code>git clone {}
cd {}
</code>

to install all dependencies, create a new virtualenv and install all required packages as:<br>
<code>pip install -r reuqirements</code>

Usage:<br>
run <code>main.py</code><br>

### A Short Summary
We are using ELA and Metadata Analysis to achieve insgiht into authencity of an image<br>
<i>1. ELA</i><br>
when a lossy algorithm like JPEG compresses an image, compression process introduces artifacts or discrepencies in it. these can appear as blocks or regions within an image, exhibiting pixel values that differ from those of the surrounding areas. when an image goes under manipulation, compression artifacts are disrupted for tampered region.<br>
in ELA, we calculate absolute mean of image at different compression level:
<image>
by doing this, we are essentially amplifying the variations caused by compression artifacts.
<br>
CASIA2.0 dataset contains set of real and tampered images, we have used this dataset, and it is pre-processed to produce ELA of every image(optimal image quality for compression level for calculating absolute diff was 90%). These preprocessed dataset is then trained on DenseNet121.

<i>2. Weather Validation using Metadata Analysis</i><br>
image contains lot of metadata with it, say, camera model, date, time, location etc. By 'weather validation' to gain insight into the authenticity of an image, we mean precisely validating the depicted weather. A trained Weather CNN detects a weather depicted in an image(preferrably outdoor), and this reuslt of weather CNN is validated using Historical weather data. for fetching a weather data all you need a good open source weather database, place, date and time. Using metadata analysis, we could extract longitude and latitude, as well as the date and time. then parsing this metadata, we can send a request to weather-API to get original weather on that place on given date and time, and validate our weather-CNN's result.
<br>The dataset for training weather-CNN was collected from various sources. if you want to access the dataset, you can contact me. We have collected a total of 1,804 training images and 451 validation images, and the categories we narrowed down for the classification are the following:
<ul>
<li> Lighting
<li> rainy
<li> cloudy
<li> sunny
</ul>

### Results
For ELA with DenseNet, using standard practises for training and optimizing the model, the accuracies model achieved were:
| Metric                | Accuracy  |
|-----------------------|----------:|
| Train Accuracy        |   98.34%  |
| Validation Accuracy   |   93.78%  |
| Test Accuracy         |   87.24%  |

For Weather CNN:<br>
| Metric                | Accuracy  |
|-----------------------|----------:|
| Train Accuracy        |   91.2%   |
| Validation Accuracy   |   81.6%   |
| Test Accuracy         |   73.4%   |

The output of both modules(ELA and Weather Validation using Metadata), is displayed together for better insight into authenticity of image:
<image>  

