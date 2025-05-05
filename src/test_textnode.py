import unittest

from textnode import TextNode, TextType

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
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)

        node3 = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        self.assertNotEqual(node, node3)

        node4 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node4)

    def test_url_empty(self):
        node = TextNode("Text Node", TextType.NORMAL)
        self.assertEqual(node.url, None)

        node2 = TextNode("Text Node", TextType.NORMAL, "http://example.com")
        self.assertNotEqual(node2.url, None)

if __name__ == "__main__":
    unittest.main()
