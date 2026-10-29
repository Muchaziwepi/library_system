"""Custom exceptions so the rest of the app can handle problems precisely."""


class LibraryError(Exception):
    """Base class for all library-related errors."""


class InvalidInputError(LibraryError):
    """Raised when user input fails validation."""


class BookNotFoundError(LibraryError):
    """Raised when a book ID does not exist."""


class MemberNotFoundError(LibraryError):
    """Raised when a member ID does not exist."""


class DuplicateRecordError(LibraryError):
    """Raised when adding a record that already exists."""


class BookUnavailableError(LibraryError):
    """Raised when no copies of a book are available to issue."""


class IssueLimitError(LibraryError):
    """Raised when a member already holds the maximum number of books."""


class NotIssuedError(LibraryError):
    """Raised when returning a book the member has not borrowed."""
