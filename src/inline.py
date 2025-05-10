import re
from textnode import TextType, TextNode

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

def extract_markdown_images(text) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        # Find all images in text
        images = extract_markdown_images(node.text)

        if not images:
            result.append(node)
            continue

        # Now we need to split text and create new nodes
        current_text = node.text
        for alt_text, url in images:
            # split on first occurence of image
            # Note: maxsplit paramter being 1 is important for avoiding
            # issues where the image appears more than once
            image_markdown = f"![{alt_text}]({url})"
            parts = current_text.split(image_markdown, 1)

            # Don't add empty text to a TextNode
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))

            result.append(TextNode(alt_text, TextType.IMAGE, url))

            # Important step: set current_text to the next array element
            # otherwise you will have the old image in the text that needs
            # to be split by the next image and overlapping text
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))

    return result

def split_nodes_link(old_nodes) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        links = extract_markdown_links(node.text)

        if not links:
            result.append(node)
            continue

        # Now we must split text and create new nodes
        current_text = node.text
        for alt_text, url in links:
            # split on first occurence of links
            # Note: maxsplits=1 is important for duplicate links
            # in the same text
            link_markdown = f"[{alt_text}]({url})"
            parts = current_text.split(link_markdown, 1)

            # Don't add empty text to a TextNode
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))

            result.append(TextNode(alt_text, TextType.LINK, url))

            # Important step: set current_text to the next array element
            # otherwise you will have the old image in the text that needs
            # to be split by the next link and overlapping text
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))

    return result

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
