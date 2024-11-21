from uuid import uuid4

class Book():
    def __init__(self, title: str, author: str, year: int) -> None:
        self.id = str(uuid4())
        self.title = title
        self.author = author
        self.year = year
        self.status = "В наличии"

    def __str__(self) -> str:
        return f"ID: {self.id}, Title: {self.title}, Author: {self.author}, Year: {self.year}, Status: {self.status}"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }


    def set_status(self, new_staus) -> str:
        if new_staus in ["В наличии", "Выдана"]:
            self.status = new_staus
            return f"Статус успешно изменен"
        else:
            raise ValueError("Недопустимый статус")

