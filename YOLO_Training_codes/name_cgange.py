import os

def rename_files(image_folder, annotation_folder):
    image_extensions = ['.jpg', '.jpeg', '.png']
    annotation_extensions = ['.xml']

    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f)) and f.lower().endswith(tuple(image_extensions))]
    annotation_files = [f for f in os.listdir(annotation_folder) if os.path.isfile(os.path.join(annotation_folder, f)) and f.lower().endswith(tuple(annotation_extensions))]

    # Sort files to ensure they're in the same order
    image_files.sort()
    annotation_files.sort()

    for index, (old_image, old_annotation) in enumerate(zip(image_files, annotation_files)):
        new_name = f"car{index}"
        image_ext = os.path.splitext(old_image)[1]
        annotation_ext = os.path.splitext(old_annotation)[1]

        new_image_name = f"{new_name}{image_ext}"
        new_annotation_name = f"{new_name}{annotation_ext}"

        os.rename(os.path.join(image_folder, old_image), os.path.join(image_folder, new_image_name))
        os.rename(os.path.join(annotation_folder, old_annotation), os.path.join(annotation_folder, new_annotation_name))

# Example usage
image_folder_path = 'C:/Users/l1972/OneDrive/Desktop/fresh/Full_Indian_NPs/google_images/images'
annotation_folder_path = 'C:/Users/l1972/OneDrive/Desktop/fresh/Full_Indian_NPs/google_images/xml'
rename_files(image_folder_path, annotation_folder_path)
