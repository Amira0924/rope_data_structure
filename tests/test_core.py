"""Tests for the Rope class."""

import unittest

from rope_data_structure import Rope


class TestRope(unittest.TestCase):
    def test_empty_rope(self):
        rope = Rope("")
        self.assertEqual(len(rope), 0)
        self.assertEqual(str(rope), "")

    def test_single_leaf(self):
        rope = Rope("hello")
        self.assertEqual(len(rope), 5)
        self.assertEqual(str(rope), "hello")
        self.assertEqual(rope[1], "e")
        self.assertEqual(rope[-1], "o")

    def test_large_string_builds_balanced_tree(self):
        text = "x" * 2000
        rope = Rope(text)
        self.assertEqual(len(rope), 2000)
        self.assertEqual(str(rope), text)
        self.assertEqual(rope[1999], "x")

    def test_index_out_of_range(self):
        rope = Rope("abc")
        with self.assertRaises(IndexError):
            _ = rope[3]
        with self.assertRaises(IndexError):
            _ = rope[-4]

    def test_negative_index(self):
        rope = Rope("abcdef")
        self.assertEqual(rope[-1], "f")
        self.assertEqual(rope[-6], "a")

    def test_slice_returns_rope(self):
        rope = Rope("abcdefgh")
        sub = rope[2:5]
        self.assertIsInstance(sub, Rope)
        self.assertEqual(str(sub), "cde")

    def test_slice_with_step_not_one(self):
        rope = Rope("abcdefgh")
        sub = rope[1:8:2]
        self.assertIsInstance(sub, Rope)
        self.assertEqual(str(sub), "bdfh")

    def test_slice_empty(self):
        rope = Rope("abcdef")
        sub = rope[3:3]
        self.assertIsInstance(sub, Rope)
        self.assertEqual(len(sub), 0)
        self.assertEqual(str(sub), "")

    def test_slice_with_negative_bounds(self):
        rope = Rope("abcdefgh")
        sub = rope[-5:-2]
        self.assertEqual(str(sub), "def")

    def test_insert_middle(self):
        rope = Rope("abcdef")
        new_rope = rope.insert(3, "XYZ")
        self.assertEqual(str(new_rope), "abcXYZdef")
        # Original unchanged
        self.assertEqual(str(rope), "abcdef")

    def test_insert_start_and_end(self):
        rope = Rope("abc")
        self.assertEqual(str(rope.insert(0, "X")), "Xabc")
        self.assertEqual(str(rope.insert(3, "X")), "abcX")

    def test_insert_negative_index(self):
        rope = Rope("abc")
        self.assertEqual(str(rope.insert(-1, "X")), "abXc")

    def test_insert_out_of_range(self):
        rope = Rope("abc")
        with self.assertRaises(IndexError):
            rope.insert(4, "X")
        with self.assertRaises(IndexError):
            rope.insert(-4, "X")

    def test_delete_range(self):
        rope = Rope("abcdefgh")
        new_rope = rope.delete(2, 5)
        self.assertEqual(str(new_rope), "abfgh")

    def test_delete_empty_range_returns_same(self):
        rope = Rope("abcdef")
        new_rope = rope.delete(3, 3)
        self.assertIs(new_rope, rope)

    def test_delete_negative_bounds(self):
        rope = Rope("abcdefgh")
        self.assertEqual(str(rope.delete(-6, -3)), "abfgh")

    def test_append_and_prepend(self):
        rope = Rope("middle")
        self.assertEqual(str(rope.append("!" )), "middle!")
        self.assertEqual(str(rope.prepend("> ")), "> middle")

    def test_repr(self):
        rope = Rope("hi")
        self.assertEqual(repr(rope), "Rope('hi')")

    def test_type_error_on_bad_init(self):
        with self.assertRaises(TypeError):
            Rope(123)

    def test_type_error_on_bad_index(self):
        rope = Rope("abc")
        with self.assertRaises(TypeError):
            _ = rope[1.5]

    def test_large_slice_preserves_content(self):
        text = "".join(chr(ord("a") + (i % 26)) for i in range(1000))
        rope = Rope(text)
        sub = rope[100:900]
        self.assertEqual(str(sub), text[100:900])


if __name__ == "__main__":
    unittest.main()
