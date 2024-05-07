import unittest
from textwrap import dedent
from .convert_text import (
    block_to_html_node,
    markdown_to_html_node,
    _get_list_item_children,
)
from .block_markdown import BlockType


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

        expected = f"<blockquote>line 1 of quote\nline 2 of quote</blockquote>"
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
        expected = (
            "<div><blockquote>"
            + "abc\n"
            + "d<i>e</i>f\n"
            + "ghi"
            + "</blockquote></div>"
        )
        self.assertEqual(result.to_html(), expected)

    def test_inline_in_code(self):
        input = "```This *code* is **amazing**!\nSimply the best!```"
        result = markdown_to_html_node(input)
        expected = (
            "<div><pre><code>"
            + "This <i>code</i> is <b>amazing</b>!\n"
            + "Simply the best!</code></pre></div>"
        )
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
