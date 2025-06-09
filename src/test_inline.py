import unittest

from htmlnode import HTMLNode, LeafNode
from inline import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_single_code_block(self):
        """Test splitting a single code block"""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_multiple_code_blocks(self):
        """Test splitting multiple code blocks in one string"""
        node = TextNode("First `code` and second `block` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and second ", TextType.TEXT),
            TextNode("block", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_bold_text(self):
        """Test splitting bold text with ** delimiter"""
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_italic_text(self):
        """Test splitting italic text with * delimiter"""
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_no_delimiters(self):
        """Test text with no delimiters remains unchanged"""
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        # Should return the original node unchanged
        expected = [node]

        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_start_and_end(self):
        """Test delimiters at the beginning and end of text"""
        node = TextNode("`start` middle `end`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("start", TextType.CODE),
            TextNode(" middle ", TextType.TEXT),
            TextNode("end", TextType.CODE),
        ]

        self.assertEqual(new_nodes, expected)

    def test_empty_delimiter_content(self):
        """Test empty content between delimiters"""
        node = TextNode("Text with `` empty and `code` block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode(" empty and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_unmatched_delimiter_raises_error(self):
        """Test that unmatched delimiters raise ValueError"""
        node = TextNode("This has `unmatched delimiter", TextType.TEXT)

        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertIn("Invalid markdown, unmatched delimiter", str(context.exception))

    def test_multiple_unmatched_delimiters_raises_error(self):
        """Test that multiple unmatched delimiters raise ValueError"""
        node = TextNode("This `has` three `delimiters", TextType.TEXT)

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_non_text_nodes_passed_through(self):
        """Test that non-TEXT nodes are passed through unchanged"""
        nodes = [
            TextNode("This is `code`", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]

        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Already italic", TextType.ITALIC),
        ]

        self.assertEqual(new_nodes, expected)

    def test_html_nodes_passed_through(self):
        """Test that HTML nodes are passed through unchanged"""
        html_node = LeafNode("span", "HTML content")
        text_node = TextNode("Text with `code`", TextType.TEXT)

        nodes = [html_node, text_node]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

        expected = [
            html_node,
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]

        self.assertEqual(new_nodes, expected)

    def test_empty_node_list(self):
        """Test empty input list"""
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])

    def test_consecutive_delimiters(self):
        """Test consecutive delimiters"""
        node = TextNode("Text `first``second` more", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("first", TextType.CODE),
            TextNode("second", TextType.CODE),
            TextNode(" more", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

    def test_only_delimiters(self):
        """Test string that is only delimiters"""
        node = TextNode("``", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        # Should result in empty list since all parts are empty
        expected = []

        self.assertEqual(new_nodes, expected)

    def test_chaining_multiple_delimiters(self):
        """Test that function can be chained for multiple delimiter types"""
        # Start with text that has both code and bold
        node = TextNode("This is `code` and **bold** text", TextType.TEXT)

        # First pass: handle code
        nodes_after_code = split_nodes_delimiter([node], "`", TextType.CODE)

        # Second pass: handle bold
        final_nodes = split_nodes_delimiter(nodes_after_code, "**", TextType.BOLD)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(final_nodes, expected)


if __name__ == "__main__":
    unittest.main()
