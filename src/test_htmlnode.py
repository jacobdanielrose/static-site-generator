import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html_with_href(self):
        node = HTMLNode(props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_with_multiple_props(self):
        props = {
            "src": "https://example.com/goofy.jpg",
            "alt": "this is a goofy image"
        }
        node = HTMLNode(props=props)
        result = node.props_to_html()

        # Check that it starts with a space
        self.assertTrue(result.startswith(' '))

        # Check that each prop is in the result
        self.assertIn('src="https://example.com/goofy.jpg"', result)
        self.assertIn('alt="this is a goofy image"', result)

    def test_empty_props_to_html(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_empty_dict_props_to_html(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_none_tag(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_notag_to_raw_text(self):
        node = LeafNode(None, "My tag is None")
        self.assertEqual(node.to_html(), "My tag is None")

    def test_leaf_with_props(self):
        node = LeafNode("a", "Clicky click!", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Clicky click!</a>')

    def test_leaf_with_different_tags(self):
        node1 = LeafNode("h1", "Header")
        self.assertEqual(node1.to_html(), "<h1>Header</h1>")

        node2 = LeafNode("img", "Image", {"src": "picture.jpg", "alt": "a picture"})
        self.assertEqual(node2.to_html(), '<img src="picture.jpg" alt="a picture">Image</img>')

        node3 = LeafNode("span", "Inline text")
        self.assertEqual(node3.to_html(), "<span>Inline text</span>")
