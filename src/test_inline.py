import unittest

from inline import split_nodes_delimiter
from textnode import TextNode, TextType

class TestInline(unittest.TestCase):
    def test_inline_with_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_inline_with_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_inline_with_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)

    def test_inline_with_multiple_sections(self):
        node = TextNode("This is _text_ **with** a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        newer_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        final_nodes = split_nodes_delimiter(newer_nodes, "**", TextType.BOLD)
        expected_result = [
              TextNode("This is ", TextType.TEXT),
              TextNode("text", TextType.ITALIC),
              TextNode(" ", TextType.TEXT),
              TextNode("with", TextType.BOLD),
              TextNode(" a ", TextType.TEXT),
              TextNode("code block", TextType.CODE),
              TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(final_nodes, expected_result)
