import unittest

from .textnode import TextNode, TextType
from .htmlnode import LeafNode
from .inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


class TestSplitNodesOnDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    # def test_no_delimiter(self):
    #     node = TextNode("This is text with *all* **sorts** of `things`, okay?", TextType.TEXT)
    #     with self.assertRaises(ValueError):
    #         split_nodes_delimiter([node], "*", TextType.TEXT)

    def test_adjacent_empty_delimiter(self):
        node = TextNode("This is text with an `` empty code block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode(" empty code block", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_starting_delimiter(self):
        node = TextNode("**Bold** at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_ending_delimiter(self):
        node = TextNode("End with *italics*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("End with ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unclosed_delimiter(self):
        node = TextNode("I'm going to both **bold** and **bo..", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_many_delimiters(self):
        node = TextNode(
            "**lots** of **things** are **bolded** in **here**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("lots", TextType.BOLD),
            TextNode(" of ", TextType.TEXT),
            TextNode("things", TextType.BOLD),
            TextNode(" are ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" in ", TextType.TEXT),
            TextNode("here", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    # Originally I misunderstood node type vs. node.text_type.  This tests the former, I want to test the latter
    # def test_non_textnode(self):
    #     node = LeafNode("b", "bolded **leafnode** text")
    #     new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    #     expected = [LeafNode("b", "bolded **leafnode** text")]
    #     self.assertEqual(new_nodes[0].to_html(), expected[0].to_html())

    def test_multiple_nodes(self):
        node = TextNode("We have *italics `and code`*", TextType.TEXT)
        node2 = TextNode("Code `in the` middle", TextType.TEXT)
        node3 = TextNode("*Bold* `at` the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2, node3], "`", TextType.CODE)
        expected = [
            TextNode("We have *italics ", TextType.TEXT),
            TextNode("and code", TextType.CODE),
            TextNode("*", TextType.TEXT),
            TextNode("Code ", TextType.TEXT),
            TextNode("in the", TextType.CODE),
            TextNode(" middle", TextType.TEXT),
            TextNode("*Bold* ", TextType.TEXT),
            TextNode("at", TextType.CODE),
            TextNode(" the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    ############ Extra tests copied from the Boot.dev solution ############
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestMarkdownImagesAndLinks(unittest.TestCase):
    def test_images_basic(self):
        md_text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        textNodeList = extract_markdown_images(md_text)
        self.assertEqual(
            textNodeList,
            [
                (
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                (
                    "another",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                ),
            ],
        )

    def test_links_basic(self):
        md_text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        textNodeList = extract_markdown_links(md_text)
        self.assertEqual(
            textNodeList,
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
