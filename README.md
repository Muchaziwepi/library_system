# Library Management System (CLI)

Run: `python main.py`  (Python 3.10+)

| File | Responsibility |
|---|---|
| `main.py` | Entry point |
| `cli.py` | Menus, prompts, printing |
| `library.py` | Business logic (add, search, issue, return, fines) |
| `models.py` | `Book`, `Member`, `IssueRecord` classes |
| `storage.py` | JSON file load/save |
| `validators.py` | Input validation |
| `exceptions.py` | Custom exceptions |

Rules: 14-day loan, max 3 books per member, Rs.2/day fine on late returns.
Data is saved to `library_data.json` after every change.
