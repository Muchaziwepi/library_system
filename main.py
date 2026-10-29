"""Entry point: python main.py"""

import sys

import cli
from library import Library
from exceptions import LibraryError


def main() -> None:
    try:
        library = Library("library_data.json")
    except LibraryError as e:
        print(f"Could not start: {e}")
        sys.exit(1)
    cli.run(library)


if __name__ == "__main__":
    main()
