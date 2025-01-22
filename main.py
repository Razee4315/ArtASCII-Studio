import sys
from gui import main as gui_main
from cli import main as cli_main

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_main()
    else:
        gui_main()
