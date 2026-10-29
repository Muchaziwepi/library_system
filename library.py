"""Core business logic. No input() or print() here - that belongs to the CLI."""

from datetime import date, datetime

from exceptions import (BookNotFoundError, BookUnavailableError,
                        DuplicateRecordError, InvalidInputError,
                        IssueLimitError, MemberNotFoundError, NotIssuedError)
from models import DATE_FMT, Book, IssueRecord, Member
from storage import load_data, save_data
from validators import require_id, require_positive_int, require_text

LOAN_DAYS = 14
MAX_BOOKS_PER_MEMBER = 3
FINE_PER_DAY = 2   # in rupees


class Library:
    def __init__(self, data_file: str = "library_data.json"):
        self.data_file = data_file
        self.books: dict[str, Book] = {}
        self.members: dict[str, Member] = {}
        self.records: list[IssueRecord] = []
        self._load()

    # ---------- persistence ----------
    def _load(self) -> None:
        data = load_data(self.data_file)
        self.books = {b["book_id"]: Book.from_dict(b) for b in data["books"]}
        self.members = {m["member_id"]: Member.from_dict(m) for m in data["members"]}
        self.records = [IssueRecord.from_dict(r) for r in data["records"]]

    def save(self) -> None:
        save_data(self.data_file, {
            "books": [b.to_dict() for b in self.books.values()],
            "members": [m.to_dict() for m in self.members.values()],
            "records": [r.to_dict() for r in self.records],
        })

    # ---------- lookups ----------
    def get_book(self, book_id: str) -> Book:
        book_id = require_id(book_id, "Book ID")
        try:
            return self.books[book_id]
        except KeyError:
            raise BookNotFoundError(f"No book found with ID '{book_id}'.") from None

    def get_member(self, member_id: str) -> Member:
        member_id = require_id(member_id, "Member ID")
        try:
            return self.members[member_id]
        except KeyError:
            raise MemberNotFoundError(f"No member found with ID '{member_id}'.") from None

    def _next_id(self, prefix: str, existing) -> str:
        return f"{prefix}{len(existing) + 1:03d}"

    # ---------- books ----------
    def add_book(self, title: str, author: str, copies: str = "1") -> Book:
        title = require_text(title, "Title")
        author = require_text(author, "Author")
        copies = require_positive_int(copies, "Number of copies")

        # Same title + author already there? Add copies instead of a duplicate.
        for book in self.books.values():
            if book.title.lower() == title.lower() and book.author.lower() == author.lower():
                book.total_copies += copies
                book.available_copies += copies
                self.save()
                return book

        book = Book(self._next_id("B", self.books), title, author, copies, copies)
        self.books[book.book_id] = book
        self.save()
        return book

    def available_books(self) -> list[Book]:
        return [b for b in self.books.values() if b.is_available()]

    def search_books(self, keyword: str) -> list[Book]:
        keyword = require_text(keyword, "Search keyword")
        return [b for b in self.books.values() if b.matches(keyword)]

    # ---------- members ----------
    def add_member(self, name: str) -> Member:
        name = require_text(name, "Name")
        member = Member(self._next_id("M", self.members), name)
        self.members[member.member_id] = member
        self.save()
        return member

    # ---------- issue / return ----------
    def active_records(self, member_id: str | None = None) -> list[IssueRecord]:
        return [r for r in self.records
                if r.is_active and (member_id is None or r.member_id == member_id)]

    def issue_book(self, book_id: str, member_id: str) -> IssueRecord:
        book = self.get_book(book_id)
        member = self.get_member(member_id)

        if not book.is_available():
            raise BookUnavailableError(f"'{book.title}' has no copies available right now.")
        if len(self.active_records(member.member_id)) >= MAX_BOOKS_PER_MEMBER:
            raise IssueLimitError(
                f"{member.name} already has {MAX_BOOKS_PER_MEMBER} books issued.")
        if any(r.book_id == book.book_id for r in self.active_records(member.member_id)):
            raise DuplicateRecordError(f"{member.name} already has '{book.title}'.")

        book.available_copies -= 1
        record = IssueRecord.new(book.book_id, member.member_id, LOAN_DAYS)
        self.records.append(record)
        self.save()
        return record

    def return_book(self, book_id: str, member_id: str) -> IssueRecord:
        book = self.get_book(book_id)
        member = self.get_member(member_id)

        for record in self.active_records(member.member_id):
            if record.book_id == book.book_id:
                today = date.today()
                due = datetime.strptime(record.due_date, DATE_FMT).date()
                record.return_date = today.strftime(DATE_FMT)
                record.fine = max(0, (today - due).days) * FINE_PER_DAY
                book.available_copies += 1
                self.save()
                return record

        raise NotIssuedError(f"{member.name} has not borrowed '{book.title}'.")

    def overdue_records(self) -> list[IssueRecord]:
        today = date.today().strftime(DATE_FMT)
        return [r for r in self.active_records() if r.due_date < today]
