import os
import xml.etree.ElementTree as ET

def convert_xml_to_yolo(xml_file, output_dir):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    filename = root.find('filename').text
    image_width = int(root.find('size/width').text)
    image_height = int(root.find('size/height').text)

    base_filename = os.path.splitext(os.path.basename(xml_file))[0]
    output_filename = base_filename + '.txt'

    with open(os.path.join(output_dir, output_filename), 'w') as f:
        for obj in root.findall('object'):
            xmin = float(obj.find('bndbox/xmin').text)
            ymin = float(obj.find('bndbox/ymin').text)
            xmax = float(obj.find('bndbox/xmax').text)
            ymax = float(obj.find('bndbox/ymax').text)

            x_center = (xmin + xmax) / 2 / image_width
            y_center = (ymin + ymax) / 2 / image_height
            width = (xmax - xmin) / image_width
            height = (ymax - ymin) / image_height

            # Write class index (0) and bounding box coordinates
            f.write(f"0 {x_center} {y_center} {width} {height}\n")

def batch_convert_xml_to_yolo(xml_folder, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    xml_files = [f for f in os.listdir(xml_folder) if f.endswith('.xml')]
    for xml_file in xml_files:
        convert_xml_to_yolo(os.path.join(xml_folder, xml_file), output_dir)

# Example usage
xml_folder = 'C:/Users/l1972/OneDrive/Desktop/fresh/Full_Indian_NPs/google_images/xml'
output_dir = 'C:/Users/l1972/OneDrive/Desktop/fresh/Full_Indian_NPs/yolov5_annotations'
batch_convert_xml_to_yolo(xml_folder, output_dir)
