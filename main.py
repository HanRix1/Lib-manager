from library.cli import create_parser
from library.library import add_book, all_book_list, change_status, remove_book, search_book
import json

def main():
    parser = create_parser()
    args = parser.parse_args()
    filename = "books.json"

    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
            data = []
    
    try:
        if args.command == "add":
            result = add_book(data, args.title, args.author, args.year)
            print(f"Книга с ID:{result} добавлена!")

        elif args.command == "remove":
            res = remove_book(data, args.id)
            print(res)

        elif args.command == "search":
            result = search_book(data, args.query, args.by)
            print(result)

        elif args.command == "list":
            result = all_book_list()
            print(result)

        elif args.command == "change_status":
            result = change_status(args.id, args.status)
            print(result)

        else:
            parser.print_help()

    except Exception as e:
        print(f"Ошибка: {e}")



if __name__ == "__main__":
    main()

