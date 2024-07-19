import os
import random
from shutil import copyfile

# Define paths
ORIGINAL_IMAGE_PATH = "C:/Users/l1972/OneDrive/Desktop/fresh/Full_Indian_NPs/images/"
ORIGINAL_ANNOTATIONS_PATH = "C:/Users/l1972/OneDrive/Desktop/fresh/Full_Indian_NPs/yolov5_annotations/"

TRAIN_IMAGE_PATH = "C:/Users/l1972/OneDrive/Desktop/fresh/Full_Indian_NPs/Dataset/train/images/"
TRAIN_ANNOTATIONS_PATH = "C:/Users/l1972/OneDrive/Desktop/fresh/Full_Indian_NPs/Dataset/train/annots"

VAL_IMAGE_PATH = "C:/Users/l1972/OneDrive/Desktop/fresh/Full_Indian_NPs/Dataset/val/images"
VAL_ANNOTATIONS_PATH = "C:/Users/l1972/OneDrive/Desktop/fresh/Full_Indian_NPs/Dataset/val/annots"

# Create directories if they don't exist
os.makedirs(TRAIN_IMAGE_PATH, exist_ok=True)
os.makedirs(TRAIN_ANNOTATIONS_PATH, exist_ok=True)
os.makedirs(VAL_IMAGE_PATH, exist_ok=True)
os.makedirs(VAL_ANNOTATIONS_PATH, exist_ok=True)

# Define split ratios
train_ratio = 0.8  # 80% for training
val_ratio = 0.2    # 20% for validation

# Get list of images
images = os.listdir(ORIGINAL_IMAGE_PATH)

# Shuffle images
random.shuffle(images)

# Split images
num_images = len(images)
num_train = int(train_ratio * num_images)
num_val = num_images - num_train

# Copy images and annotations to respective folders
for i, image in enumerate(images):
    if i < num_train:
        copyfile(ORIGINAL_IMAGE_PATH + image, TRAIN_IMAGE_PATH + image)
        annotation_file = image.split(".")[0] + ".xml"
        copyfile(ORIGINAL_ANNOTATIONS_PATH + annotation_file, TRAIN_ANNOTATIONS_PATH + annotation_file)
    else:
        copyfile(ORIGINAL_IMAGE_PATH + image, VAL_IMAGE_PATH + image)
        annotation_file = image.split(".")[0] + ".xml"
        copyfile(ORIGINAL_ANNOTATIONS_PATH + annotation_file, VAL_ANNOTATIONS_PATH + annotation_file)
