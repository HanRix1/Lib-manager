import argparse


def create_parser():
    parser = argparse.ArgumentParser(description="Управление библиотекой книг")
    subparser = parser.add_subparsers(dest="command")

    # Команда добавления книги
    add_parser = subparser.add_parser("add", help="Добавить книгу")
    add_parser.add_argument("title", help="Название ккниги")
    add_parser.add_argument("author", help="Автор книги")
    add_parser.add_argument("year", type=int, help="Год издания")

    # Команда удаления книги
    remove_parser = subparser.add_parser("remove", help="Удалить книгу")
    remove_parser.add_argument("id", help="ID книги")

    # Команда поиска книги
    search_parser = subparser.add_parser("search", help="Поиск книги")
    search_parser.add_argument("query", help="Поисковый запрос")
    search_parser.add_argument(
        "--by",
        choices=["title", "author", "year"],
        default="title",
        help="Поле для поиска",
    )

    # Команда отображения всех книг
    subparser.add_parser("list", help="Отобразить все книги")

    # Команда изменения статуса книги
    change_status_parser = subparser.add_parser(
        "change_status", help="Изменить статус книги"
    )
    change_status_parser.add_argument("id", help="ID книги")
    change_status_parser.add_argument(
        "status", choices=["В наличии", "Выдана"], help="Новый статус"
    )

    return parser
