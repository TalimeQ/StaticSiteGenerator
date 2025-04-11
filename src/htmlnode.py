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
            raise ValueError("No value for leaf node")
        if self.tag == None:
            return self.value
        
        html_text = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_text

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props = None):
        super().__init__(tag,None,children,props)

    def to_html(self):
        #check if we should exit
        if self.tag == None:
            raise ValueError("No tag for parent node")
        if self.children == None:
            raise ValueError("Children provided for parent node have no value")

        parent_string = f"<{self.tag}>"  
        for child in self.children:
            parent_string += child.to_html()
        
        return parent_string + f"</{self.tag}>"
