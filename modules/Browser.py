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
        # Bind to the Configure event
        self.window.bind("<Configure>", self.on_resize)

    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + self.canvas.winfo_height():
                continue
            if y + VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c)
        self.update_scroll_region()
        self.update_scrollbar_position()  # Update scrollbar position after drawing

    def load(self, url):
        body = url.request()
        text = show(body)
        self.display_list = layout(
            text, self.canvas.winfo_width())  # Pass width for layout
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
            fraction = float(args[1])
            content_height = max(
                y for x, y, c in self.display_list) if self.display_list else self.canvas.winfo_height()
            self.scroll = int(fraction * content_height)
        elif args[0] == 'scroll':
            self.scroll += int(args[1]) * SCROLL_STEP

        # Update scrollbar position based on self.scroll
        content_height = max(
            y for x, y, c in self.display_list) if self.display_list else self.canvas.winfo_height()
        self.scrollbar.set(self.scroll / content_height,
                           (self.scroll + self.canvas.winfo_height()) / content_height)

        # Update canvas display
        self.draw()

    def update_scroll_region(self):
        content_height = max(
            y for x, y, c in self.display_list) if self.display_list else 0
        self.canvas.config(scrollregion=(
            0, 0, self.canvas.winfo_width(), content_height))

    def update_scrollbar_position(self):
        content_height = max(
            y for x, y, c in self.display_list) if self.display_list else self.canvas.winfo_height()
        self.scrollbar.set(self.scroll / content_height,
                           (self.scroll + self.canvas.winfo_height()) / content_height)

    def on_resize(self, event):
        body = URL(sys.argv[1]).request()
        text = show(body)
        # Re-layout with new width
        self.display_list = layout(text, event.width)
        self.update_scroll_region()
        self.draw()


if __name__ == "__main__":
    import sys
    browser = Browser()
    browser.load(URL(sys.argv[1]))
    tkinter.mainloop()
