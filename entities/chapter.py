class Chapter:
    """Represents a manga chapter"""
    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return f"Chapter(url={self.url})"