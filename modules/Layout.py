import tkinter
import tkinter.font
from .Text import Text
from .utilities import HSTEP, VSTEP, PARAGRAPH_GAP, get_font, WIDTH


def get_fixed_width_font(size, weight, style):
    return tkinter.font.Font(family="Courier New", size=size, weight=weight, slant=style)


class Layout:
    def __init__(self, tree, width=WIDTH):
        self.display_list = []
        self.width = width
        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.size = 12

        self.line = []
        self.recurse(tree)
        self.flush()

    def token(self, tok): pass

    def recurse(self, tree):
        if isinstance(tree, Text):
            for word in tree.text.split():
                self.word(word)
        else:
            self.open_tag(tree.tag)
            for child in tree.children:
                self.recurse(child)
            self.close_tag(tree.tag)

    def open_tag(self, tag):
        if tag == "i":
            self.style = "italic"
        elif tag == "b":
            self.weight = "bold"
        elif tag == "small":
            self.size -= 2
        elif tag == "big":
            self.size += 4
        elif tag == "br":
            self.flush()

    def close_tag(self, tag):
        if tag == "i":
            self.style = "roman"
        elif tag == "b":
            self.weight = "normal"
        elif tag == "small":
            self.size += 2
        elif tag == "big":
            self.size -= 4
        elif tag == "p":
            self.flush()
            self.cursor_y += VSTEP
