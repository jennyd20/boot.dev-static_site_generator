import unittest

from .htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_basic_constructor(self):
        node = HTMLNode("p", "Text", [], {"<a>": {"href": "https://www.google.com"}})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Text")
        self.assertEqual(node.children, [])

        props = node.props
        self.assertIsInstance(props, dict)
        assert isinstance(props, dict)
        self.assertEqual(len(props), 1)
        k, v = list(props.items())[0]
        self.assertEqual(k, "<a>")
        self.assertEqual(v, {"href": "https://www.google.com"})

    def test_no_args_constructor(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )


class TestLeafNode(unittest.TestCase):
    def test_constructor(self):
        node = LeafNode("tag", "value", None)
        self.assertEqual(node.tag, "tag")
        self.assertEqual(node.value, "value")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_invalid_constructor(self):
        node = LeafNode("b", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(
            node2.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_no_tag(self):
        node = LeafNode(None, "more stuff here")
        self.assertEqual(node.to_html(), "more stuff here")

    def test_multipe_props(self):
        node = LeafNode("p", "Clicky", {"a": "b", "c": "d"})
        self.assertEqual(node.to_html(), '<p a="b" c="d">Clicky</p>')

    def test_complicated_value(self):
        node = LeafNode(
            "i",
            "This is a longer string: a=b and 'More text' with \"More text\" and an internal <> and {{}} for good measure",
        )
        self.assertEqual(
            node.to_html(),
            "<i>This is a longer string: a=b and 'More text' with \"More text\" and an internal <> and {{}} for good measure</i>",
        )


class TestParentNode(unittest.TestCase):
    def test_constructor(self):
        node = ParentNode("a", ["b", "c"], {"d": "e"})
        self.assertEqual(node.tag, "a")
        self.assertIsNone(node.value)
        self.assertEqual(node.children, ["b", "c"])
        self.assertEqual(node.props, {"d": "e"})

    def test_invalid_constructor(self):
        node = ParentNode("a", None)
        node2 = ParentNode(None, [])
        with self.assertRaises(ValueError):
            node.to_html()
        with self.assertRaises(ValueError):
            node2.to_html()

    def test_basic_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_single_child(self):
        node = ParentNode("b", [LeafNode("i", "bold and italicized here")])
        self.assertEqual(node.to_html(), "<b><i>bold and italicized here</i></b>")

    def test_two_leaf_children(self):
        children = [LeafNode(None, "first child"), LeafNode("b", "bolded second child")]
        node = ParentNode("i", children)
        self.assertEqual(node.to_html(), "<i>first child<b>bolded second child</b></i>")

    def test_many_children(self):
        children = [
            LeafNode("a", 1),
            LeafNode("b", 2),
            LeafNode("c", 3),
            LeafNode("d", 4),
        ]
        node = ParentNode("i", children)
        self.assertEqual(node.to_html(), "<i><a>1</a><b>2</b><c>3</c><d>4</d></i>")

    def test_sub_children(self):
        grandchildren1 = [LeafNode("a", "atext"), LeafNode("b", "btext")]
        grandchildren2 = [LeafNode("c", "ctext"), LeafNode("d", "dtext")]
        child1 = ParentNode("first", grandchildren1)
        child2 = ParentNode("second", grandchildren2)
        node = ParentNode("top", [child1, child2])
        self.assertEqual(
            node.to_html(),
            "<top><first><a>atext</a><b>btext</b></first><second><c>ctext</c><d>dtext</d></second></top>",
        )


if __name__ == "__main__":
    unittest.main()
