import unittest
from blocks import BlockType, markdown_to_blocks, block_to_blocktype, markdown_to_html_node

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_headings(self):
        md = """
# h1 Heading

## h2 Heading

### h3 Heading

#### h4 Heading

##### h5 Heading

###### h6 Heading
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# h1 Heading",
                "## h2 Heading",
                "### h3 Heading",
                "#### h4 Heading",
                "##### h5 Heading",
                "###### h6 Heading"
            ],
        )

    def test_markdown_to_blocks_singlebock(self):
        md = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n- This is a list\n- with items"
            ]
        )

    def test_markdown_to_blocks_excessive_newlines(self):
            md = "Hi\n\n\nMy name is bobby"
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "Hi",
                    "My name is bobby"
                ]
            )

    def test_block_to_blocktype_heading(self):
        block1 = "# hello sir"
        self.assertEqual(block_to_blocktype(block1), BlockType.HEADING)

        block2 = "## hello sir"
        self.assertEqual(block_to_blocktype(block2), BlockType.HEADING)

        block3 = "### hello sir"
        self.assertEqual(block_to_blocktype(block3), BlockType.HEADING)

        block4 = "#### hello sir"
        self.assertEqual(block_to_blocktype(block4), BlockType.HEADING)

        block5 = "##### hello sir"
        self.assertEqual(block_to_blocktype(block5), BlockType.HEADING)

        block6 = "###### hello sir"
        self.assertEqual(block_to_blocktype(block6), BlockType.HEADING)

        block7 = "####### hello sir"
        self.assertNotEqual(block_to_blocktype(block7), BlockType.HEADING)

        block8 = "#######hello sir"
        self.assertNotEqual(block_to_blocktype(block8), BlockType.HEADING)

    def test_block_to_blocktype_code(self):
        block1 = '```const test = "Hello";\nconsole.log(test);```'
        self.assertEqual(block_to_blocktype(block1), BlockType.CODE)

        block2 = '`const test = "Hello";\nconsole.log(test);``'
        self.assertNotEqual(block_to_blocktype(block2), BlockType.CODE)

    def test_block_to_blocktype_quote(self):
        block1 = ">This\n>is\n>a\n>quote"
        self.assertEqual(block_to_blocktype(block1), BlockType.QUOTE)

        block2 = ">This\nis\n>a\n>quote"
        self.assertNotEqual(block_to_blocktype(block2), BlockType.QUOTE)

    def test_block_to_blocktype_unordered_list(self):
        block1 = "- Flour\n- Cheese\n- Tomatoes"
        self.assertEqual(block_to_blocktype(block1), BlockType.UNORDERED_LIST)

        block2 = "- Flour\n2. Cheese\n- Tomatoes"
        self.assertNotEqual(block_to_blocktype(block2), BlockType.UNORDERED_LIST)

        block3 = "- Flour\n-Cheese\n- Tomatoes"
        self.assertNotEqual(block_to_blocktype(block3), BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_ordered_list(self):
        block1 = "1. Flour\n2. Cheese\n3. Tomatoes"
        self.assertEqual(block_to_blocktype(block1), BlockType.ORDERED_LIST)

        block2 = "1. Flour\n3. Cheese\n4. Tomatoes"
        self.assertNotEqual(block_to_blocktype(block2), BlockType.ORDERED_LIST)

    def test_block_to_blocktype_paragraph(self):
        block = "This is just a paragraph"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)


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
