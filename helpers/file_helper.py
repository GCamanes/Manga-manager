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
        try:
            file_name = os.path.basename(urlsplit(url).path)
            file_extension = os.path.splitext(file_name)[-1]
            destination_path = os.path.join(destination_folder, new_name + file_extension if new_name != None else file_name)

            response = requests.get(url)

            if response.status_code == 200:
                with open(destination_path, 'wb') as file:
                    file.write(response.content)
                return destination_path
            else:
                raise ValueError(f"Failed to download file {url}. Status code: {response.status_code}")
        except Exception as e:
            raise e

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
            raise ValueError(f"Failed to convert image {input_path} {e}")

