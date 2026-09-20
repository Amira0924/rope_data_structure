# Rope Data Structure

A rope stores a long string as a balanced tree of substrings, making slicing, concatenation, and indexing efficient without copying the entire string on every edit.

## Usage

```python
from rope_data_structure import Rope

rope = Rope("The quick brown fox")
sub = rope[4:9]          # returns a Rope, not a str
print(str(sub))          # "quick"

edited = rope.insert(4, "very ")
print(str(edited))       # "The very quick brown fox"

removed = rope.delete(4, 9)
print(str(removed))      # "The  brown fox"
```

## Why this exists

Standard Python strings are flat arrays. Slicing a string copies the slice, so repeatedly taking substrings of a very large string becomes O(n) per slice. A rope splits the string into small immutable leaves and a balanced binary tree. Slicing a rope traverses only the leaves that intersect the slice, so the cost is proportional to the number of leaves touched, not the total string length. This implementation always keeps the tree balanced by building it from a flat string in a divide-and-conquer fashion; no rebalancing is needed after construction.

## Trade-off

Indexing a single character in a rope is O(log n) instead of O(1) because we walk from the root to a leaf. For workloads that do many small random accesses, a plain string may be faster. This library is best when you need many large substrings or edits from a long, mostly static string.

## Edge case

Slicing with a step other than 1 (e.g. `rope[::2]`) forces the rope to materialize the full string, then slices that string, and rebuilds a rope. This is O(n) and is the only operation that loses the rope's efficiency. The API returns a `Rope` for all slices, including stepped ones, to keep the return type consistent.
