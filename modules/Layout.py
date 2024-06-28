import tkinter
import tkinter.font
from Text import Text
from utilities import HSTEP, VSTEP, PARAGRAPH_GAP, get_font


class Layout:
    def __init__(self, tokens, width=800):
        self.display_list = []
        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.WIDTH = width
        self.size = 12
        self.line = []
        self.centered = False  # Flag to indicate centered text
        for tok in tokens:
            self.token(tok)
        self.flush()

    def token(self, tok):
        if isinstance(tok, Text):
            for word in tok.text.split():
                self.word(word)
        elif tok.tag == "i":
            self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b":
            self.weight = "bold"
        elif tok.tag == "/b":
            self.weight = "normal"
        elif tok.tag == "small":
            self.size -= 2
        elif tok.tag == "/small":
            self.size += 2
        elif tok.tag == "big":
            self.size += 4
        elif tok.tag == "/big":
            self.size -= 4
        elif tok.tag == "br":
            self.flush()
            self.cursor_y += tkinter.font.Font(
                size=self.size).metrics("linespace")
        elif tok.tag == "/p":
            self.flush()
            self.cursor_y += VSTEP + PARAGRAPH_GAP
        elif tok.tag == "h1" and "class=title" in tok.tag:
            self.centered = True
            self.size = 24  # Adjust size for h1 title
        elif tok.tag == "/h1":
            self.centered = False
            self.size = 12  # Reset size after h1 title

    def word(self, word):
        font = get_font(self.size, self.weight, self.style)
        w = font.measure(word)
        space_width = font.measure(" ")

        if self.cursor_x + w > self.WIDTH - HSTEP:
            self.flush()
            self.cursor_y += font.metrics("linespace") * 1.25
            self.cursor_x = HSTEP

        self.line.append((self.cursor_x, word, font))
        self.cursor_x += w + space_width

    def flush(self):
        if not self.line:
            return

        metrics = [font.metrics() for x, word, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + max_ascent

        # Calculate line width for centering
        line_width = sum(font.measure(word) for x, word, font in self.line) + \
            (len(self.line) - 1) * self.line[0][2].measure(" ")
        if self.centered:
            offset_x = (self.WIDTH - line_width) / 2
        else:
            offset_x = 0

        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x + offset_x, y, word, font))

        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + max_descent
        self.cursor_x = HSTEP
        self.line = []
