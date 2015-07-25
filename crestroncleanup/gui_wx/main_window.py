import os
import wx
import wx.aui

import embedded_graphics_16 as eg


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
        dlg = wx.FileDialog(self, 'Choose a file', '', '', '*.smw', wx.OPEN)
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


class FilePanel(wx.Panel):
    """
    File Panel contains the File Note Book.
    """

    def __init__(self, *args, **kwargs):
        super(FilePanel, self).__init__(*args, **kwargs)
        self.file_notebook = FileNoteBook(self)
        sizer = wx.BoxSizer()
        sizer.Add(self.file_notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)
        wx.CallAfter(self.file_notebook.SendSizeEvent)


class FileNoteBook(wx.aui.AuiNotebook):
    """
    File Note Book contains the tabbed file views.
    """

    def __init__(self, *args, **kwargs):
        super(FileNoteBook, self).__init__(*args, **kwargs)

    def add_file(self, filepath, filename):
        """
        Add a file page to the file notebook.
        :param filepath: Name of directory path containing the file.
        :param filename: Name of the file.
        """
        file_page = FilePage(filepath, filename, self)
        self.AddPage(file_page, filename)


class FilePage(wx.Panel):
    """
    File Page contains the controls to interact with the file.
    """

    TBFLAGS = (wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)

    def __init__(self, filepath, filename, *args, **kwargs):
        """
        :param filepath: Name of directory path containing the file.
        :param filename: Name of the file.
        """
        super(FilePage, self).__init__(*args, **kwargs)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self._create_toolbar(), 0, wx.EXPAND)

        text_box = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE)

        sizer = wx.BoxSizer()
        sizer.Add(text_box, 1, wx.EXPAND)
        main_sizer.Add(sizer, 1, wx.EXPAND)
        self.SetSizer(main_sizer)

        with open(os.path.join(filepath, filename)) as f:
            text_box.SetValue(f.read())

    def _create_toolbar(self):
        # Draw the toolbar
        toolbar = wx.ToolBar(self, style=self.TBFLAGS)
        toolbar.SetMargins((4, 4))
        toolbar.SetToolSeparation(32)

        # Save Button
        toolbar.AddLabelTool(wx.ID_SAVE, 'Save', eg.GetBitmap_save_png(), shortHelp='Save the file')
        self.Bind(wx.EVT_TOOL, self._on_save, id=wx.ID_SAVE)

        toolbar.AddSeparator()

        # Process Button
        toolbar.AddSimpleTool(wx.ID_CONVERT, eg.GetBitmap_play_png(), shortHelpString='Process file')
        self.Bind(wx.EVT_TOOL, self._on_process, id=wx.ID_CONVERT)

        toolbar.AddSeparator()

        # Settings Button
        toolbar.AddSimpleTool(wx.ID_SETUP, eg.GetBitmap_cog_png(), shortHelpString='Change file settings')
        self.Bind(wx.EVT_TOOL, self._on_settings, id=wx.ID_SETUP)

        toolbar.AddStretchableSpace()

        # Pacman Button
        toolbar.AddSimpleTool(wx.ID_ANY, eg.GetBitmap_pacman_png(), shortHelpString='Pacman')
        self.Bind(wx.EVT_TOOL, self._on_pacman, id=wx.ID_SETUP)

        toolbar.Realize()
        return toolbar

    def _on_save(self, event):
        pass

    def _on_settings(self, event):
        pass

    def _on_process(self, event):
        pass

    def _on_pacman(self, event):
        pass
