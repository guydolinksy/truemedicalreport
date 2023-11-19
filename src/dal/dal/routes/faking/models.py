from datetime import date


class Post():
    id: int
    title: str
    description: str
    created_at: date

    def __init__(self, id, title, description, created_at):
        self.id = id
        self.title = title
        self.description = description
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": str(self.created_at.strftime('%d-%m-%Y'))
        }
