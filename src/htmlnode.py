
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag, self.value, self.children, self.props = tag,value,children,props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return str(map(lambda prop: f" {prop}=\"{self.props[prop]}\"", self.props))

    def __repr__(self):
        return f"Tag:{self.tag}\nValue:{self.value}\nChildren:{self.children}\nProps:{self.props}"