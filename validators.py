"""Input validation helpers. Each returns a cleaned value or raises InvalidInputError."""

from exceptions import InvalidInputError


def require_text(value: str, field: str, max_len: int = 100) -> str:
    value = (value or "").strip()
    if not value:
        raise InvalidInputError(f"{field} cannot be empty.")
    if len(value) > max_len:
        raise InvalidInputError(f"{field} must be at most {max_len} characters.")
    return value


def require_positive_int(value: str, field: str) -> int:
    try:
        number = int(str(value).strip())
    except ValueError:
        raise InvalidInputError(f"{field} must be a whole number.") from None
    if number <= 0:
        raise InvalidInputError(f"{field} must be greater than zero.")
    return number


def require_id(value: str, field: str) -> str:
    """IDs are stored upper-case, e.g. 'b001' -> 'B001'."""
    return require_text(value, field, max_len=20).upper()
