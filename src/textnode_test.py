import unittest

from .textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("text", "b", "www.link.com")
        node2 = TextNode("different text", "b", "www.link.com")
        self.assertNotEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("text", "b", "www.link.com")
        node2 = TextNode("text", "i", "www.link.com")
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("text", "b", "www.link.com")
        node2 = TextNode("text", "b", "www.link2.com")
        self.assertNotEqual(node, node2)

    def test_all_not_eq(self):
        node = TextNode("text", "b", "www.link.com")
        node2 = TextNode("text2", "i", "www.link2.com")
        self.assertNotEqual(node, node2)

    def test_none_url_eq(self):
        node = TextNode("text", "b")
        node2 = TextNode("text", "b", None)
        self.assertEqual(node, node2)

    def test_empty_url(self):
        node = TextNode("text", "b", "")
        self.assertEqual(node.url, "")

    def test_no_url(self):
        node = TextNode("Text", "style")
        self.assertIsNone(node.url)


class TestTextNodeToHtml(unittest.TestCase):
    def test_textnode_to_html(self):
        node = TextNode("text", TextType.BOLD)
        result = text_node_to_html_node(node)
        self.assertEqual(result.to_html(), "<b>text</b>")


class FromBootDevLesson(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


if __name__ == "__main__":
    unittest.main()
