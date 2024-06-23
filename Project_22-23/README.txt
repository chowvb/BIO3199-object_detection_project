"""
This repository contains all the code used for my final year project: Using Deep Learning to Investigate Food Preferences in Small UK Garden Birds During Winter

Some of the scripts used in this repository have been adapted to work on smaller datasets saved onto GitHub. I would recommend starting with the R folder to download training data for the image classification model first

R Folder:
1) bird_list.csv
This file contains the list of birdspecies that the image classification model was trained on. it contains the common name of the bird along with the Taxonomic ID number. This file is a pre-requisite to the iNaturalist_training_data_download.R 

2) iNaturalist_training_data_download.R 
Uses the names and taxonomic ID numbers from the bird_list.csv to retrieve research grade images from iNaturalist Citizen Science Database. The download function was adapted from a function created by Dr Roy Sanderson (Newcastle University).


Python Folder: 
Contains all of the code to pre-process training images for model training along with pre-processing of test images collected from Gosforth Nature Reserve. This project was coded using Jupyter Notebook for easy debugging and running different segments of code.  
Within this folder Keras with Tensorflow is required, along with the latest NVIDIA Cuda drivers, etc.


Pre-processing Scripts:
1) iNaturalist_Image_Preprocessing.ipynb
Megadetector (https://github.com/microsoft/CameraTraps/blob/main/megadetector.md) is utilised within this script to detect and crop images that contains animals. (Some images downloaded from the R script are not always images of birds).

2) data_preprocessing.ipynb 
Filters all the camera trap images taken from Gosforth Nature Reserve by the date the image was taken. 
MegaDetector is then used to detect and crop images containing animals and the empty images are deleted. 


Image Classification Models Scripts:
1) Bird_Classification_Default_Uncropped_Training_Images.ipynb
The first iteration of the image classification model used in the research project, model is trained on data that were not preprocessed using MegaDetector (Detection and cropping of images) 

2) Bird_Classification_Default.ipynb
The main images classification model used in the reasearch project. Trained on Preprocessed MegaDetector generated using the data_preprocessing.ipynb file. Architecture & Weights are stored in Species_Classification_Model_Gray.h5 file

3) Bird_Classification_BW.ipynb
A black and white image classification model. Model is trained on Preprocessed MegaDetector data however, all the training images are augmented to grayscale images before training. Architecture & Weights are stored in Species_Classification_Model_Gray.h5 file


Prediction Scripts:
1) Image_Predict_Single.ipynb
A small script that predicts the species of a test image. Prediction scores are then saved into a .csv file.

2) Count_Species_Breakdown.ipynb
Similar script to the single image predictor but it is looped through the whole test image directory. The output is a .csv file that gives the count for each species for each data collection day. 

3) Test_Dataset_&_Confusion_Matrix_Gen.ipynb
Produces a test dataset by randomly selecting files from data collected from Gosforth Nature Reserve, The user of the manually identifies the animal in the images using the built in application. The image classification model then predicts the animal within the images and a confusion matrix is produced. 
"""