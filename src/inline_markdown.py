import re
from .textnode import TextType, TextNode


def _split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # Only split TextNodes - other nodes just get re-added
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        sections = node.text.split(delimiter)

        # If the split has resulted in an even number, then a delimiter has not been closed.
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax, delimiter not closed in text: {node.text}")

        # Otherwise, every section will alternate between the new type and the TEXT text type.
        # Skip empty sections.
        for i, split_text in enumerate(sections):
            if not split_text:
                continue
            # Determine what the type of this section will be
            new_type = TextType.TEXT if i % 2 == 0 else text_type
            new_node = TextNode(split_text, new_type)
            new_nodes.append(new_node)
    return new_nodes


# Takes raw text and returns a list of tuples
# Each tuple should contain the alt text and the URL of any markdown images
def _extract_markdown_images(text):
    rgex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(rgex, text)
    return matches


# This one should extract markdown links instead of images. It should return tuples of anchor text and URLs.
# Only match if there is no "!"" preceding the square brackets
def _extract_markdown_links(text):
    rgex = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    # TODO Simpler?
    # rgex = r"^[^!]\[(.*?)\]\((.*?)\)"
    matches = re.findall(rgex, text)
    return matches


def _split_nodes_image(old_nodes):
    return _split_img_and_link_nodes(old_nodes, TextType.IMAGE)


def _split_nodes_link(old_nodes):
    return _split_img_and_link_nodes(old_nodes, TextType.LINK)


def _split_img_and_link_nodes(old_nodes, type):
    def _get_regex(match, type):
        c = "!" if type == TextType.IMAGE else ""
        return f"{c}[{match[0]}]({match[1]})"

    extract_markdown_func = (
        _extract_markdown_images if type == TextType.IMAGE else _extract_markdown_links
    )

    new_nodes = []
    for node in old_nodes:
        matches = extract_markdown_func(node.text)

        # If there are no matches, just add the text node back to the list
        if not matches:
            new_nodes.append(node)
            continue

        processed_txt = node.text
        for match in matches:
            # Split regex is given from tutorial
            split_text = processed_txt.split(_get_regex(match, type), 1)
            before_text, after_text = split_text
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))
            # Create node from the match itself
            new_nodes.append(TextNode(match[0], type, match[1]))
            processed_txt = after_text

        # After processing all the images, put the remainder into a text node
        if processed_txt:
            new_nodes.append(TextNode(processed_txt, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = _split_nodes_link(nodes)
    nodes = _split_nodes_image(nodes)
    nodes = _split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = _split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = _split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
