"""Core rope implementation.

A rope is a balanced binary tree where each leaf holds a substring of the
original string. Concatenation and slicing are O(log n), and index-based
access is O(log n). The tree is built by splitting a string into fixed-size
chunks and recursively combining them, keeping the tree balanced without
rotations by always combining two subtrees of roughly equal size.
"""

from dataclasses import dataclass
from typing import Union


@dataclass
class _Leaf:
    """Leaf node holding a substring."""

    text: str

    def __len__(self) -> int:
        return len(self.text)


@dataclass
class _Branch:
    """Internal node combining two subtrees."""

    left: "RopeNode"
    right: "RopeNode"
    length: int

    def __init__(self, left: "RopeNode", right: "RopeNode") -> None:
        self.left = left
        self.right = right
        self.length = len(left) + len(right)

    def __len__(self) -> int:
        return self.length


RopeNode = Union[_Leaf, _Branch]


class Rope:
    """A rope: an immutable balanced tree of string chunks.

    All operations return new Rope instances; the original is never mutated.
    """

    def __init__(self, text: str = "") -> None:
        """Build a rope from a string.

        The string is split into chunks of at most 512 characters. Splitting
        into fixed-size leaves keeps leaves large enough to amortize tree
        traversal overhead while keeping slices cheap.
        """
        if not isinstance(text, str):
            raise TypeError("Rope expects a string")
        self._root = self._build(text, 0, len(text))

    @staticmethod
    def _build(text: str, start: int, end: int) -> RopeNode:
        """Recursively build a balanced tree over text[start:end]."""
        chunk_size = 512
        if end - start <= chunk_size:
            return _Leaf(text[start:end])
        mid = (start + end) // 2
        left = Rope._build(text, start, mid)
        right = Rope._build(text, mid, end)
        return _Branch(left, right)

    def __len__(self) -> int:
        return len(self._root)

    def __str__(self) -> str:
        """Return the full string represented by the rope."""
        parts: list[str] = []
        self._collect(self._root, parts)
        return "".join(parts)

    def __repr__(self) -> str:
        return f"Rope({str(self)!r})"

    @staticmethod
    def _collect(node: RopeNode, parts: list[str]) -> None:
        if isinstance(node, _Leaf):
            parts.append(node.text)
        else:
            Rope._collect(node.left, parts)
            Rope._collect(node.right, parts)

    def __getitem__(self, index: Union[int, slice]) -> Union[str, "Rope"]:
        """Return a character or a sub-rope.

        Slicing returns a new Rope, not a string, to preserve the rope's
        efficient substring operations.
        """
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            if step != 1:
                # Step slicing requires materializing the string; this is an
                # unusual operation for a rope, so we accept the O(n) cost.
                return Rope(str(self)[start:stop:step])
            if start >= stop:
                return Rope("")
            return self._slice(start, stop)
        if isinstance(index, int):
            if index < 0:
                index += len(self)
            if index < 0 or index >= len(self):
                raise IndexError("rope index out of range")
            return self._char_at(index)
        raise TypeError("rope indices must be integers or slices")

    def _char_at(self, index: int) -> str:
        """Return the character at a non-negative index."""
        node = self._root
        while isinstance(node, _Branch):
            left_len = len(node.left)
            if index < left_len:
                node = node.left
            else:
                index -= left_len
                node = node.right
        return node.text[index]

    def _slice(self, start: int, stop: int) -> "Rope":
        """Return a new rope for text[start:stop] with 0 <= start < stop <= len(self)."""
        if start == 0 and stop == len(self):
            return self
        # Find all leaves that intersect the range and collect their substrings.
        parts: list[str] = []

        def visit(node: RopeNode, node_start: int) -> None:
            node_end = node_start + len(node)
            if stop <= node_start or start >= node_end:
                return
            if isinstance(node, _Leaf):
                local_start = max(start - node_start, 0)
                local_stop = min(stop - node_start, len(node.text))
                if local_start < local_stop:
                    parts.append(node.text[local_start:local_stop])
            else:
                left_len = len(node.left)
                visit(node.left, node_start)
                visit(node.right, node_start + left_len)

        visit(self._root, 0)
        return Rope("".join(parts))

    def insert(self, index: int, text: str) -> "Rope":
        """Return a new rope with text inserted at index."""
        if not isinstance(text, str):
            raise TypeError("inserted text must be a string")
        if index < 0:
            index += len(self)
        if index < 0 or index > len(self):
            raise IndexError("insert index out of range")
        return Rope(str(self)[:index] + text + str(self)[index:])

    def delete(self, start: int, end: int) -> "Rope":
        """Return a new rope with text[start:end] removed.

        Negative indices follow Python slice conventions.
        """
        length = len(self)
        start, end, _ = slice(start, end).indices(length)
        if start >= end:
            return self
        return Rope(str(self)[:start] + str(self)[end:])

    def append(self, text: str) -> "Rope":
        """Return a new rope with text appended."""
        return self.insert(len(self), text)

    def prepend(self, text: str) -> "Rope":
        """Return a new rope with text prepended."""
        return self.insert(0, text)
