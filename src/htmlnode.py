class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_str = ""
        if self.props:
            for k, v in self.props.items():
                html_str += f' {k}="{v}"'
        return html_str

    def __repr__(self):
        return f"HTMLNode({self.tag=}, {self.value=}, {self.children=}, {self.props=})"

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires a value")
        if not self.tag:
            return self.value

        html_str = f"<{self.tag}"
        html_str += super().props_to_html()
        html_str += f">{self.value}</{self.tag}>"
        return html_str


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode requires a tag")
        if self.children is None:
            raise ValueError("ParentNode requires children")

        html_str = f"<{self.tag}"
        html_str += super().props_to_html() + ">"
        for c in self.children:
            html_str += c.to_html()
        html_str += f"</{self.tag}>"

        return html_str
