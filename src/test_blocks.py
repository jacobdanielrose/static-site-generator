import unittest
from blocks import BlockType, markdown_to_blocks, block_to_blocktype

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
