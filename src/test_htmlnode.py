import unittest

from htmlnode import HTMLNode

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
