from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os
sys.path.append(os.path.join(os.getcwd()))


class AddImageGUI(QWidget):
    add_image_signal = pyqtSignal(str, str)

    def __init__(self, asset_name: str, image_categories: list, MainWindow) -> None:
        super().__init__(MainWindow)
        self.MainWindow = MainWindow
        self.asset_name: str = asset_name
        self.image_categories: list = image_categories
        self.resize(721, 417)
        self.setWindowTitle(u"Add Image")

        self.frame = QFrame(self)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(-40, -10, 781, 501))
        self.frame.setStyleSheet(u"background-color: white")

        self.setup_font()
        self.add_frame()
        self.add_labels()
        self.image_path()
        self.choose_category()
        self.add_image_button()

    def setup_font(self):
        self.font = QFont()
        self.font.setFamily(u"Segoe UI")
        self.font.setPointSize(16)
        self.font.setBold(False)
        self.font.setWeight(50)

        self.font1 = QFont()
        self.font1.setFamily(u"Segoe UI")
        self.font1.setPointSize(14)
        self.font1.setBold(False)
        self.font1.setWeight(50)

        self.font2 = QFont()
        self.font2.setFamily(u"Segoe UI")
        self.font2.setPointSize(14)
        self.font2.setBold(True)
        self.font2.setWeight(75)

    def add_frame(self):
        self.frame = QFrame(self)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(-40, -10, 781, 501))
        self.frame.setStyleSheet(u"background-color: white")

    def add_labels(self):
        self.main_label = QLabel(self.frame)
        self.main_label.setObjectName(u"main_label")
        self.main_label.setGeometry(QRect(60, 30, 681, 31))
        self.main_label.setFont(self.font)
        self.main_label.setStyleSheet(u"color:rgb(69, 119, 185)")
        self.main_label.setText(f'Add new image for asset: "{self.asset_name}"')

        self.image_path_label = QLabel(self.frame)
        self.image_path_label.setObjectName(u"image_path_label")
        self.image_path_label.setGeometry(QRect(60, 100, 121, 31))
        self.image_path_label.setFont(self.font)
        self.image_path_label.setStyleSheet(u"color:rgb(69, 119, 185)")
        self.image_path_label.setText(u"Image path:")

        self.category_label = QLabel(self.frame)
        self.category_label.setObjectName(u"category_label")
        self.category_label.setGeometry(QRect(60, 180, 161, 31))
        self.category_label.setFont(self.font)
        self.category_label.setStyleSheet(u"color:rgb(69, 119, 185)")
        self.category_label.setText(u"Image category:")

    def image_path(self):
        self.path_input = QLineEdit(self.frame)
        self.path_input.setObjectName(u"path_input")
        self.path_input.setGeometry(QRect(220, 102, 481, 31))
        self.path_input.setFont(self.font1)
        self.path_input.setStyleSheet(u"QLineEdit {\n"
                                      "	border: 1px solid black;\n"
                                      "    padding-left: 5px;\n"
                                      "    color: rgb(89, 89, 89);\n"
                                      "}\n"
                                      "")
        self.path_input.setReadOnly(True)

        self.path_button = QToolButton(self.frame)
        self.path_button.setObjectName(u"path_button")
        self.path_button.setGeometry(QRect(701, 102, 27, 31))
        self.path_button.setStyleSheet(u"background-color: rgb(130, 130, 130);\n"
                                       "color: white")
        self.path_button.setText(u"...")
        self.path_button.clicked.connect(self.open_file_dialog)

    def choose_category(self):
        self.comboBox = QComboBox(self.frame)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(220, 180, 481, 31))
        self.comboBox.setFont(self.font1)
        self.comboBox.setStyleSheet(u"border: 1px solid black;\n"
                                    "padding-left: 5px;\n"
                                    "color: rgb(89, 89, 89);")
        self.comboBox.addItems(self.image_categories)

    def add_image_button(self):
        self.add_image_button = QPushButton(self.frame)
        self.add_image_button.setObjectName(u"add_image_button")
        self.add_image_button.setGeometry(QRect(330, 310, 121, 41))
        self.add_image_button.setFont(self.font2)
        self.add_image_button.setStyleSheet(u"/* Normal state styles */\n"
                                            "QPushButton {\n"
                                            "    color: rgb(69, 119, 185);\n"
                                            "    border: 2px solid rgb(241, 241, 241);\n"
                                            "    border-radius: 10px;\n"
                                            "    background-color: rgb(241, 241, 241);\n"
                                            "}\n"
                                            "\n"
                                            "/* Hover state styles */\n"
                                            "QPushButton:hover {\n"
                                            "    color: white;\n"
                                            "    background-color: darkgray;\n"
                                            "}\n"
                                            "")

        self.add_image_button.setText(u"Add")
        self.add_image_button.clicked.connect(self.add_image)

    def open_file_dialog(self):
        # Open browse pictures dialog with native OS file browser
        image_path = QFileDialog.getOpenFileName(self,
                                                 caption='Choose Image',
                                                 directory='c:\\',
                                                 filter="Image files (*.jpg *.png *.jpeg)")
        if image_path[0]:
            self.path_input.setText(image_path[0])

    def add_image(self):
        image_path = self.path_input.text().strip()
        image_category = self.comboBox.currentText()
        self.add_image_signal.emit(image_path, image_category)
        self.close()
