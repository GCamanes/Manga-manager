import re
from urllib.parse import urlsplit
from PIL import Image

class StringHelper:
    # Create folder only if it doesn't exist
    @staticmethod
    def remove_up_to_nth_hyphen(s, n=2) -> str:
        pattern = r'^(?:[^-]+-){' + str(n) + '}'
        return re.sub(pattern, '', s)