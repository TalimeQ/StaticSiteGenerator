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
            return LeafNode("img","",{
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
        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception(f"No matching delimiter was found for {delimiter} in {old_node.text}")
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

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        checked_text = old_node.text
        matches = extract_markdown_images(checked_text)
        if(len(matches) == 0 ):
            new_nodes.append(old_node)
            continue
        for match in matches:
            sections =  checked_text.split(f"![{match[0]}]({match[1]})",1)
            if len(sections) != 2:
                raise Exception("invalid markdown")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0],TextType.TEXT))

            new_nodes.append(TextNode(
                match[0],
                TextType.IMAGE,
                match[1],
                ))
            checked_text = sections[1]
        if checked_text != "":
            new_nodes.append(TextNode(checked_text,TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        checked_text = old_node.text
        matches = extract_markdown_links(checked_text)
        if(len(matches) == 0 ):
            new_nodes.append(old_node)
            continue
        for match in matches:
            sections = checked_text.split(f"[{match[0]}]({match[1]})",1)
            if len(sections) != 2:
                raise Exception("invalid markdown")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0],TextType.TEXT))
            new_nodes.append(TextNode(
                    match[0],
                    TextType.LINK,
                    match[1],
                ))
            checked_text = sections[1]
        if checked_text != "":
             new_nodes.append(TextNode(checked_text,TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    #we could match it but fuck it
    
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
 
    return nodes