import re


class BlockType:
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    block_strs = []
    sections = markdown.split("\n\n")
    for sect in sections:
        block = sect.strip()
        if block:
            block_strs.append(block)
    return block_strs


# TODO: return a tuple where the second part is the stuff inside the block type markdown
def block_to_block_type(markdown):
    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    heading_rgex = r"^#{1,6} "
    if re.search(heading_rgex, markdown):
        return BlockType.HEADING

    # Code blocks must start with 3 backticks and end with 3 backticks.
    code_regex = r"(?s)^```.*```$"
    if re.search(code_regex, markdown):
        return BlockType.CODE

    # Every line in a quote block must start with a > character.
    quote_regex = r"(?m)^>.*$"
    if re.search(quote_regex, markdown):
        return BlockType.QUOTE

    # Every line in an unordered list block must start with a * or - character.
    unordered_list_regex = r"(?m)^[*-].*$"
    if re.search(unordered_list_regex, markdown):
        return BlockType.UNORDERED_LIST

    # Every line in an ordered list block must start with a number followed by a . character.
    # The number must start at 1 and increment by 1 for each line.
    if _is_ordered_list(markdown):
        return BlockType.ORDERED_LIST

    # By default, if nothing else matches than this is a paragraph
    return BlockType.PARAGRAPH


# Verify that each line starts with a number followed by a ., and the number increments for each line
def _is_ordered_list(markdown):
    current_num = 0
    lines = markdown.splitlines()

    for line in lines:
        if "." not in line:
            return False
        try:
            num = int(line.split(".")[0])
        except ValueError:
            return False
        if num != current_num + 1:
            return False
        current_num = num
    return True
