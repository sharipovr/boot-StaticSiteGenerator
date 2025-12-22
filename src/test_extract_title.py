import unittest

from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello world   "), "Hello world")

    def test_extract_title_ignores_h2(self):
        md = "## Not title\n\n# Real title\n"
        self.assertEqual(extract_title(md), "Real title")

    def test_extract_title_raises_if_missing(self):
        with self.assertRaises(Exception):
            extract_title("## No h1 here")


if __name__ == "__main__":
    unittest.main()


