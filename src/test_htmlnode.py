import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_with_props(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"class": "my-class"})
        expected = ' class="my-class"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            props={
                "id": "main-content",
                "class": "container large",
                "data-test": "value",
            }
        )
        result = node.props_to_html()
        # Check that it starts with space and contains all props
        self.assertTrue(result.startswith(" "))
        self.assertIn('id="main-content"', result)
        self.assertIn('class="container large"', result)
        self.assertIn('data-test="value"', result)

    def test_repr(self):
        node = HTMLNode(
            tag="a",
            value="Click me",
            children=None,
            props={"href": "https://example.com"},
        )
        expected = "HTMLNode(a, Click me, None, {'href': 'https://example.com'})"
        self.assertEqual(repr(node), expected)

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag_raw_text(self):
        node = LeafNode(None, "Just some raw text")
        expected = "Just some raw text"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_empty_string_value(self):
        # Empty string is still a valid value
        node = LeafNode("p", "")
        expected = "<p></p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_special_characters(self):
        node = LeafNode("p", "Text with <special> & characters")
        expected = "<p>Text with <special> & characters</p>"
        self.assertEqual(node.to_html(), expected)

    def test_inheritance_from_htmlnode(self):
        # Test that LeafNode properly inherits from HTMLNode
        node = LeafNode("span", "Test", {"class": "test"})
        self.assertIsNone(node.children)  # Should always be None for leaf nodes
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "Test")
        self.assertEqual(node.props, {"class": "test"})

    def test_repr(self):
        node = LeafNode("a", "Link text", {"href": "https://example.com"})
        expected = "HTMLNode(a, Link text, None, {'href': 'https://example.com'})"
        self.assertEqual(repr(node), expected)


class TestParentNode(unittest.TestCase):

    def test_parent_node_repr(self):
        node = HTMLNode(
            tag="div", value="Parent Node", children=None, props={"id": "parent"}
        )
        expected = "HTMLNode(div, Parent Node, None, {'id': 'parent'})"
        self.assertEqual(repr(node), expected)

    def test_parent_node_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_to_html_with_children(self):
        child1 = LeafNode("p", "Child 1")
        child2 = LeafNode("p", "Child 2")
        parent = ParentNode(tag="div", children=[child1, child2])
        expected = "<div><p>Child 1</p><p>Child 2</p></div>"
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_with_grandchildren(self):
        grandchild = LeafNode("span", "Grandchild")
        child = ParentNode(tag="div", children=[grandchild])
        parent = ParentNode(tag="section", children=[child])
        expected = "<section><div><span>Grandchild</span></div></section>"
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_with_nested_parents(self):
        child1 = LeafNode("p", "Child 1")
        child2 = LeafNode("p", "Child 2")
        parent1 = ParentNode(tag="div", children=[child1])
        parent2 = ParentNode(tag="section", children=[parent1, child2])
        expected = "<section><div><p>Child 1</p></div><p>Child 2</p></section>"
        self.assertEqual(parent2.to_html(), expected)

    def test_grandchild_has_no_tag(self):
        grandchild = LeafNode(None, "Grandchild with no tag")
        child = ParentNode(tag="div", children=[grandchild])
        parent = ParentNode(tag="section", children=[child])
        expected = "<section><div>Grandchild with no tag</div></section>"
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_with_great_grandchildren(self):
        great_grandchild = LeafNode("span", "Great Grandchild")
        grandchild = ParentNode(tag="div", children=[great_grandchild])
        child = ParentNode(tag="section", children=[grandchild])
        parent = ParentNode(tag="article", children=[child])
        expected = "<article><section><div><span>Great Grandchild</span></div></section></article>"
        self.assertEqual(parent.to_html(), expected)

    def test_for_empty_children(self):
        node = ParentNode(tag="div", children=[])
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()
