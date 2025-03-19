import re

class ChapterPatterns:
    def __init__(self, patterns=None):
        self.patterns = set(patterns) if patterns else set()

    def __repr__(self):
        return f"ChapterPatterns(patterns={self.patterns})"
    
    def to_dict(self) -> dict:
        return {"patterns": sorted(list(self.patterns))}

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            return cls(())
        return cls(data.get("patterns", []))

    def add_pattern(self, candidate: str) -> None:
        normalized = re.sub(r'\d', '#', candidate)
        match = re.search(r"(.*[\d#])[^#\d]*$", normalized)
        pattern = match.group(1) if match else normalized
        self.patterns.add(pattern)