# Image Tampering Detection Using ELA and Metadata Analysis

Image forensics has witnessed significant growth in recent years, driven by advancements in computer vision and the surge of digital data. Ensuring the authenticity of images has become a top priority, as sophisticated manipulation techniques continue to emerge. We propose a multi-modal approach to gain insight into the image's authenticity.

### Live Demo
You can try the live demo of the application here.\
[Live Demo](https://imagetamperingdetection.streamlit.app/)
 

### Running Locally
Clone the repo<br>
```bash
git clone https://github.com/jayant1211/Image-Tampering-Detection-using-ELA-and-Metadata-Analysis.git
cd Image-Tampering-Detection-using-ELA-and-Metadata-Analysis/
```

to install all dependencies, create a new virtualenv, and install all required packages as:<br>
```bash
pip install -r reuqirements
```

Usage:<br>
Keep the model in <i>ELA_Training</i> Folder<br>
run <code>streamlit run app.py</code> for local inference<br>

### A Short Summary
We are using ELA and Metadata Analysis to achieve insight into the authenticity of an image<br>
#### 1. ELA
when a lossy algorithm like JPEG compresses an image, the compression process introduces artifacts or discrepancies in it. these can appear as blocks or regions within an image, exhibiting pixel values that differ from those of the surrounding areas. when an image goes under manipulation, compression artifacts are disrupted for the tampered region.<br>

in ELA, we calculate the absolute mean of an image at different compression levels:
<p align="center">
  <img src="https://github.com/jayant1211/Image-Tampering-Detection-using-ELA-and-Metadata-Analysis/blob/main/rsc/ela.jpg" alt="ELA Real Image" width="75%" height="75%">
</p>
<p align="center">ELA</p>
by doing this, we are essentially amplifying the variations caused by compression artifacts.
<p align="center">
  <img src="https://github.com/jayant1211/Image-Tampering-Detection-using-ELA-and-Metadata-Analysis/blob/main/rsc/fake_img.jpg" alt="Fake Image" width="75%" height="75%">
</p>
<p align="center">ELA for fake image</p>
The CASIA2.0 dataset contains a set of real and tampered images, we have used this dataset, and it is pre-processed to produce the ELA of every image(optimal image quality for compression level for calculating absolute diff was 90%). This preprocessed dataset is then trained on DenseNet121.
<br>
<br>

#### 2. Weather Validation using Metadata Analysis
image contains a lot of metadata with it, say, camera model, date, time, location, etc. By 'weather validation' to gain insight into the authenticity of an image, we mean precisely validating the depicted weather. A trained Weather CNN detects weather depicted in an image(preferably outdoor), and this result of Weather CNN is validated using Historical weather data. for fetching weather data all you need is a good open-source weather database, place, date, and time. Using metadata analysis, we could extract longitude and latitude, as well as the date and time. then parsing this metadata, we can send a request to weather-API to get the original weather on that place on a given date and time and validate our weather-CNN's result.
<br>The dataset for training weather-CNN was collected from various sources. We have collected a total of 1,804 training images and 451 validation images, and the categories we narrowed down for the classification are the following:
<ul>
<li> Lighting
<li> rainy
<li> cloudy
<li> sunny
</ul>

### Training
In case you want to retrain the ELA models, download the CASIA2.0 Dataset and put it inside ELA_Training and run <code>main.ipynb</code>. If you want to access the weather dataset, you can contact me.

### Results
For ELA with DenseNet, using standard practices for training and optimizing the model, the accuracies model achieved were:
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
<p align="center">
  <img src="https://github.com/jayant1211/Image-Tampering-Detection-using-ELA-and-Metadata-Analysis/blob/main/res/edited.jpg" alt="ELA Real Image" width="45%" height="45%">
  <img src="https://github.com/jayant1211/Image-Tampering-Detection-using-ELA-and-Metadata-Analysis/blob/main/res/fake1.jpg" alt="ELA Real Image" width="45%" height="45%">
</p>
<p align="center">Tampered Images</p>

<p align="center">
  <img src="https://github.com/jayant1211/Image-Tampering-Detection-using-ELA-and-Metadata-Analysis/blob/main/res/org1.jpg" alt="ELA Real Image" width="45%" height="45%">
  <img src="https://github.com/jayant1211/Image-Tampering-Detection-using-ELA-and-Metadata-Analysis/blob/main/res/org2.jpg" alt="ELA Real Image" width="45%" height="45%">
</p>
<p align="center">Real Images</p>

[Video Result](https://youtu.be/aEpDw_GZb9g)

### To-Dos
- [ ] Use scene classification model to remove user dependency for checking whether the image is outdoor or not. (In progress)
- [ ] Integration of Web-Traces and more modalities to Improve upon the Results.

## Cite
If you use our study in your research, please consider citing us, Thanks:

<h3>BibTeX Citation</h3>

  <pre><code>
@INPROCEEDINGS{10169948,
  author={Madake, Jyoti and Meshram, Jayant and Mondhe, Ajinkya and Mashalkar, Pruthviraj},
  booktitle={2023 4th International Conference for Emerging Technology (INCET)}, 
  title={Image Tampering Detection Using Error Level Analysis and Metadata Analysis}, 
  year={2023},
  volume={},
  number={},
  pages={1-7},
  doi={10.1109/INCET57972.2023.10169948}}

  </code></pre>
