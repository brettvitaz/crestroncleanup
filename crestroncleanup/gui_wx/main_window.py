import os
import wx
import wx.aui


class MainWindow(wx.Frame):
    """
    Main Window contains the application.
    """
    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title, size=(800, 600))
        self.CreateStatusBar()

        # Create the menus
        file_menu = wx.Menu()

        self.Bind(wx.EVT_MENU, self.on_open, file_menu.Append(wx.ID_OPEN, '&Open\tCtrl+O', 'Open a file'))
        file_menu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.on_exit, file_menu.Append(wx.ID_EXIT, 'E&xit', 'Close the program'))

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, '&File')
        self.SetMenuBar(menu_bar)

        # Create the file panel
        self.file_panel = FilePanel(self)

        self.Show(True)

    def on_open(self, event):
        """
        Show an open file dialog to select the file.
        :param event: Menu event.
        """
        dlg = wx.FileDialog(self, 'Choose a file', '', '', '*.smw', wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            self.file_panel.file_note_book.add_file(dirname, filename)
            wx.CallAfter(self.file_panel.file_note_book.SendSizeEvent)
        dlg.Destroy()

    def on_exit(self, event):
        """
        Exit the app.
        :param event: Menu event.
        """
        self.Close(True)


class FilePanel(wx.Panel):
    """
    File Panel contains the File Note Book.
    """
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.file_note_book = FileNoteBook(self)
        sizer = wx.BoxSizer()
        sizer.Add(self.file_note_book, 1, wx.EXPAND)
        self.SetSizer(sizer)
        wx.CallAfter(self.file_note_book.SendSizeEvent)


class FileNoteBook(wx.aui.AuiNotebook):
    """
    File Note Book contains the tabbed file views.
    """
    def __init__(self, *args, **kwargs):
        wx.aui.AuiNotebook.__init__(self, *args, **kwargs)

    def add_file(self, filepath, filename):
        """
        Add a file page to the file note book.
        :param filepath: Name of directory path containing the file.
        :param filename: Name of the file.
        """
        file_page = FilePage(filepath, filename, self)
        self.AddPage(file_page, filename)


class FilePage(wx.Panel):
    """
    File Page contains the controls to interact with the file.
    """
    def __init__(self, filepath, filename, *args, **kwargs):
        """
        :param filepath: Name of directory path containing the file.
        :param filename: Name of the file.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        text_box = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE)
        sizer = wx.BoxSizer()
        sizer.Add(text_box, 1, wx.EXPAND)
        self.SetSizer(sizer)

        with open(os.path.join(filepath, filename)) as f:
            text_box.SetValue(f.read())


def main():
    gui = wx.App(False)
    MainWindow(None, 'Crestron Cleanup')
    gui.MainLoop()


if __name__ == '__main__':
    main()
