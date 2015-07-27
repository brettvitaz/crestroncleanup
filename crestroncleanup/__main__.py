import sys

from crestroncleanup import crestroncleanup_console
from crestroncleanup import crestroncleanup_gui


def main():
    if len(sys.argv) > 1:
        crestroncleanup_console.main()
    else:
        crestroncleanup_gui.main()


if __name__ == '__main__':
    main()
