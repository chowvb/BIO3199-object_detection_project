"""
This script loops through all the raw images/data collected from the camera traps from Gosforth Nature Reserve,
It then sorts and seperates all of the images by date into different folders (This is crucial to the research project.)
"""
# Import modules
import os, shutil, pathlib, exifread

# Define the current working directory
cwd = pathlib.Path("test_data")

# Loop through each folder in the test_data folder 
for location in os.listdir(cwd):

    # Define the new file pathway
    location_dir = cwd/location

    # Loop through the next set of folders
    for feed_type in os.listdir(location_dir):

        # Define new folder paths to be used
        feed_type_dir = location_dir/feed_type
        image_folder_dir = feed_type_dir/"raw_images"

        # Loop through all of the folders containing camera-trap images
        for cameratrap_folder in os.listdir(image_folder_dir):
            
            # Loop through each of the images
            for image in os.listdir(image_folder_dir/cameratrap_folder):

                # Use try to skip/pass corrupted/invalid file types in the folders
                try:
                    # Create an image file path to the camera-trap image
                    exif_file = str(feed_type_dir/"raw_images"/cameratrap_folder/image)

                    # Open the image 
                    img_file = open(exif_file, "rb")

                    # Extract the tags embedded within the image using exifread
                    tags = exifread.process_file(img_file)

                    # Extract only the time and date of the original photo from exifdata
                    date_of_image = str(tags["EXIF DateTimeOrigin"])
                    day_of_image = str(date_of_image[0:10])

                    # Replace the ":" with a "_" as it will be easier to open later on
                    date = day_of_image.replace(":", "_")

                    # Define the new file location path for each of the image to be copied to 
                    newpath1 = feed_type_dir/"date"/date/"raw_image"
                    img_file.close()

                    # Check if there is already the file or date folder present to prevent any duplication of data.
                    if not os.path.exists(newpath1):
                        os.makedirs(newpath1)
                    
                    dated_image_path = newpath1/image
                    if not os.path.exists(dated_image_path):
                        shutil.copy(exif_file, dated_image_path)
                except:
                    pass