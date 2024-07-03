from .Layout import Layout
from .wbetools import record, js_hide
from .BlockLayout import BlockLayout
from .utilities import WIDTH, VSTEP, HSTEP


class DocumentLayout:
    def __init__(self, node, width=WIDTH):
        self.node = node
        self.parent = None
        self.previous = None
        self.children = []
        self.width = width

    def layout(self, width=None):
        if width:
            self.width = width
        record("layout_pre", self)
        child = BlockLayout(self.node, self, None, self.width)
        self.children.append(child)

        self.x = HSTEP
        self.y = VSTEP
        child.layout()
        self.height = child.height
        record("layout_post", self)

    def paint(self):
        return []

    @js_hide
    def __repr__(self):
        return "DocumentLayout()"
