import tkinter
import tkinter.font
from .Text import Text
from .utilities import HSTEP, VSTEP, PARAGRAPH_GAP, get_font


def get_fixed_width_font(size, weight, style):
    return tkinter.font.Font(family="Courier New", size=size, weight=weight, slant=style)


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
        self.superscript = False  # Flag for superscript
        self.normal_size = self.size  # Store normal size for resetting after superscript
        self.in_pre = False  # Flag for preformatted text
        self.in_abbr = False  # Flag for abbr
        for tok in tokens:
            self.token(tok)
        self.flush()

    def token(self, tok):
        if isinstance(tok, Text):
            if self.in_pre:
                self.preformatted_text(tok.text)
            else:
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
        elif tok.tag == "sup":
            self.superscript = True
            self.size = self.normal_size // 2  # Make text smaller
        elif tok.tag == "/sup":
            self.superscript = False
            self.size = self.normal_size  # Reset size after superscript
        elif tok.tag == "abbr":
            self.in_abbr = True
        elif tok.tag == "/abbr":
            self.in_abbr = False
        elif tok.tag == "pre":
            self.in_pre = True
        elif tok.tag == "/pre":
            self.in_pre = False

    def preformatted_text(self, text):
        font = get_fixed_width_font(self.size, self.weight, self.style)
        for line in text.split("\n"):
            if self.cursor_x + font.measure(line) > self.WIDTH - HSTEP:
                self.flush()
                self.cursor_y += font.metrics("linespace") * 1.25
                self.cursor_x = HSTEP
            self.line.append((self.cursor_x, line, font))
            self.flush()
            self.cursor_y += font.metrics("linespace")
            self.cursor_x = HSTEP

    def word(self, word):
        font = get_font(self.size, self.weight, self.style)
        parts = word.split("\u00AD")
        space_width = font.measure(" ")

        for part in parts:
            w = font.measure(part)
            if self.cursor_x + w > self.WIDTH - HSTEP:
                self.flush()
                self.cursor_y += font.metrics("linespace") * 1.25
                self.cursor_x = HSTEP

            if self.in_abbr:
                for char in part:
                    if char.islower():
                        self.line.append(
                            (self.cursor_x, char.upper(), get_font(self.size, "bold", self.style)))
                        self.cursor_x += get_font(self.size, "bold",
                                                  self.style).measure(char.upper())
                    else:
                        self.line.append((self.cursor_x, char, font))
                        self.cursor_x += font.measure(char)
                self.cursor_x += space_width
            else:
                self.line.append((self.cursor_x, part, font))
                self.cursor_x += w + space_width

            if part != parts[-1]:  # Not the last part, so append a hyphen
                hyphen_width = font.measure("-")
                if self.cursor_x + hyphen_width > self.WIDTH - HSTEP:
                    self.flush()
                    self.cursor_y += font.metrics("linespace") * 1.25
                    self.cursor_x = HSTEP

                self.line.append((self.cursor_x, "-", font))
                self.cursor_x += hyphen_width

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
            if self.superscript:
                y = self.cursor_y  # Align top of superscript with the top of normal text
            else:
                y = baseline - font.metrics("ascent")
            self.display_list.append((x + offset_x, y, word, font))

        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + max_descent
        self.cursor_x = HSTEP
        self.line = []
