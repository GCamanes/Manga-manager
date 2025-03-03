import os
import requests
from urllib.parse import urlsplit
from PIL import Image

class FileHelper:
    # Create folder only if it doesn't exist
    @staticmethod
    def create_folder(path):
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        return False

    # Function to download a file from a URL
    @staticmethod
    def download_file(url: str, destination_folder: str, new_name: str = None):
        file_name = os.path.basename(urlsplit(url).path)
        file_extension = os.path.splitext(file_name)[-1]
        destination_path = os.path.join(destination_folder, new_name + file_extension if new_name != None else file_name)

        response = requests.get(url)

        if response.status_code == 200:
            with open(destination_path, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded successfully: {destination_path}")
            return destination_path
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
            return None

    # Function to convert a WEBP image to PNG with optional output filename
    @staticmethod
    def convert_webp_to_png(input_path):   
        if (not input_path.endswith(".webp")):
            return input_path
        try:
            image = Image.open(input_path)
            # Convert and save as PNG
            new_file_path = os.path.splitext(input_path)[0] + ".png"
            image.save(new_file_path, "PNG")
            # Delete the original .webp file
            os.remove(input_path)
            return new_file_path
        except Exception as e:
            print(f"Error while converting image: {e}")

    # Batch convert all WEBP images in a folder to PNG
    @staticmethod
    def batch_convert_webp_to_png(folder_path):
        """
        Converts all WEBP images in a folder to PNG format.

        :param folder_path: Path to the folder containing WEBP images.
        """
        for filename in os.listdir(folder_path):
            if filename.endswith(".webp"):
                input_path = os.path.join(folder_path, filename)
                output_path = os.path.join(folder_path, filename.replace(".webp", ".png"))
                FileHelper.convert_webp_to_png(input_path, output_path)
