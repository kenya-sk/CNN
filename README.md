## Introduction
This repository performs individual detection in consideration of overlap by using CNN in each pixel.


## Network
This model consists of three convolution layers (conv1-conv3), two max-pooling layers (pool1 and pool2), and four fully connected layers (fc1-fc4). Conv1 has 7×7×3 filters, conv2 has 7×7×32 filters and conv3 has 5×5× 32 filters. Max pooling layers with 2×2 kernel size are used after conv1 and conv2. Batch normalization was applied to conv1-con3 and fc1-fc3. The activate function was applied after every convolutional layer and fully connected layer by Leaky ReLU.
<img src="./image/demo/model.png" alt="model" height= 400 vspace="25" hspace="70">

## Getting Started
### Install Required Packages
First ensure that you have installed the required packages (requirements.txt).  


## Training
To create training data in the following procedure. Each file is included in the directory (src/datasets).
1. To get images from movie. To input the path of movie file and the path of output image file.
```
my_make.sh
```
or
```
g++ -o video2image video2image.cpp -std=c++11 `pkg-config --cflags opencv` `pkg-config --libs opencv`
```

2. By clicking the image, labeling is done and training data is created. To input the path of image file.
```
python3 image2trainingData.py
```

3. If you want training data of arbitrary frames, to create it by the following procedure.  
To input the path of video file. To press "P" when the desired frame appear. To press "S" when you finish selecting feature point and want to save. To press "Q" when you want to finish creating training data.
```
python3 video2training_data.py
```


## Training Your Own Model
To train your own models, follow these steps. Each file is included in the directory (src/model).  
The following technique was used to train the model.
- Down Sampling
- Early Stopping
- Batch Normalization
- Data Augmentation (Horizontal flip)
- Hard Negative Mining

### Training
To set the path of training/validation image and path of answer data(density map).  
Each parameter can be set with argument.
```
python3 train.py
```

### Prediction
To perform individual detection with the trained model.  
Each parameter can be set with argument.
```
python3 predict.py
```


### Evaluation
The evaluation metrics of individual detection are accuracy, recall, precision, and F-measure. The position of the individual predicted by CNN and the position of the answer label were associated by using the Hungarian algorithm. True Positive defined ad If the matching distance was less than or equal to the threshold value (default is 15).

```
python3 evaluation.py
```
