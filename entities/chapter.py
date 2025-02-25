class Chapter:
    """Represents a manga chapter"""
    def __init__(self, number, url):
        self.number = number
        self.url = url

    def __repr__(self):
        return f"Chapter(number={self.number}, url={self.url})"