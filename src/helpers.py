from textnode import TextNode,TextType
from htmlnode import LeafNode

import re

        #self.text = text
        #self.text_type = text_type
        #self.url = url

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text,None)
        case TextType.BOLD:
            return LeafNode("b",text_node.text,None)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text,None)
        case TextType.CODE:
            return LeafNode("code",text_node.text,None)
        case TextType.LINK:
            return LeafNode("a",text_node.text,{"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img",None,{
                "src" : text_node.url,
                "alt" : text_node.text})
        case _:
            raise Exception("Invalid node type")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        split_text = old_node.text.split(f'{delimiter}')
        if len(split_text) == 1:
            raise Exception(f"No matching delimiter was found for {delimiter} in {node.text}")
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(split_text[i],TextType.TEXT))
            else:
                split_nodes.append(TextNode(split_text[i],text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)