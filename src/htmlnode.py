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
