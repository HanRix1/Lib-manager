from enum import Enum
from typing import Union
from library.book import Book
import json


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
    return None


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


def remove_book(data: list[dict], target_id: str) -> dict:
    """Удаляет книгу из списка данных по указанному ID.

    Функция ищет и удаляет книгу с заданным идентификатором (target_id) из списка словарей (data).
    Если книга с указанным идентификатором отсутствует, вызывается исключение ValueError.

    Args:
        data (list[dict]): Список словарей, содержащих информацию о книгах.
        target_id (str): Строка, представляющая идентификатор книги, которую необходимо удалить.

    Raises:
        ValueError: Если книга с указанным target_id не найдена в списке.

    Returns:
        dict: Удаленная книга.
    """
    for book in data:
        if book["id"] == target_id:
            res = book
            data.remove(book)
            return res
    raise ValueError(f"Книга с ID: {target_id} не найдена в списке.")


def search_book(data: list[dict], query: str, option: str) -> list[dict]:
    """Ищет книгу по запросу используя критерии поиска.

    Функция ищет книгу по указанному запросу (query) и критериям поиска
    (option: title, author, year) в списке словаерй (data). Если критерий посика не корректен
    вызвается исключение ValueError.
    
    Args:
        data (list[dict]): Список словарей, содержащих информацию о книгах.
        query (str): Поисковый запрос.
        option (str): Критерий поиска: title, author или year.

    Raises:
        ValueError: Если критерий посика не корректен.

    Returns:
        list[dict]: Список найденых книг.
    """
    searchoption = ["title", "author", "year"]
    if option not in searchoption:
        raise ValueError(f"Некорректный статус: {option}. Допустимые статусы: {searchoption}")
     
    res = [book for book in data if str(book[option]) == query]
    return res
    

def all_book_list(data: list[dict]) -> str:
    """Функция форматирования списка.
    
    Функция принимает список книг, представленный словарями 
    с информацией о каждой книге, и форматирует их в строку.

    Args:
        data (list[dict]): Список словарей с информацией о книгах.

    Returns:
        str: Отформатированная строка, содержащая информацию о книгах.
    """
    result = [f"Всего найдено {len(data)} книг:"]
    for book in data:
        book_info = (
            f"ID: {book['id']}\n"
            f"\tНазвание: {book['title']}\n"
            f"\tАвтор: {book['author']}\n"
            f"\tГод издания: {book['year']}\n"
            f"\tСтатус: {book['status']}"
        )
        result.append(book_info)    
    return "\n\n".join(result)



def change_status(data: list[dict], target_id: str, new_status: str) -> list[dict]:
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
        list[dict]: Форматированный список книг.
    """
    if new_status not in ["Выдана", "В наличии"]:
        raise ValueError(f"Некорректный статус: {new_status}. Допустимые статусы: {[status.value for status in StatusOption]}")
        
    for book in data:
        if book["id"] == target_id:
            book["status"] = new_status.value
            return f"Статус книги с ID: {target_id} успешно изменен!"
    raise ValueError(f"Книги с ID: {target_id} нет в списке!")