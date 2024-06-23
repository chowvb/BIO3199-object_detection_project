# Newcastle University Research Dissertation Thesis 
Using Deep Learning to Investigate Food Preferences in Small UK Garden Birds During Winter.

## Pre-requisites
This repository contains all of the code used in my final year project. Some of the code may not work currently. I am adapting it to work on smaller datasets.  
This project utilises Keras with TensorFlow, the latest NVIDIA CUDA drivers are also required, the project used YOLO5 architecture (https://github.com/ultralytics/yolov5).  
**Note:** This project was completed in 2022/2023, the latest versions of MegaDetector (https://github.com/microsoft/CameraTraps/blob/main/megadetector.md) may not be compatable. Having read through the meagadetector.md (MegaDetector Used: https://github.com/microsoft/CameraTraps/blob/8fe14a50f95b27d57cea74fe65a36ba4b9c4d9ac/megadetector.md#downloading-the-model).  

## Order of Files to run
### Species Classification
1) Add species of animal that the species identifier is to be modelled on into birds_list.csv
2) Run iNaturalist_training_data_download.R to create folders for each of the species and download images from the iNaturalist Database.
3) Run iNaturalist_Image_Preprocessing.py.  This script will sort through the images downloaded from iNaturalist using MegaDetector to ensure that the images downloaded contain a bird in the image (When MegaDetector returns 90% Confidence). A .json containing the 