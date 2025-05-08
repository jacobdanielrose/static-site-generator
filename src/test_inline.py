import unittest

from inline import extract_markdown_images, extract_markdown_links, split_nodes_delimiter
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

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_result = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(extract_markdown_images(text), expected_result)

    def test_extract_markdown_images_empty(self):
        text = "![]()"
        expected_result = [("", "")]
        self.assertEqual(extract_markdown_images(text), expected_result)

    def test_extract_markdown_images_nested(self):
        text = "![outer ![inner](inner-url)](outer-url)"
        expected_result = [("inner", "inner-url")]
        self.assertEqual(extract_markdown_images(text), expected_result)

    def test_extract_markdown_images_proper_negative_lookbehind(self):
        text = "Look at this![link](url)"
        expected_result = [("link", "url")]
        self.assertEqual(extract_markdown_images(text), expected_result)

    def test_extract_markdown_images_special_characters(self):
        text = "![A photo with spaces and special #characters](https://example.com/my%20image%20file%23v2.png)"
        expected_result = [("A photo with spaces and special #characters", "https://example.com/my%20image%20file%23v2.png")]
        self.assertEqual(extract_markdown_images(text), expected_result)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_result = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(extract_markdown_links(text), expected_result)

    def test_extract_markdown_links_special_characters(self):
        text = "[A photo with spaces and special #characters](https://example.com/my%20path%20test%23)"
        expected_result = [("A photo with spaces and special #characters", "https://example.com/my%20path%20test%23")]
        self.assertEqual(extract_markdown_links(text), expected_result)

    def test_extract_markdown_links_nested(self):
        text = "[outer [inner](inner-url)](outer-url)"
        expected_result = [("inner", "inner-url")]
        self.assertEqual(extract_markdown_links(text), expected_result)

    def test_extract_markdown_links_empty(self):
        text = "[]()"
        expected_result = [("", "")]
        self.assertEqual(extract_markdown_links(text), expected_result)
