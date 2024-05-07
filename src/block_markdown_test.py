import unittest
from textwrap import dedent
from .block_markdown import BlockType, markdown_to_blocks, block_to_block_type


class MarkdownToBlocks(unittest.TestCase):
    def test_basic(self):
        md = dedent(
            """\
            # This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is a list item
            * This is another list item
            """
        )
        result = markdown_to_blocks(md)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item",
        ]
        self.assertEqual(result, expected)

    def test_basic_2(self):
        md = dedent(
            """\
            This is **bolded** paragraph

            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line

            * This is a list
            * with items
            """
        )
        result = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        self.assertEqual(result, expected)

    def test_remove_whitespace(self):
        md = dedent(
            """\
            
                    
            Whee!  Lots of spaces.    At the end and start.    

                random indent
                    further random indent



            excess space between blocks      
               there was space at the end of the last line.

            """
        )
        result = markdown_to_blocks(md)
        expected = [
            "Whee!  Lots of spaces.    At the end and start.",
            "random indent\n        further random indent",
            "excess space between blocks      \n   there was space at the end of the last line.",
        ]
        self.assertEqual(result, expected)


class BlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        input = "This is a plain paragraph."
        self.assertEqual(block_to_block_type(input), BlockType.PARAGRAPH)

    def test_heading_1(self):
        input = "# Heading the first"
        self.assertEqual(block_to_block_type(input), BlockType.HEADING)

    def test_heading_3(self):
        input = "### Heading the third"
        self.assertEqual(block_to_block_type(input), BlockType.HEADING)

    def test_heading_6(self):
        input = "###### Heading the max"
        self.assertEqual(block_to_block_type(input), BlockType.HEADING)

    def test_heading_8(self):
        input = "######## Not a heading anymore"
        self.assertEqual(block_to_block_type(input), BlockType.PARAGRAPH)

    def test_heading_multiline(self):
        input = dedent(
            """\
            #### Valid heading
            with multiple lines, baby
            YEEEAAAAHH"""
        )
        self.assertEqual(block_to_block_type(input), BlockType.HEADING)

    def test_code(self):
        input = "```test_code = True```"
        self.assertEqual(block_to_block_type(input), BlockType.CODE)

    def test_code_multiline(self):
        input = dedent(
            """\
            ``` a = "so much code"
            b = "to test here"
            c = True```"""
        )
        self.assertEqual(block_to_block_type(input), BlockType.CODE)

    def test_quote(self):
        input = dedent(
            """\
            > I am quoting
            > a prior quote
            > from a cool author"""
        )
        self.assertEqual(block_to_block_type(input), BlockType.QUOTE)

    def test_quote_broken(self):
        input = dedent(
            """\
            > I am quoting
            a prior quote
            > from a cool author"""
        )
        self.assertEqual(block_to_block_type(input), BlockType.QUOTE)

    def test_unordered_list_stars(self):
        input = dedent(
            """\
            * Dishes
            * Refill medications
            * Stay awake"""
        )
        self.assertEqual(block_to_block_type(input), BlockType.UNORDERED_LIST)

    def test_unordered_list_dashes(self):
        input = dedent(
            """\
            - Feed the dog
            - Play with the dog
            - Make sure the dog naps"""
        )
        self.assertEqual(block_to_block_type(input), BlockType.UNORDERED_LIST)

    def test_unordered_list_mixed(self):
        input = dedent(
            """\
            * Enjoy the sunshine
            - Be inside
            * Exercise"""
        )
        self.assertEqual(block_to_block_type(input), BlockType.UNORDERED_LIST)

    def test_unordered_list_broken(self):
        input = dedent(
            """\
            * Dishes
            Refill medications
            * Stay awake"""
        )
        self.assertEqual(block_to_block_type(input), BlockType.UNORDERED_LIST)

    def test_ordered_list_correct_basic(self):
        input = dedent(
            """\
            1. The beginning
            2. the middle
            3. the end"""
        )
        self.assertEqual(block_to_block_type(input), BlockType.ORDERED_LIST)

    def test_ordered_list_correct_extra_symbols(self):
        input = dedent(
            """\
            1. The **beginning**!  Really.
            2. the middle.  *Kinda boring*.
            3. the end.  We are done, yaaay##!``` ALL THE > SYMBOLS"""
        )
        self.assertEqual(block_to_block_type(input), BlockType.ORDERED_LIST)

    def test_ordered_list_bad_start(self):
        input = dedent(
            """\
            0. the beginning
            1. the middle
            2. the end"""
        )
        self.assertEqual(block_to_block_type(input), BlockType.PARAGRAPH)

    def test_ordered_list_incorrect_wrong_order(self):
        input = dedent(
            """\
            1. the beginning.
            3. the end
            2. the middle"""
        )
        self.assertEqual(block_to_block_type(input), BlockType.PARAGRAPH)

    def test_ordered_list_incorrect_no_dots(self):
        input = dedent(
            """\
            1 the beginning
            3 the middle.  Has a period here.
            2 the end"""
        )
        self.assertEqual(block_to_block_type(input), BlockType.PARAGRAPH)

    def test_mix_and_match_1(self):
        input = dedent(
            """\
            ```the beginning
            > Not a list
            1. Still not a list
            ### Or a heading```"""
        )
        self.assertEqual(block_to_block_type(input), BlockType.CODE)

    def test_mix_and_match_2(self):
        input = dedent(
            """\
            >unordered line
            >```Internal code```
            >  ### Heading
            >1. list
            >2. list2
            > * unordered"""
        )
        self.assertEqual(block_to_block_type(input), BlockType.QUOTE)


if __name__ == "__main__":
    unittest.main()
