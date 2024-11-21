from enum import Enum
from typing import Union
from library.book import Book
import json

def open_json_file(filename, mode):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                with open(filename, "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = []

            result = func(data, *args, **kwargs)

            if mode != "r":  
                try:
                    with open(filename, "w") as file:
                        json.dump(data, file, indent=4)
                except ValueError:
                    print(f"Режим обработки файла {mode} введен не корректно")
                except json.JSONDecodeError as e:
                    print(f"Ошибка декодиорования Json: {e}")
            return result
        return wrapper
    return decorator

def open_json_file_for_writing(filename):
    return open_json_file(filename, "w")  # "w" для перезаписи файла

def open_json_file_for_reading(filename):
    return open_json_file(filename, "r")  # "r" для чтения из файла

FILENAME = "books.json"


@open_json_file_for_writing(FILENAME)
def add_book(data, title: str, author: str, year: int) -> str:
    new_book = Book(title, author, year).to_dict()
    data.append(new_book)
    return(f"Книга {title} успешно добавлена!")


@open_json_file_for_writing(FILENAME)
def remove_book(data, target_id: str) -> str:
    filtered_data = [book for book in data if book["id"] != target_id]
    if len(filtered_data) == len(data):
        raise ValueError(f"Книги с ID: {target_id} нету в списке")
    data[:] = filtered_data
    return f"Книга с ID {target_id} удалена"

class SearchOption(Enum):
    value1: str = "title"
    value2: str = "author"
    value3: str = "year"

@open_json_file_for_reading(FILENAME)
def search_book(data, option: Union[SearchOption, str], query: str) -> str:
    if isinstance(new_status, str):
        try:
            new_status = StatusOption(new_status)
        except ValueError:
            raise ValueError(f"Некорректный статус: {new_status}. Допустимые статусы: {[status.value for status in StatusOption]}")
     
    res = [book for book in data if book[option] == query]
    buf = len(res)
    if buf:
        ans = [f"По запросу {option}={query} найдено {buf} книг:\n"]
        for book in res:
            book_info = (
                f"ID: {book['id']}\n"
                f"\tНазвание: {book['title']}\n"
                f"\tАвтор: {book['author']}\n"
                f"\tГод издания: {book['year']}\n"
                f"\tСтатус: {book['status']}"
            )
            ans.append(book_info)
        return "\n\n".join(ans)
    else:
        raise ValueError(f"По запросу {option}={query} ничего не найдено!")
    

@open_json_file_for_reading(FILENAME)
def all_book_list(data) -> str:
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


class StatusOption(Enum):
    satus1: str = "В наличии"
    status2: str = "Выдана"


@open_json_file_for_writing(FILENAME)
def change_status(data, target_id: str, new_status: Union[StatusOption, str]) -> str:
    if isinstance(new_status, str):
        try:
            new_status = StatusOption(new_status)
        except ValueError:
            raise ValueError(f"Некорректный статус: {new_status}. Допустимые статусы: {[status.value for status in StatusOption]}")
        
    for book in data:
        if book["id"] == target_id:
            book["status"] = new_status.value
            return f"Статус книги с ID: {target_id} успешно изменен!"
    raise ValueError(f"Книги с ID: {target_id} нет в списке!")