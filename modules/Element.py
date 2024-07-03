class Element:
    def __init__(self, tag, attributes, parent):
        self.tag = tag
        self.attributes = attributes
        self.children = []
        self.parent = parent

    def __repr__(self):
        attrs = [" " + k + "=\"" + v + "\"" for k,
                 v in self.attributes.items()]
        attr_str = ""
        for attr in attrs:
            attr_str += attr
        return "<" + self.tag + attr_str + ">"
