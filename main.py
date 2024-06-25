from modules.URL import URL
from modules.utilities import load
import sys


if __name__ == "__main__":
    print(load(URL(sys.argv[1])))
