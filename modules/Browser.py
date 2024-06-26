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

        self.scrollbar = tkinter.Scrollbar(
            self.window, orient=tkinter.VERTICAL, command=self.on_scroll
        )
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.scroll = 0
        self.window.bind("<Down>", self.scroll_down)
        self.window.bind("<Up>", self.scroll_up)
        # Windows and MacOS
        self.window.bind("<MouseWheel>", self.on_mouse_wheel)
        # Linux scroll up
        self.window.bind("<Button-4>", self.on_mouse_wheel_linux)
        # Linux scroll down
        self.window.bind("<Button-5>", self.on_mouse_wheel_linux)

    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + HEIGHT:
                continue
            if y + VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c)
        self.update_scroll_region()

    def load(self, url):
        body = url.request()
        text = show(body)
        self.display_list = layout(text)
        self.update_scroll_region()
        self.draw()

    def scroll_down(self, e=None):
        self.scroll += SCROLL_STEP
        self.update_scroll_region()
        self.draw()

    def scroll_up(self, e=None):
        self.scroll -= SCROLL_STEP
        if self.scroll < 0:
            self.scroll = 0
        self.update_scroll_region()
        self.draw()

    def on_mouse_wheel(self, e):
        if e.delta < 0:
            self.scroll_down()
        else:
            self.scroll_up()

    def on_mouse_wheel_linux(self, e):
        if e.num == 5:
            self.scroll_down()
        elif e.num == 4:
            self.scroll_up()

    def on_scroll(self, *args):
        if args[0] == 'moveto':
            self.scroll = float(args[1]) * self.canvas.bbox('all')[3]
        elif args[0] == 'scroll':
            self.scroll += int(args[1]) * SCROLL_STEP
        self.draw()

    def update_scroll_region(self):
        content_height = max(
            y for x, y, c in self.display_list) if self.display_list else 0
        self.canvas.config(scrollregion=(0, 0, WIDTH, content_height))


if __name__ == "__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()
