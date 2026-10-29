"""Command-line interface: menus, prompts and printing."""

from exceptions import LibraryError
from library import FINE_PER_DAY, LOAN_DAYS, Library

MENU = """
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
==============================================="""


def print_books(books) -> None:
    if not books:
        print("No books to show.")
        return
    print(f"{'ID':<6} {'Title':<30} {'Author':<20} Avail/Total")
    print("-" * 70)
    for book in books:
        print(book)


# ---------- menu actions ----------
def add_book(lib: Library) -> None:
    title = input("Title: ")
    author = input("Author: ")
    copies = input("Copies [1]: ") or "1"
    book = lib.add_book(title, author, copies)
    print(f"Saved: {book.book_id} - '{book.title}' ({book.total_copies} copies total).")


def view_available(lib: Library) -> None:
    print_books(lib.available_books())


def search(lib: Library) -> None:
    results = lib.search_books(input("Search by title, author or ID: "))
    print_books(results)


def add_member(lib: Library) -> None:
    member = lib.add_member(input("Member name: "))
    print(f"Registered: {member.member_id} - {member.name}")


def issue(lib: Library) -> None:
    book_id = input("Book ID: ")
    member_id = input("Member ID: ")
    record = lib.issue_book(book_id, member_id)
    print(f"Issued! Due back on {record.due_date} ({LOAN_DAYS}-day loan).")


def return_book(lib: Library) -> None:
    book_id = input("Book ID: ")
    member_id = input("Member ID: ")
    record = lib.return_book(book_id, member_id)
    if record.fine:
        print(f"Returned late. Fine: Rs.{record.fine} (Rs.{FINE_PER_DAY}/day).")
    else:
        print("Returned on time. Thank you!")


def view_issued(lib: Library) -> None:
    records = lib.active_records()
    if not records:
        print("No books are currently issued.")
        return
    overdue = {id(r) for r in lib.overdue_records()}
    print(f"{'Book':<6} {'Title':<28} {'Member':<18} {'Due':<12} Status")
    print("-" * 75)
    for r in records:
        title = lib.books[r.book_id].title[:26]
        member = lib.members[r.member_id].name[:16]
        status = "OVERDUE" if id(r) in overdue else "On loan"
        print(f"{r.book_id:<6} {title:<28} {member:<18} {r.due_date:<12} {status}")


def view_members(lib: Library) -> None:
    if not lib.members:
        print("No members registered.")
        return
    for member in lib.members.values():
        count = len(lib.active_records(member.member_id))
        print(f"{member}  ({count} book(s) issued)")


ACTIONS = {
    "1": add_book, "2": view_available, "3": search, "4": add_member,
    "5": issue, "6": return_book, "7": view_issued, "8": view_members,
}


def run(lib: Library) -> None:
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid choice. Please enter a number from the menu.")
            continue
        try:
            action(lib)
        except LibraryError as e:        # all expected problems end up here
            print(f"Error: {e}")
        except (KeyboardInterrupt, EOFError):
            print("\nAction cancelled.")
