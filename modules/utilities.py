import tkinter.font
from Text import Text
from Tag import Tag

WIDTH = 800
HEIGHT = 600
HSTEP, VSTEP = 13, 18
PARAGRAPH_GAP = 2 * VSTEP


def show(body):
    out = []
    buffer = ""
    in_tag = False
    entity_buffer = ""

    for c in body:
        if c == "<":
            in_tag = True
            if buffer:
                out.append(Text(buffer))
                buffer = ""
            if entity_buffer:
                out.append(Text(entity_buffer))
                entity_buffer = ""
            buffer += c
        elif c == ">":
            in_tag = False
            buffer += c
            out.append(Tag(buffer))
            buffer = ""
        elif not in_tag:
            if c == "&":
                entity_buffer += c
            elif entity_buffer:
                entity_buffer += c
                if entity_buffer == "&lt;":
                    out.append(Text("<"))
                    entity_buffer = ""
                elif entity_buffer == "&gt;":
                    out.append(Text(">"))
                    entity_buffer = ""
                elif entity_buffer == "&amp;":
                    out.append(Text("&"))
                    entity_buffer = ""
                elif len(entity_buffer) > 4 and not entity_buffer.startswith("&lt") and not entity_buffer.startswith("&gt") and not entity_buffer.startswith("&amp"):
                    out.append(Text(entity_buffer))
                    entity_buffer = ""
            else:
                buffer += c
        else:
            buffer += c

    if buffer:
        if in_tag:
            out.append(Tag(buffer))
        else:
            out.append(Text(buffer))

    if entity_buffer:
        out.append(Text(entity_buffer))

    return out


def layout(tokens, width):
    font = tkinter.font.Font()
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    weight = "normal"
    style = "roman"
    for tok in tokens:
        if isinstance(tok, Text):
            for word in tok.text.split():
                font = tkinter.font.Font(
                    size=16,
                    weight=weight,
                    slant=style,
                )
                w = font.measure(word)
                if word == '\n':
                    cursor_y += PARAGRAPH_GAP
                    cursor_x = HSTEP
                else:
                    display_list.append((cursor_x, cursor_y, word, font))
                    cursor_x += w + font.measure(" ")
                    if cursor_x + w > WIDTH - HSTEP:
                        cursor_y += font.metrics("linespace") * 1.25
                        cursor_x = HSTEP
        elif tok.tag == "i":
            style = "italic"
        elif tok.tag == "/i":
            style = "roman"
        elif tok.tag == "b":
            weight = "bold"
        elif tok.tag == "/b":
            weight = "normal"
    return display_list
