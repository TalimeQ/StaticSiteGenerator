from enum import Enum

class TextType(Enum):
    NORMAL = "Normal"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINK = "Link"
    IMAGE = "Image"

class TextNode:
    def __init__(self,text,text_type,url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, value):
        return self.text == value.text and self.url == value.url and self.text_type == value.text_type
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
