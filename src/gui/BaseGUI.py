
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from abc import abstractmethod

from PyQt5.QtWidgets import QWidget


class BaseGUI(QWidget):
    def __init__(self, MainWindow) -> None:
        super(BaseGUI, self).__init__()
        self.main_window = MainWindow

        # ------------------- Font -------------------
        self.project_name_font = QFont()
        self.project_name_font = QFont()
        self.project_name_font.setFamily(u"Segoe UI")
        self.project_name_font.setPointSize(18)
        self.project_name_font.setBold(True)
        self.project_name_font.setWeight(75)

        self.view_button_font = QFont()
        self.view_button_font.setFamily(u"Segoe UI")
        self.view_button_font.setPointSize(16)

        self.main_label_font = QFont()
        self.main_label_font.setFamily(u"Segoe UI")
        self.main_label_font.setPointSize(24)
        self.main_label_font.setBold(True)
        self.main_label_font.setWeight(75)

        self.sub_header_font = QFont()
        self.sub_header_font.setFamily(u"Segoe UI")
        self.sub_header_font.setPointSize(20)
        self.sub_header_font.setBold(False)
        self.sub_header_font.setWeight(50)

        self.filter_label_font = QFont()
        self.filter_label_font.setFamily(u"Segoe UI")
        self.filter_label_font.setPointSize(14)
        self.filter_label_font.setBold(True)
        self.filter_label_font.setWeight(60)

        # ------------------- Frame -------------------
        self.menu_frame = QFrame(self)
        self.menu_frame.setObjectName(u"menu_frame")
        self.menu_frame.setGeometry(QRect(0, 0, 241, 901))
        self.menu_frame.setStyleSheet(u"background-color: rgb(218, 218, 218)")
        self.menu_frame.setFrameShape(QFrame.StyledPanel)
        self.menu_frame.setFrameShadow(QFrame.Raised)

        self.content_frame = QFrame(self)
        self.content_frame.setObjectName(u"content_frame")
        self.content_frame.setGeometry(QRect(240, 0, 1571, 901))
        self.content_frame.setStyleSheet(u"background-color:rgb(255, 255, 255)")
        self.content_frame.setFrameShape(QFrame.StyledPanel)
        self.content_frame.setFrameShadow(QFrame.Raised)
