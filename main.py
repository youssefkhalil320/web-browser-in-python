from modules.URL import URL
from modules.Browser import Browser
import sys
import tkinter


if __name__ == "__main__":
    # print(load(URL(sys.argv[1])))
    browser = Browser()
    if len(sys.argv) > 1:
        browser.load(URL(sys.argv[1]))
    tkinter.mainloop()
