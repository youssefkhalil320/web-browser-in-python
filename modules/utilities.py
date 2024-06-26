WIDTH = 800
HEIGHT = 600
HSTEP, VSTEP = 13, 18
PARAGRAPH_GAP = 2 * VSTEP


def show(body):
    in_tag = False
    entity_buffer = ""
    output = []

    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False

        if not in_tag:
            if c == "&":
                entity_buffer += c
            elif entity_buffer:
                entity_buffer += c
                if entity_buffer == "&lt;":
                    output.append("<")
                    entity_buffer = ""
                elif entity_buffer == "&gt;":
                    output.append(">")
                    entity_buffer = ""
                elif entity_buffer == "&amp;":
                    output.append("&")
                    entity_buffer = ""
                elif len(entity_buffer) > 4 and not entity_buffer.startswith("&lt") and not entity_buffer.startswith("&gt") and not entity_buffer.startswith("&amp"):
                    output.append(entity_buffer)
                    entity_buffer = ""
            else:
                output.append(c)
        else:
            output.append(c)

    return ''.join(output)


def layout(text, width):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        if c == '\n':
            cursor_y += PARAGRAPH_GAP
            cursor_x = HSTEP
        else:
            display_list.append((cursor_x, cursor_y, c))
            cursor_x += HSTEP
            if cursor_x >= width - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP
    return display_list
