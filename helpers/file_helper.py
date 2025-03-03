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

    # Function to download a file from a URL
    @staticmethod
    def download_file(url, destination_folder):
        """
        Downloads a file from the given URL and saves it to the destination folder with the same filename.

        :param url: URL of the file to download.
        :param destination_folder: Folder where the file will be saved.
        """
        # Extract file name from the URL
        file_name = os.path.basename(urlsplit(url).path)
        destination_path = os.path.join(destination_folder, file_name)

        response = requests.get(url)

        if response.status_code == 200:
            with open(destination_path, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded successfully: {destination_path}")
            return file_name
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
            return None

    # Function to convert a WEBP image to PNG with optional output filename
    @staticmethod
    def convert_webp_to_png(input_path, output_path=None):
        """
        Converts a WEBP image to PNG format.

        :param input_path: Path to the input WEBP image.
        :param output_path: Optional path to save the output PNG image. If not provided, defaults to input filename with .png extension.
        """
        if output_path is None:
            # If no output path is provided, use the input file name with '.png' extension
            output_path = os.path.splitext(input_path)[0] + ".png"
        
        try:
            image = Image.open(input_path)
            image.save(output_path, "PNG")
            print(f"Image converted successfully: {output_path}")
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
