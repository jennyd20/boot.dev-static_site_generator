import unittest
from textwrap import dedent
from .initialize import _extract_title


class ExtractTitle(unittest.TestCase):
    def test_regular(self):
        input = dedent(
            """\
            # This is my title

            ```Followed by code```

            * li 1
            * li 2
            * li 3
            """
        )
        title = _extract_title(input)
        self.assertEqual(title, "This is my title")

    def test_no_title(self):
        input = dedent(
            """\
            ## No title here

            > To be
            > or not to be
            """
        )
        with self.assertRaises(ValueError):
            _extract_title(input)

    def test_extra_titles(self):
        input = dedent(
            """\
            # This is exciting
            # So very exciting!

            1. This had better fail
            2. Or I did something wrong
            """
        )
        with self.assertRaises(ValueError):
            _extract_title(input)

    def test_middle_title(self):
        input = dedent(
            """\
            Hello there
            
            # This title is in the middle

            Goodbye now
            """
        )
        title = _extract_title(input)
        self.assertEqual(title, "This title is in the middle")

    def test_empty_title(self):
        input = dedent(
            """\
            # 
            
            There was nothing there!
            """
        )
        with self.assertRaises(ValueError):
            _extract_title(input)


if __name__ == "__main__":
    unittest.main()
