from .htmlnode import ParentNode
from .textnode import text_node_to_html_node
from .block_markdown import BlockType, markdown_to_blocks, block_to_block_type
from .inline_markdown import text_to_textnodes


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


# Note: each individual line inside the code block will be treated as its own paragraph
def _code_to_html_node(block):
    filtered = block[3:-3]
    children = _get_children(filtered)
    code_block = ParentNode("code", children)
    return ParentNode("pre", [code_block])


# Note: each individual line inside the quote block will be treated as its own paragraph
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


def _strip_chars_from_lines(block, num_to_strip):
    stripped_lines = []
    for line in block.splitlines():
        stripped_lines.append(line[num_to_strip:])
    return "\n".join(stripped_lines)


def _get_children(block):
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
