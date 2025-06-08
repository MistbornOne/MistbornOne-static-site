from textnode import TextNode, TextType


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""

        html_attrs = []
        for key, value in self.props.items():
            html_attrs.append(f'{key}="{value}"')

        return " " + " ".join(html_attrs)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return self.value

        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        elif self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have children")

        props_html = self.props_to_html()
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"


def text_node_to_html(text_node):
    if not isinstance((text_node), TextNode):
        raise Exception(
            "Must be one of the following: Text, Bold, Italic, Code, Links, or Images"
        )

    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text).to_html()
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("strong", text_node.text).to_html()
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("em", text_node.text).to_html()
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text).to_html()
    elif text_node.text_type == TextType.LINKS:
        return LeafNode("a", text_node.text, {"href": text_node.url}).to_html()
    elif text_node.text_type == TextType.IMAGES:
        return LeafNode(
            "img", "", {"src": text_node.url, "alt": text_node.text}
        ).to_html()
    else:
        raise Exception(f"Unknown text type: {text_node.text_type}")
