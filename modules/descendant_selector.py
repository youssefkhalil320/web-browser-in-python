from .wbetools import js_hide


class DescendantSelector:
    def __init__(self, ancestor, descendant):
        self.ancestor = ancestor
        self.descendant = descendant
        self.priority = ancestor.priority + descendant.priority

    def matches(self, node):
        if not self.descendant.matches(node):
            return False
        while node.parent:
            if self.ancestor.matches(node.parent):
                return True
            node = node.parent
        return False

    @js_hide
    def __repr__(self):
        return ("DescendantSelector(ancestor={}, descendant={}, priority={})") \
            .format(self.ancestor, self.descendant, self.priority)
