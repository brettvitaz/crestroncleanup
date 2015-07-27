import wx

from crestroncleanup.gui_wx import main_window


def main():
    gui = wx.App(False)
    main_window.MainWindow(None, 'Crestron Cleanup')
    gui.MainLoop()


if __name__ == '__main__':
    main()
