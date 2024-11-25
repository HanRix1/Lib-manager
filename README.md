# Консольное приложение для управления библиотекой книг

Консольное приложение для управления библиотекой книг. Позволяет добавлять, удалять, искать и отображать книги. Каждая книга содержит следующие поля:

- **ID**: Уникальный идентификатор, генерируется автоматически.
- **title**: Название книги.
- **author**: Автор книги.
- **year**: Год издания.
- **status**: Статус книги (“в наличии”, “выдана”).

## Примечания:

- Все данные о книгах хранятся в JSON файле: `books.json`.
- Функции и переменные анотированы.
- Наличие документации, в виде docstring, к функциям и основным блокам кода.
- Покрытие тестами 95%.

## Команды

### Добавление книги

Команда `add` с параметрами `title`, `author` и `year`, добавляет книгу в библиотеку с уникальным `ID` и статусом “в наличии”.

Пример команды:

```bash
python main.py add "Война и мир" "Лев Толстой" 1869
```

### Удаление книги

Команда `remove` с параметром `ID` позволяет удалить книгу из библиотеки.

Пример команды:

```bash
python main.py remove {ID}
```

### Поиск книги

Команда `search` с параметром `query` позволяет искать книги по фильтру `--by`: `title`, `author` или `year`. По умолчанию фильтр поиска - `title`.

Пример команды:

```bash
python main.py search "Война и Мир" --by title
python main.py search "Анна Каренина"  # Вызов по умолчанию
```

### Отображение всех книг

Команда `list` служит для отображения всех книг.

Пример команды:

```bash
python main.py list
```

### Изменение статуса книги

Команда `change_status` с параметрами `ID` позволяет изменить статус у выбранной книги на один из двух возможных: "В наличии", "Выдана".

Пример команды:

```bash
python main.py change_status {ID} "Выдана"
```
