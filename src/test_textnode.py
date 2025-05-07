import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("This is a text node", TextType.CODE, "http://example.com")
        node4 = TextNode("This is a text node", TextType.CODE, "http://example.com")
        self.assertEqual(node3, node4)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

        node3 = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        self.assertNotEqual(node, node3)

        node4 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node4)

    def test_url_empty(self):
        node = TextNode("Text Node", TextType.TEXT)
        self.assertEqual(node.url, None)

        node2 = TextNode("Text Node", TextType.TEXT, "http://example.com")
        self.assertNotEqual(node2.url, None)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_list(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
        self.assertEqual(html_node.value, "This is a link node")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.google.com/picture.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://www.google.com/picture.jpg" ,"alt": "This is an image node"})
        self.assertEqual(html_node.value, "")

    def test_text_to_html_failed(self):
        node = TextNode("This is a failed test", None)
        self.assertRaises(Exception, text_node_to_html_node, node)

if __name__ == "__main__":
    unittest.main()
