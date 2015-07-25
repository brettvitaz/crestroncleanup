import os
import wx
import wx.aui

from gui_wx import embedded_graphics_16 as eg


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
