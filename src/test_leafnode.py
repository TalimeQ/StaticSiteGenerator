import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_text(self):
        node = LeafNode(None, "Test123")
        self.assertEqual(node.to_html(),"Test123")

    def test_no_value(self):
        node = LeafNode(None,None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_complex(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),"<a href=\"https://www.google.com\">Click me!</a>")
