import unittest
import functools
from textnode import TextNode, TextType
from markdown_converter import *
from main import *


class TestTextNode(unittest.TestCase):
    '''def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("hello world", TextType.BOLD)
        node2 = TextNode("goodbye world", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_split_nodes_delimiter(self):
        old_nodes = [TextNode("This is text with a **bold** and a **bold** word", TextType.TEXT)]
        print(split_nodes_delimiter(old_nodes, '**', TextType.BOLD))
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        print(extract_markdown_images(text))
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        print(extract_markdown_links(text))
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        print(split_nodes_image([node]))
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        print(split_nodes_link([node]))
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        print(text_to_textnodes(text))
    def test_markdown_to_blocks(self):
        markdown = "#This is a heading\n\nThis is a paragraph. **bold text**\n\n*Item One\n*Item two\n*item three"
        print(markdown_to_blocks(markdown))
    def test_block_to_block_type(self):
        block = ">test line\n* test line\n>yes"
        print(block_to_block_type(block))
    def test_markdown_to_html_node(self):
        markdown = "## First test to see if anything breaks\n\n1. hello\n2. goodbye"
        text = markdown_to_html_node(markdown)
        print(text)'''
    def test_extract_title(self):
        markdown = "hello world\nhello world again\n# this time bigger"
        print(extract_title(markdown))

if __name__ == "__main__":
    unittest.main()