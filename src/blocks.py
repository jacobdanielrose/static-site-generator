from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline import text_to_textnodes
from textnode import TextNode, text_node_to_html_node

class BlockType(Enum):
    """Represents the type of formatting required for a given block of markdown text"""
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown: str) -> list[str]:
    """Convert markdown to a list of markdown blocks as strings"""
    blocks = list(map(lambda x: x.strip(), markdown.split("\n\n")))
    blocks_ = [x for x in blocks if x]
    return blocks_

def block_to_blocktype(block: str) -> BlockType:
    """Returns the BlockType for a given block markdown  text"""
    is_quote, is_unordered_list, is_ordered_list =  True, True, True
    lines = block.split("\n")

    list_seperator, is_unordered_list = get_list_seperator(block)

    # code block check
    if len(lines[0]) >= 3 and len(lines[-1])>= 3 and lines[0][:3] == "```" and lines[len(lines)-1][-3:] == "```":
        return BlockType.CODE

    # rest of the checks require looking at each line, ergo: loopy time!
    for i, line in enumerate(lines):
        # checks if any of first 6 characters are a # followed by a space
        length = min(6, len(line)-1)
        for j in range(length):
            if line[j] == "#":
                if line[j+1] == " ":
                    return BlockType.HEADING
            else:
                break

        # bool checks
        if length > 0 and line[0] != ">":
            is_quote = False
        if not line.startswith(list_seperator):
            is_unordered_list = False
        if not line.startswith(f"{i+1}. "):
            is_ordered_list = False

    if is_quote:
        return BlockType.QUOTE
    elif is_unordered_list:
        return BlockType.UNORDERED_LIST
    elif is_ordered_list:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def get_list_seperator(block: str) -> tuple[str, bool]:
    """Returns the unordered list seperator in the first position.
    and a bool representing whether the block is an unordered list in the second position
    """
    lines = block.split("\n")
    for line in lines:
        if not line:
            continue
        else:
            if line.startswith("-"):
                return "- ", True
            if line.startswith("*"):
                return "* ", True
            if line.startswith("+"):
                return "+ ", True
            return "", False
    return "", False


def markdown_to_html_node(markdown: str) -> ParentNode:
    """Convert markdown string to an HTMLNode tree."""
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_blocktype(block)
        match block_type:
            case BlockType.CODE:
                code = create_codeblock_html_node(block)
                nodes.append(code)

            case BlockType.QUOTE:
                quote_node = create_quote_html_node(block)
                nodes.append(quote_node)

            case BlockType.HEADING:
                heading = create_heading_html_node(block)
                nodes.append(heading)

            case BlockType.UNORDERED_LIST:
                ul_node = create_list_html_node("ul", block)
                nodes.append(ul_node)

            case BlockType.ORDERED_LIST:
                ol_node = create_list_html_node("ol", block)
                nodes.append(ol_node)

            case BlockType.PARAGRAPH:
                paragraph_node = create_paragraph_html_node(block)
                nodes.append(paragraph_node)

    return ParentNode("div", nodes)


def text_to_children(text: str) -> list[HTMLNode]:
    """Convert markdown string to an array of HTMLNodes"""
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes

def create_list_html_node(tag: str, block: str) -> ParentNode:
    """Creates a HTML Node for either an ordered or unordered list based on the input tag"""
    lines = block.split("\n")
    line_nodes = []
    for line in lines:
        html_nodes = text_to_children(line[line.index(" ") + 1:])
        line_node = ParentNode("li", html_nodes)
        line_nodes.append(line_node)
    return ParentNode(tag, line_nodes)

def create_heading_html_node(block: str) -> ParentNode:
    """Creates a header HTMLNode"""
    count = block[:block.index(" ")].count("#")
    html_nodes = text_to_children(block[count+1:])
    return ParentNode(f"h{count}", html_nodes)

def create_codeblock_html_node(block: str) -> ParentNode:
    """Creates a code block HTMLNode"""
    lines = block.split("\n")
    if not (block.strip().startswith("```") and block.strip().endswith("```")):
        print("There appears to be an error with your code block Markdown. Please have a look!")
    code_content = "\n".join(lines[1:-1]) + "\n"
    child = LeafNode("code",code_content)
    return ParentNode("pre",[child])

def create_paragraph_html_node(block: str) -> ParentNode:
    """Creates a paragraph HTMLNode"""
    text = block.replace("\n", " ")
    html_nodes = text_to_children(text)
    return ParentNode("p", html_nodes)

def create_quote_html_node(block: str) -> ParentNode:
    """Creates a blockquote HTMLNode"""
    lines = block.split("\n")
    paragraphs = []

    for line in lines:
        # Extract content after '>'
        content = line[line.index(">") + 1:].lstrip()
        if content:
            html_nodes = text_to_children(content)
            paragraphs.extend(html_nodes)
        elif not content:
            paragraphs.append(LeafNode("br", None))

    return ParentNode("blockquote", paragraphs)
