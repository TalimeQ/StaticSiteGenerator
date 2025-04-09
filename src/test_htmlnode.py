import unittest

from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_default(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node.tag, node2.tag)
   
    def test_equal(self):
        node = HTMLNode("p")
        node2 = HTMLNode("h")
        self.assertNotEqual(node.tag, node2.tag)
    
    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_props(self):
        node = HTMLNode(None,None,None, {
    "href": "https://www.google.com",
    "target": "_blank",})
        
        string_rep = " href=\"https://www.google.com\" target=\"_blank\""

        self.assertEqual(node.props_to_html(),string_rep)
