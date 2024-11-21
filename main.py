from library.cli import create_parser
from library.library import add_book, all_book_list, change_status, remove_book, search_book

def main():
    parser = create_parser()
    args = parser.parse_args()

    try:
        if args.command == "add":
            result = add_book(args.title, args.author, args.year)
            print(result)

        elif args.command == "remove":
            result = remove_book(args.id)
            print(result)

        elif args.command == "search":
            result = search_book(args.query, args.by)
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

 