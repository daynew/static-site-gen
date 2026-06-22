class HTMLNode:

    def __init__(self, tag: str | None = None, value: str | None = None, children: list['HTMLNode'] | None = None, props: dict[str, str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplemented()

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ''
        html = ''
        for prop in self.props:
            html += f' {prop}="{self.props[prop]}"'
        return html

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        if self.tag != other.tag:
            return False
        if self.value != other.value:
            return False
        if self.children != other.children:
            return False
        if self.props != other.props:
            return False
        return True

    def __repr__(self):
        indent = '    '
        result = [f'HTMLNode(']
        result.append(indent + f'{self.tag}')
        result.append(indent + f'{self.value}')
        for child in self.children:
            lines = repr(child).split('\n')
            indented_lines = map(lambda l: indent + l, lines)
            result.append('\n'.join(indented_lines))
        result.append(indent + self.props_to_html())
        result.append(')')
        return '\n'.join(result)


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, "{self.props_to_html()}")'


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have child nodes")
        html = []
        html.append(f'<{self.tag}{self.props_to_html()}>')
        for child in self.children:
            html.append(child.to_html())
        html.append(f'</{self.tag}>')
        return ''.join(html)
