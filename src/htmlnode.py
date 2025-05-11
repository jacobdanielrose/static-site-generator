from blocks import block_to_blocktype, markdown_to_blocks

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props is None:
            return ""

        mapped = map(lambda element: f' {element[0]}="{element[1]}"', self.props.items())
        return ''.join(mapped)

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag},{self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag == None:
            return self.value

        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        elif self.children == None:
            raise ValueError("ParentNode must have children")

        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"
        children_html = "".join(map(lambda child: child.to_html(), self.children))

        return opening_tag + children_html + closing_tag

def markdown_to_html_node(markdown) -> HTMLNode:
    """Convert markdown string to an HTMLNode tree."""
    from blocks import BlockType
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

def text_to_children(text) -> list[HTMLNode]:
    from inline import text_to_textnodes
    from textnode import text_node_to_html_node

    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)

    return html_nodes

def create_list_html_node(tag, block) -> ParentNode:
    lines = block.split("\n")
    line_nodes = []
    for line in lines:
        html_nodes = text_to_children(line[line.index(" ") + 1:])
        line_node = ParentNode("li", html_nodes)
        line_nodes.append(line_node)
    return ParentNode(tag, line_nodes)

def create_heading_html_node(block) -> ParentNode:
    count = block[:block.index(" ")].count("#")
    html_nodes = text_to_children(block[count+1:])
    return ParentNode(f"h{count}", html_nodes)

def create_codeblock_html_node(block) -> ParentNode:
    lines = block.split("\n")
    if not (block.strip().startswith("```") and block.strip().endswith("```")):
        print("There appears to be an error with your code block Markdown. Please have a look!")
    code_content = "\n".join(lines[1:-1]) + "\n"
    child = LeafNode("code",code_content)
    return ParentNode("pre",[child])

def create_paragraph_html_node(block) -> ParentNode:
    text = block.replace("\n", " ")
    html_nodes = text_to_children(text)
    return ParentNode("p", html_nodes)

def create_quote_html_node(block) -> ParentNode:
    lines = block.split("\n")
    line_nodes = []
    for i, line in enumerate(lines):
        if i == 0:
            html_nodes = text_to_children(line[line.index(">") + 1:].lstrip())
            line_nodes.extend(html_nodes)
        else:
            html_nodes = text_to_children(line[line.index(">") + 1:])
            line_nodes.extend(html_nodes)
    p_node = ParentNode("p", line_nodes)
    return ParentNode("blockquote", [p_node])
