# Import Python packages
import sys
# import os
# import cv2
import wx
from screeninfo import get_monitors

# Import from custom modules
from attributes_gui import set_attributes
from attributes_gui import get_subjects
from attributes_gui import ATTRIBUTES
from data_fusion_gui import data_fusion
from media_tools_gui import any2avi
from media_tools_gui import clip2frames
from media_tools_gui import clip2vid
from media_tools_gui import frames2clip
from media_tools_gui import hevc2avi
from media_tools_gui import vid2clip
from bbox_tools_gui import remove_bbox
from bbox_tools_gui import remove_bbox_v2
from bbox_tools_gui import draw_bbox
from bbox_tools_gui import id_bbox
from bbox_tools_gui import track_bbox
from bbox_tools_gui import track_bbox_v2
from bbox_tools_gui import TRACKERS
from yolo_gui import run_yolo3

version = "0.2.0"


class MainFrame(wx.Frame):
    """ Home window of the suite.

    Provides access to the different tools by clickable buttons.

    :var self.commands: dict
        Available tools and activation status.
    :var self.option: str
        Currently chosen tool.
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="Main menu - PAD suite"):
        """ Create the main frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str
            Frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(1200, 550))
        self.commands = dict(
            {"any2avi": False, "clip2frames": False, "clip2vid": False,
             "frames2clip": False, "hevc2avi": False, "vid2clip": False,
             "Bounding Box Creator": False, 
             "Bounding Box Identification": False,
             "Bounding Box Remover": False,
             "Bounding Box Remover v2": False,
             "Bounding Box Tracking": False,
             "Bounding Box Tracking v2:": False,
             "Attributes Manager": False, "Data Fusion": False,
             "Run YOLO!": False})
        self.option = "None"

        self.panel = wx.Panel(self)
        self.sizer_main = wx.BoxSizer(wx.VERTICAL)

        welcome_text = wx.StaticText(self.panel, label="Welcome to the "
                                                       "Pedestrian Awareness "
                                                       "Dataset tools suite")
        welcome_font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        welcome_text.SetFont(welcome_font)
        self.sizer_main.Add(welcome_text, 1, wx.ALIGN_CENTER | wx.ALL, 10)

        version_text = wx.StaticText(self.panel, label="version: " + version)
        version_font = wx.Font(12, wx.DEFAULT, wx.ITALIC, wx.NORMAL)
        version_text.SetFont(version_font)
        self.sizer_main.Add(version_text, 1, wx.ALIGN_CENTER | wx.DOWN, 20)

        self.sizer_logos = wx.BoxSizer(wx.HORIZONTAL)
        self.bmp_scale = 0.5
        self.frame = wx.Image("logoUAH.png", wx.BITMAP_TYPE_ANY)
        self.ratio = self.frame.GetWidth() / self.frame.GetHeight()
        self.s_frame = self.frame.Scale(self.frame.GetWidth() * self.bmp_scale,
                                        self.frame.GetHeight() * self.bmp_scale,
                                        wx.IMAGE_QUALITY_HIGH)
        self.bmp = self.s_frame.ConvertToBitmap()
        self.image = wx.StaticBitmap(self.panel, -1, self.bmp,
                                     size=(self.s_frame.GetWidth(),
                                           self.s_frame.GetHeight()))
        self.sizer_logos.Add(self.image, 1, wx.ALL | wx.CENTER, 5)

        self.frame2 = wx.Image("logoEPS.jpg", wx.BITMAP_TYPE_ANY)
        self.ratio2 = self.frame2.GetWidth() / self.frame2.GetHeight()
        self.s_frame2 = self.frame2.Scale(self.frame2.GetWidth() *
                                          self.bmp_scale,
                                          self.frame2.GetHeight() *
                                          self.bmp_scale,
                                          wx.IMAGE_QUALITY_HIGH)
        self.bmp2 = self.s_frame2.ConvertToBitmap()
        self.image2 = wx.StaticBitmap(self.panel, -1, self.bmp2,
                                      size=(self.s_frame2.GetWidth(),
                                            self.s_frame2.GetHeight()))
        self.sizer_logos.Add(self.image2, 1, wx.ALL | wx.CENTER, 5)
        self.sizer_main.Add(self.sizer_logos, 1, wx.ALL | wx.CENTER, 20)

        self.sizer_header = wx.BoxSizer(wx.HORIZONTAL)
        static_text = wx.StaticText(self.panel, label="Choose tool to use")
        self.sizer_header.Add(static_text, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)
        self.sizer_main.Add(self.sizer_header, 0, wx.ALIGN_CENTER | wx.ALL, 15)

        self.sizer_tools = wx.BoxSizer(wx.HORIZONTAL)
        self.any2avi_btn = wx.Button(self.panel, label="any2avi")
        self.any2avi_btn.Bind(wx.EVT_BUTTON, self.option_clicked)
        self.sizer_tools.Add(self.any2avi_btn, 0, wx.ALL | wx.CENTER, 10)

        self.clip2frames_btn = wx.Button(self.panel, label="clip2frames")
        self.clip2frames_btn.Bind(wx.EVT_BUTTON, self.option_clicked)
        self.sizer_tools.Add(self.clip2frames_btn, 0, wx.ALL | wx.CENTER, 10)

        self.clip2vid_btn = wx.Button(self.panel, label="clip2vid")
        self.clip2vid_btn.Bind(wx.EVT_BUTTON, self.option_clicked)
        self.sizer_tools.Add(self.clip2vid_btn, 0, wx.ALL | wx.CENTER, 10)

        self.frames2clip_btn = wx.Button(self.panel, label="frames2clip")
        self.frames2clip_btn.Bind(wx.EVT_BUTTON, self.option_clicked)
        self.sizer_tools.Add(self.frames2clip_btn, 0, wx.ALL | wx.CENTER, 10)

        self.hevc2avi_btn = wx.Button(self.panel, label="hevc2avi")
        self.hevc2avi_btn.Bind(wx.EVT_BUTTON, self.option_clicked)
        self.sizer_tools.Add(self.hevc2avi_btn, 0, wx.ALL | wx.CENTER, 10)

        self.vid2clip_btn = wx.Button(self.panel, label="vid2clip")
        self.vid2clip_btn.Bind(wx.EVT_BUTTON, self.option_clicked)
        self.sizer_tools.Add(self.vid2clip_btn, 0, wx.ALL | wx.CENTER, 10)
        self.sizer_main.Add(self.sizer_tools, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.sizer_tools2 = wx.BoxSizer(wx.HORIZONTAL)
        self.bboxdraw_btn = wx.Button(self.panel, label="Bounding Box Creator")
        self.bboxdraw_btn.Bind(wx.EVT_BUTTON, self.option_clicked)
        self.sizer_tools2.Add(self.bboxdraw_btn, 0, wx.ALL | wx.CENTER, 10)
        self.bboxid_btn = wx.Button(self.panel,
                                    label="Bounding Box Identification")
        self.bboxid_btn.Bind(wx.EVT_BUTTON, self.option_clicked)
        self.sizer_tools2.Add(self.bboxid_btn, 0, wx.ALL | wx.CENTER, 10)
        self.bboxremove_btn = wx.Button(self.panel,
                                        label="Bounding Box Remover")
        self.bboxremove_btn.Bind(wx.EVT_BUTTON, self.option_clicked)
        self.sizer_tools2.Add(self.bboxremove_btn, 0, wx.ALL | wx.CENTER, 10)
        self.bboxremove_btn2 = wx.Button(self.panel,
                                         label="Bounding Box Remover v2")
        self.bboxremove_btn2.Bind(wx.EVT_BUTTON, self.option_clicked)
        self.sizer_tools2.Add(self.bboxremove_btn2, 0, wx.ALL | wx.CENTER, 10)
        self.bboxtrack_btn = wx.Button(self.panel,
                                       label="Bounding Box Tracking")
        self.bboxtrack_btn.Bind(wx.EVT_BUTTON, self.option_clicked)
        self.sizer_tools2.Add(self.bboxtrack_btn, 0, wx.ALL | wx.CENTER, 10)
        self.bboxtrack_btn2 = wx.Button(self.panel,
                                        label="Bounding Box Tracking v2")
        self.bboxtrack_btn2.Bind(wx.EVT_BUTTON, self.option_clicked)
        self.sizer_tools2.Add(self.bboxtrack_btn2, 0, wx.ALL | wx.CENTER, 10)
        self.sizer_main.Add(self.sizer_tools2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.sizer_tools3 = wx.BoxSizer(wx.HORIZONTAL)
        self.attributes_btn = wx.Button(self.panel, label="Attributes Manager")
        self.attributes_btn.Bind(wx.EVT_BUTTON, self.option_clicked)
        self.sizer_tools3.Add(self.attributes_btn, 0, wx.ALL | wx.CENTER, 10)
        self.fusion_btn = wx.Button(self.panel, label="Data Fusion")
        self.fusion_btn.Bind(wx.EVT_BUTTON, self.option_clicked)
        self.sizer_tools3.Add(self.fusion_btn, 0, wx.ALL | wx.CENTER, 10)
        self.yolo_btn = wx.Button(self.panel, label="Run YOLO!")
        self.yolo_btn.Bind(wx.EVT_BUTTON, self.option_clicked)
        self.sizer_tools3.Add(self.yolo_btn, 0, wx.ALL | wx.CENTER, 10)
        self.sizer_main.Add(self.sizer_tools3, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.panel.SetSizer(self.sizer_main)
        self.Show()

    def option_clicked(self, event):
        """ Handle method triggered when a button is pressed.

        The corresponding tool is launched, without closing the main window.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.option = event.GetEventObject().GetLabel()
        for element in self.commands.keys():
            self.commands[element] = False
        self.commands[self.option] = True
        print(f"\n[INFO] Launching {self.option}... \n")
        if self.option == self.clip2frames_btn.Label:
            Clip2framesFrame(mainMenu, wx.ID_ANY, "clip2frames - PAD suite")
        elif self.option == self.clip2vid_btn.Label:
            Clip2vidFrame(mainMenu, wx.ID_ANY, "clip2vid - PAD suite")
        elif self.option == self.frames2clip_btn.Label:
            Frames2clipFrame(None, wx.ID_ANY, "frames2clip - PAD suite")
        elif self.option == self.hevc2avi_btn.Label:
            HEVC2AVIFrame(mainMenu, wx.ID_ANY, "hevc2avi - PAD suite")
        elif self.option == self.any2avi_btn.Label:
            Any2AVIFrame(mainMenu, wx.ID_ANY, "any2avi - PAD suite")
        elif self.option == self.vid2clip_btn.Label:
            Vid2clipFrame(mainMenu, wx.ID_ANY, "vid2clip - PAD suite")
        elif self.option == self.bboxdraw_btn.Label:
            BboxesDrawFrame(None, wx.ID_ANY, "Bounding Box Creator - PAD suite")
        elif self.option == self.bboxremove_btn.Label:
            BboxesRemoveFrame(None, wx.ID_ANY, "Bounding Box Remover "
                                               "- PAD suite")
        elif self.option == self.bboxremove_btn2.Label:
            BboxesRemove2SetUpFrame(None, wx.ID_ANY, "Bounding Box Remover v2"
                                                     "- PAD suite")
        elif self.option == self.bboxid_btn.Label:
            BboxesIdSetUpFrame(mainMenu, wx.ID_ANY,
                               "Bounding Box Identification - PAD suite")
        elif self.option == self.bboxtrack_btn.Label:
            BboxesTrackFrame(None, wx.ID_ANY, "Bounding Box Tracking"
                                              " - PAD suite")
        elif self.option == self.bboxtrack_btn2.Label:
            BboxesTrack2Frame(None, wx.ID_ANY, "Bounding Box Tracking v2"
                                              " - PAD suite")
        elif self.option == self.attributes_btn.Label:
            AttributesSetUpFrame(mainMenu, wx.ID_ANY, "Attributes Manager"
                                                      " - PAD suite")
        elif self.option == self.fusion_btn.Label:
            DataFusionFrame(mainMenu, wx.ID_ANY, "Data Fusion - PAD suite")
        elif self.option == self.yolo_btn.Label:
            YOLOFrame(None, wx.ID_ANY, "YOLO! - PAD suite")


class Any2AVIFrame(wx.Frame):
    """ Window for setting up the input parameters for the mp42avi Converter.

    Input: video file in MP4 format.
    Output: video file in AVI format.
    Use: select as many input videos as necessary.

    :var self.params: dict
        Parameters introduced by the user (input/output paths).
    :var self.status: str
        Register if the Converter has run succesfully.
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="any2avi - PAD suite"):
        """ Create frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str
            Frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(500, 200))
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.anypath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        anypath_text = wx.StaticText(self.panel, label="Source video files:")
        self.anypath_sizer.Add(anypath_text, 0,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.anypath_input = wx.TextCtrl(self.panel)
        self.anypath_sizer.Add(self.anypath_input, 1,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.anypath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.anypath_browse.Bind(wx.EVT_BUTTON, self.press_browse_anypath)
        self.anypath_sizer.Add(self.anypath_browse, 0,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.anypath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.avipath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        avipath_text = wx.StaticText(self.panel,
                                     label="Output AVI files directory:")
        self.avipath_sizer.Add(avipath_text, 0,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.avipath_input = wx.TextCtrl(self.panel)
        self.avipath_sizer.Add(self.avipath_input, 1,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.avipath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.avipath_browse.Bind(wx.EVT_BUTTON, self.press_browse_avipath)
        self.avipath_sizer.Add(self.avipath_browse, 0,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.avipath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(self.main_sizer)
        self.Show()

        self.params = dict()
        self.status = ""

    def press_browse_anypath(self, event):
        """ Handle method triggered when input path Browse button is pressed.

        Launch a file browser to select the input files (multiple selection).
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Source video files", "", "",
                                "Video files (*.mp4; *.hevc; *.wmv; *.avc)|"
                                "*.mp4;*.hevc;*.wmv;*.avc",
                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |
                                wx.FD_MULTIPLE)
        browser.ShowModal()
        self.params["any_path"] = browser.GetPaths()
        browser.Destroy()
        self.anypath_input.SetValue(",".join(self.params["any_path"]))

    def press_browse_avipath(self, event):
        """ Handle method triggered when output path Browse button is pressed.

        Launch a file browser to select the output directory.
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.DirDialog(self, "Output AVI directory", "",
                               wx.DD_NEW_DIR_BUTTON)
        browser.ShowModal()
        self.params["avi_path"] = browser.GetPath()
        browser.Destroy()
        self.avipath_input.SetValue(self.params["avi_path"])

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Launch the hevc2avi Converter with the chosen paths.
        The window is closed when the Converter has run succesfully.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.params["any_path"] = self.anypath_input.GetValue().split(",")
        self.params["avi_path"] = self.avipath_input.GetValue()
        if not self.params["any_path"] or not self.params["avi_path"]:
            print(f"[ERROR] You didn't enter anything! \n")
        else:
            print(f'[INFO] Input videos path: '
                  f'{", ".join(self.params["any_path"])}')
            print(f'[INFO] Output AVI videos path: '
                  f'{", ".join(self.params["avi_path"])} \n')
            self.status = any2avi(**self.params)
            if self.status == "done":
                print(f"[INFO] Your converted video is ready! \n")
                self.Close()


class Clip2framesFrame(wx.Frame):
    """ Window for setting up the input parameters for the clip2frames
    Converter.

    Input: video clips in AVI/MP4 format.
    Output: clips chopped into frames, in PNG format.
    Use: select as many input clips as necessary. The corresponding frames for
    each clip will be stored in its own directory.

    :var self.params: dict
        Parameters introduced by the user (input/output paths).
    :var self.status: str
        Register if the Converter has run succesfully.
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="clip2frames - PAD suite"):
        """ Create frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str6
            Frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(500, 200))
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.clippath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        clippath_text = wx.StaticText(self.panel, label="Source clips:")
        self.clippath_sizer.Add(clippath_text, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.clippath_input = wx.TextCtrl(self.panel)
        self.clippath_sizer.Add(self.clippath_input, 1,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.clippath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.clippath_browse.Bind(wx.EVT_BUTTON, self.press_browse_clippath)
        self.clippath_sizer.Add(self.clippath_browse, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.clippath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.framepath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        framepath_text = wx.StaticText(self.panel,
                                       label="Output frames directory:")
        self.framepath_sizer.Add(framepath_text, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.framepath_input = wx.TextCtrl(self.panel)
        self.framepath_sizer.Add(self.framepath_input, 1,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.framepath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.framepath_browse.Bind(wx.EVT_BUTTON, self.press_browse_framepath)
        self.framepath_sizer.Add(self.framepath_browse, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.framepath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(self.main_sizer)
        self.Show()

        self.params = dict()
        self.status = ""

    def press_browse_clippath(self, event):
        """ Handle method triggered when input path Browse button is pressed.

        Launch a file browser to select the input files (multiple selection).
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Source clips", "", "",
                                "Video files (*.avi; *.mp4)|*.avi;*.mp4",
                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |
                                wx.FD_MULTIPLE)
        browser.ShowModal()
        self.params["clip_path"] = browser.GetPaths()
        browser.Destroy()
        self.clippath_input.SetValue(",".join(self.params["clip_path"]))

    def press_browse_framepath(self, event):
        """ Handle method triggered when output path Browse button is pressed.

        Launch a file browser to select the output directory.
        Selected path is stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.DirDialog(self, "Output frames directory", "",
                               wx.DD_NEW_DIR_BUTTON)
        browser.ShowModal()
        self.params["frame_path"] = browser.GetPath()
        browser.Destroy()
        self.framepath_input.SetValue(self.params["frame_path"])

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Launch the clip2frames Converter with the chosen paths.
        The window is closed when the Converter has run succesfully.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.params["clip_path"] = self.clippath_input.GetValue().split(",")
        self.params["frame_path"] = self.framepath_input.GetValue()
        if not self.params["clip_path"] or not self.params["frame_path"]:
            print(f"[ERROR] You didn't enter anything! \n")
        else:
            print(f'[INFO] Input clip path: '
                  f'{", ".join(self.params["clip_path"])}')
            print(f'[INFO] Output frames path: {self.params["frame_path"]} \n')
            self.status = clip2frames(**self.params)
            if self.status == "done":
                print(f"[INFO] Your frames are ready! \n")
                self.Close()


class Clip2vidFrame(wx.Frame):
    """ Window for setting up the input parameters for the clip2vid Converter.

    Input: video clips in AVI/MP4 format.
    Output: merged clips in AVI format.
    Use: select as many input clips as necessary.

    :var self.params: dict
        Parameters introduced by the user (input/output paths).
    :var self.status: str
        Register if the Converter has run succesfully.
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="clip2vid - PAD suite"):
        """ Create frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str
            Frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(500, 200))
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.clippath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        clippath_text = wx.StaticText(self.panel, label="Source clips:")
        self.clippath_sizer.Add(clippath_text, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.clippath_input = wx.TextCtrl(self.panel)
        self.clippath_sizer.Add(self.clippath_input, 1,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.clippath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.clippath_browse.Bind(wx.EVT_BUTTON, self.press_browse_clippath)
        self.clippath_sizer.Add(self.clippath_browse, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.clippath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.vidpath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        vidpath_text = wx.StaticText(self.panel, label="Output video:")
        self.vidpath_sizer.Add(vidpath_text, 0,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.vidpath_input = wx.TextCtrl(self.panel)
        self.vidpath_sizer.Add(self.vidpath_input, 1,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.vidpath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.vidpath_browse.Bind(wx.EVT_BUTTON, self.press_browse_vidpath)
        self.vidpath_sizer.Add(self.vidpath_browse, 0,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.vidpath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(self.main_sizer)
        self.Show()

        self.params = dict()
        self.status = ""

    def press_browse_clippath(self, event):
        """ Handle method triggered when input path Browse button is pressed.

        Launch a file browser to select the input files (multiple selection).
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically
        generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Source clips", "", "",
                                "Video files (*.avi; *.mp4)|*.avi;*.mp4",
                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |
                                wx.FD_MULTIPLE)
        browser.ShowModal()
        self.params["clip_path"] = browser.GetPaths()
        browser.Destroy()
        self.clippath_input.SetValue(",".join(self.params["clip_path"]))

    def press_browse_vidpath(self, event):
        """ Handle method triggered when output path Browse button is pressed.

        Launch a file browser to select the path of the output file.
        Selected path is stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Output video", "", "",
                                "AVI files (*.avi)|*.avi", wx.FD_SAVE |
                                wx.FD_OVERWRITE_PROMPT)
        browser.ShowModal()
        self.params["vid_path"] = browser.GetPath()
        browser.Destroy()
        self.vidpath_input.SetValue(self.params["vid_path"])

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Launch the clip2vid Converter with the chosen paths.
        The window is closed when the Converter has run succesfully.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.params["clip_path"] = self.clippath_input.GetValue().split(",")
        self.params["vid_path"] = self.vidpath_input.GetValue()
        if not self.params["clip_path"] or not self.params["vid_path"]:
            print(f"[ERROR] You didn't enter anything!")
        else:
            print(f'[INFO] Input clips paths: '
                  f'{", ".join(self.params["clip_path"])}')
            print(f'[INFO] Output video path: {self.params["vid_path"]} \n')
            self.status = clip2vid(**self.params)
            if self.status == "done":
                print(f"[INFO] Your merged video is ready! \n")
                self.Close()


class Frames2clipFrame(wx.Frame):
    """ Window for setting up the input parameters for the frames2clip
    Converter.

    Input: frames in PNG format.
    Output: clips built from the input frames, in AVI format.
    Use: select as many input frames as necessary. Only one clip can be created
    at a time.

    :var self.params: dict
        Parameters introduced by the user (input/output paths, fps).
    :var self.status: str
        Register if the Converter has run succesfully.
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="frames2clip - PAD suite"):
        """ Create frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str
            Frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(500, 250))
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.framepath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        framepath_text = wx.StaticText(self.panel, label="Source frames:")
        self.framepath_sizer.Add(framepath_text, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.framepath_input = wx.TextCtrl(self.panel)
        self.framepath_sizer.Add(self.framepath_input, 1,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.framepath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.framepath_browse.Bind(wx.EVT_BUTTON, self.press_browse_framepath)
        self.framepath_sizer.Add(self.framepath_browse, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.framepath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.clippath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        clippath_text = wx.StaticText(self.panel, label="Output clip:")
        self.clippath_sizer.Add(clippath_text, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.clippath_input = wx.TextCtrl(self.panel)
        self.clippath_sizer.Add(self.clippath_input, 1,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.clippath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.clippath_browse.Bind(wx.EVT_BUTTON, self.press_browse_clippath)
        self.clippath_sizer.Add(self.clippath_browse, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.clippath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.fps_sizer = wx.BoxSizer(wx.HORIZONTAL)
        fps_text = wx.StaticText(self.panel, label="Frames per second (fps):")
        self.fps_sizer.Add(fps_text, 0, wx.RIGHT | wx.LEFT, 10)
        self.fps_input = wx.SpinCtrl(self.panel, id=wx.ID_ANY,
                                     style=wx.SP_ARROW_KEYS | wx.ALIGN_RIGHT,
                                     min=1, max=300)
        self.fps_sizer.Add(self.fps_input, 1, wx.RIGHT | wx.LEFT, 10)
        self.main_sizer.Add(self.fps_sizer, 0, wx.ALL, 10)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(self.main_sizer)
        self.Show()

        self.params = dict()
        self.status = ""

    def press_browse_framepath(self, event):
        """ Handle method triggered when input path Browse button is pressed.

        Launch a file browser to select the input files (multiple selection).
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Source frames", "", "",
                                "PNG files (*.png)|*.png",
                                wx.FD_OPEN | wx.FD_MULTIPLE |
                                wx.FD_FILE_MUST_EXIST)
        browser.ShowModal()
        self.params["frame_path"] = browser.GetPaths()
        browser.Destroy()
        self.framepath_input.SetValue(",".join(self.params["frame_path"]))

    def press_browse_clippath(self, event):
        """ Handle method triggered when output path Browse button is pressed.

        Launch a file browser to select the path of the output file.
        Selected path is stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Output clip", "", "",
                                "AVI files (*.avi)|*.avi",
                                wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        browser.ShowModal()
        self.params["clip_path"] = browser.GetPath()
        browser.Destroy()
        self.clippath_input.SetValue(self.params["clip_path"])

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Read FPS value.
        Launch the frames2clip Converter with the chosen paths.
        The window is closed when the Converter has run succesfully.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.params["frame_path"] = self.framepath_input.GetValue().split(",")
        self.params["clip_path"] = self.clippath_input.GetValue()
        self.params["fps"] = float(self.fps_input.GetValue())
        if not self.params["frame_path"] or not self.params["clip_path"] \
                or not self.params["fps"]:
            print(f"[ERROR] You didn't enter anything! \n")
        else:
            print(f'[INFO] Input frames path: '
                  f'{", ".join(self.params["frame_path"])}')
            print(f'[INFO] Output clip path: {self.params["clip_path"]}')
            print(f'[INFO] Frame rate: {self.params["fps"]} \n')
            self.status = frames2clip(**self.params)
            if self.status == "done":
                print(f"[INFO] Your clip is ready! \n")
                self.Close()


class HEVC2AVIFrame(wx.Frame):
    """ Window for setting up the input parameters for the hevc2avi Converter.

    Input: video file in HEVC format.
    Output: video file in AVI format.
    Use: select as many input videos as necessary.

    :var self.params: dict
        Parameters introduced by the user (input/output paths).
    :var self.status: str
        Register if the Converter has run succesfully.
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="hevc2avi - PAD suite"):
        """ Create frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str
            Frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(500, 200))
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.hevcpath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        hevcpath_text = wx.StaticText(self.panel, label="Source HEVC files:")
        self.hevcpath_sizer.Add(hevcpath_text, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.hevcpath_input = wx.TextCtrl(self.panel)
        self.hevcpath_sizer.Add(self.hevcpath_input, 1,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.hevcpath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.hevcpath_browse.Bind(wx.EVT_BUTTON, self.press_browse_hevcpath)
        self.hevcpath_sizer.Add(self.hevcpath_browse, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.hevcpath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.avipath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        avipath_text = wx.StaticText(self.panel,
                                     label="Output AVI files directory:")
        self.avipath_sizer.Add(avipath_text, 0,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.avipath_input = wx.TextCtrl(self.panel)
        self.avipath_sizer.Add(self.avipath_input, 1,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.avipath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.avipath_browse.Bind(wx.EVT_BUTTON, self.press_browse_avipath)
        self.avipath_sizer.Add(self.avipath_browse, 0,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.avipath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(self.main_sizer)
        self.Show()

        self.params = dict()
        self.status = ""

    def press_browse_hevcpath(self, event):
        """ Handle method triggered when input path Browse button is pressed.

        Launch a file browser to select the input files (multiple selection).
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Source HEVC files", "", "",
                                "HEVC files (*.hevc)|*.hevc",
                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |
                                wx.FD_MULTIPLE)
        browser.ShowModal()
        self.params["hevc_path"] = browser.GetPaths()
        browser.Destroy()
        self.hevcpath_input.SetValue(",".join(self.params["hevc_path"]))

    def press_browse_avipath(self, event):
        """ Handle method triggered when output path Browse button is pressed.

        Launch a file browser to select the output directory.
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.DirDialog(self, "Output AVI directory", "",
                               wx.DD_NEW_DIR_BUTTON)
        browser.ShowModal()
        self.params["avi_path"] = browser.GetPath()
        browser.Destroy()
        self.avipath_input.SetValue(self.params["avi_path"])

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Launch the hevc2avi Converter with the chosen paths.
        The window is closed when the Converter has run succesfully.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.params["hevc_path"] = self.hevcpath_input.GetValue().split(",")
        self.params["avi_path"] = self.avipath_input.GetValue()
        if not self.params["hevc_path"] or not self.params["avi_path"]:
            print(f"[ERROR] You didn't enter anything! \n")
        else:
            print(f'[INFO] Input HEVC videos: '
                  f'{", ".join(self.params["hevc_path"])}')
            print(f'[INFO] Output AVI videos path: '
                  f'{self.params["avi_path"]}\n')
            self.status = hevc2avi(**self.params)
            if self.status == "done":
                print(f"[INFO] Your converted video is ready! \n")
                self.Close()


class Vid2clipFrame(wx.Frame):
    """ Window for setting up the input parameters for the vid2clip Converter.

    Input: video file in AVI/MP4 format.
    Output: video file in AVI format.
    Use: select the video file to be cut, as well as the start and stop times,
    in milliseconds.

    :var self.params: dict
        Parameters introduced by the user (input/output paths,
         start/stop times).
    :var self.status: str
        Register if the Converter has run succesfully.
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="vid2clip - PAD suite"):
        """ Create frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str
            Frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(500, 340))
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.vidpath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        vidpath_text = wx.StaticText(self.panel, label="Source video:")
        self.vidpath_sizer.Add(vidpath_text, 0,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.vidpath_input = wx.TextCtrl(self.panel)
        self.vidpath_sizer.Add(self.vidpath_input, 1,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.vidpath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.vidpath_browse.Bind(wx.EVT_BUTTON, self.press_browse_vidpath)
        self.vidpath_sizer.Add(self.vidpath_browse, 0,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.vidpath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.clippath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        clippath_text = wx.StaticText(self.panel, label="Output clip:")
        self.clippath_sizer.Add(clippath_text, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.clippath_input = wx.TextCtrl(self.panel)
        self.clippath_sizer.Add(self.clippath_input, 1,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.clippath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.clippath_browse.Bind(wx.EVT_BUTTON, self.press_browse_clippath)
        self.clippath_sizer.Add(self.clippath_browse, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.clippath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.starttime_sizer = wx.BoxSizer(wx.HORIZONTAL)
        starttime_text = wx.StaticText(self.panel, label="Start time:")
        self.starttime_sizer.Add(starttime_text, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.starttime_input = wx.SpinCtrl(self.panel, id=wx.ID_ANY,
                                           style=wx.SP_ARROW_KEYS |
                                           wx.ALIGN_RIGHT,
                                           min=0, max=3.6e8)
        self.starttime_sizer.Add(self.starttime_input, 1,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        starttime_ms = wx.StaticText(self.panel, id=wx.ID_ANY,
                                     label="milliseconds")
        self.starttime_sizer.Add(starttime_ms, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.starttime_sizer, 0, wx.ALL, 15)

        self.stoptime_sizer = wx.BoxSizer(wx.HORIZONTAL)
        stoptime_text = wx.StaticText(self.panel, label="Stop time:")
        self.stoptime_sizer.Add(stoptime_text, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.stoptime_input = wx.SpinCtrl(self.panel, id=wx.ID_ANY,
                                          style=wx.SP_ARROW_KEYS |
                                          wx.ALIGN_RIGHT,
                                          min=0, max=3.6e8)
        self.stoptime_sizer.Add(self.stoptime_input, 1,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        stoptime_ms = wx.StaticText(self.panel, id=wx.ID_ANY,
                                    label="milliseconds")
        self.stoptime_sizer.Add(stoptime_ms, 0, wx.RIGHT | wx.LEFT | wx.CENTER,
                                10)
        self.main_sizer.Add(self.stoptime_sizer, 0, wx.ALL, 15)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(self.main_sizer)
        self.Show()

        self.params = dict()
        self.status = ""

    def press_browse_vidpath(self, event):
        """ Handle method triggered when input path Browse button is pressed.

        Launch a file browser to select the input file (single selection).
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Source video", "", "",
                                "Video files (*.avi; *.mp4)|*.avi;*.mp4",
                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        browser.ShowModal()
        self.params["vid_path"] = browser.GetPath()
        browser.Destroy()
        self.vidpath_input.SetValue(self.params["vid_path"])

    def press_browse_clippath(self, event):
        """ Handle method triggered when output path Browse button is pressed.

        Launch a file browser to select the path to the output file.
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Output clip", "", "",
                                "AVI files (*.avi)|*.avi",
                                wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        browser.ShowModal()
        self.params["clip_path"] = browser.GetPath()
        browser.Destroy()
        self.clippath_input.SetValue(self.params["clip_path"])

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Read values for start and stop times.
        Launch the vid2clip Converter with the chosen paths.
        The window is closed when the Converter has run succesfully.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.params["vid_path"] = self.vidpath_input.GetValue()
        self.params["clip_path"] = self.clippath_input.GetValue()
        self.params["start_time"] = float(self.starttime_input.GetValue())
        self.params["stop_time"] = float(self.stoptime_input.GetValue())
        if self.params["start_time"] >= self.params["stop_time"]:
            print(f'[ERROR] Stop time must be after start time.')
            # sys.exit()
        elif not self.params["vid_path"] or not self.params["clip_path"]\
                or not self.params["start_time"] \
                or not self.params["stop_time"]:
            print(f"[ERROR] You didn't enter anything! \n")
        else:
            print(f'[INFO] Input video: {self.params["vid_path"]}')
            print(f'[INFO] Output clip: {self.params["clip_path"]}')
            print(f'[INFO] Start time: {self.params["start_time"]} ms')
            print(f'[INFO] Stop time: {self.params["stop_time"]} ms \n')
            self.status = vid2clip(**self.params)
            if self.status == "done":
                print(f"[INFO] Your clip is ready! \n")
                self.Close()


class BboxesDrawFrame(wx.Frame):
    """ Window for setting up the input parameters to the Bounding Box Creator.

    Input: PNG frames to draw bounding boxes on,
            subjects to code the boxes with.
    Output: PNG frames with bounding boxes, TSV file with bounding box data.
    Use: select as many frames as necessary. Subjects must be comma-separated.
    After drawing each bounding box, press ENTER to confirm or C to cancel and
    skip to the next frame.
    PNG files must be named as "frame_{code}_bboxes.png". TSV files will be
    named as "frame_{code}_data.tsv".
    If the data file already exists, new bounding boxes data will be appended.

    :var self.params: dict
        Parameters introduced by the user (frames path, subject codes)
    :var self.status: str
        Register if the Bounding Box Creator has run succesfully.
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="Bounding Box Creator - PAD suite"):
        """ Create frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str
            Frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(500, 150))
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.framepath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        framepath_text = wx.StaticText(self.panel, label="Source frames:")
        self.framepath_sizer.Add(framepath_text, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.framepath_input = wx.TextCtrl(self.panel)
        self.framepath_sizer.Add(self.framepath_input, 1,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.framepath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.framepath_browse.Bind(wx.EVT_BUTTON, self.press_browse_framepath)
        self.framepath_sizer.Add(self.framepath_browse, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.framepath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(self.main_sizer)
        self.Show()

        self.params = dict()
        self.status = ""

    def press_browse_framepath(self, event):
        """ Handle method triggered when input path Browse button is pressed.

        Launch a file browser to select the input files (multiple selection).
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Source frames", "", "",
                                "PNG files (*.png)|*.png",
                                wx.FD_OPEN | wx.FD_MULTIPLE |
                                wx.FD_FILE_MUST_EXIST)
        browser.ShowModal()
        self.params["frame_path"] = browser.GetPaths()
        browser.Destroy()
        self.framepath_input.SetValue(",".join(self.params["frame_path"]))

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Read the codes of the subjects corresponding to the bounding boxes to
        be created.
        Launch the Bounding Box Creator with the chosen paths and subjects.
        The window is closed when the Creator has run succesfully.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.params["frame_path"] = sorted(self.framepath_input.GetValue().
                                           split(","))
        # self.params["subjects"] = self.subj_input.GetValue().split(",")
        if not self.params["frame_path"]:
            print(f"[ERROR] You didn't enter anything!\n")
        else:
            print(f'[INFO] Input frames: '
                  f'{", ".join(self.params["frame_path"])}\n')
            self.status = draw_bbox(**self.params)
            if self.status == "done":
                print(f"[INFO] Bounding boxes have been saved! \n")
                self.Close()


class BboxesIdSetUpFrame(wx.Frame):
    """ Window for setting up the input parameters to the Bounding Box ID

    Input: PNG frame with bounding boxes,
            TSV file with bounding box data.
    Use: choose the frame to be identified and its corresponding data file.
    Output TSV files will be named as "{input_data_name}_edit.tsv".
     PNG files will be named as "{input_frame_name}_subjects.png".

    :var self.params: dict
        Parameters introduced by the user (frames/data paths).
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="Bounding Box ID - PAD suite"):
        """ Create frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str
            Frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(500, 200))
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.framepath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        framepath_text = wx.StaticText(self.panel, label="Annotated frame:")
        self.framepath_sizer.Add(framepath_text, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.framepath_input = wx.TextCtrl(self.panel)
        self.framepath_sizer.Add(self.framepath_input, 1,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.framepath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.framepath_browse.Bind(wx.EVT_BUTTON, self.press_browse_framepath)
        self.framepath_sizer.Add(self.framepath_browse, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.framepath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.bbox_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bbox_text = wx.StaticText(self.panel, label="Bounding box data: ")
        self.bbox_sizer.Add(bbox_text, 0, wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.bbox_input = wx.TextCtrl(self.panel)
        self.bbox_sizer.Add(self.bbox_input, 1,
                            wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.bbox_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.bbox_browse.Bind(wx.EVT_BUTTON, self.press_browse_bboxpath)
        self.bbox_sizer.Add(self.bbox_browse,
                            0, wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.bbox_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(self.main_sizer)
        self.Show()

        self.params = dict()

    def press_browse_framepath(self, event):
        """ Handle method triggered when input frame path Browse button is
         pressed.

        Launch a file browser to select the input file (single selection).
        Selected path is stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Source image", "", "",
                                "Image files (*.png)|*.png",
                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        browser.ShowModal()
        self.params["frame_path"] = browser.GetPath()
        browser.Destroy()
        self.framepath_input.SetValue(self.params["frame_path"])

    def press_browse_bboxpath(self, event):
        """ Handle method triggered when input data path Browse button is
         pressed.

        Launch a file browser to select the input file (single selection).
        Selected path is stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Bounding box data", "", "",
                                "Data files (*.tsv)|*.tsv",
                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        browser.ShowModal()
        self.params["bbox_path"] = browser.GetPath()
        browser.Destroy()
        self.bbox_input.SetValue(self.params["bbox_path"])

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Launch the Bounding Box ID with the chosen paths.
        The window is closed when the ID has run succesfully.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.params["frame_path"] = self.framepath_input.GetValue()
        self.params["bbox_path"] = self.bbox_input.GetValue()
        if not self.params["frame_path"]:
            print(f"[ERROR] You didn't enter anything!\n")
        else:
            BboxesIdFrame(None, wx.ID_ANY, "Bounding Box ID - PAD suite",
                          **self.params)
            self.Close()


class BboxesIdFrame(wx.Frame):
    """ Window for linking bounding boxes to subjects using the Bounding Box ID

    Output: PNG frames with modified bounding boxes identifiers,
             TSV file with updated bounding box data.
    Use: introduce the name of the subject to tag, then click on the top left
          and botton right corners of the corresponding bounding box. Repeat
          as many times as necessary, when done press Apply.
    Output TSV files will be named as "{input_data_name}_edit.tsv".
     PNG files will be named as "{input_frame_name}_subjects.png".

    :var self.params: dict
        Parameters introduced by the user (frames/data paths).
    :var self.bbox_data : dict
        Bounding box data for every subject.
    :var self.pre_subj : str
        Last subject identified.
    :var self.status: str
        Register if the Bounding Box ID has run succesfully.
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="Bounding Box ID - PAD suite", **params):
        """ Create frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str
            Frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(1500, 900))
        self.params = params
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.subj_sizer = wx.BoxSizer(wx.HORIZONTAL)
        subj_text = wx.StaticText(self.panel, label="Choose subject:")
        self.subj_sizer.Add(subj_text, 0, wx.RIGHT | wx.LEFT | wx.TOP, 5)
        self.subj_input = wx.TextCtrl(self.panel, size=(180, 30))
        self.subj_sizer.Add(self.subj_input, 0,
                            wx.RIGHT | wx.LEFT | wx.TOP, 5)
        self.main_sizer.Add(self.subj_sizer, 1, wx.ALL | wx.EXPAND, 5)

        self.img_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.scale = 0.8
        self.frame = wx.Image(self.params["frame_path"], wx.BITMAP_TYPE_ANY)
        self.ratio = self.frame.GetWidth() / self.frame.GetHeight()
        self.disp_width, self.disp_height = get_resolution()
        self.ratio_d2f = self.disp_width/self.frame.GetWidth()
        if self.ratio_d2f <= 1.2:
            self.bmp_scale = self.scale * self.ratio_d2f
            self.s_frame = self.frame.Scale(
                self.bmp_scale * self.frame.GetWidth(),
                self.bmp_scale * self.frame.GetHeight(),
                wx.IMAGE_QUALITY_HIGH)
        else:
            self.s_frame = self.frame
            self.bmp_scale = 1
        self.bmp = self.s_frame.ConvertToBitmap()
        self.image = wx.StaticBitmap(self.panel, -1, self.bmp,
                                     size=(self.s_frame.GetWidth(),
                                           self.s_frame.GetHeight()))
        self.image.Bind(wx.EVT_LEFT_DOWN, self.left_click)
        self.img_sizer.Add(self.image, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.main_sizer.Add(self.img_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        self.panel.SetSizer(self.main_sizer)
        self.main_sizer.Fit(self)
        self.Show()
        self.Maximize(True)

        self.bbox_data = dict()
        self.pre_subj = ""
        self.status = ""

    def left_click(self, event):
        """ Handle method when a single left click action has been performed.

        Registers the position of the mouse and the name of the subject.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        tmp_subj = self.subj_input.GetValue()
        if tmp_subj not in self.bbox_data.keys():
            self.bbox_data[tmp_subj] = dict()
        if tmp_subj != self.pre_subj:
            tmp_x, tmp_y = event.GetPosition()
            self.bbox_data[tmp_subj]["X0"] = int(tmp_x / self.bmp_scale)
            self.bbox_data[tmp_subj]["Y0"] = int(tmp_y / self.bmp_scale)
        else:
            tmp_x, tmp_y = event.GetPosition()
            self.bbox_data[tmp_subj]["X1"] = int(tmp_x / self.bmp_scale)
            self.bbox_data[tmp_subj]["Y1"] = int(tmp_y / self.bmp_scale)
            self.bbox_data[tmp_subj]["W"] = self.bbox_data[tmp_subj]["X1"] \
                - self.bbox_data[tmp_subj]["X0"]
            self.bbox_data[tmp_subj]["H"] = self.bbox_data[tmp_subj]["Y1"] \
                - self.bbox_data[tmp_subj]["Y0"]
        self.pre_subj = self.subj_input.GetValue()

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Saves the registered data to the files and closes the ID window.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.status = id_bbox(self.params, self.bbox_data)
        if self.status == "done":
            print(f'[INFO] Frame has been tagged!\n')
            self.Close()


class BboxesRemoveFrame(wx.Frame):
    """ Window for setting up the input parameters to the Bounding Box Remover.

    Input: TSV file containing bounding boxes data,
            original PNG frame without bounding boxes,
            codes of the subjects to be removed.
    Output: PNG frames without the bounding boxes corresponding to the selected
             subjects, modified TSV file with updated bounding box data.
    Use: select as many data files as necessary, then select the corresponding
          frames.
          Several subjects may be included as comma-separated.
    TSV files must be named as "frame_{code}_data.tsv". PNG files will be
    named as "frame_{code}_bboxes.png".

    :var self.params: dict
        Parameters introduced by the user (frames/data paths, subject codes)
    :var self.status: str
        Register if the Bounding Box Remover has run succesfully.
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="Bounding Box Remover - PAD suite"):
        """ Create frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str
            Frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(500, 250))
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.bboxpath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bboxpath_text = wx.StaticText(self.panel, label="Bounding box data:")
        self.bboxpath_sizer.Add(bboxpath_text, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.bboxpath_input = wx.TextCtrl(self.panel)
        self.bboxpath_sizer.Add(self.bboxpath_input, 1,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.bboxpath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.bboxpath_browse.Bind(wx.EVT_BUTTON, self.press_browse_bboxpath)
        self.bboxpath_sizer.Add(self.bboxpath_browse, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.bboxpath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.framepath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        framepath_text = wx.StaticText(self.panel, label="Frame without "
                                                         "bounding boxes:")
        self.framepath_sizer.Add(framepath_text, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.framepath_input = wx.TextCtrl(self.panel)
        self.framepath_sizer.Add(self.framepath_input, 1,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.framepath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.framepath_browse.Bind(wx.EVT_BUTTON, self.press_browse_framepath)
        self.framepath_sizer.Add(self.framepath_browse, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.framepath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.subj_sizer = wx.BoxSizer(wx.HORIZONTAL)
        subj_text = wx.StaticText(self.panel, label="Subject codes:")
        self.subj_sizer.Add(subj_text, 0, wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.subj_input = wx.TextCtrl(self.panel)
        self.subj_sizer.Add(self.subj_input, 1,
                            wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.subj_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(self.main_sizer)
        self.Show()

        self.params = dict()
        self.status = ""

    def press_browse_bboxpath(self, event):
        """ Handle method triggered when input data path Browse button is
         pressed.

        Launch a file browser to select the input files (multiple selection).
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Source bounding box data files", "", "",
                                "TSV files (*.tsv)|*.tsv",
                                wx.FD_OPEN | wx.FD_MULTIPLE |
                                wx.FD_FILE_MUST_EXIST)
        browser.ShowModal()
        self.params["bbox_path"] = browser.GetPaths()
        browser.Destroy()
        self.bboxpath_input.SetValue(",".join(self.params["bbox_path"]))

    def press_browse_framepath(self, event):
        """ Handle method triggered when input frames path Browse button is
         pressed.

        Launch a file browser to select the input files (multiple selection).
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Source frames", "", "",
                                "PNG files (*.png)|*.png",
                                wx.FD_OPEN | wx.FD_MULTIPLE |
                                wx.FD_FILE_MUST_EXIST)
        browser.ShowModal()
        self.params["frame_path"] = browser.GetPaths()
        browser.Destroy()
        self.framepath_input.SetValue(",".join(self.params["frame_path"]))

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Read the codes of the subjects to be removed.
        Launch the Bounding Box Remover with the chosen paths and subjects.
        The window is closed when the Remover has run succesfully.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.params["bbox_path"] = sorted(self.bboxpath_input.GetValue().
                                          split(","))
        self.params["frame_path"] = sorted(self.framepath_input.GetValue().
                                           split(","))
        self.params["subjects"] = self.subj_input.GetValue().split(",")
        if not self.params["bbox_path"] or not self.params["frame_path"]\
                or not self.params["subjects"]:
            print(f"[ERROR] You didn't enter anything!\n")
        else:
            print(f'[INFO] Input data: {self.params["bbox_path"]}\n')
            self.status = remove_bbox(**self.params)
            if self.status == "done":
                print(f"[INFO] Removal has been completed!\n")
                self.Close()


class BboxesRemove2SetUpFrame(wx.Frame):
    """ Window for setting up the input parameters to the Bounding Box ID

    Input: PNG frame with bounding boxes,
            TSV file with bounding box data.
    Use: choose the frame to be identified and its corresponding data file.
    Output TSV files will be named as "{input_data_name}_edit.tsv".
     PNG files will be named as "{input_frame_name}_subjects.png".

    :var self.params: dict
        Parameters introduced by the user (frames/data paths).
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="Bounding Box Remover v2 - PAD suite"):
        """ Create frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str
            Frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(500, 250))
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.annotpath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        annotpath_text = wx.StaticText(self.panel, label="Annotated frame:")
        self.annotpath_sizer.Add(annotpath_text, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.annotpath_input = wx.TextCtrl(self.panel)
        self.annotpath_sizer.Add(self.annotpath_input, 1,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.annotpath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.annotpath_browse.Bind(wx.EVT_BUTTON, self.press_browse_annotpath)
        self.annotpath_sizer.Add(self.annotpath_browse, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.annotpath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.framepath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        framepath_text = wx.StaticText(self.panel, label="Empty frame:")
        self.framepath_sizer.Add(framepath_text, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.framepath_input = wx.TextCtrl(self.panel)
        self.framepath_sizer.Add(self.framepath_input, 1,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.framepath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.framepath_browse.Bind(wx.EVT_BUTTON, self.press_browse_framepath)
        self.framepath_sizer.Add(self.framepath_browse, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.framepath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.bbox_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bbox_text = wx.StaticText(self.panel, label="Bounding box data: ")
        self.bbox_sizer.Add(bbox_text, 0, wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.bbox_input = wx.TextCtrl(self.panel)
        self.bbox_sizer.Add(self.bbox_input, 1,
                            wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.bbox_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.bbox_browse.Bind(wx.EVT_BUTTON, self.press_browse_bboxpath)
        self.bbox_sizer.Add(self.bbox_browse, 0,
                            wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.bbox_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(self.main_sizer)
        self.Show()

        self.params = dict()

    def press_browse_annotpath(self, event):
        """ Handle method triggered when input frame path Browse button is
         pressed.

        Launch a file browser to select the input file (single selection).
        Selected path is stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Annotated frames", "", "",
                                "Image files (*.png)|*.png",
                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |
                                wx.FD_MULTIPLE)
        browser.ShowModal()
        self.params["annot_path"] = browser.GetPaths()
        browser.Destroy()
        self.annotpath_input.SetValue(",".join(self.params["annot_path"]))

    def press_browse_bboxpath(self, event):
        """ Handle method triggered when input data path Browse button is
         pressed.

        Launch a file browser to select the input file (single selection).
        Selected path is stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Bounding box data", "", "",
                                "Data files (*.tsv)|*.tsv",
                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |
                                wx.FD_MULTIPLE)
        browser.ShowModal()
        self.params["bbox_path"] = browser.GetPaths()
        browser.Destroy()
        self.bbox_input.SetValue(",".join(self.params["bbox_path"]))

    def press_browse_framepath(self, event):
        browser = wx.FileDialog(self, "Empty frames", "", "",
                                "Image files (*.png)|*.png",
                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST |
                                wx.FD_MULTIPLE)
        browser.ShowModal()
        self.params["frame_path"] = browser.GetPaths()
        browser.Destroy()
        self.framepath_input.SetValue(",".join(self.params["frame_path"]))

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Launch the Bounding Box ID with the chosen paths.
        The window is closed when the ID has run succesfully.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.params["annot_path"] = self.annotpath_input.GetValue().split(",")
        self.params["bbox_path"] = self.bbox_input.GetValue().split(",")
        self.params["frame_path"] = self.framepath_input.GetValue().split(",")
        if not self.params["annot_path"] or not self.params["bbox_path"] \
                or not self.params["frame_path"]:
            print(f"[ERROR] You didn't enter anything!\n")
        else:
            BboxesRemove2Frame(None, wx.ID_ANY, "Bounding Box Remover v2 "
                                                "- PAD suite", **self.params)
            self.Close()


class BboxesRemove2Frame(wx.Frame):
    """ Window for linking bounding boxes to subjects using the Bounding Box ID

    Output: PNG frames with modified bounding boxes identifiers,
             TSV file with updated bounding box data.
    Use: introduce the name of the subject to tag, then click on the top left
          and botton right corners of the corresponding bounding box. Repeat
          as many times as necessary, when done press Apply.
    Output TSV files will be named as "{input_data_name}_edit.tsv".
     PNG files will be named as "{input_frame_name}_subjects.png".

    :var self.params: dict
        Parameters introduced by the user (frames/data paths).
    :var self.bbox_data : dict
        Bounding box data for every subject.
    :var self.pre_subj : str
        Last subject identified.
    :var self.status: str
        Register if the Bounding Box ID has run succesfully.
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="Bounding Box Remover v2 - PAD suite", **params):
        """ Create frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str
            Frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(1500, 900))
        self.params = params
        self.bbox_path = self.params["bbox_path"]
        self.frame_path = self.params["frame_path"]
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.img_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.scale = 0.8
        self.frame = wx.Image(self.params["annot_path"][0], wx.BITMAP_TYPE_ANY)
        self.ratio = self.frame.GetWidth() / self.frame.GetHeight()
        self.disp_width, self.disp_height = get_resolution()
        self.ratio_d2f = self.disp_width / self.frame.GetWidth()
        if self.ratio_d2f <= 1.2:
            self.bmp_scale = self.scale * self.ratio_d2f
            self.s_frame = self.frame.Scale(
                self.bmp_scale * self.frame.GetWidth(),
                self.bmp_scale * self.frame.GetHeight(), wx.IMAGE_QUALITY_HIGH)
        else:
            self.s_frame = self.frame
            self.bmp_scale = 1
        self.bmp = self.s_frame.ConvertToBitmap()
        self.image = wx.StaticBitmap(self.panel, -1, self.bmp, size=(
            self.s_frame.GetWidth(), self.s_frame.GetHeight()))
        self.image.Bind(wx.EVT_LEFT_DOWN, self.left_click)
        self.img_sizer.Add(self.image, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.main_sizer.Add(self.img_sizer, 1, wx.EXPAND | wx.ALL, 5)

        # self.img_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.bmp_scale = 0.85
        # self.frame = wx.Image(self.params["annot_path"][0], wx.BITMAP_TYPE_ANY)
        # self.ratio = self.frame.GetWidth() / self.frame.GetHeight()
        # self.disp_width, self.disp_height = get_resolution()
        # if self.frame.GetWidth() >= self.bmp_scale * self.disp_width or \
        #         self.frame.GetHeight() >= self.bmp_scale * self.disp_height:
        #     self.s_frame = self.frame.Rescale(
        #         self.bmp_scale * self.disp_height * self.ratio,
        #         self.bmp_scale * self.disp_height, wx.IMAGE_QUALITY_HIGH)
        # else:
        #     self.s_frame = self.frame
        #     self.bmp_scale = 1
        # # self.s_frame = self.frame.Rescale(self.Size[0] / self.ratio,
        # #                                   self.bmp_scale * self.Size[0],
        # #                                   wx.IMAGE_QUALITY_HIGH)
        # self.bmp = self.s_frame.ConvertToBitmap()
        # self.image = wx.StaticBitmap(self.panel, -1, self.bmp,
        #                              size=(self.s_frame.GetWidth(),
        #                                    self.s_frame.GetHeight()))
        # self.image.Bind(wx.EVT_LEFT_DOWN, self.left_click)
        # self.img_sizer.Add(self.image, 1, wx.ALL, 5)
        # self.main_sizer.Add(self.img_sizer, 1, wx.EXPAND, 5)
        # self.bmp_scale = 0.55
        # self.frame = wx.Image(self.params["annot_path"][0],
        # wx.BITMAP_TYPE_ANY)
        # self.ratio = self.frame.GetWidth() / self.frame.GetHeight()
        # self.s_frame = self.frame.Rescale(self.Size[0] / self.ratio,
        #                                   self.bmp_scale * self.Size[0],
        #                                   wx.IMAGE_QUALITY_HIGH)
        # self.bmp = self.s_frame.ConvertToBitmap()
        # self.image = wx.StaticBitmap(self.panel, -1, self.bmp,
        #                              size=(self.s_frame.GetWidth(),
        #                                    self.s_frame.GetHeight()))
        # self.image.Bind(wx.EVT_LEFT_DOWN, self.left_click)
        # self.main_sizer.Add(self.image, 0, wx.ALL | wx.CENTER, 10)

        self.btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.prev_btn = wx.Button(self.panel, id=wx.ID_ANY, label="Previous")
        self.prev_btn.Bind(wx.EVT_BUTTON, self.press_prev)
        self.btn_sizer.Add(self.prev_btn, 0, wx.ALL | wx.CENTER, 5)

        self.next_btn = wx.Button(self.panel, id=wx.ID_ANY, label="Next")
        self.next_btn.Bind(wx.EVT_BUTTON, self.press_next)
        self.btn_sizer.Add(self.next_btn, 0, wx.ALL | wx.CENTER, 5)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.btn_sizer.Add(self.apply_btn, 0, wx.ALL | wx.CENTER, 5)
        self.main_sizer.Add(self.btn_sizer, 1, wx.ALL | wx.ALIGN_CENTER, 5)

        self.panel.SetSizer(self.main_sizer)
        self.main_sizer.Fit(self)
        self.Show()
        self.Maximize(True)

        self.bbox_data = dict()
        self.status = ""
        self.SecondClick = False
        self.gone_idx = 0
        self.in_idx = 0

    def left_click(self, event):
        """ Handle method when a single left click action has been performed.

        Registers the position of the mouse and the name of the subject.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        if not self.SecondClick:
            self.bbox_data[str(self.gone_idx)] = dict()
            tmp_x, tmp_y = event.GetPosition()
            self.bbox_data[str(self.gone_idx)]["X0"] = \
                int(tmp_x / self.bmp_scale)
            self.bbox_data[str(self.gone_idx)]["Y0"] = \
                int(tmp_y / self.bmp_scale)
            self.SecondClick = True
        else:
            tmp_x, tmp_y = event.GetPosition()
            self.bbox_data[str(self.gone_idx)]["X1"] = \
                int(tmp_x / self.bmp_scale)
            self.bbox_data[str(self.gone_idx)]["Y1"] = \
                int(tmp_y / self.bmp_scale)
            self.bbox_data[str(self.gone_idx)]["W"] = \
                self.bbox_data[str(self.gone_idx)]["X1"] \
                - self.bbox_data[str(self.gone_idx)]["X0"]
            self.bbox_data[str(self.gone_idx)]["H"] =\
                self.bbox_data[str(self.gone_idx)]["Y1"] \
                - self.bbox_data[str(self.gone_idx)]["Y0"]
            self.gone_idx += 1
            self.SecondClick = False

    def press_prev(self, event):
        if self.in_idx > 0:
            self.in_idx -= 1
        self.gone_idx = 0
        self.bbox_data.clear()
        self.SecondClick = False
        self.frame = wx.Image(self.params["annot_path"][self.in_idx],
                              wx.BITMAP_TYPE_ANY)
        self.ratio_d2f = self.disp_width / self.frame.GetWidth()
        if self.ratio_d2f <= 1.2:
            self.bmp_scale = self.scale * self.ratio_d2f
            self.s_frame = self.frame.Scale(
                self.bmp_scale * self.frame.GetWidth(),
                self.bmp_scale * self.frame.GetHeight(),
                wx.IMAGE_QUALITY_HIGH)
        else:
            self.s_frame = self.frame
            self.bmp_scale = 1
        # self.ratio = self.frame.GetWidth() / self.frame.GetHeight()
        # if self.frame.GetWidth() >= self.bmp_scale * self.disp_width or \
        #         self.frame.GetHeight() >= self.bmp_scale * self.disp_height:
        #     self.s_frame = self.frame.Rescale(
        #         self.bmp_scale * self.disp_height * self.ratio,
        #         self.bmp_scale * self.disp_height, wx.IMAGE_QUALITY_HIGH)
        # else:
        #     self.s_frame = self.frame
        #     self.bmp_scale = 1
        # self.frame = wx.Image(self.params["annot_path"][self.in_idx],
        #                       wx.BITMAP_TYPE_ANY)
        # self.ratio = self.frame.GetWidth() / self.frame.GetHeight()
        # self.s_frame = self.frame.Scale(self.bmp_scale * self.Size[0],
        #                                 self.Size[1] / self.ratio,
        #                                 wx.IMAGE_QUALITY_HIGH)
        self.bmp = self.s_frame.ConvertToBitmap()
        self.image.SetBitmap(self.bmp)
        self.Refresh()

    def press_next(self, event):
        if self.in_idx < len(self.params["annot_path"]) - 1:
            self.in_idx += 1
        self.gone_idx = 0
        self.bbox_data.clear()
        self.SecondClick = False
        self.frame = wx.Image(self.params["annot_path"][self.in_idx],
                              wx.BITMAP_TYPE_ANY)
        self.ratio_d2f = self.disp_width / self.frame.GetWidth()
        if self.ratio_d2f <= 1.2:
            self.bmp_scale = self.scale * self.ratio_d2f
            self.s_frame = self.frame.Scale(
                self.bmp_scale * self.frame.GetWidth(),
                self.bmp_scale * self.frame.GetHeight(), wx.IMAGE_QUALITY_HIGH)
        else:
            self.s_frame = self.frame
            self.bmp_scale = 1
        # self.ratio = self.frame.GetWidth() / self.frame.GetHeight()
        # if self.frame.GetWidth() >= self.bmp_scale * self.disp_width or \
        #         self.frame.GetHeight() >= self.bmp_scale * self.disp_height:
        #     self.s_frame = self.frame.Rescale(
        #         self.bmp_scale * self.disp_height * self.ratio,
        #         self.bmp_scale * self.disp_height, wx.IMAGE_QUALITY_HIGH)
        # else:
        #     self.s_frame = self.frame
        #     self.bmp_scale = 1
        # self.frame = wx.Image(self.params["annot_path"][self.in_idx],
        #                       wx.BITMAP_TYPE_ANY)
        # self.ratio = self.frame.GetWidth() / self.frame.GetHeight()
        # self.s_frame = self.frame.Scale(self.bmp_scale * self.Size[0],
        #                                 self.Size[1] / self.ratio,
        #                                 wx.IMAGE_QUALITY_HIGH)
        self.bmp = self.s_frame.ConvertToBitmap()
        self.image.SetBitmap(self.bmp)
        self.Refresh()

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Saves the registered data to the files and closes the ID window.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.params["bbox_path"] = self.bbox_path[self.in_idx]
        self.params["frame_path"] = self.frame_path[self.in_idx]
        self.status = remove_bbox_v2(self.params, self.bbox_data)
        if self.status == "done":
            print(f'[INFO] Removal has been completed!\n')
        self.frame = wx.Image(self.params["annot_path"][self.in_idx],
                              wx.BITMAP_TYPE_ANY)
        self.ratio_d2f = self.disp_width / self.frame.GetWidth()
        if self.ratio_d2f <= 1.2:
            self.bmp_scale = self.scale * self.ratio_d2f
            self.s_frame = self.frame.Scale(
                self.bmp_scale * self.frame.GetWidth(),
                self.bmp_scale * self.frame.GetHeight(), wx.IMAGE_QUALITY_HIGH)
        else:
            self.s_frame = self.frame
            self.bmp_scale = 1
        self.bmp = self.s_frame.ConvertToBitmap()
        self.image.SetBitmap(self.bmp)
        self.Refresh()


class BboxesTrackFrame(wx.Frame):
    """ Window for setting up the input parameters to the Bounding Box Tracker.

    Input: TSV files containing bounding boxes data.
    Output: TSV files with corresponding subjects according to tracking.
            Frames annotated with unique identifiers.
    Use: select the files corresponding to the frames to perform tracking over.
    TSV files must be named as "frame_{code}_data.tsv", and frames must be
    named as "frame_{code}_bboxes.png". First data file must contain the real
    names of the subjects.

    :var self.params: dict
        Parameters introduced by the user (bounding box data).
    :var self.status: str
        Register if the Bounding Box Tracker has run succesfully.
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="Bounding Box Tracking - PAD suite"):
        """ Create frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str
            Frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(500, 150))
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.bboxpath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bboxpath_text = wx.StaticText(self.panel, label="Bounding box data:")
        self.bboxpath_sizer.Add(bboxpath_text, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.bboxpath_input = wx.TextCtrl(self.panel)
        self.bboxpath_sizer.Add(self.bboxpath_input, 1,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.bboxpath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.bboxpath_browse.Bind(wx.EVT_BUTTON, self.press_browse_bboxpath)
        self.bboxpath_sizer.Add(self.bboxpath_browse, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.bboxpath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(self.main_sizer)
        self.Show()

        self.params = dict()
        self.status = ""

    def press_browse_bboxpath(self, event):
        """ Handle method triggered when input path Browse button is pressed.

        Launch a file browser to select the input files (multiple selection).
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Source bounding box data files", "", "",
                                "TSV files (*.tsv)|*.tsv",
                                wx.FD_OPEN | wx.FD_MULTIPLE |
                                wx.FD_FILE_MUST_EXIST)
        browser.ShowModal()
        self.params["bbox_path"] = browser.GetPaths()
        browser.Destroy()
        self.bboxpath_input.SetValue(",".join(self.params["bbox_path"]))

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Launch the Bounding Boxes Tracker with the chosen paths.
        The window is closed when the Tracker has run succesfully.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.params["bbox_path"] = sorted(self.bboxpath_input.GetValue().
                                          split(","))
        if not self.params["bbox_path"]:
            print(f"[ERROR] You didn't enter anything!\n")
        else:
            print(f'[INFO] Input data: {", ".join(self.params["bbox_path"])}\n')
            self.status = track_bbox(**self.params)
            if self.status == "done":
                print(f"[INFO] Tracking has been completed!\n")
                self.Close()


class BboxesTrack2Frame(wx.Frame):
    """ Window for setting up the input parameters to the Bounding Box Tracker.

    Input: scene frames.
    Output: TSV files with corresponding subjects according to tracking.
            Frames annotated with the unique identifiers.
    Use: select the files corresponding to the frames to perform tracking over.
    TSV files must be named as "frame_{code}_data.tsv", and frames must be
    named as "frame_{code}_bboxes.png". First data file must contain the real
    names of the subjects.

    :var self.params: dict
        Parameters introduced by the user (bounding box data).
    :var self.status: str
        Register if the Bounding Box Tracker has run succesfully.
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="Bounding Box Tracking v2 - PAD suite"):
        """ Create frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str
            Frame title, to be displayed as window name.
        """
        super().__init__(fr_parent, fr_id, fr_title, size=(500, 250))
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.framepath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        framepath_text = wx.StaticText(self.panel, label="Input frames:")
        self.framepath_sizer.Add(framepath_text, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.framepath_input = wx.TextCtrl(self.panel)
        self.framepath_sizer.Add(self.framepath_input, 1,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.framepath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.framepath_browse.Bind(wx.EVT_BUTTON, self.press_browse_framepath)
        self.framepath_sizer.Add(self.framepath_browse, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.framepath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.tracker_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tracker_text = wx.StaticText(self.panel, label="Choose tracker:")
        self.tracker_sizer.Add(tracker_text, 0,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.tracker_choice = wx.Choice(self.panel, id=wx.ID_ANY,
                                        choices=TRACKERS,
                                        style=wx.CB_SORT)
        self.tracker_sizer.Add(self.tracker_choice, 0,
                               wx.LEFT | wx.RIGHT | wx.CENTER, 10)
        self.main_sizer.Add(self.tracker_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.subject_sizer = wx.BoxSizer(wx.HORIZONTAL)
        subject_text = wx.StaticText(self.panel, label="Tracking subject:")
        self.subject_sizer.Add(subject_text, 0,
                               wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.subject_input = wx.TextCtrl(self.panel)
        self.subject_sizer.Add(self.subject_input, 1,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.subject_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(self.main_sizer)
        self.Show()

        self.params = dict()
        self.status = ""

    def press_browse_framepath(self, event):
        """ Handle method triggered when input path Browse button is pressed.

        Launch a file browser to select the input files (multiple selection).
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Source frames", "", "",
                                "PNG files (*.png)|*.png",
                                wx.FD_OPEN | wx.FD_MULTIPLE |
                                wx.FD_FILE_MUST_EXIST)
        browser.ShowModal()
        self.params["frame_path"] = browser.GetPaths()
        browser.Destroy()
        self.framepath_input.SetValue(",".join(self.params["frame_path"]))

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Launch the Bounding Boxes Tracker with the chosen paths.
        The window is closed when the Tracker has run succesfully.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.params["frame_path"] = sorted(self.framepath_input.GetValue().
                                           split(","))
        self.params["tracker"] = self.tracker_choice.GetStringSelection()
        self.params["subject"] = self.subject_input.GetValue()

        if not self.params["frame_path"] or not self.params["subject"]:
            print(f"[ERROR] You didn't enter anything!\n")
        else:
            print(f'[INFO] Input frames: {", ".join(self.params["frame_path"])}'
                  f'\n')
            self.status = track_bbox_v2(**self.params)
            if self.status == "done":
                print(f"[INFO] Tracking has been completed!\n")
                self.Close()
            elif self.status == "error":
                print(f"[ERROR] An error occurred during tracking.\n")
                self.Close()


class AttributesSetUpFrame(wx.Frame):
    """ Window for setting up the input parameters to the Attributes Manager.

    Input: observation file exported from BORIS.
    Output: file with subjects and corresponding attributes. Only output
    directory is chosen, file name is generated automatically.
    Use: choose input and output paths, then press "Apply". No field can be
    left empty.

    :var self.params: dict
        Parameters introduced by the user (BORIS data/output paths).
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="Attributes Manager - PAD suite"):
        """ Create frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str
            Frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(500, 200))

        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.borispath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        borispath_text = wx.StaticText(self.panel,
                                       label="Path to source BORIS file:")
        self.borispath_sizer.Add(borispath_text, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.borispath_input = wx.TextCtrl(self.panel)
        self.borispath_sizer.Add(self.borispath_input, 1,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.borispath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.borispath_browse.Bind(wx.EVT_BUTTON, self.press_browse_borispath)
        self.borispath_sizer.Add(self.borispath_browse, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.borispath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.attribpath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        attribpath_text = wx.StaticText(self.panel,
                                        label="Path to save TSV file to:")
        self.attribpath_sizer.Add(attribpath_text, 0,
                                  wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.attribpath_input = wx.TextCtrl(self.panel)
        self.attribpath_sizer.Add(self.attribpath_input, 1,
                                  wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.attribpath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.attribpath_browse.Bind(wx.EVT_BUTTON,
                                    self.press_browse_attribpath)
        self.attribpath_sizer.Add(self.attribpath_browse, 0,
                                  wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.attribpath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(self.main_sizer)
        self.Show()

        self.params = dict()

    def press_browse_borispath(self, event):
        """ Handle method triggered when input path Browse button is pressed.

        Launch a file browser to select the input file (single selection).
        Selected path is stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Source BORIS file", "", "",
                                "TSV files (*.tsv)|*.tsv",
                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        browser.ShowModal()
        self.params["boris_path"] = browser.GetPath()
        browser.Destroy()
        self.borispath_input.SetValue(self.params["boris_path"])

    def press_browse_attribpath(self, event):
        """ Handle method triggered when output path Browse button is pressed.

        Launch a file browser to select the output path directory.
        Selected path is stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.DirDialog(self, "Output directory", "",
                               wx.DD_NEW_DIR_BUTTON)
        browser.ShowModal()
        self.params["attrib_path"] = browser.GetPath()
        browser.Destroy()
        self.attribpath_input.SetValue(self.params["attrib_path"])

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Launch the Attributes Manager with the chosen arguments, after
        extracting the subjects from the BORIS file.
        The window is closed when the Manager has run succesfully.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.params["boris_path"] = self.borispath_input.GetValue()
        self.params["attrib_path"] = self.attribpath_input.GetValue()
        if not self.params["boris_path"] or not self.params["attrib_path"]:
            print(f"[ERROR] You didn't enter anything!\n")
        else:
            print(f'[INFO] Input BORIS file: {self.params["boris_path"]}')
            print(f'[INFO] utput TSV path: {self.params["attrib_path"]} \n')
            self.params["subjects"] = get_subjects(**self.params)
            if len(self.params["subjects"]) > 0:
                print(f'[INFO] Subjects have been extracted! '
                      f'{", ".join(self.params["subjects"])} \n')
                AttributesFrame(None, wx.ID_ANY,
                                "Attributes Manager - PAD suite", **self.params)
                self.Close()


class AttributesFrame(wx.Frame):
    """ Window for matching attributes to corresponding subjects.

    Use: choose a subject and tick the corresponding attributes, then press
    "Apply". Repeat as many times as subjects. It is not possible to set
    attributes twice for the same subject.

    :var self.subjects: list
        Subjects from BORIS file.
    :var self.subject_idx: int
        Index of the chosen subject in the pull-down menu.
    :var self.attribs: list
        Attributes to be set as affirmative.
    :var self.params: dict
        Parameters introduced by the user (BORIS data/output paths).
    :var self.status: str
        Register if the Attributes Manager has run succesfully.
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="Attributes Manager - PAD suite", **kwargs):
        """ Create frame, using inheritance.

        :param fr_parent: parent frame, if any.
        :param fr_id: frame wxID, if any.
        :param fr_title: frame title, to be displayed as window name.
        :param kwargs: input parameters (input and output paths).
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(600, 700))
        self.subject = []
        self.subject_idx = []
        self.attribs = []
        self.params = kwargs

        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.subj_sizer = wx.BoxSizer(wx.HORIZONTAL)
        subj_text = wx.StaticText(self.panel, label="Choose subject:")
        self.subj_sizer.Add(subj_text, 0, wx.LEFT | wx.TOP, 10)
        self.subj_choice = wx.Choice(self.panel, id=wx.ID_ANY,
                                     choices=self.params["subjects"],
                                     style=wx.CB_SORT)
        self.subj_sizer.Add(self.subj_choice, 0,
                            wx.LEFT | wx.TOP | wx.RIGHT, 10)

        attrib_text = wx.StaticText(self.panel, label="Choose attributes:")
        self.subj_sizer.Add(attrib_text, 0, wx.LEFT | wx.TOP, 10)
        self.attrib_choice = wx.CheckListBox(self.panel,
                                             choices=ATTRIBUTES)
        self.subj_sizer.Add(self.attrib_choice, 1, wx.ALL | wx.EXPAND, 10)
        self.main_sizer.Add(self.subj_sizer, 1, wx.ALL, 10)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        self.panel.SetSizer(self.main_sizer)
        self.Show()
        self.status = ""

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Reads the chosen subject and attributes, and passes them for the file
        to be written.
        Print message when attributes have been set succesfully.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.subject = self.subj_choice.GetStringSelection()
        self.attribs = list(self.attrib_choice.GetCheckedStrings())
        self.status = set_attributes(self.subject, self.attribs, **self.params)
        if self.status == "done":
            print(f"[INFO] Attributes have been set!\n")


class DataFusionFrame(wx.Frame):
    """"""
    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="Data Fusion - PAD suite"):
        """ Create frame, using inheritance.

        :param fr_parent: parent frame, if any.
        :param fr_id: frame wxID, if any.
        :param fr_title: frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(600, 250))

        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.borispath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        borispath_text = wx.StaticText(self.panel,
                                       label="Path to source BORIS file:")
        self.borispath_sizer.Add(borispath_text, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.borispath_input = wx.TextCtrl(self.panel)
        self.borispath_sizer.Add(self.borispath_input, 1,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.borispath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.borispath_browse.Bind(wx.EVT_BUTTON, self.press_browse_borispath)
        self.borispath_sizer.Add(self.borispath_browse, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.borispath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.clippath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        clippath_text = wx.StaticText(self.panel, label="Source clip:")
        self.clippath_sizer.Add(clippath_text, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.clippath_input = wx.TextCtrl(self.panel)
        self.clippath_sizer.Add(self.clippath_input, 1,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.clippath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.clippath_browse.Bind(wx.EVT_BUTTON, self.press_browse_clippath)
        self.clippath_sizer.Add(self.clippath_browse, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.clippath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.fusionpath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        fusionpath_text = wx.StaticText(self.panel, label="Output clip:")
        self.fusionpath_sizer.Add(fusionpath_text, 0,
                                  wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.fusionpath_input = wx.TextCtrl(self.panel)
        self.fusionpath_sizer.Add(self.fusionpath_input, 1,
                                  wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.fusionpath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.fusionpath_browse.Bind(wx.EVT_BUTTON,
                                    self.press_browse_fusionpath)
        self.fusionpath_sizer.Add(self.fusionpath_browse, 0,
                                  wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.fusionpath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(self.main_sizer)
        self.Show()

        self.params = dict()
        self.status = ""

    def press_browse_borispath(self, event):
        """ Handle method triggered when input path Browse button is pressed.

        Launch a file browser to select the input file (single selection).
        Selected path is stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Source BORIS file", "", "",
                                "TSV files (*.tsv)|*.tsv",
                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        browser.ShowModal()
        self.params["boris_path"] = browser.GetPath()
        browser.Destroy()
        self.borispath_input.SetValue(self.params["boris_path"])

    def press_browse_clippath(self, event):
        """ Handle method triggered when input path Browse button is pressed.

        Launch a file browser to select the input file (single selection).
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Source clip", "", "",
                                "Video files (*.avi; *.mp4)|*.avi;*.mp4",
                                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        browser.ShowModal()
        self.params["clip_path"] = browser.GetPath()
        browser.Destroy()
        self.clippath_input.SetValue(self.params["clip_path"])

    def press_browse_fusionpath(self, event):
        """ Handle method triggered when output path Browse button is pressed.

        Launch a file browser to select the path to the output file.
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Output clip", "", "",
                                "AVI files (*.avi)|*.avi",
                                wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        browser.ShowModal()
        self.params["fusion_path"] = browser.GetPath()
        browser.Destroy()
        self.fusionpath_input.SetValue(self.params["fusion_path"])

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Launch the Data Fusion with the chosen paths.
        The window is closed when the Converter has run succesfully.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.params["boris_path"] = self.borispath_input.GetValue()
        self.params["clip_path"] = self.clippath_input.GetValue()
        self.params["fusion_path"] = self.fusionpath_input.GetValue()
        if not self.params["boris_path"] or not self.params["clip_path"] or \
                not self.params["fusion_path"]:
            print(f"[ERROR] You didn't enter anything! \n")
        else:
            print(f'[INFO] Input BORIS file: {self.params["boris_path"]}')
            print(f'[INFO] Input clip: {self.params["clip_path"]}')
            print(f'[INFO] Output clip: {self.params["fusion_path"]}\n')
            self.status = data_fusion(**self.params)
            if self.status == "done":
                print(f'[INFO] Behavioral video is ready!\n')
                self.Close()


class YOLOFrame(wx.Frame):
    """ Window for setting up the parameters to perform YOLO analysis with.

    Input: PNG frames to perform YOLO on,
            path to save annotated frames to,
            directory containing YOLO-COCO data,
            detection thershold,
            non-maxima supression threshold.
    Output: annotated PNG frames,
             TSV file with bounding box data.
    Use: ain't it obvious man? just throw in the frames and config files, then
          sit and chill for just a bit...

    :var self.params: dict
        Parameters introduced by the user (frames/output/config path,
         detection/non-maxima supression threshold).
    :var self.status: str
        Register if the Bounding Box Remover has run succesfully.
    """

    def __init__(self, fr_parent=None, fr_id=wx.ID_ANY,
                 fr_title="YOLO! - PAD suite"):
        """ Create frame, using inheritance.

        :param fr_parent: frame
            Parent frame, if any.
        :param fr_id: wxID
            Frame wxID, if any.
        :param fr_title: str
            Frame title, to be displayed as window name.
        """

        super().__init__(fr_parent, fr_id, fr_title, size=(600, 350))
        self.panel = wx.Panel(self)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.framepath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        framepath_text = wx.StaticText(self.panel,
                                       label="Give me sum frames!:")
        self.framepath_sizer.Add(framepath_text, 0,
                                 wx.RIGHT | wx.LEFT | wx.TOP, 10)
        self.framepath_input = wx.TextCtrl(self.panel)
        self.framepath_sizer.Add(self.framepath_input, 1,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.framepath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.framepath_browse.Bind(wx.EVT_BUTTON, self.press_browse_framepath)
        self.framepath_sizer.Add(self.framepath_browse, 0,
                                 wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.framepath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.bboxpath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bboxpath_text = wx.StaticText(self.panel, label="Place to save stuff:")
        self.bboxpath_sizer.Add(bboxpath_text, 0,
                                wx.RIGHT | wx.LEFT | wx.TOP, 10)
        self.bboxpath_input = wx.TextCtrl(self.panel)
        self.bboxpath_sizer.Add(self.bboxpath_input, 1,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.bboxpath_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.bboxpath_browse.Bind(wx.EVT_BUTTON, self.press_browse_bboxpath)
        self.bboxpath_sizer.Add(self.bboxpath_browse, 0,
                                wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.bboxpath_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.yolo_sizer = wx.BoxSizer(wx.HORIZONTAL)
        yolo_text = wx.StaticText(self.panel,
                                  label="weights, classes,... ya know:")
        self.yolo_sizer.Add(yolo_text, 0, wx.RIGHT | wx.LEFT | wx.TOP, 10)
        self.yolo_input = wx.TextCtrl(self.panel)
        self.yolo_sizer.Add(self.yolo_input, 1,
                            wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.yolo_browse = wx.Button(self.panel, id=wx.ID_FIND)
        self.yolo_browse.Bind(wx.EVT_BUTTON, self.press_browse_yolo)
        self.yolo_sizer.Add(self.yolo_browse, 0,
                            wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.yolo_sizer, 1, wx.ALL | wx.EXPAND, 10)

        self.confid_sizer = wx.BoxSizer(wx.HORIZONTAL)
        confid_text = wx.StaticText(self.panel,
                                    label="How high the standards?:")
        self.confid_sizer.Add(confid_text, 0, wx.RIGHT | wx.LEFT, 10)
        self.confid_input = wx.SpinCtrl(self.panel, id=wx.ID_ANY,
                                        style=wx.SP_ARROW_KEYS |
                                        wx.ALIGN_RIGHT,
                                        min=0, max=100)
        self.confid_sizer.Add(self.confid_input, 1, wx.RIGHT | wx.LEFT, 10)
        confid_pc = wx.StaticText(self.panel, id=wx.ID_ANY, label="%")
        self.confid_sizer.Add(confid_pc, 0, wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.confid_sizer, 0, wx.ALL, 10)

        self.thresh_sizer = wx.BoxSizer(wx.HORIZONTAL)
        thresh_text = wx.StaticText(self.panel,
                                    label="things on top of things?")
        self.thresh_sizer.Add(thresh_text, 0,
                              wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.thresh_input = wx.SpinCtrl(self.panel, id=wx.ID_ANY,
                                        style=wx.SP_ARROW_KEYS |
                                        wx.ALIGN_RIGHT,
                                        min=0, max=100)
        self.thresh_sizer.Add(self.thresh_input, 1,
                              wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        thresh_pc = wx.StaticText(self.panel, id=wx.ID_ANY, label="%")
        self.thresh_sizer.Add(thresh_pc, 0, wx.RIGHT | wx.LEFT | wx.CENTER, 10)
        self.main_sizer.Add(self.thresh_sizer, 0, wx.ALL, 10)

        self.apply_btn = wx.Button(self.panel, id=wx.ID_APPLY,
                                   label="DO IT ALREADY, DAWG!")
        self.apply_btn.Bind(wx.EVT_BUTTON, self.press_apply)
        self.main_sizer.Add(self.apply_btn, 0, wx.ALL | wx.CENTER, 10)

        self.panel.SetSizer(self.main_sizer)
        self.Show()

        self.params = dict()
        self.status = ""

    def press_browse_framepath(self, event):
        """ Handle method triggered when input frames path Browse button is
         pressed.

        Launch a file browser to select the input files (multiple selection).
        Selected paths are stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.FileDialog(self, "Source images", "", "",
                                "Image files (*.png)|*.png",
                                wx.FD_OPEN | wx.FD_MULTIPLE |
                                wx.FD_FILE_MUST_EXIST)
        browser.ShowModal()
        self.params["frame_path"] = browser.GetPaths()
        browser.Destroy()
        self.framepath_input.SetValue(",".join(self.params["frame_path"]))

    def press_browse_bboxpath(self, event):
        """ Handle method triggered when output data path Browse button is
         pressed.

        Launch a file browser to select the output directory.
        Selected path is stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.DirDialog(self, "Output path", "", wx.DD_NEW_DIR_BUTTON)
        browser.ShowModal()
        self.params["bbox_path"] = browser.GetPath()
        browser.Destroy()
        self.bboxpath_input.SetValue(self.params["bbox_path"])

    def press_browse_yolo(self, event):
        """ Handle method triggered when config files path Browse button is
         pressed.

        Launch a file browser to select the config files directory.
        Selected path is stored and displayed in the Input field.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        browser = wx.DirDialog(self, "Path to YOLO data", "",
                               wx.DD_DIR_MUST_EXIST)
        browser.ShowModal()
        self.params["yolo_path"] = browser.GetPath()
        browser.Destroy()
        self.yolo_input.SetValue(self.params["yolo_path"])

    def press_apply(self, event):
        """ Handle method triggered when Apply button is pressed.

        Read values for thresholds.
        Launch YOLO with the chosen paths.
        The window is closed when YOLO has run succesfully.

        :param event: action that triggers the method. Automatically generated.
        :return: nothing.
        """

        self.params["frame_path"] = self.framepath_input.GetValue().split(",")
        self.params["bbox_path"] = self.bboxpath_input.GetValue()
        self.params["yolo_path"] = self.yolo_input.GetValue()
        self.params["confidence"] = self.confid_input.GetValue()/100
        self.params["threshold"] = self.thresh_input.GetValue()/100
        if not self.params["frame_path"] or not self.params["bbox_path"] \
                or not self.params["yolo_path"] \
                or not self.params["confidence"] \
                or not self.params["threshold"]:
            print(f"[ERROR] You didn't enter anything! \n")
        else:
            print(f'[INFO] Input media: '
                  f'{", ".join(self.params["frame_path"])}')
            print(f'[INFO] Output path: {self.params["bbox_path"]}')
            print(f'[INFO] Detection confidence: {self.params["confidence"]}')
            print(f'[INFO] Non-maxima supression threshold: '
                  f'{self.params["threshold"]} \n')
            self.status = run_yolo3(**self.params)
            if self.status == "done":
                print(f"\n[INFO] YOLO is already done, dawg!\n")
                self.Close()


def get_resolution():
    monis = get_monitors()
    id1 = str(monis[0]).find("(")
    id2 = str(monis[0]).find("x")
    id3 = str(monis[0]).find("+")
    disp_width = int(str(monis[0])[id1+1:id2])
    disp_height = int(str(monis[0])[id2+1:id3])
    return disp_width, disp_height


if __name__ == "__main__":
    app = wx.App()
    mainMenu = MainFrame(None, wx.ID_ANY, "Main menu - PAD suite")
    app.MainLoop()
