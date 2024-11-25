from unittest import mock

import pytest

from library.book import Book
from library.cli import create_parser
from library.library import (
    add_book,
    change_status,
    load_file,
    remove_book,
    save_file,
    search_book,
)


@pytest.fixture(scope="class")
def temp_filename(tmp_path_factory):
    file_path = tmp_path_factory.mktemp("data") / "example.json"
    return str(file_path)

@pytest.fixture(scope="class")
def parser():
    return create_parser()

class TestCLI:
    @pytest.mark.parametrize(
        "title, author, year, raises_exception",
        [
            ("Война и мир", "Лев Толстой", 2025, False),
            ("В" * 101, "Лев Толстой", 1869, True),
            ("Война и мир", "d"*51, 1869, True),
            (None, "Лев Толстой", 1869, True),
            ("Война и мир", None, 1869, True),
            ("Война и мир", "Лев Толстой", 2026, True),
            ("Война и мир", "Лев Толстой", -2022, True),
        ],
        ids=[1, 2, 3, 4, 5, 6, 7],
    )
    def test_add_book(self, temp_filename, parser, title, author, year, raises_exception):
        args = parser.parse_args(["add", title, author, f"{year}"])
        data = load_file(temp_filename)

        if raises_exception:
            with pytest.raises(ValueError):
                add_book(data, args.title, args.author, args.year)
        else:
            res = add_book(data, args.title, args.author, args.year)
            save_file(temp_filename, data)
            updated_data = load_file(temp_filename)
            assert len(updated_data) == 1
            assert updated_data[0]["id"] == res
            assert updated_data[0]["title"] == title
            assert updated_data[0]["author"] == author
            assert updated_data[0]["year"] == year
            assert updated_data[0]["status"] == "В наличии"


    @pytest.mark.parametrize(
        "book_id, raises_exception",
        [
            ("97b37b56-d5ec-4c21-ab61-1f5f5794d1a4", False),
            ("c19e3bff-b29d-4357-bf08-a6cb9fe51231", True),
        ],
    )
    def test_book_remove(self, temp_filename, parser, book_id, raises_exception):
        with mock.patch("library.book.uuid4", return_value="97b37b56-d5ec-4c21-ab61-1f5f5794d1a4"):
            initial_data = []
            initial_data.append(Book("Война и мир", "Лев Толстой", 1869).to_dict())

        books_qnt = len(initial_data)
        save_file(temp_filename, initial_data)

        updated_data = load_file(temp_filename)
        args = parser.parse_args(["remove", f"{book_id}"])
        if raises_exception:
            with pytest.raises(ValueError):
                remove_book(updated_data, args.id)
        else:
            result = remove_book(updated_data, args.id)
            save_file(temp_filename, updated_data)
            assert len(updated_data) == books_qnt - 1
            assert result == initial_data[0]


    @pytest.mark.parametrize(
        "query, option",
        [
            ("Война и мир", "--by=title"),
            ("Лев Толстой", "--by=author"),
            (1869, "--by=year"),
            ("Война и мир", ""),
        ],
        ids=[1, 2, 3, 4],
    )
    def test_search_book(self, temp_filename, parser, query, option):
        initial_data = []
        initial_data.append(Book("Война и мир", "Лев Толстой", 1869).to_dict())
        initial_data.append(Book("Анна Каренина", "Лев Толстой", 1878).to_dict())
        save_file(temp_filename, initial_data)

        updated_data = load_file(temp_filename)
        arguments = ["search", f"{query}", f"{option}"] if option else ["search", f"{query}"]
        args = parser.parse_args(arguments)
        result = search_book(updated_data, args.query, args.by)
        for book in result:
            assert book[option[5:] or "title"] == query


    @pytest.mark.parametrize(
        "book_id, status, raises_exception",
        [
            ("97b37b56-d5ec-4c21-ab61-1f5f5794d1a4", "Выдана", False),
            ("97b37b56-d5ec-4c21-ab61-1f5f5794d1a4", "В наличии", False),
            ("c19e3bff-b29d-4357-bf08-a6cb9fe51231", "Выдана", True),
        ],
    )
    def test_book_change_status(self, temp_filename, parser, book_id, status, raises_exception):
        with mock.patch("library.book.uuid4", return_value="97b37b56-d5ec-4c21-ab61-1f5f5794d1a4"):
            initial_data = []
            initial_data.append(Book("Война и мир", "Лев Толстой", 1869).to_dict())
        save_file(temp_filename, initial_data)

        updated_data = load_file(temp_filename)
        args = parser.parse_args(["change_status", book_id, status])
        if raises_exception:
            with pytest.raises(ValueError):
                change_status(updated_data, args.id, args.status)
        else:
            result = change_status(updated_data, args.id, args.status)
            save_file(temp_filename, updated_data)
            for book in result:
                if book["id"] == book_id:
                    assert book["status"] == status
                    return
