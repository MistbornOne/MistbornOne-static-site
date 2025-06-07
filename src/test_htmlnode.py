import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
