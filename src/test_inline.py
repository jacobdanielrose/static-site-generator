import unittest

from inline import text_to_textnodes, split_nodes_image, split_nodes_link, extract_markdown_images, extract_markdown_links, split_nodes_delimiter
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        expected_result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        self.assertListEqual(expected_result, split_nodes_image([node]))


    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT
        )
        expected_result =  [
             TextNode("This is text with a link ", TextType.TEXT),
             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
             TextNode(" and ", TextType.TEXT),
             TextNode(
                 "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
             ),
         ]
        self.assertEqual(split_nodes_link([node]), expected_result)

    def test_split_images_no_images(self):
        # Test a node with no images
        node = TextNode("This is text with no images", TextType.TEXT)
        expected_result = [node]
        self.assertListEqual(expected_result, split_nodes_image([node]))

    def test_split_images_empty_text(self):
        # Test with empty text before/after images
        node = TextNode("![image](https://example.com/img.jpg)Text after", TextType.TEXT)
        expected_result = [
            TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode("Text after", TextType.TEXT)
        ]
        self.assertListEqual(expected_result, split_nodes_image([node]))

    def test_split_images_non_text_node(self):
        # Test with a node that's already an image type
        node = TextNode("image", TextType.IMAGE, "https://example.com/img.jpg")
        expected_result = [node]
        self.assertListEqual(expected_result, split_nodes_image([node]))

    def test_split_images_multiple_nodes(self):
        # Test with multiple nodes in the input list
        node1 = TextNode("Text with ![img](https://example.com/1.jpg)", TextType.TEXT)
        node2 = TextNode("More text", TextType.TEXT)
        expected_result = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://example.com/1.jpg"),
            TextNode("More text", TextType.TEXT)
        ]
        self.assertListEqual(expected_result, split_nodes_image([node1, node2]))

    def test_split_images_duplicate_image(self):
        # Test with the same image appearing twice
        node = TextNode(
            "Here's ![img](https://example.com/img.jpg) and again ![img](https://example.com/img.jpg)",
            TextType.TEXT
        )
        expected_result = [
            TextNode("Here's ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://example.com/img.jpg"),
            TextNode(" and again ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://example.com/img.jpg")
        ]
        self.assertListEqual(expected_result, split_nodes_image([node]))

    def test_split_images_at_start_and_end(self):
        # Test with links at the beginning and end of text
        node = TextNode(
            "![first](https://example.com/1)middle![last](https://example.com/2)",
            TextType.TEXT
        )
        expected_result = [
            TextNode("first", TextType.IMAGE, "https://example.com/1"),
            TextNode("middle", TextType.TEXT),
            TextNode("last", TextType.IMAGE, "https://example.com/2")
        ]
        self.assertListEqual(expected_result, split_nodes_image([node]))


    def test_split_links_no_links(self):
        # Test a node with no links
        node = TextNode("This is text with no links", TextType.TEXT)
        expected_result = [node]
        self.assertListEqual(expected_result, split_nodes_link([node]))

    def test_split_links_empty_text(self):
        # Test with empty text before/after links
        node = TextNode("[link](https://example.com)Text after", TextType.TEXT)
        expected_result = [
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode("Text after", TextType.TEXT)
        ]
        self.assertListEqual(expected_result, split_nodes_link([node]))

    def test_split_links_consecutive_links(self):
        # Test with links appearing right after each other
        node = TextNode(
            "Text[link1](https://example.com/1)[link2](https://example.com/2)",
            TextType.TEXT
        )
        expected_result = [
            TextNode("Text", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://example.com/1"),
            TextNode("link2", TextType.LINK, "https://example.com/2")
        ]
        self.assertListEqual(expected_result, split_nodes_link([node]))

    def test_split_links_at_start_and_end(self):
        # Test with links at the beginning and end of text
        node = TextNode(
            "[first](https://example.com/1)middle[last](https://example.com/2)",
            TextType.TEXT
        )
        expected_result = [
            TextNode("first", TextType.LINK, "https://example.com/1"),
            TextNode("middle", TextType.TEXT),
            TextNode("last", TextType.LINK, "https://example.com/2")
        ]
        self.assertListEqual(expected_result, split_nodes_link([node]))

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected_result, text_to_textnodes(text))

    def test_text_to_textnodes_empty_string(self):
        text = ""
        expected_result = []
        self.assertListEqual(expected_result, text_to_textnodes(text))

    def test_text_to_textnodes_adjacent_formatting(self):
        text = "I am **bold**_italic_"
        expected_result = [
            TextNode("I am ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC)
        ]
        self.assertListEqual(expected_result, text_to_textnodes(text))

    def test_text_to_textnodes_unmatched_delimeter(self):
        text = "**bold is great"
        with self.assertRaisesRegex(Exception, "Missing closing symbol. Not valid Markdown"):
            text_to_textnodes(text)

    def test_text_to_textnodes_multiple_instances(self):
        text = "**bold** goes **boldly** where no one else goes"
        expected_result = [
            TextNode("bold", TextType.BOLD),
            TextNode(" goes ", TextType.TEXT),
            TextNode("boldly", TextType.BOLD),
            TextNode(" where no one else goes", TextType.TEXT)
        ]
        self.assertListEqual(expected_result, text_to_textnodes(text))
