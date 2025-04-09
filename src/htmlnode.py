class HTMLNode:
    def __init__(self,tag = None,value = None ,children = None,props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        
        string = ""
        for key in self.props:
            string += " " + key +"=\"" + self.props[key] + "\""
        return string

    def __repr__(self):
        return f"HTMLNODE({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self,tag,value,props = None):
       super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        
        html_text = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_text
