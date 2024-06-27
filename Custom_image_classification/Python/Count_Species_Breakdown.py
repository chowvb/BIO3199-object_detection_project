# Import modules
import tensorflow as tf
from tensorflow import keras 
import matplotlib.pyplot as plt
import os, pathlib
import pandas as pd
import numpy as np

# Define a function that utilises the colour image classification model created. Input argument is the file name to be predicted.
def sp_predict(image_name):
    # Load model weights
    new_model = load_model("Species_Classification_Model.h5")

    # Define image size
    image_size = (200, 200)

    # define the file path for the image to be predicted (input arg from the function)
    test_image = os.path.abspath(image_dir/image_name)
    
    # Preprocess the image to the same format as the images used whn training the images
    img = keras.preprocessing.image.load_img(
        test_image, 
        target_size = image_size
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    # Store the predicted outcome
    pred = new_model.predict(img_array)
    list = pred.flatten()

    # Multiple the scores to change them to a percentage
    probability = list*100
    comp = {spp_list[i]:probability[i] for i in range(len(spp_list))}
    dic = comp

    # Store all of the scores into a dataframe
    df = pd.dataframe(probability, spp_list, columns = ["Species Match (%)"])
    species = df.sort_values(by=["Species Match (%)"], ascending = False).round(2)

    # Return the dataframe asa the output of the function
    return species


# Loop through the directory and use megadetector to detect animals and crop the bounding boxes and save the image into a "cropped" folder

# Define the working directory path 
cwd = pathlib.Path("test_data")
root_dir = pathlib.Path("training_data/raw_images")

# Create an list to store all the names of species in the training data
spp_list = []
for species in os.listdir(root_dir):
    spp_list.append(species)

# Create a dataframe that 
my_data_df = pd.DataFrame()
df_columns = {
    "Date":(),
    "Location":(),
    "Feed":()
}

for species in os.listdir(root_dir):
    df_columns.update({species:0})

# Store the date in df_columns into the dataframe
for key in df_columns:
    my_data_df[key] = df_columns[key]

for location in os.listdir(cwd):
    #print(location,":") # Print the location for debugging if the code breaks.
    feed_type_dir = cwd/location
    
    # loop through the folder containing the different types of feed
    for feed_type in os.listdir(feed_type_dir):

        # Store the dates that the images were captured
        data_dir = feed_type_dir/feed_type/"date"

        # Loop through the dates within the feed types folder
        
