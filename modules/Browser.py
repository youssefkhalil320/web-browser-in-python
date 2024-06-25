import tkinter
from utilities import show, layout, WIDTH, HEIGHT, VSTEP, HSTEP
from URL import URL

SCROLL_STEP = 100


class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Simple Browser")
        self.window.geometry(f"{WIDTH}x{HEIGHT}")

        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()
        self.scroll = 0

        self.window.bind("<Down>", self.scroll_down)
        self.window.bind("<Up>", self.scroll_up)
        self.window.bind("<MouseWheel>", self.on_mouse_wheel)
        self.window.bind("<Button-4>", self.on_mouse_wheel_linux)
        self.window.bind("<Button-5>", self.on_mouse_wheel_linux)

    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + HEIGHT:
                continue
            if y + VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c)

    def load(self, url):
        body = url.request()
        text = show(body)
        self.display_list = layout(text)
        self.draw()

    def scroll_down(self, e):
        self.scroll += SCROLL_STEP
        self.draw()

    def scroll_up(self, e):
        self.scroll -= SCROLL_STEP
        if self.scroll < 0:
            self.scroll = 0
        self.draw()

    def on_mouse_wheel(self, e):
        if e.delta < 0:
            self.scroll_down(e)
        else:
            self.scroll_up(e)

    def on_mouse_wheel_linux(self, e):
        if e.num == 5:
            self.scroll_down(e)
        elif e.num == 4:
            self.scroll_up(e)


if __name__ == "__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()
