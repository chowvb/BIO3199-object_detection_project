# Import Modules
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras import layers
import os, pathlib

# Copy images to training, validation and test folders
original_dir = pathlib.Path("training_data/cropped_images")

# Get the number of different classes for our machine learning model 
classes = os.listdir(original_dir)
classes = len(classes)

"""Generatng a Dataset:
Define the desired image size to resize the images from iNaturalist to (PCs with GPUs will be able to run a larger
image size (255,255,3). Note: in the image size below image_size = (200,200) normally you would include the number of
colour channels (,3) at the end but, if it it isn't defined now keras will automatically default the colour channels to 3.
The batch size is also defined in this section, again more powerful machines could run at a higher batch_size, at the 
and complete model training faster but at the detrement of accuracy)
"""

# Define the input image size and batch size for the ML model 
image_size = (200,200)
batch_size = 16

"""
Seperate all the training data downloaded from iNaturalist into a training and validation dataset using 
image_dataset_from_directory() provided by keras preprocessing module. This module requires the arguments: 
Path to image directory, 
Validation_split (as a ratio 0.2 = 20% Validation/80% Training), 
Subset is required if validation split is defined in the function. 
Seed is an optional argument for random shuffling and transformation
image_size - preprocesses the images to the defined size before
batch_size - package images in to batches (number = number of images packaged into each batch)
label_mode - labels to be encoded as categorical for categorical entropy loss later when defining the model. 
"""


train_dataset, validation_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    "training_data/cropped_images",
    validation_split = 0.2,
    subset= "both",
    seed = 1337,
    image_size = image_size,
    batch_size= batch_size,
    label_mode = "categorical "
)

"""
Data augmentation adds random rotations and flips when the image is inputted into the first layer of the model,
RandomFlip is set to horizontal due to it beoing unlikely that the birds captured by the camera-traps will be flying upside down.
"""

# Define data augmentation to be performed onto training data.
data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1)
    ]
)

# Apply data augmentaiton to the training images.
train_dataset = train_dataset.map(
    lambda img, label:(data_augmentation(img), label),
    num_parallel_calls = tf.data.AUTOTUNE
)

# Prefetching samples in GPU memory will help maximise GPU utilisation 
train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)
validation_dataset = validation_dataset.prefetch(tf.data.AUTOTUNE)

# Building the DeepLearning Model 

def make_model(input_shape, num_classes):
    inputs=keras.Input(shape= input_shape)
    
    # Entry block 
    x = data_augmentation(inputs) # Perform data augmentation for gpu training 
    x = layers.Rescaling(1.0/255)(x) # Scale pixel values
    x = layers.Conv2D(128,3,strides = 2, padding="same")(x) 
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    
    previous_block_activation = x # Set aside residual
    
    # Subsequent blocks, can be adjusted for different fiter sizes. 
    for size in [256,512,728]: # Loop through filter sizes for multiple convolutional blocks
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size,3,padding="same")(x)
        x = layers.BatchNormalization()(x)
        
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)
        
        x = layers.MaxPooling2D(3,strides=2, padding="same")(x)
        
        # Project residual 
        
        residual = layers.Conv2D(size,1, strides =2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x,residual]) # Add back residual 
        previous_block_activation = x # Set aside next residual
        
    x = layers.SeparableConv2D(1024,3,padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    
    x = layers.GlobalAveragePooling2D()(x) # Global average pooling to reduce spatial dimensions
    if num_classes ==2: # Check the number of classes/labels for the activation function. 
        activation = "sigmoid"
        units = 1 
    else:
        activation = "softmax"
        units = num_classes 
        
    x = layers.Dropout(0.5)(x) # drop out for regularization 
    
    x = layers.Flatten()(x) # Flatten the output layer for the final dense layer
    
    outputs = layers.Dense(units, activation = activation)(x)
    print(units)
    return keras.Model(inputs,outputs)

"""The model image_size takes the image size defined at the start and adds a 3 into the argument to tell the model to expect
an RGB image with 3 colour channels
"""
# Call the model
model = make_model(input_shape= image_size +(3,),num_classes = classes)
model.summary()
#keras.utils.plot_model(model,show_shapes=True) 