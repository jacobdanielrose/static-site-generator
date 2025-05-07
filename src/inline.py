from textnode import TextType,TextNode, text_node_to_html_node
from htmlnode import LeafNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        # check for valid delimiter parts
        else:
            if node.text.count(delimiter) % 2 != 0:
                raise Exception("Missing closing symbol. Not valid Markdown")

            # split and create sections based on delimiter
            temp_nodes = []
            sections = node.text.split(delimiter)
            for i,section in enumerate(sections):
                if i % 2 == 0:
                    # Only add non-empty strings
                    if section:
                        temp_nodes.append(TextNode(section, TextType.TEXT))
                else:
                    temp_nodes.append(TextNode(section, text_type))
            new_nodes.extend(temp_nodes)
    return new_nodes
