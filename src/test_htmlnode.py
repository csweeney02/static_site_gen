import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        dict = {"href":"https://www.google.com", "target": "_blank",}
        node = HTMLNode(None,None,None,dict)
        print(node.props_to_html)

if __name__ == "__main__":
    unittest.main()