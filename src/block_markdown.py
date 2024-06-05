import re
from .htmlnode import ParentNode
from .textnode import text_node_to_html_node
from .inline_markdown import text_to_textnodes


class BlockType:
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = []
    sections = markdown.split("\n\n")
    for sect in sections:
        block = sect.strip()
        if block:
            blocks.append(block)
    return blocks


# TODO: return a tuple where the second part is the stuff inside the block type markdown
def block_to_block_type(markdown_block):
    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    heading_rgex = r"^#{1,6} "
    if re.search(heading_rgex, markdown_block):
        return BlockType.HEADING

    # Code blocks must start with 3 backticks and end with 3 backticks.
    code_regex = r"(?s)^```.*```$"
    if re.search(code_regex, markdown_block):
        return BlockType.CODE

    # Every line in a quote block must start with a > character.
    quote_regex = r"(?m)^>.*$"
    if re.search(quote_regex, markdown_block):
        return BlockType.QUOTE

    # Every line in an unordered list block must start with a * or - character.
    unordered_list_regex = r"(?m)^[*-].*$"
    if re.search(unordered_list_regex, markdown_block):
        return BlockType.UNORDERED_LIST

    # Every line in an ordered list block must start with a number followed by a . character.
    # The number must start at 1 and increment by 1 for each line.
    if _is_ordered_list(markdown_block):
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


# A block is a set of text, defined by being separated from another block by a whole line
# Assume we're only getting well formed blocks
# Address each block type separately
def block_to_html_node(block, type):
    match type:
        case BlockType.PARAGRAPH:
            return _paragraph_to_html_node(block)
        case BlockType.HEADING:
            return _heading_to_html_node(block)
        case BlockType.CODE:
            return _code_to_html_node(block)
        case BlockType.QUOTE:
            return _quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return _unordered_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return _ordered_to_html_node(block)
        case _:
            raise ValueError(f"Invalid type of block: {type}")


################ HTML NODE CREATORS ################


def _paragraph_to_html_node(block):
    # No character filtering required
    children = _get_children(block)
    return ParentNode("p", children)


def _heading_to_html_node(block):
    h_count = 0
    for h in block:
        if h == "#":
            h_count += 1
            if h_count > 6:
                raise ValueError("Invalid # header count")
        else:
            break

    filtered = block[h_count + 1 :]
    children = _get_children(filtered)
    return ParentNode("h" + str(h_count), children)


# Note: keep newlines in the code block.  Not true with all other blocks.
def _code_to_html_node(block):
    filtered = block[3:-3].strip()
    children = _get_children(filtered, True)
    code_block = ParentNode("code", children)
    return ParentNode("pre", [code_block])


def _quote_to_html_node(block):
    filtered = _strip_chars_from_lines(block, 2)
    children = _get_children(filtered)
    return ParentNode("blockquote", children)


def _unordered_to_html_node(block):
    filtered = _strip_chars_from_lines(block, 2)
    children = _get_list_item_children(filtered)
    return ParentNode("ul", children)


def _ordered_to_html_node(block):
    filtered = _strip_chars_from_lines(block, 3)
    children = _get_list_item_children(filtered)
    return ParentNode("ol", children)


################ HELPER METHODS ################


# Strip a given number of characters from lines
# for blocks whose lines all have a symbol in the front,
# such as quotes, unordered lists, and ordered lists
def _strip_chars_from_lines(block, num_to_strip):
    stripped_lines = []
    for line in block.splitlines():
        stripped_lines.append(line[num_to_strip:])
    return "\n".join(stripped_lines)


def _get_children(block, keep_newlines = False):
    # Code does keep newlines, but everything else does not.
    if not keep_newlines:
        block = re.sub("\n", " ", block)
    textnodes = text_to_textnodes(block)
    html_nodes = []
    for n in textnodes:
        html_nodes.append(text_node_to_html_node(n))
    return html_nodes


def _get_list_item_children(block):
    li_html_nodes = []
    for line in block.splitlines():
        inner_html_node = _get_children(line)
        li_html_nodes.append(ParentNode("li", inner_html_node))
    return li_html_nodes


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        new_node = block_to_html_node(block, block_type)
        children.append(new_node)

    # External wrap
    node = ParentNode("div", children)
    return node
