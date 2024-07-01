
# Import modules 
import os, pathlib, shutil, random
import numpy as np 
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model 
import matplotlib.pyplot as plt 
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix

# Create a directory for the species labels to be produced for sorting
species_list_dir = pathlib.Path("training_data/cropped_images")
unlabelled_dir = pathlib.Path("cm_dataset/unlabelled")
labelled_dir = pathlib.Path("cm_dataset/labelled")

sp_list = []
classes = []

for species in os.listdir(species_list_dir):
    sp_list.append(species)

    classes.append(species)

classes.append("Other")

for item in sp_list:
    species_label_dir = labelled_dir/item

    if not os.path.exists(species_label_dir):
        os.makedirs(species_label_dir)

def sp_predict_colour(image_name):
    # Load the model trained earlier
    new_model = load_model("Species_Classificaiton_Model.h5")

    # Specify the image size 
    image_size = (200,200)

    # Create a path to the image inputted into the function 
    test_image = os.path.abspath(unlabelled_dir/image_name)

    # Preprocess the image 
    img = keras.preprocessing.image.load_img(
        test_image,
        target_size= image_size)
    
    # Convert the image into an array 
    img_array = keras.preprocessing.image.img_to_array(img)

    # Expand the image dimensions 
    img_array = tf.expand_dims(img_array, 0)

    # using our model predict the species of bird in the image 
    pred = new_model.predict(img_array)

    list = pred.flatten()

    # Save the probability as a percentage 
    probability = list * 100

    comp = {sp_list[i]:probability[i] for i in range(len(sp_list))}
    
    # Store data into a dataframe 
    df = pd.DataFrame(probability, sp_list, columns = ["Species Match (%)"])
    species = df.sort_values(by= ["Species Match (%)"], ascending= False).round(2)
    return species