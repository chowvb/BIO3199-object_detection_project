# Import required modules
import os, pathlib, subprocess

# Set the working directory path for training images
cwd = pathlib.Path("training_data")

# Set the filepath for uncropped iNaturalist images

raw_images_dir = pathlib.Path(cwd/"raw_images")

# Loop through all of the species in the raw_images_dir
for species in os.listdir(raw_images_dir):

    # Print the name of the species
    print(species)

    # Define species filepath (Location of the saved images)
    pre_crop_images_dir = str(os.path.abspath(raw_images_dir/species))

    # Destination filepath (Where the cropped images are to be saved to)
    cropped_image_dir = str(os.path.abspath(cwd/"cropped_images"/species))

    # Destination path for .json file containing bounding boc co-ordinates for images.
    json_output_path = str(os.path.abspath(cwd/"file.json"))

    # Check if a directory for the cropped images is already present, if not then create a new folder
    if not os.path.exists(cropped_image_dir):
        os.makedirs(cropped_image_dir)
    
    # Output file path for crop log that MegaDetector produces
    log_dir = os.path.abspath(pathlib.Path("crop_log"))

    # Create a function that will run python scripts
    def run_python_script(command):
        try:
            result = subprocess.run(command, capture_output=True, text= True, check=True)
            print("Output:", result.stdout)
            print("Error", result.stderr)
            print("Command Executed Successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")
            print(f"Error: {e.stderr}")

    # Define command arguments for run_batch_detector.py
    rbd_command = [
        "python",
        "C:/git/cameratraps/detection/run_detector_batch.py",
        "C:/megadetector/md_v5a.0.0.pt",
        pre_crop_images_dir,
        json_output_path,
        "--recursive",
        "--output_relative_filenames",
        "--threshold",
        "0.5"
    ]
    
    # Define command arguments for crop_detections.py
    cd_command = [
        "python",
        "C:/git/cameratraps/classification/crop_detections.py",
        json_output_path,
        cropped_image_dir,
        "--images-dir",
        pre_crop_images_dir,
        "--square-crops",
        "--logdir",
        log_dir
    ]

    # Execute run_batch_detectory.py
    run_python_script(rbd_command)
    
    # Execute crop_detections.py
    run_python_script(cd_command)
    
    # Remove .json file after running to declutter folders
    os.remove(json_output_path)