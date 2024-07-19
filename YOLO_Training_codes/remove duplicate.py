import os
from collections import defaultdict

def find_duplicate_files(folder):
    file_dict = defaultdict(list)
    duplicate_files = []

    # Iterate through files in the folder
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath):
            file_dict[filename].append(filepath)

    # Check for files with same name
    for filename, filepaths in file_dict.items():
        if len(filepaths) > 1:
            duplicate_files.extend(filepaths)

    return duplicate_files

# Example usage
folder_path = 'C:/Users/l1972/OneDrive/Desktop/fresh/Full_Indian_NPs/google_images/'
duplicate_files = find_duplicate_files(folder_path)

if duplicate_files:
    print("Duplicate files found:")
    for file in duplicate_files:
        print(file)
else:
    print("No duplicate files found.")
