from enum import Enum

from library.cli import create_parser
from library.library import (
    add_book,
    book_list_formatter,
    change_status,
    load_file,
    remove_book,
    save_file,
    search_book,
)


class Command(Enum):
    ADD = "add"
    REMOVE = "remove"
    SEARCH = "search"
    LIST = "list"
    CHANGE_STATUS = "change_status"


def main():

    parser = create_parser()
    args = parser.parse_args()
    filename = "books.json"
    data = load_file(filename)
    command = Command(args.command)

    match command:
        case Command.ADD:
            result = add_book(data, args.title, args.author, args.year)
            save_file(filename, data)
            print(f"Книга с ID:{result} добавлена!")
        case Command.REMOVE:
            result = remove_book(data, args.id)
            save_file(filename, data)
            print(f"Книга с ID:{result} удалена!")
        case Command.SEARCH:
            result = search_book(data, args.query, args.by)
            print(f"По запросу {args.query} = {args.by} найдено {len(result)} книги(а):\n" +
                  book_list_formatter(result))
        case Command.LIST:
            print(book_list_formatter(data))
        case Command.CHANGE_STATUS:
            result = change_status(data, args.id, args.status)
            save_file(filename, data)
            print("Статус успешно изменен!")
        case _:
            parser.print_help()



if __name__ == "__main__":
    main()
