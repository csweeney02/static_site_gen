import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        dict = {"href":"https://www.google.com", "target": "_blank",}
        node = HTMLNode(None,None,None,dict)
        print(node.props_to_html())
    def test_leafnode_to_html(self):
        leaf = LeafNode("p", "This is a paragraph of text.")
        leaf2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        print(leaf.to_html())
        print(leaf2.to_html())
    def test_parentnode_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node2 = ParentNode("h", [node, LeafNode("a", "Click me!", {"href":"https://www.google.com"})])
        print(node.to_html())
        print(node2.to_html())

if __name__ == "__main__":
    unittest.main()