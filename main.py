from modules.URL import URL
from modules.Browser import Browser
from modules.HTMLParser import HTMLParser
from modules.utilities import print_tree
import sys
import tkinter


if __name__ == "__main__":
    # print(load(URL(sys.argv[1])))
    # browser = Browser()
    # if len(sys.argv) > 1:
    #     browser.load(URL(sys.argv[1]))
    # tkinter.mainloop()
    body = URL(sys.argv[1]).request()
    nodes = HTMLParser(body).parse()
    print_tree(nodes)
    # print tree test
