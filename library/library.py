import json
from typing import TypedDict

from library.book import Book


class BookTemplate(TypedDict):
    """Типизированный словарь, представляющий информацию о книге.

    Args:
        id (str): Уникальный идентификатор книги.
        title (str): Название книги.
        author (str): Автор книги.
        year (int): Год издания книги.
        status (str): Статус книги (например, "available", "checked_out").

    """

    id: str
    title: str
    author: str
    year: int
    status: str


def book_list_formatter(books: list[BookTemplate]) -> str:
    """Форматирует список книг в читаемый формат.

    Эта функция принимает список объектов типа BookTemplate и форматирует их в строку,
    где каждая книга представлена в отдельном блоке с информацией о её ID, названии, авторе,
    годе издания и статусе. Каждый блок книги разделён двумя новыми строками.

    Args:
        books (list[BookTemplate]): Список книг, где каждая книга представлена в формате BookTemplate.

    Returns:
        str: Отформатированная строка, содержащая информацию о всех книгах из списка.

    """
    result = []
    for book in books:
        book_info = (
            f"ID: {book['id']}\n"
            f"\tНазвание: {book['title']}\n"
            f"\tАвтор: {book['author']}\n"
            f"\tГод издания: {book['year']}\n"
            f"\tСтатус: {book['status']}"
        )
        result.append(book_info)
    return "\n\n".join(result)



def load_file(filename: str) -> list[BookTemplate]:
    """Загружает данные из файла в формате JSON.

    Args:
        filename (str): Имя файла, из которого загружаются данные.
    
    Returns:
        list[BookTemplate]: Список словарей, содержащих загруженные данные.

    """
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    return data

def save_file(filename: str, data: list[dict]) -> None:
    """Сохранение файла.
    Функция сохраняет (data) в файл (filename). Так как эта функция использоваться
    после операции чтения файла, ошибки связанные с открытием файла не обрабатываются.

    Args:
        filename (str): Название файла.
        data Список словарей, содержащих информацию о книгах.

    Returns:
        _type_: None

    """
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
    except json.JSONDecodeError as e:
            print(f"Ошибка декодиорования Json: {e}")



def add_book(data: list[dict], title: str, author: str, year: int) -> str:
    """Добавляет новую книгу в список данных.

    Функция создаёт новую книгу с заданным заголовком, автором и годом выпуска, 
    преобразует её в словарь и добавляет в список `data`. Предполагается, что объект 
    класса `Book` автоматически генерирует уникальный идентификатор (ID) для каждой книги.

    Args:
        data (list[dict]): Список словарей, содержащих информацию о книгах.
        title (str): Заголовок добавляемой книги.
        author (str): Автор добавляемой книги.
        year (int): Год выпуска добавляемой книги.

    Returns:
        str: ID добавленной книги.

    """
    new_book = Book(title, author, year).to_dict()
    data.append(new_book)
    return new_book["id"]


def remove_book(data: list[dict], target_id: str) -> BookTemplate:
    """Удаляет книгу из списка данных по указанному ID.

    Функция ищет и удаляет книгу с заданным идентификатором (target_id) из списка словарей (data).
    Если книга с указанным идентификатором отсутствует, вызывается исключение ValueError.

    Args:
        data (list[dict]): Список словарей, содержащих информацию о книгах.
        target_id (str): Строка, представляющая идентификатор книги, которую необходимо удалить.

    Raises:
        ValueError: Если книга с указанным target_id не найдена в списке.

    Returns:
        BookTemplate: Удаленная книга.

    """
    for book in data:
        if book["id"] == target_id:
            res = book
            data.remove(book)
            return res
    raise ValueError(f"Книга с ID: {target_id} не найдена в списке.")


def search_book(data: list[dict], query: str, option: str) -> list[BookTemplate]:
    """Ищет книги по запросу используя критерии поиска.

    Функция ищет книги по указанному запросу (query) и критериям поиска
    (option: title, author, year) в списке словаерй (data). Если критерий посика не корректен
    вызвается исключение ValueError.
    
    Args:
        data (list[dict]): Список словарей, содержащих информацию о книгах.
        query (str): Поисковый запрос.
        option (str): Критерий поиска: title, author или year.

    Returns:
        list[BookTemplate]: Список найденых книг.

    """
    result = [book for book in data if str(book[option]) == query]
    return result



def change_status(data: list[dict], target_id: str, new_status: str) -> list[BookTemplate]:
    """Менят статус книги по ее ID.

    Функция ищет и удаляет книгу с заданным идентификатором (target_id) из списка словарей (data) и 
    изменят статус (new_status) на один из доступных ("Выдана", "В наличии"). Если новый стаус не соотвествует
    шаблону или книга с указанным идентификатором отсутствует, вызывается исключение ValueError.

    Args:
        data (list[dict]): Список словарей, содержащих информацию о книгах.
        target_id (str): Строка, представляющая идентификатор книги, которую необходимо изменить.
        new_status (Union[StatusOption, str]): Новый статус.

    Raises:
        ValueError: Если книга с указанным target_id не найдена в списке или новый стаус не соотвествует шаблону.

    Returns:
        list[BookTemplate]: Форматированный список книг.

    """
    tamplate = ["Выдана", "В наличии"]
    if new_status not in tamplate:
        raise ValueError(f"Некорректный статус: {new_status}. Допустимые статусы: {tamplate}")

    for book in data:
        if book["id"] == target_id:
            book["status"] = new_status
            return data
    raise ValueError(f"Книги с ID: {target_id} нет в списке!")
