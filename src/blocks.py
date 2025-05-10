import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    blocks = list(map(lambda x: x.strip(), markdown.split("\n\n")))
    blocks_ = [x for x in blocks if x]
    return blocks_

def block_to_blocktype(block) -> BlockType:
    is_quote, is_unordered_list, is_ordered_list =  True, True, True
    lines = block.split("\n")

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
        if not line.startswith("- "):
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
