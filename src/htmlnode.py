class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props is None:
            return ""

        mapped = map(lambda element: f' {element[0]}="{element[1]}"', self.props.items())
        return ''.join(mapped)

    def __repr__(self) -> str:
        return f"HTMLNode | tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("LeafNode must have a value")
        elif self.tag == None:
            return self.value
        else:
            props_html = self.props_to_html()
            return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        elif self.children == None:
            raise ValueError("ParentNode must have a child")

        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"
        children_html = "".join(map(lambda child: child.to_html(), self.children))

        return opening_tag + children_html + closing_tag
