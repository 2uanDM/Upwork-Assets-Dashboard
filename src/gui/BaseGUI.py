
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtWidgets import QWidget
import json
import os

# Import the css json
css_path = os.path.join(os.getcwd(), 'assets', 'css', 'css.json')
with open(css_path, "r", encoding='utf8') as f:
    css_dict = json.load(f)


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()


class BaseGUI(QWidget):
    def __init__(self, MainWindow) -> None:
        """
            The setup function must be called sequentially, or else the UI will not be setup properly
        Args:
            MainWindow (QStackedWidget): The main window
        """
        super(BaseGUI, self).__init__()
        self.main_window = MainWindow
        self.css = css_dict

        # ------------------- Setup Fonts -------------------
        self.setup_fonts()
        # ------------------- Setup Main Frame -------------------
        self.setup_main_frame()
        # ------------------- Setup Content Frame -------------------
        self.setup_content_frame()
        # ------------------- Setup Master Table -------------------
        self.setup_master_table()
        # ------------------- Setup Detail Table -------------------

        # Retranslate Ui
        self.retranslate_base_ui()

    def retranslate_base_ui(self):
        self.app_name.setText(QCoreApplication.translate("Form", u"ROCKET\nPROJECT", None))
        self.asset_catalogue_button.setText(QCoreApplication.translate("Form", u"Asset catalogue", None))
        self.main_label.setText(QCoreApplication.translate("Form", u"ASSET CATALOGUE", None))
        self.asset_list_label.setText(QCoreApplication.translate("Form", u"ASSET LIST", None))
        self.filter_label.setText(QCoreApplication.translate("Form", u"Filter", None))
        self.number_input.setText(QCoreApplication.translate("Form", u"11", None))
        self.search_input.setText(QCoreApplication.translate("Form", u"office", None))
        self.apply_filter_button.setText(QCoreApplication.translate("Form", u"Apply Filter", None))

        # -- Master Table --
        ___qtablewidgetitem = self.master_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Image", None))
        ___qtablewidgetitem = self.master_table.horizontalHeaderItem(1)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Asset#", None))
        ___qtablewidgetitem1 = self.master_table.horizontalHeaderItem(2)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Asset name", None))
        ___qtablewidgetitem2 = self.master_table.horizontalHeaderItem(3)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Category", None))

    def setup_fonts(self):
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
        self.filter_label_font.setWeight(70)

        self.font_for_table_header = QFont()
        self.font_for_table_header.setFamily(u"Segoe UI")
        self.font_for_table_header.setPointSize(13)
        self.font_for_table_header.setBold(True)
        self.font_for_table_header.setWeight(68)

    def setup_main_frame(self):
        self.menu_frame = QFrame(self)
        self.menu_frame.setObjectName(u"menu_frame")
        self.menu_frame.setGeometry(QRect(0, 0, 241, 901))
        self.menu_frame.setStyleSheet(u"background-color: rgb(218, 218, 218)")
        self.menu_frame.setFrameShape(QFrame.StyledPanel)
        self.menu_frame.setFrameShadow(QFrame.Raised)

        self.app_name = QLabel(self.menu_frame)
        self.app_name.setObjectName(u"app_name")
        self.app_name.setGeometry(QRect(20, 10, 141, 101))
        self.app_name.setFont(self.project_name_font)
        self.app_name.setStyleSheet(u"color:rgb(69, 119, 185)")

        self.asset_catalogue_button = QPushButton(self.menu_frame)
        self.asset_catalogue_button.setObjectName(u"asset_catalogue_button")
        self.asset_catalogue_button.setGeometry(QRect(0, 150, 241, 61))
        self.asset_catalogue_button.setFont(self.view_button_font)
        self.asset_catalogue_button.setLayoutDirection(Qt.LeftToRight)
        self.asset_catalogue_button.setStyleSheet(self.css.get('asset_catalogue_button'))

        self.catalogue_icon = QLabel(self.menu_frame)
        self.catalogue_icon.setObjectName(u"catalogue_icon")
        self.catalogue_icon.setGeometry(QRect(20, 160, 41, 41))
        self.catalogue_icon.setStyleSheet(u"background-color:rgb(241, 241, 241)")
        self.catalogue_icon.setPixmap(QPixmap(os.path.join(os.getcwd(), "assets", "catalogue.png")))

    def setup_content_frame(self):
        self.content_frame = QFrame(self)
        self.content_frame.setObjectName(u"content_frame")
        self.content_frame.setGeometry(QRect(240, 0, 1571, 901))
        self.content_frame.setStyleSheet(u"background-color:rgb(255, 255, 255)")
        self.content_frame.setFrameShape(QFrame.StyledPanel)
        self.content_frame.setFrameShadow(QFrame.Raised)

        self.main_label = QLabel(self.content_frame)
        self.main_label.setObjectName(u"main_label")
        self.main_label.setGeometry(QRect(30, 10, 291, 51))
        self.main_label.setFont(self.main_label_font)
        self.main_label.setStyleSheet(u"color:rgb(69, 119, 185)")

    def setup_master_table(self):
        self.asset_list_label = QLabel(self.content_frame)
        self.asset_list_label.setObjectName(u"asset_list_label")
        self.asset_list_label.setGeometry(QRect(30, 60, 131, 41))
        self.asset_list_label.setFont(self.sub_header_font)
        self.asset_list_label.setStyleSheet(u"color:rgb(69, 119, 185)")

        self.filter_label = QLabel(self.content_frame)
        self.filter_label.setObjectName(u"filter_label")
        self.filter_label.setGeometry(QRect(100, 120, 51, 31))
        self.filter_label.setFont(self.filter_label_font)
        self.filter_label.setStyleSheet(u"color:rgb(89, 89, 89)")

        self.number_input = QLineEdit(self.content_frame)
        self.number_input.setObjectName(u"number_input")
        self.number_input.setGeometry(QRect(160, 120, 91, 31))
        self.number_input.setFont(self.filter_label_font)
        self.number_input.setStyleSheet(self.css.get('number_input'))
        self.number_input.setAlignment(Qt.AlignCenter)

        self.search_input = QLineEdit(self.content_frame)
        self.search_input.setObjectName(u"search_input")
        self.search_input.setGeometry(QRect(260, 120, 241, 31))
        self.search_input.setFont(self.filter_label_font)
        self.search_input.setStyleSheet(self.css.get('search_input'))

        self.apply_filter_button = QPushButton(self.content_frame)
        self.apply_filter_button.setObjectName(u"apply_filter_button")
        self.apply_filter_button.setGeometry(QRect(520, 120, 151, 31))
        self.apply_filter_button.setFont(self.filter_label_font)
        self.apply_filter_button.setLayoutDirection(Qt.LeftToRight)
        self.apply_filter_button.setStyleSheet(self.css.get('apply_filter_button'))

        # ------------------- Master Table -------------------
        self.master_table = QTableWidget(self.content_frame)
        self.master_table.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.master_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.master_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.master_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.master_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)

        self.master_table.setObjectName(u"master_table")
        self.master_table.setGeometry(QRect(20, 160, 681, 701))
        self.master_table.setStyleSheet(self.css.get('master_table'))
        self.master_table.verticalHeader().setVisible(False)
        # Add below line of the horizontal header

        # CSS for the header
        header = self.master_table.horizontalHeader()
        header.setStyleSheet(
            "QHeaderView::section {background-color: rgb(231, 231, 231); color: rgb(69, 119, 185); border: 1.5px solid rgb(89, 89, 89); border-top: none; border-left: none; border-right: none;padding: 3px;}"
        )

        header.setDefaultSectionSize(150)
        header.setDefaultAlignment(Qt.AlignLeft)
        header.setFont(self.font_for_table_header)
        header.setFixedHeight(35)
        self.master_table.setColumnWidth(2, 227)
        # Set border to the table
        self.master_table.setFrameShape(QFrame.StyledPanel)
        self.master_table.setFrameShadow(QFrame.Raised)
        self.master_table.setLineWidth(1)
        self.master_table.setMidLineWidth(0)

    def setup_detail_table(self):
        pass
