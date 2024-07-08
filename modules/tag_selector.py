from .wbetools import js_hide
from .Element import Element


class TagSelector:
    def __init__(self, tag):
        self.tag = tag
        self.priority = 1

    def matches(self, node):
        return isinstance(node, Element) and self.tag == node.tag

    @js_hide
    def __repr__(self):
        return "TagSelector(tag={}, priority={})".format(
            self.tag, self.priority)
