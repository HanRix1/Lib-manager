from dataclasses import asdict, dataclass, field
from datetime import date
from uuid import UUID, uuid4


@dataclass
class Book:
    title: str
    author: str
    year: int
    status: str = "В наличии"
    id: UUID = field(default_factory=lambda: uuid4())

    def to_dict(self) -> dict:
        """Метод сериализующий экземпляр класса в словарь.

        Returns:
            dict: резульирующий словарь

        """
        return asdict(self) | dict(id=str(self.id))

    def validate(self) -> dict:
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


        if self.status not in ["В наличии", "Нет в наличии"]:
            errors["status"] = "Недопустимый статус."

        return errors

    def __post_init__(self) -> None:
        errors = self.validate()
        if errors:
            raise ValueError(f"Ошибка валидации: {errors}")

