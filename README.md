# 📚 Library Management System

A command-line Library Management System built in Python. It lets a librarian add books, register members, issue and return books, track what is on loan, and keep all data saved between sessions.

Built to demonstrate core Python concepts: object-oriented programming, modular design, file handling, input validation and exception handling.

---

## ✨ Features

- **Add books** with title, author and number of copies (adding the same book again increases its copies instead of creating a duplicate)
- **View available books** that still have copies on the shelf
- **Search** by title, author or book ID
- **Register members** with auto-generated IDs (`M001`, `M002`, ...)
- **Issue books** with a 14-day loan period and a limit of 3 books per member
- **Return books** with automatic fine calculation (₹2 per day after the due date)
- **Track issued books** with due dates and an `OVERDUE` flag
- **Persistent storage**: data is saved to a JSON file after every change

---

## 🚀 Getting Started

### Requirements
- Python 3.10 or newer (no external libraries needed)

### Run it

```bash
git clone https://github.com/YOUR-USERNAME/library-management-system.git
cd library-management-system
python main.py
```

A `library_data.json` file is created automatically the first time you add data.

---

## 🖥️ Sample Session

```
========== LIBRARY MANAGEMENT SYSTEM ==========
 1. Add a book
 2. View available books
 3. Search for books
 4. Register a member
 5. Issue a book
 6. Return a book
 7. View issued books
 8. View all members
 0. Exit
===============================================
Choose an option: 1
Title: Python Crash Course
Author: Eric Matthes
Copies [1]: 2
Saved: B001 - 'Python Crash Course' (2 copies total).

Choose an option: 4
Member name: Sally
Registered: M001 - Sally

Choose an option: 5
Book ID: B001
Member ID: M001
Issued! Due back on 2026-11-12 (14-day loan).

Choose an option: 5
Book ID: B999
Member ID: M001
Error: No book found with ID 'B999'.
```

> 📸 *Add screenshots of your own runs here, for example:*
> `![Main menu](screenshots/menu.png)`

---

## 🗂️ Project Structure

```
library-management-system/
├── main.py          # Entry point
├── cli.py           # Menu, prompts and printing
├── library.py       # Core logic: add, search, issue, return, fines
├── models.py        # Book, Member and IssueRecord classes
├── storage.py       # Loads and saves the JSON data file
├── validators.py    # Input validation helpers
├── exceptions.py    # Custom exceptions
└── README.md
```

| Module | Responsibility |
|---|---|
| `main.py` | Starts the app and handles startup errors |
| `cli.py` | All user interaction (input and output only) |
| `library.py` | The `Library` class that holds the business rules |
| `models.py` | Dataclasses for books, members and issue records |
| `storage.py` | Safe file reading and writing (temp file, then replace) |
| `validators.py` | Cleans and checks user input |
| `exceptions.py` | Custom error types for clear messages |

---

## 📏 Library Rules

| Rule | Value |
|---|---|
| Loan period | 14 days |
| Maximum books per member | 3 |
| Late fine | ₹2 per day |
| Same book twice to one member | Not allowed |

---

## 🛡️ Validation and Error Handling

The program shows a clear message instead of crashing when:

- a field is empty or too long
- copies are not a positive whole number
- a book or member ID does not exist
- no copies of a book are available
- a member has reached the issue limit
- a book is returned by someone who never borrowed it
- the data file is corrupted or cannot be read or written

---

## 🧠 Python Concepts Demonstrated

- Classes, objects and dataclasses
- Functions and modular programming
- Dictionaries, lists and type hints
- File handling with JSON
- Custom exceptions and `try`/`except`
- Input validation
- The `datetime` module for due dates and fines

---

## 🔮 Possible Improvements

- Member borrowing history
- Renew-book option
- Librarian login
- Export reports to CSV
- A graphical or web interface

---

## 👩‍💻 Author

**Sally Miriro Muchaziwepi**
BSc Computer Science student

*Created as part of an internship project, by invexom*
