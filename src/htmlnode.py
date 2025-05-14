class HTMLNode():
    """Class representing the most general type of HTML node. Not meant to be used itself, but rather to use one of its inherited classes"""
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str | None:
        """Simply returns the properly formatted HTML as a text string"""
        raise NotImplementedError()

    def props_to_html(self) -> str:
        """Simply takes the props to be passed to the html tag and renders them as properly formatted HTML"""
        if self.props is None:
            return ""

        mapped = map(lambda element: f' {element[0]}="{element[1]}"', self.props.items())
        return ''.join(mapped)

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag},{self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    """Class representing an html tag with no children. Value is simply the text to be enclosed in the tag: e.g. <p>this is text</p>"""
    def __init__(self, tag: str, value: str | None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str | None:
        if self.value is None and self.tag != "br":
            raise ValueError("LeafNode must have a value, unless it is self-closing tag, i.e. <br>")
        if self.tag == None:
            return self.value

        if self.tag == "br":
            return f"<{self.tag}>"

        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    """Class representing an enclosing tag with no value itself but containing children. e.g. blockquote in: <blockquote><p>this is text</p></blockquote>"""
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        elif self.children == None:
            raise ValueError("ParentNode must have children")

        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"
        children_html = "".join(map(lambda child: child.to_html(), self.children))

        return opening_tag + children_html + closing_tag
