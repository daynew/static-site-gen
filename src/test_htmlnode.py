import unittest
import copy
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_eq_empty(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_eq_full(self):
        nested_child = HTMLNode('b', 'bolded')
        nested_child_2 = copy.copy(nested_child)
        props = {"prop1": "value1"}
        props_2 = props.copy()
        node = HTMLNode('p', 'some text', nested_child, props)
        node2 = HTMLNode('p', 'some text', nested_child_2, props_2)
        self.assertEqual(node, node2)

    def test_not_eq_tag(self):
        nested_child = HTMLNode('b', 'bolded')
        nested_child_2 = copy.copy(nested_child)
        props = {"prop1": "value1"}
        props_2 = props.copy()
        node = HTMLNode('p', 'some text', nested_child, props)
        node2 = HTMLNode('span', 'some text', nested_child_2, props_2)
        self.assertNotEqual(node, node2)

    def test_not_eq_value(self):
        nested_child = HTMLNode('b', 'bolded')
        nested_child_2 = copy.copy(nested_child)
        props = {"prop1": "value1"}
        props_2 = props.copy()
        node = HTMLNode('p', 'some text', nested_child, props)
        node2 = HTMLNode('p', 'some not equal text', nested_child_2, props_2)
        self.assertNotEqual(node, node2)

    def test_not_eq_child(self):
        nested_child = HTMLNode('b', 'bolded')
        nested_child_2 = copy.copy(nested_child)
        nested_child_2.value = 'not equal value'
        props = {"prop1": "value1"}
        props_2 = props.copy()
        node = HTMLNode('p', 'some text', nested_child, props)
        node2 = HTMLNode('p', 'some text', nested_child_2, props_2)
        self.assertNotEqual(node, node2)

    def test_not_eq_prop(self):
        nested_child = HTMLNode('b', 'bolded')
        nested_child_2 = copy.copy(nested_child)
        props = {"prop1": "value1"}
        props_2 = props.copy()
        props_2["extra_prop"] = "should cause not equal"
        node = HTMLNode('p', 'some text', nested_child, props)
        node2 = HTMLNode('p', 'some text', nested_child_2, props_2)
        self.assertNotEqual(node, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Go to example", {'href': 'https://example.com'})
        self.assertEqual(
            node.to_html(), '<a href="https://example.com">Go to example</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
