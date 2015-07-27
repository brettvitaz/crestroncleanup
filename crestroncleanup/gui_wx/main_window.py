import wx
import wx.aui

from crestroncleanup.gui_wx.file_panel import FilePanel


class MainWindow(wx.Frame):
    """
    Main Window contains the application.
    """

    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title, size=(800, 600))
        self.CreateStatusBar()

        # Create the menus
        file_menu = wx.Menu()

        # Open menu item
        self.open_item = file_menu.Append(wx.ID_OPEN, '&Open\tCtrl+O', 'Open a file')
        self.Bind(wx.EVT_MENU, self._on_open, self.open_item)

        # Close menu item
        self.close_item = file_menu.Append(wx.ID_CLOSE, '&Close\tCtrl+W', 'Close current file')
        self.close_item.Enable(False)
        self.Bind(wx.EVT_MENU, self._on_close, self.close_item)

        file_menu.AppendSeparator()

        # Exit menu item
        self.exit_item = file_menu.Append(wx.ID_EXIT, 'E&xit', 'Close the program')
        self.Bind(wx.EVT_MENU, self._on_exit, self.exit_item)

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, '&File')
        self.SetMenuBar(menu_bar)

        # Create the file panel
        self.file_panel = FilePanel(self)

        # Handle page events to update close menu item enabled state
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self._on_page_changed, self.file_panel.file_notebook)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self._on_page_closed, self.file_panel.file_notebook)

        self.Show(True)

    def _on_open(self, event):
        """
        Show an open file dialog to select the file.
        :param event: Menu event.
        """
        dlg = wx.FileDialog(self, 'Open Crestron SIMPL file', '', '', 'Crestron SIMPL files (*.smw)|*.smw',
                            (wx.FD_OPEN | wx.FD_FILE_MUST_EXIST))
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            filepath = dlg.GetDirectory()
            self.file_panel.file_notebook.add_file(filepath, filename)
            wx.CallAfter(self.file_panel.file_notebook.SendSizeEvent)
        dlg.Destroy()

    def _on_exit(self, event):
        """
        Exit the app.
        :param event: Menu event.
        """
        self.Close(True)

    def _on_close(self, event):
        """
        Close the currently opened notebook page
        :param event:
        :return:
        """
        page = self.file_panel.file_notebook.GetSelection()
        self.file_panel.file_notebook.DeletePage(page)
        # This is a workaround because AuiNotebook doesn't post events when pages are deleted programmatically.
        self.close_item.Enable(self.file_panel.file_notebook.PageCount > 0)

    def _on_page_changed(self, event):
        """
        :type event: wx.aui.AuiNotebookEvent
        """
        # Update Close menu item enabled state.
        self.close_item.Enable(event.EventObject.PageCount > 0)

    def _on_page_closed(self, event):
        """
        :type event: wx.aui.AuiNotebookEvent
        """
        # Update Close menu item enabled state.
        self.close_item.Enable(event.EventObject.PageCount > 0)
