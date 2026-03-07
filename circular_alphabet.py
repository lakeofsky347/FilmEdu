"""
circular_alphabet.py – Circular alphabet utilities for letters.

Provides a CircularAlphabet class that treats the 26 letters as a circular
list (after 'z' comes 'a', before 'a' comes 'z'), along with convenience
functions for common operations.
"""

from typing import List


class CircularAlphabet:
    """
    Represents the alphabet as a circular sequence of letters.

    Both upper-case and lower-case variants are supported.  The circularity
    means that shifting past 'z' wraps back to 'a' (and equivalently for
    upper-case letters).

    Example usage
    -------------
    >>> ca = CircularAlphabet()
    >>> ca.next_letter('a')
    'b'
    >>> ca.next_letter('z')
    'a'
    >>> ca.shift('a', 3)
    'd'
    >>> ca.shift('y', 3)
    'b'
    """

    def __init__(self) -> None:
        # Two circular lists – index i maps to the letter at position i.
        self._lower: List[str] = [chr(ord('a') + i) for i in range(26)]
        self._upper: List[str] = [chr(ord('A') + i) for i in range(26)]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _index(self, letter: str) -> int:
        """Return the 0-based position of *letter* in the alphabet."""
        if not (isinstance(letter, str) and len(letter) == 1 and letter.isalpha()):
            raise ValueError(f"Expected a single alphabetic character, got {letter!r}")
        if letter.islower():
            return ord(letter) - ord('a')
        return ord(letter) - ord('A')

    def _alphabet(self, letter: str) -> List[str]:
        """Return the correct (lower/upper) alphabet list for *letter*."""
        return self._lower if letter.islower() else self._upper

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def next_letter(self, letter: str) -> str:
        """Return the letter that follows *letter* in the circular alphabet.

        >>> CircularAlphabet().next_letter('z')
        'a'
        >>> CircularAlphabet().next_letter('Z')
        'A'
        """
        alpha = self._alphabet(letter)
        i = self._index(letter)
        return alpha[(i + 1) % 26]

    def prev_letter(self, letter: str) -> str:
        """Return the letter that precedes *letter* in the circular alphabet.

        >>> CircularAlphabet().prev_letter('a')
        'z'
        >>> CircularAlphabet().prev_letter('A')
        'Z'
        """
        alpha = self._alphabet(letter)
        i = self._index(letter)
        return alpha[(i - 1) % 26]

    def shift(self, letter: str, n: int) -> str:
        """Shift *letter* forward by *n* positions (wraps around).

        Negative values of *n* shift backwards.

        >>> CircularAlphabet().shift('a', 3)
        'd'
        >>> CircularAlphabet().shift('y', 3)
        'b'
        >>> CircularAlphabet().shift('d', -3)
        'a'
        """
        alpha = self._alphabet(letter)
        i = self._index(letter)
        return alpha[(i + n) % 26]

    def position(self, letter: str) -> int:
        """Return the 0-based position of *letter* (0 for 'a'/'A', 25 for 'z'/'Z').

        >>> CircularAlphabet().position('a')
        0
        >>> CircularAlphabet().position('Z')
        25
        """
        return self._index(letter)

    def letter_at(self, index: int, upper: bool = False) -> str:
        """Return the letter at the given circular *index*.

        Indices wrap around so that ``letter_at(26)`` returns the same letter
        as ``letter_at(0)``.

        >>> CircularAlphabet().letter_at(0)
        'a'
        >>> CircularAlphabet().letter_at(27)
        'b'
        >>> CircularAlphabet().letter_at(0, upper=True)
        'A'
        """
        alpha = self._upper if upper else self._lower
        return alpha[index % 26]

    def distance(self, start: str, end: str) -> int:
        """Return the forward circular distance from *start* to *end*.

        The result is always in the range ``[0, 25]``.

        >>> CircularAlphabet().distance('a', 'c')
        2
        >>> CircularAlphabet().distance('z', 'b')
        2
        """
        if start.islower() != end.islower():
            raise ValueError("Both letters must have the same case")
        return (self._index(end) - self._index(start)) % 26


# ---------------------------------------------------------------------------
# Module-level convenience functions
# ---------------------------------------------------------------------------

_default = CircularAlphabet()


def next_letter(letter: str) -> str:
    """Convenience wrapper – see :meth:`CircularAlphabet.next_letter`."""
    return _default.next_letter(letter)


def prev_letter(letter: str) -> str:
    """Convenience wrapper – see :meth:`CircularAlphabet.prev_letter`."""
    return _default.prev_letter(letter)


def shift(letter: str, n: int) -> str:
    """Convenience wrapper – see :meth:`CircularAlphabet.shift`."""
    return _default.shift(letter, n)
