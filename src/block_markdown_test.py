import unittest
from textwrap import dedent
from .block_markdown import (
    BlockType,
    markdown_to_blocks,
    markdown_to_html_node,
    block_to_block_type,
    block_to_html_node,
    _get_list_item_children,
)


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


class BlockToHtmlNode(unittest.TestCase):
    def test_simple_paragraph(self):
        input = "This is the simplest paragraph."
        type = BlockType.PARAGRAPH
        result = block_to_html_node(input, type)

        expected = f"<p>This is the simplest paragraph.</p>"
        self.assertEqual(result.to_html(), expected)

    def test_simple_heading(self):
        input = f"## This is the second simplest header."
        type = BlockType.HEADING
        result = block_to_html_node(input, type)

        expected = f"<h2>This is the second simplest header.</h2>"
        self.assertEqual(result.to_html(), expected)

    def test_complicated_code(self):
        input = "```This is a code block with *italicized text*, yo!```"
        type = BlockType.CODE
        result = block_to_html_node(input, type)

        expected = f"<pre><code>This is a code block with <i>italicized text</i>, yo!</code></pre>"
        self.assertEqual(result.to_html(), expected)

    def test_quote(self):
        input = "> line 1 of quote\n> line 2 of quote"
        type = BlockType.QUOTE
        result = block_to_html_node(input, type)

        expected = f"<blockquote>line 1 of quote line 2 of quote</blockquote>"
        self.assertEqual(result.to_html(), expected)

    def test_create_list_html_nodes(self):
        input = "item1\nitem2\nitem3"
        result = _get_list_item_children(input)
        result_text = "".join([i.to_html() for i in result])
        expected = "<li>item1</li><li>item2</li><li>item3</li>"
        self.assertEqual(result_text, expected)

    def test_unordered_list(self):
        input = "- line 1 of list\n- line 2 of list"
        type = BlockType.UNORDERED_LIST
        result = block_to_html_node(input, type)
        expected = dedent(
            """\
            <ul>
            <li>line 1 of list</li>
            <li>line 2 of list</li>
            </ul>
            """
        ).replace("\n", "")
        self.assertEqual(result.to_html(), expected)

    def test_ordered_list(self):
        input = "1. line 1 of list\n2. line 2 of list"
        type = BlockType.ORDERED_LIST
        result = block_to_html_node(input, type)
        expected = dedent(
            """\
            <ol>
            <li>line 1 of list</li>
            <li>line 2 of list</li>
            </ol>
            """
        ).replace("\n", "")
        self.assertEqual(result.to_html(), expected)


class MarkdownToHtml(unittest.TestCase):
    def test_paragraph(self):
        input = "The most basic text."
        result = markdown_to_html_node(input)
        expected = "<div><p>The most basic text.</p></div>"
        self.assertEqual(result.to_html(), expected)

    def test_ordered_list(self):
        input = "1. one\n2. two"
        result = markdown_to_html_node(input)
        expected = dedent(
            """\
            <div>
            <ol>
            <li>one</li>
            <li>two</li>
            </ol>
            </div>
            """
        ).replace("\n", "")
        self.assertEqual(result.to_html(), expected)

    def test_unordered_list(self):
        input = "* one\n* two"
        result = markdown_to_html_node(input)
        expected = dedent(
            """\
            <div>
            <ul>
            <li>one</li>
            <li>two</li>
            </ul>
            </div>
            """
        ).replace("\n", "")
        self.assertEqual(result.to_html(), expected)

    def test_extended_quotes(self):
        input = "> abc\n> d*e*f\n> ghi"
        result = markdown_to_html_node(input)
        expected = "<div><blockquote>abc d<i>e</i>f ghi</blockquote></div>"
        self.assertEqual(result.to_html(), expected)

    def test_inline_in_code(self):
        input = "```This *code* is **amazing**!\nSimply the best!```"
        result = markdown_to_html_node(input)
        expected = "<div><pre><code>This <i>code</i> is <b>amazing</b>! Simply the best!</code></pre></div>"
        self.assertEqual(result.to_html(), expected)

    def test_complex(self):
        input = dedent(
            """\
            Now **this** gets interesting.
                       
            > Here we are with multiple lines
        
            ##### And a new [linky link](https://www.example.com), yay!
            """
        )
        result = markdown_to_html_node(input)
        expected = dedent(
            """\
            <div>
            <p>Now <b>this</b> gets interesting.</p>
            <blockquote>Here we are with multiple lines</blockquote>
            <h5>And a new <a href=\"https://www.example.com\">linky link</a>, yay!</h5>
            </div>
            """
        ).replace("\n", "")
        self.assertEqual(result.to_html(), expected)

    def test_complex2(self):
        input = dedent(
            """\
            1. Here's
            2.  A new
            3.     *list* to play with
            

            ```TODO: implement this code```

            Now, how about a... ![rickroll](rickroll_pic.jpg)
            
            - Napping dog
            - Biting dog
            - Playful dog

            * Starred list
            * For good measure
            """
        )
        result = markdown_to_html_node(input)
        expected = dedent(
            """\
            <div>
            
            <ol>
            <li>Here's</li>
            <li> A new</li>
            <li>    <i>list</i> to play with</li>
            </ol>

            <pre>
            <code>TODO: implement this code
            </code>
            </pre>
            
            <p>Now, how about a... <img src="rickroll_pic.jpg" alt="rickroll"></img></p>
            
            <ul>
            <li>Napping dog</li>
            <li>Biting dog</li>
            <li>Playful dog</li>
            </ul>

            <ul>
            <li>Starred list</li>
            <li>For good measure</li>
            </ul>
            </div>
            """
        ).replace("\n", "")
        self.assertEqual(result.to_html(), expected)


class FromBootDevLesson(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
