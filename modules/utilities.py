import tkinter.font
from modules.Text import Text
from modules.Element import Element
from .wbetools import patchable


WIDTH = 800
HEIGHT = 600
HSTEP, VSTEP = 13, 18
PARAGRAPH_GAP = 2 * VSTEP
FONTS = {}


def show(body):
    out = []
    buffer = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
            if buffer:
                out.append(Text(buffer.replace("&shy;", "\u00AD")))
            buffer = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(buffer))
            buffer = ""
        else:
            buffer += c
    if not in_tag and buffer:
        out.append(Text(buffer.replace("&shy;", "\u00AD")))

    return out


def get_font(size, weight, style):
    key = (size, weight, style)
    if key not in FONTS:
        font = tkinter.font.Font(size=size, weight=weight,
                                 slant=style)
        label = tkinter.Label(font=font)
        FONTS[key] = (font, label)
    return FONTS[key][0]


@patchable
def paint_tree(layout_object, display_list):
    display_list.extend(layout_object.paint())

    for child in layout_object.children:
        paint_tree(child, display_list)


if __name__ == "__main__":
    tt = Text("dd")
