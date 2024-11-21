from datetime import date
from typing import Dict
from uuid import UUID
from dataclasses import dataclass, as_dict

@dataclass
class Book:
    id: UUID
    title: str
    author: str
    year: int
    status: str = "В наличии"
    
    def to_dict(self) -> Dict:
        return as_dict(self)

    def validate(self) -> Dict:
        errors = {}

        if not self.title:
            errors["title"] = "Название не может быть пустым."
        elif len(self.title) > 100:
            errors["title"] = "Название слишком длинное (максимум 100 символов)."


        if not self.author:
            errors["author"] = "Автор не может быть пустым."
        elif len(self.author) > 50:
            errors["author"] = "Имя автора слишком длинное (максимум 50 символов)."


        if not isinstance(self.year, int) or self.year < 0:
            errors["year"] = "Год должен быть положительным целым числом."
        elif self.year > date.today().year + 1:
            errors["year"] = "Год не может быть в будущем."


        if self.status not in ["В наличии", "Нет в наличии", "Заказ", "Выдан"]:
            errors["status"] = "Недопустимый статус."

        return errors

    def __post_init__(self) -> None:
        errors = self.validate()
        if errors:
            raise ValueError(f"Ошибка валидации: {errors}")

