import sys
import crestroncleanup_console
import crestroncleanup_gui

if __name__ == '__main__':
    if len(sys.argv) > 1:
        crestroncleanup_console.main()
    else:
        crestroncleanup_gui.main()
