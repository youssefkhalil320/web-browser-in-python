import tkinter
import tkinter.font
from Text import Text
from utilities import HSTEP, VSTEP, PARAGRAPH_GAP


class Layout:
    def __init__(self, tokens, width=800):
        self.display_list = []
        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.WIDTH = width
        for tok in tokens:
            self.token(tok)

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

    def word(self, word):
        font = tkinter.font.Font(
            size=16,
            weight=self.weight,
            slant=self.style,
        )
        w = font.measure(word)
        space_width = font.measure(" ")

        if word == '\n':
            self.cursor_y += PARAGRAPH_GAP
            self.cursor_x = HSTEP
        elif self.cursor_x + w > self.WIDTH - HSTEP:
            self.cursor_y += font.metrics("linespace") * 1.25
            self.cursor_x = HSTEP
            self.display_list.append(
                (self.cursor_x, self.cursor_y, word, font))
            self.cursor_x += w + space_width
        else:
            self.display_list.append(
                (self.cursor_x, self.cursor_y, word, font))
            self.cursor_x += w + space_width
