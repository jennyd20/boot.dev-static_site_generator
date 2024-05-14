import unittest

from .textnode import TextNode, TextType
from .inline_markdown import (
    _split_nodes_delimiter,
    _extract_markdown_images,
    _extract_markdown_links,
    _split_nodes_image,
    _split_nodes_link,
    text_to_textnodes,
)


class TestSplitNodesOnDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = _split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_adjacent_empty_delimiter(self):
        node = TextNode("This is text with an `` empty code block", TextType.TEXT)
        new_nodes = _split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode(" empty code block", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_starting_delimiter(self):
        node = TextNode("**Bold** at the start", TextType.TEXT)
        new_nodes = _split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_ending_delimiter(self):
        node = TextNode("End with *italics*", TextType.TEXT)
        new_nodes = _split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("End with ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unclosed_delimiter(self):
        node = TextNode("I'm going to both **bold** and **bo..", TextType.TEXT)
        with self.assertRaises(ValueError):
            _split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_many_delimiters(self):
        node = TextNode(
            "**lots** of **things** are **bolded** in **here**", TextType.TEXT
        )
        new_nodes = _split_nodes_delimiter([node], "**", TextType.BOLD)
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

    def test_multiple_nodes(self):
        node = TextNode("We have *italics `and code`*", TextType.TEXT)
        node2 = TextNode("Code `in the` middle", TextType.TEXT)
        node3 = TextNode("*Bold* `at` the start", TextType.TEXT)
        new_nodes = _split_nodes_delimiter([node, node2, node3], "`", TextType.CODE)
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
        new_nodes = _split_nodes_delimiter([node], "**", TextType.BOLD)
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
        new_nodes = _split_nodes_delimiter([node], "**", TextType.BOLD)
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
        new_nodes = _split_nodes_delimiter([node], "**", TextType.BOLD)
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
        new_nodes = _split_nodes_delimiter([node], "*", TextType.ITALIC)
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
        new_nodes = _split_nodes_delimiter([node], "`", TextType.CODE)
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
        textNodeList = _extract_markdown_images(md_text)
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

    def test_image_at_start(self):
        md_text = "![start img](https://upload.wikimedia.org/wikipedia/en/f/f7/RickRoll.png) and more"
        textNodeList = _extract_markdown_images(md_text)
        self.assertEqual(
            textNodeList,
            [
                (
                    "start img",
                    "https://upload.wikimedia.org/wikipedia/en/f/f7/RickRoll.png",
                )
            ],
        )

    def test_links_basic(self):
        md_text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        textNodeList = _extract_markdown_links(md_text)
        self.assertEqual(
            textNodeList,
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )

    def test_link_at_start(self):
        md_text = "[start link](https://www.example.com) and more"
        textNodeList = _extract_markdown_links(md_text)
        self.assertEqual(
            textNodeList,
            [("start link", "https://www.example.com")],
        )

    def test_split_nodes_image(self):
        md_text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"
        node = TextNode(
            md_text,
            TextType.TEXT,
        )
        new_nodes = _split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
                ),
            ],
        )

    def test_multiple_image_nodes(self):
        node = TextNode("We have *italics `and code`*", TextType.TEXT)
        node2 = TextNode(
            "![here's an image!](https://www.markdownguide.org/assets/images/markdown-mark-white.svg).  Do you like it?",
            TextType.TEXT,
        )
        node3 = TextNode("*Bold* `at` the start", TextType.TEXT)
        node4 = TextNode(
            "Finishing with [a link](https://markdownguide.org)", TextType.TEXT
        )
        node5 = TextNode(
            "jk, here's ![another cool image](https://upload.wikimedia.org/wikipedia/en/f/f7/RickRoll.png)",
            TextType.TEXT,
        )
        new_nodes = _split_nodes_image([node, node2, node3, node4, node5])
        expected = [
            TextNode("We have *italics `and code`*", TextType.TEXT),
            TextNode(
                "here's an image!",
                TextType.IMAGE,
                "https://www.markdownguide.org/assets/images/markdown-mark-white.svg",
            ),
            TextNode(".  Do you like it?", TextType.TEXT),
            TextNode("*Bold* `at` the start", TextType.TEXT),
            TextNode(
                "Finishing with [a link](https://markdownguide.org)", TextType.TEXT
            ),
            TextNode("jk, here's ", TextType.TEXT),
            TextNode(
                "another cool image",
                TextType.IMAGE,
                "https://upload.wikimedia.org/wikipedia/en/f/f7/RickRoll.png",
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link(self):
        md_text = "This is text with a [primary search page](https://www.google.com) and another [web search engine](https://www.bing.com).  Isn't that neat?"
        node = TextNode(
            md_text,
            TextType.TEXT,
        )
        new_nodes = _split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "primary search page",
                    TextType.LINK,
                    "https://www.google.com",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "web search engine",
                    TextType.LINK,
                    "https://www.bing.com",
                ),
                TextNode(".  Isn't that neat?", TextType.TEXT),
            ],
        )

    def test_multiple_link_nodes(self):
        node = TextNode("We have *italics `and code`*", TextType.TEXT)
        node2 = TextNode(
            "![here's an image!](https://www.markdownguide.org/assets/images/markdown-mark-white.svg).  Do you like it?",
            TextType.TEXT,
        )
        node3 = TextNode("[start link](https://test.com)", TextType.TEXT)
        node4 = TextNode(
            "Finishing with [a link](https://markdownguide.org)", TextType.TEXT
        )
        node5 = TextNode(
            "jk, here's ![another cool image](https://upload.wikimedia.org/wikipedia/en/f/f7/RickRoll.png)",
            TextType.TEXT,
        )
        new_nodes = _split_nodes_link([node, node2, node3, node4, node5])
        expected = [
            TextNode("We have *italics `and code`*", TextType.TEXT),
            TextNode(
                "![here's an image!](https://www.markdownguide.org/assets/images/markdown-mark-white.svg).  Do you like it?",
                TextType.TEXT,
            ),
            TextNode("start link", TextType.LINK, "https://test.com"),
            TextNode("Finishing with ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://markdownguide.org"),
            TextNode(
                "jk, here's ![another cool image](https://upload.wikimedia.org/wikipedia/en/f/f7/RickRoll.png)",
                TextType.TEXT,
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_images_and_links(self):
        node1 = TextNode(
            "my image ![i_1](https://www.markdownguide.org/assets/images/markdown-mark-white.svg), with a link [l_1](https://www.google.com)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "[l_2](https://www.bing.com) a second link, ![i_2](https://upload.wikimedia.org/wikipedia/en/f/f7/RickRoll.png) is the image now",
            TextType.TEXT,
        )
        new_nodes = _split_nodes_image(_split_nodes_link([node1, node2]))
        expected = [
            TextNode("my image ", TextType.TEXT),
            TextNode(
                "i_1",
                TextType.IMAGE,
                "https://www.markdownguide.org/assets/images/markdown-mark-white.svg",
            ),
            TextNode(", with a link ", TextType.TEXT),
            TextNode("l_1", TextType.LINK, "https://www.google.com"),
            TextNode("l_2", TextType.LINK, "https://www.bing.com"),
            TextNode(" a second link, ", TextType.TEXT),
            TextNode(
                "i_2",
                TextType.IMAGE,
                "https://upload.wikimedia.org/wikipedia/en/f/f7/RickRoll.png",
            ),
            TextNode(" is the image now", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


class TestTextToTextNodes(unittest.TestCase):
    def test_one_of_each_type(self):
        md = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        result = text_to_textnodes(md)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "image",
                TextType.IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)

    def test_start_and_end(self):
        md = "**start with BOLD** and end with *italic text here*"
        result = text_to_textnodes(md)
        expected = [
            TextNode("start with BOLD", TextType.BOLD),
            TextNode(" and end with ", TextType.TEXT),
            TextNode("italic text here", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)

    def test_exclamations(self):
        md = "! Here is a sentence!  Here is a !![rickroll](https://upload.wikimedia.org/wikipedia/en/f/f7/RickRoll.png).  This is so neat!!"
        result = text_to_textnodes(md)
        expected = [
            TextNode("! Here is a sentence!  Here is a !", TextType.TEXT),
            TextNode(
                "rickroll",
                TextType.IMAGE,
                "https://upload.wikimedia.org/wikipedia/en/f/f7/RickRoll.png",
            ),
            TextNode(".  This is so neat!!", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_invalid(self):
        md = "This is **invalid * I forgot an asterisk"
        with self.assertRaises(ValueError):
            text_to_textnodes(md)

    # TODO: nesting not currently supported
    # def test_nested(self):
    #     md = "This [link is **bold**](https://www.google.com) and `emphasized *code*`"
    #     result = text_to_textnodes(md)
    #     expected = [
    #         TextNode("This ", TextType.TEXT),
    #         TextNode(
    #             "link is **bold**",
    #             TextType.LINK,
    #             "https://www.google.com",
    #         ),
    #         TextNode(" and ", TextType.TEXT),
    #         TextNode("emphasized *code*", TextType.CODE)
    #     ]
    #     self.assertEqual(result, expected)

class FromBootDevLesson(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = _split_nodes_delimiter([node], "**", TextType.BOLD)
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
        new_nodes = _split_nodes_delimiter([node], "**", TextType.BOLD)
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
        new_nodes = _split_nodes_delimiter([node], "**", TextType.BOLD)
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
        new_nodes = _split_nodes_delimiter([node], "*", TextType.ITALIC)
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
        new_nodes = _split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = _extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = _extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = _split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            TextType.TEXT,
        )
        new_nodes = _split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = _split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = _split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
