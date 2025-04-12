from enum import Enum
from htmlnode import *
from helpers import *

class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH",
    HEADING = "HEADING",
    CODE = "CODE"
    QUOTE = "QUOTE"
    ULIST = "UNORDERED_LIST"
    OLIST = "ORDERED_LIST"


def markdown_to_blocks(markdown):
    sections = markdown.split("\n\n")
    cleared_sections = []
    for section in sections:
        subsections = section.split("\n")
        merged = ""
        for subsection in subsections:
            stripped = subsection.strip()
            if merged == "" and stripped != "":
                merged += stripped
            elif stripped != "":
                merged += f"\n{stripped}"
        cleared_sections.append(merged)
    
    return cleared_sections

def block_to_block_type(markdown_text_block):
    lines = markdown_text_block.split("\n")
    
    if markdown_text_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    
    if markdown_text_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.HEADING
        return BlockType.QUOTE

    if markdown_text_block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.HEADING
        return BlockType.ULIST
    
    if markdown_text_block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.HEADING
            i += 1
        return BlockType.OLIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    split_blocks = markdown_to_blocks(markdown)
    children = []
    for block in split_blocks:
        if block == "":
           continue
        html_node = block_to_html_node(block)
        children.append(html_node)      
    return ParentNode("div", children,None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        nodes.append(html_node)
    return nodes

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode("p", children)

def code_to_html_node(block):
    text = block[4:-3]
    text_node = TextNode(text,TextType.CODE)
    html_node = text_node_to_html_node(text_node)
    return ParentNode("pre",[html_node])

def olist_to_html_node(block):
    lines = block.split("\n")
    html_nodes = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)   
        html_nodes.append(ParentNode("li",children))
    return ParentNode("ol",html_nodes)

def ulist_to_html_node(block):
    lines = block.split("\n")
    html_nodes = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)   
        html_nodes.append(ParentNode("li",children))
    return ParentNode("ul",html_nodes)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    text = " ".join(new_lines)
    children = text_to_children(text)   
    return ParentNode("blockquote",children)