"""Data classes: Book, Member and IssueRecord."""

from dataclasses import dataclass, asdict
from datetime import date, timedelta

DATE_FMT = "%Y-%m-%d"


@dataclass
class Book:
    book_id: str
    title: str
    author: str
    total_copies: int = 1
    available_copies: int = 1

    def is_available(self) -> bool:
        return self.available_copies > 0

    def matches(self, keyword: str) -> bool:
        keyword = keyword.lower()
        return (keyword in self.title.lower()
                or keyword in self.author.lower()
                or keyword == self.book_id.lower())

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(**data)

    def __str__(self) -> str:
        return (f"{self.book_id:<6} {self.title[:30]:<30} {self.author[:20]:<20} "
                f"{self.available_copies}/{self.total_copies}")


@dataclass
class Member:
    member_id: str
    name: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Member":
        return cls(**data)

    def __str__(self) -> str:
        return f"{self.member_id:<6} {self.name}"


@dataclass
class IssueRecord:
    book_id: str
    member_id: str
    issue_date: str
    due_date: str
    return_date: str = ""   # empty string = still issued
    fine: int = 0

    @property
    def is_active(self) -> bool:
        return not self.return_date

    @staticmethod
    def new(book_id: str, member_id: str, loan_days: int) -> "IssueRecord":
        today = date.today()
        due = today + timedelta(days=loan_days)
        return IssueRecord(book_id, member_id,
                           today.strftime(DATE_FMT), due.strftime(DATE_FMT))

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "IssueRecord":
        return cls(**data)
