import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, markdown_to_html_node

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

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(),"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_missing_tag(self):
        node = ParentNode(None, [LeafNode("b", "Bold text")])
        with self.assertRaisesRegex(ValueError, "ParentNode must have a tag"):
            node.to_html()

    def test_to_html_missing_children(self):
        node = ParentNode("p", None)
        with self.assertRaisesRegex(ValueError, "ParentNode must have children"):
            node.to_html()

    def test_to_html_empty_child(self):
        node = ParentNode("p", [])
        self.assertEqual(node.to_html(), "<p></p>")

    def test_to_html_with_children_and_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><span>child</span></div>'
        )

class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_empty(self):
        md = ""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


        # md = "```\ncode here\n```"

        # node = markdown_to_html_node(md)
        # html = node.to_html()
        # self.assertEqual(
        #     html,
        #     "<div><pre><code>\ncode here\n</code></pre></div>",
        # )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>"
        )

    def test_unordered_list(self):
        md = """
- First item
- Second item
- Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>"
        )

        md = """
+ First item
+ Second item
+ Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>"
        )

        md = """
* First item
* Second item
* Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>"
        )

    def test_blockquote(self):
        md = """
> This is a blockquote.
> It spans multiple lines.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>This is a blockquote. It spans multiple lines.</p></blockquote></div>"
        )
