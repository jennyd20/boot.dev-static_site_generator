from .textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # Only split TextNodes - other nodes just get re-added
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        sections = node.text.split(delimiter)

        # If the split has resulted in an even number, then a delimiter has not been closed.
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax found in text: {node.text}")

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


# Not necessary

# def __convert_delimiter(delimiter):
#     match delimiter:
#         case "**":
#             return TextType.BOLD
#         case "*":
#             return TextType.ITALIC
#         case "`":
#             return TextType.CODE
#         case _:
#             # If not a known delimiter, just assume it is text.
#             return TextType.TEXT


# Takes raw text and returns a list of tuples
# Each tuple should contain the alt text and the URL of any markdown images
def extract_markdown_images(text):
    return None


# This one should extract markdown links instead of images. It should return tuples of anchor text and URLs.
def extract_markdown_links(text):
    return None
