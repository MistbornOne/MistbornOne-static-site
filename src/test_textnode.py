import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node3 = TextNode("This is a test node", TextType.BOLD)
        node4 = TextNode("This is a test node", TextType.ITALIC)
        self.assertNotEqual(node3, node4)

    def test_url_none(self):
        url_none = TextNode("This is a link", TextType.LINKS)
        self.assertIsNone(url_none.url)

    def test_url_provided(self):
        node_with_url = TextNode(
            "This is a link", TextType.LINKS, "https://ianwatkins.dev"
        )
        self.assertEqual(node_with_url.url, "https://ianwatkins.dev")

    def test_different_urls(self):
        url_none2 = TextNode("This is a link", TextType.LINKS)
        node_with_url2 = TextNode(
            "This is a link", TextType.LINKS, "https://ianwatkins.dev"
        )
        self.assertNotEqual(url_none2, node_with_url2)


if __name__ == "__main__":
    unittest.main()
