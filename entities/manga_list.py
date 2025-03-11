class MangaList:
    def __init__(self, ids: list[str]):
        self.ids: list[str] = ids

    def __repr__(self):
        return f"MangaList(ids={self.ids})"
    
    def to_dict(self) -> dict:
        return {
            "ids": self.ids,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict) or "ids" not in data or not isinstance(data["ids"], list):
            return cls([])
        return cls([str(id) for id in data["ids"]])

    def add_manga(self, new_id):
        if new_id not in self.ids:
            self.ids.append(new_id)
            self.ids.sort()
            return True
        return False