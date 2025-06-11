import unittest

from htmlnode import HTMLNode, LeafNode
from inline import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
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


# ==== Test Regex Patterns ====


def test_image_regex():
    text = "Here is an image ![alt text](http://example.com/image.png)"
    result = extract_markdown_images(text)
    expected = [("alt text", "http://example.com/image.png")]
    assert result == expected, f"Expected {expected}, got {result}"

    text = "No image here"
    result = extract_markdown_images(text)
    expected = []
    assert result == expected, f"Expected {expected}, got {result}"

    text = "Empty alt ![](https://example.com/image.png)"
    result = extract_markdown_images(text)
    expected = [("", "https://example.com/image.png")]
    assert result == expected, f"Expected {expected}, got {result}"

    text = "Just text with no images"
    result = extract_markdown_images(text)
    expected = []
    assert result == expected, f"Expected {expected}, got {result}"

    text = (
        "Text with spaces in alt ![alt text with spaces](http://example.com/image.png)"
    )
    result = extract_markdown_images(text)
    expected = [("alt text with spaces", "http://example.com/image.png")]
    assert result == expected, f"Expected {expected}, got {result}"

    text = "Multiple images ![first](http://example.com/first.png) and ![second](http://example.com/second.png)"
    result = extract_markdown_images(text)
    expected = [
        ("first", "http://example.com/first.png"),
        ("second", "http://example.com/second.png"),
    ]
    assert result == expected, f"Expected {expected}, got {result}"

    text = "Special characters in alt ![alt with !@#$%^&*()](http://example.com/special.png)"
    result = extract_markdown_images(text)
    expected = [("alt with !@#$%^&*()", "http://example.com/special.png")]
    assert result == expected, f"Expected {expected}, got {result}"

    text = "Local image ![local image](./local-image.png)"
    result = extract_markdown_images(text)
    expected = [("local image", "./local-image.png")]
    assert result == expected, f"Expected {expected}, got {result}"

    text = "Multiline images ![first](http://example.com/first.png)\n![second](http://example.com/second.png)"
    result = extract_markdown_images(text)
    expected = [
        ("first", "http://example.com/first.png"),
        ("second", "http://example.com/second.png"),
    ]
    assert result == expected, f"Expected {expected}, got {result}"


def test_link_regex():
    text = "Here is a link [example](http://example.com)"
    result = extract_markdown_links(text)
    expected = [("example", "http://example.com")]
    assert result == expected, f"Expected {expected}, got {result}"

    text = "No link here"
    result = extract_markdown_links(text)
    expected = []
    assert result == expected, f"Expected {expected}, got {result}"

    text = "Empty link text []()"
    result = extract_markdown_links(text)
    expected = [("", "")]
    assert result == expected, f"Expected {expected}, got {result}"

    text = "Just text with no links"
    result = extract_markdown_links(text)
    expected = []
    assert result == expected, f"Expected {expected}, got {result}"

    text = "Text with spaces in link [link with spaces](http://example.com)"
    result = extract_markdown_links(text)
    expected = [("link with spaces", "http://example.com")]
    assert result == expected, f"Expected {expected}, got {result}"

    text = "Multiple links [first](http://example.com/first) and [second](http://example.com/second)"
    result = extract_markdown_links(text)
    expected = [
        ("first", "http://example.com/first"),
        ("second", "http://example.com/second"),
    ]
    assert result == expected, f"Expected {expected}, got {result}"

    text = (
        "Special characters in link [link with !@#$%^&*()](http://example.com/special)"
    )
    result = extract_markdown_links(text)
    expected = [("link with !@#$%^&*()", "http://example.com/special")]
    assert result == expected, f"Expected {expected}, got {result}"

    text = "Local link [local link](./local-link.html)"
    result = extract_markdown_links(text)
    expected = [("local link", "./local-link.html")]
    assert result == expected, f"Expected {expected}, got {result}"


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        nodes = [
            TextNode(
                "Here is an image ![alt](https://img.com/image.png)", TextType.TEXT
            )
        ]
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGES, "https://img.com/image.png"),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_image_at_start(self):
        nodes = [TextNode("![start](start.png) and text", TextType.TEXT)]
        expected = [
            TextNode("start", TextType.IMAGES, "start.png"),
            TextNode(" and text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_image_at_end(self):
        nodes = [TextNode("Text before ![end](end.png)", TextType.TEXT)]
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("end", TextType.IMAGES, "end.png"),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_only_image(self):
        nodes = [TextNode("![only](only.png)", TextType.TEXT)]
        expected = [TextNode("only", TextType.IMAGES, "only.png")]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_no_images(self):
        nodes = [TextNode("Just text here.", TextType.TEXT)]
        expected = [TextNode("Just text here.", TextType.TEXT)]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_multiple_images(self):
        nodes = [TextNode("![one](1.png) middle ![two](2.png)", TextType.TEXT)]
        expected = [
            TextNode("one", TextType.IMAGES, "1.png"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("two", TextType.IMAGES, "2.png"),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_ignores_non_text_nodes(self):
        nodes = [
            TextNode("Text with ![img](img.png)", TextType.TEXT),
            TextNode("<b>bold</b>", TextType.BOLD),
        ]
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("img", TextType.IMAGES, "img.png"),
            TextNode("<b>bold</b>", TextType.BOLD),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        nodes = [TextNode("Click [here](https://example.com)", TextType.TEXT)]
        expected = [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINKS, "https://example.com"),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_link_at_start(self):
        nodes = [TextNode("[start](s.com) then more", TextType.TEXT)]
        expected = [
            TextNode("start", TextType.LINKS, "s.com"),
            TextNode(" then more", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_link_at_end(self):
        nodes = [TextNode("Go to [end](e.com)", TextType.TEXT)]
        expected = [
            TextNode("Go to ", TextType.TEXT),
            TextNode("end", TextType.LINKS, "e.com"),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_only_link(self):
        nodes = [TextNode("[only](o.com)", TextType.TEXT)]
        expected = [TextNode("only", TextType.LINKS, "o.com")]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_no_links(self):
        nodes = [TextNode("Plain text", TextType.TEXT)]
        expected = [TextNode("Plain text", TextType.TEXT)]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_multiple_links(self):
        nodes = [TextNode("[one](1.com) and [two](2.com)", TextType.TEXT)]
        expected = [
            TextNode("one", TextType.LINKS, "1.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.LINKS, "2.com"),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_ignores_images(self):
        # Confirm image markdown is not parsed as a link
        nodes = [TextNode("Image: ![img](img.com) not a link", TextType.TEXT)]
        expected = [TextNode("Image: ![img](img.com) not a link", TextType.TEXT)]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_ignores_non_text_nodes(self):
        nodes = [
            TextNode("[link](l.com)", TextType.TEXT),
            TextNode("strong", TextType.BOLD),
        ]
        expected = [
            TextNode("link", TextType.LINKS, "l.com"),
            TextNode("strong", TextType.BOLD),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)


if __name__ == "__main__":
    unittest.main()
