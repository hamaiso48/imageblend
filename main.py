import wx._adv
import wx._html
import wx
import os

from wx.core import ID_ANY
import backend
import convertimage

class BlueFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, files):
        self.window.blue_entry.SetLabel(files[0])
        return 0

class RedFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, files):
        self.window.red_entry.SetLabel(files[0])
        return 0

class App(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(500,300), style=wx.DEFAULT_FRAME_STYLE)

        # ステータスバーの初期化
        self.CreateStatusBar()
        self.SetStatusText('')
        self.GetStatusBar().SetBackgroundColour(None)

        panel = wx.Panel(self, wx.ID_ANY)

        ### 赤パネル ###
        red_label = wx.StaticText(panel, wx.ID_ANY, 'ここにファイルをドロップしてください', style=wx.SIMPLE_BORDER | wx.TE_CENTER, size=(30,30))
        red_label.SetBackgroundColour("#fa8794")
        ### 青パネル ###
        blue_label = wx.StaticText(panel, wx.ID_ANY, 'ここにファイルをドロップしてください', style=wx.SIMPLE_BORDER | wx.TE_CENTER, size=(30,30))
        blue_label.SetBackgroundColour("#87cefa")
        # ドロップ対象の設定
        red_label.SetDropTarget(RedFileDropTarget(self))
        blue_label.SetDropTarget(BlueFileDropTarget(self))

        # テキスト入力ウィジット
        self.red_entry = wx.TextCtrl(panel, wx.ID_ANY)
        self.red_entry.SetForegroundColour("#e60000")
        self.blue_entry = wx.TextCtrl(panel, wx.ID_ANY)
        self.blue_entry.SetForegroundColour("#006ae6")

        # プレビュー or ファイル出力 のラジオボタン
        button_array = ('プレビュー表示', 'ファイル出力')
        self.radio_outputmode = wx.RadioBox(panel, wx.ID_ANY, '', choices=button_array, style=wx.RA_HORIZONTAL)

        # 初期表示時はプレビューを選択しておく
        self.radio_outputmode.SetSelection(0)

        # 実行ボタン
        button_execute = wx.Button(panel, wx.ID_ANY, '実行')
        button_execute.Bind(wx.EVT_BUTTON, self.click_button_execute)

        # レイアウト
        layout_outputmode = wx.BoxSizer(wx.HORIZONTAL)
        layout_outputmode.Add(self.radio_outputmode, flag=wx.EXPAND)

        layout = wx.GridSizer(6, 1, 0, 0)
        layout.Add(red_label         , flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        layout.Add(self.red_entry    , flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        layout.Add(blue_label        , flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        layout.Add(self.blue_entry   , flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        layout.Add(layout_outputmode , flag=wx.ALIGN_CENTER)
        layout.Add(button_execute    , flag=wx.EXPAND | wx.ALL, border=7)
        panel.SetSizer(layout)

        self.Show()

    def click_button_execute(self, event):
        self.SetStatusText('実行中')
        blue_path = self.blue_entry.GetValue()
        red_path = self.red_entry.GetValue()
        image_blue_path = convertimage.main(blue_path)
        image_red_path  = convertimage.main(red_path)
        filename = os.path.basename(red_path)
        backend.main(image_red_path, image_blue_path, filename, self.radio_outputmode.GetSelection())
        self.SetStatusText('')

app = wx.App()
App(None, -1, 'イメージブレンド')
app.MainLoop()
