
import typing
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QStyleOptionViewItem, QWidget
from src.utils.database_crud import CrudDB
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


class QComboBoxDelegate(QStyledItemDelegate):
    """
        This class is used to create a combobox in a specific cell of the table
    Args:
        options (list): The list of options for the combobox
        target_row (int): The row where the combobox should be applied
        target_column (int): The column where the combobox should be applied
    """

    def __init__(self, options: list, target_row: int, target_column: int, parent):
        super().__init__(parent)
        self.options = options
        self.target_row = target_row
        self.target_column = target_column

    def createEditor(self, parent, option, index) -> QWidget:
        row = index.row()
        column = index.column()

        # Specify the desired cell where the delegate should be applied
        if row == self.target_row and column == self.target_column:
            editor = QComboBox(parent)
            editor.addItems(self.options)
            return editor
        else:
            return super().createEditor(parent, option, index)  # Use the default editor for other cells

    def setEditorData(self, editor, index) -> None:
        current_text = index.model().data(index, Qt.EditRole)
        # If the editor is a QComboBox, this will select the current text
        if isinstance(editor, QComboBox):
            editor.setCurrentText(current_text)
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index) -> None:
        if isinstance(editor, QComboBox):
            model.setData(index, editor.currentText(), Qt.EditRole)
        else:
            super().setModelData(editor, model, index)


class BaseGUI(QWidget):
    buttons_path = os.path.join(os.getcwd(), 'assets', 'buttons')

    def __init__(self, MainWindow) -> None:
        """
            The setup function must be called sequentially, or else the UI will not be setup properly
        Args:
            MainWindow (QStackedWidget): The main window
        """
        super(BaseGUI, self).__init__()
        self.main_window = MainWindow
        self.css = css_dict

        # ------------------- Connect the database -------------------
        self.db = CrudDB()

        # ------------------- Setup Fonts -------------------
        self.setup_fonts()
        # ------------------- Setup Main Frame -------------------
        self.setup_main_frame()
        # ------------------- Setup Content Frame -------------------
        self.setup_content_frame()
        # ------------------- Setup Master Table -------------------
        self.setup_master_table()
        # ------------------- Setup Detail Table -------------------
        self.setup_detail_table()
        # ------------------- Setup Attribute Table -------------------
        self.setup_attribute_table()
        # ------------------- Setup Shape Table -------------------
        self.setup_shape_table()
        # ------------------- Setup Media Frame -------------------
        self.setup_media_frame()
        # ------------------- Setup CRUD buttons -------------------
        self.setup_crud_asset_detail_buttons()
        self.setup_crud_attribute_buttons()
        self.setup_crud_shape_buttons()
        self.setup_crud_media_buttons()
        # ------------------- Setup sort buttons -------------------
        self.setup_sort_button()

        # Retranslate Ui
        self.retranslate_base_ui()

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

        self.font_for_page_label = QFont()
        self.font_for_page_label.setFamily(u"Segoe UI")
        self.font_for_page_label.setPointSize(14)
        self.font_for_page_label.setBold(False)
        self.font_for_page_label.setWeight(50)

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
        self.catalogue_icon.setPixmap(QPixmap(os.path.join(os.getcwd(), "assets", "icon", "catalogue.png")))

    def setup_content_frame(self):
        self.content_frame = QFrame(self)
        self.content_frame.setObjectName(u"content_frame")
        self.content_frame.setGeometry(QRect(240, 0, 1591, 901))
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
        self.number_input.setPlaceholderText("Asset #")

        self.search_input = QLineEdit(self.content_frame)
        self.search_input.setObjectName(u"search_input")
        self.search_input.setGeometry(QRect(260, 120, 241, 31))
        self.search_input.setFont(self.filter_label_font)
        self.search_input.setStyleSheet(self.css.get('search_input'))
        self.search_input.setPlaceholderText("Asset name")

        self.apply_filter_button = QPushButton(self.content_frame)
        self.apply_filter_button.setObjectName(u"apply_filter_button")
        self.apply_filter_button.setGeometry(QRect(520, 120, 151, 31))
        self.apply_filter_button.setFont(self.filter_label_font)
        self.apply_filter_button.setLayoutDirection(Qt.LeftToRight)
        self.apply_filter_button.setStyleSheet(self.css.get('apply_filter_button'))

        # ------------------- Master Table -------------------
        self.master_table = QTableWidget(self.content_frame)
        self.master_table.setColumnCount(4)
        self.master_table.setRowCount(10)

        __qtablewidgetitem = QTableWidgetItem()
        self.master_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.master_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.master_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.master_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)

        self.master_table.setObjectName(u"master_table")
        self.master_table.setGeometry(QRect(20, 160, 681, 691))
        self.master_table.setStyleSheet(self.css.get('master_table'))
        self.master_table.verticalHeader().setVisible(False)

        # CSS for the header
        header = self.master_table.horizontalHeader()
        header.setStyleSheet(
            "QHeaderView::section {background-color: rgb(231, 231, 231); color: rgb(69, 119, 185); border: 1.5px solid rgb(89, 89, 89); border-top: none; border-left: none; border-right: 1px solid rgb(89, 89, 89); padding: 3px;}"
        )

        header.setDefaultSectionSize(150)
        header.setDefaultAlignment(Qt.AlignLeft)
        header.setFont(self.font_for_table_header)
        header.setFixedHeight(35)

        # Other properties
        self.master_table.setColumnWidth(2, 227)
        for i in range(10):
            self.master_table.setRowHeight(i, 65)  # Set the height of the rows
        # When click on a cell of a row in the master table, it will choose the whole row
        self.master_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Cannot edit the cells
        self.master_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # --================== Pagination ==================--
        self.page_label = QLabel(self.content_frame)
        self.page_label.setObjectName(u"page_label")
        self.page_label.setGeometry(QRect(160, 859, 191, 31))
        self.page_label.setText("Page 1/1")
        self.page_label.setFont(self.font_for_page_label)
        self.page_label.setStyleSheet(u"color:rgb(89, 89, 89)")
        self.page_label.setAlignment(Qt.AlignCenter)

        # --================== Previous button ==================--
        self.previous_page_button = ClickableLabel(self.content_frame)
        self.previous_page_button.setObjectName(u"previous_page_button")
        self.previous_page_button.setGeometry(QRect(130, 860, 31, 31))
        self.previous_page_button.setPixmap(QPixmap(os.path.join(self.buttons_path, "previous.png")))

        # --================== Next button ==================--
        self.next_page_button = ClickableLabel(self.content_frame)
        self.next_page_button.setObjectName(u"next_page_button")
        self.next_page_button.setGeometry(QRect(350, 860, 31, 31))
        self.next_page_button.setPixmap(QPixmap(os.path.join(self.buttons_path, "next.png")))

        # --================== Download catalogue button ==================--
        self.download_catalogue_button = QPushButton(self.content_frame)
        self.download_catalogue_button.setObjectName(u"download_catalogue_button")
        self.download_catalogue_button.setGeometry(QRect(500, 860, 201, 31))
        self.download_catalogue_button.setFont(self.filter_label_font)
        self.download_catalogue_button.setLayoutDirection(Qt.LeftToRight)
        self.download_catalogue_button.setStyleSheet(self.css.get('apply_filter_button'))
        self.download_catalogue_button.setText("Download catalogue")

    def setup_detail_table(self):
        self.asset_detail_label = QLabel(self.content_frame)
        self.asset_detail_label.setObjectName(u"asset_detail_label")
        self.asset_detail_label.setGeometry(QRect(720, 10, 171, 41))
        self.asset_detail_label.setFont(self.sub_header_font)
        self.asset_detail_label.setStyleSheet(u"color:rgb(69, 119, 185)")

        self.asset_detail_table = QTableWidget(self.content_frame)
        self.asset_detail_table.setColumnCount(2)
        self.asset_detail_table.setRowCount(7)

        # Hide the horizontal header
        self.asset_detail_table.horizontalHeader().hide()
        self.asset_detail_table.verticalHeader().hide()

        # Set the width of column
        self.asset_detail_table.setColumnWidth(0, 150)
        self.asset_detail_table.setColumnWidth(1, 630)

        # First row: Asset number and Asset Name
        self.asset_number_item = QTableWidgetItem()
        self.asset_number_item.setBackground(QColor(231, 231, 231))  # Set your desired background color
        self.asset_number_item.setFont(QFont('Segoe UI', 14, 68))
        self.asset_number_item.setTextAlignment(Qt.AlignCenter)
        self.asset_number_item.setForeground(QColor(69, 119, 185))
        self.asset_detail_table.setItem(0, 0, self.asset_number_item)

        self.asset_name_item = QTableWidgetItem()
        self.asset_name_item.setBackground(QColor(231, 231, 231))
        self.asset_name_item.setFont(QFont('Segoe UI', 14, 68))
        self.asset_name_item.setTextAlignment(Qt.AlignCenter)
        self.asset_name_item.setForeground(QColor(69, 119, 185))
        self.asset_detail_table.setItem(0, 1, self.asset_name_item)

        # Second row: Asset variant and its value
        self.asset_variant_item = QTableWidgetItem()
        self.asset_variant_item.setText("Asset variant")
        self.asset_variant_item.setTextAlignment(Qt.AlignCenter)
        self.asset_variant_item.setFlags(self.asset_variant_item.flags() & ~Qt.ItemIsEditable)
        self.asset_detail_table.setItem(1, 0, self.asset_variant_item)

        self.asset_variant_value_item = QTableWidgetItem()
        self.asset_variant_value_item.setText("")
        self.asset_detail_table.setItem(1, 1, self.asset_variant_value_item)

        # Third row: Asset category and its value
        self.asset_category_item = QTableWidgetItem()
        self.asset_category_item.setText("Asset category")
        self.asset_category_item.setTextAlignment(Qt.AlignCenter)
        self.asset_category_item.setFlags(self.asset_category_item.flags() & ~Qt.ItemIsEditable)
        self.asset_detail_table.setItem(2, 0, self.asset_category_item)

        self.asset_category_value_item = QComboBoxDelegate(
            options=self.db.get_list_of_asset_categories(),
            target_row=2,
            target_column=1,
            parent=self.asset_detail_table
        )
        self.asset_detail_table.setItemDelegateForRow(2, self.asset_category_value_item)

        # Fourth row: Description and its value
        self.asset_description_item = QTableWidgetItem()
        self.asset_description_item.setText("Description")
        self.asset_description_item.setTextAlignment(Qt.AlignCenter)
        self.asset_description_item.setFlags(self.asset_description_item.flags() & ~Qt.ItemIsEditable)
        self.asset_detail_table.setItem(3, 0, self.asset_description_item)

        self.asset_description_value_item = QTableWidgetItem()
        self.asset_description_value_item.setText("")
        self.asset_detail_table.setItem(3, 1, self.asset_description_value_item)

        # Change the height of the fourth row
        self.asset_detail_table.setRowHeight(3, 120)

        # Fifth row: Importlist header and its value
        self.import_list_header_item = QTableWidgetItem()
        self.import_list_header_item.setText("Importlist header")
        self.import_list_header_item.setTextAlignment(Qt.AlignCenter)
        self.import_list_header_item.setFlags(self.import_list_header_item.flags() & ~Qt.ItemIsEditable)
        self.asset_detail_table.setItem(4, 0, self.import_list_header_item)

        self.import_list_header_value_item = QTableWidgetItem()
        self.import_list_header_value_item.setText("")
        self.asset_detail_table.setItem(4, 1, self.import_list_header_value_item)

        # Sixth row: Importlist 2nd row and its value
        self.import_list_2nd_row_item = QTableWidgetItem()
        self.import_list_2nd_row_item.setText("Importlist 2nd row")
        self.import_list_2nd_row_item.setTextAlignment(Qt.AlignCenter)
        self.import_list_2nd_row_item.setFlags(self.import_list_2nd_row_item.flags() & ~Qt.ItemIsEditable)
        self.asset_detail_table.setItem(5, 0, self.import_list_2nd_row_item)

        self.import_list_2nd_row_value_item = QTableWidgetItem()
        self.import_list_2nd_row_value_item.setText("")
        self.asset_detail_table.setItem(5, 1, self.import_list_2nd_row_value_item)

        # Seventh row: Importlist 3rd row and its value
        self.import_list_3rd_row_item = QTableWidgetItem()
        self.import_list_3rd_row_item.setText("Importlist 3rd row")
        self.import_list_3rd_row_item.setTextAlignment(Qt.AlignCenter)
        self.import_list_3rd_row_item.setFlags(self.import_list_3rd_row_item.flags() & ~Qt.ItemIsEditable)
        self.asset_detail_table.setItem(6, 0, self.import_list_3rd_row_item)

        self.import_list_3rd_row_value_item = QTableWidgetItem()
        self.import_list_3rd_row_value_item.setText("")
        self.asset_detail_table.setItem(6, 1, self.import_list_3rd_row_value_item)

        # Other properties
        self.asset_detail_table.setObjectName(u"asset_detail_table")
        self.asset_detail_table.setGeometry(QRect(720, 60, 801, 271))
        self.asset_detail_table.setStyleSheet(self.css.get('master_table'))

    def setup_attribute_table(self):
        self.attribute_table = QTableWidget(self.content_frame)
        self.attribute_table.setColumnCount(4)
        self.attribute_table.verticalHeader().hide()

        attribute_order_number_item = QTableWidgetItem()
        attribute_order_number_item.setText("#")
        self.attribute_table.setHorizontalHeaderItem(0, attribute_order_number_item)

        attribute_name_item = QTableWidgetItem()
        attribute_name_item.setText("Attribute")
        self.attribute_table.setHorizontalHeaderItem(1, attribute_name_item)

        attribute_date_type_item = QTableWidgetItem()
        attribute_date_type_item.setText("Datatype")
        self.attribute_table.setHorizontalHeaderItem(2, attribute_date_type_item)

        attribute_remarks_item = QTableWidgetItem()
        attribute_remarks_item.setText("Remarks")
        self.attribute_table.setHorizontalHeaderItem(3, attribute_remarks_item)

        # Other properties
        self.attribute_table.setObjectName(u"attribute_table")
        self.attribute_table.setGeometry(QRect(720, 340, 801, 191))
        self.attribute_table.setStyleSheet(self.css.get('master_table'))

        # CSS for the header
        header = self.attribute_table.horizontalHeader()
        header.setStyleSheet(
            "QHeaderView::section {background-color: rgb(231, 231, 231); color: rgb(69, 119, 185); border: 1.5px solid rgb(89, 89, 89); border-top: none; border-left: none;border-right: 1px solid rgb(89, 89, 89); padding: 3px;}"
        )
        header.setDefaultSectionSize(150)
        header.setDefaultAlignment(Qt.AlignLeft)
        header.setFont(self.font_for_table_header)
        header.setFixedHeight(35)
        # Change the width of the columns
        self.attribute_table.setColumnWidth(0, 67)
        self.attribute_table.setColumnWidth(1, 200)
        self.attribute_table.setColumnWidth(2, 120)
        self.attribute_table.setColumnWidth(3, 410)

    def setup_shape_table(self):
        self.shape_table = QTableWidget(self.content_frame)
        self.shape_table.setColumnCount(3)
        self.shape_table.verticalHeader().hide()

        shape_order_number_item = QTableWidgetItem()
        shape_order_number_item.setText("#")
        self.shape_table.setHorizontalHeaderItem(0, shape_order_number_item)

        shape_name_item = QTableWidgetItem()
        shape_name_item.setText("Shape")
        self.shape_table.setHorizontalHeaderItem(1, shape_name_item)

        shape_description_item = QTableWidgetItem()
        shape_description_item.setText("Description")
        self.shape_table.setHorizontalHeaderItem(2, shape_description_item)

        # Other properties
        self.shape_table.setObjectName(u"shape_table")
        self.shape_table.setGeometry(QRect(720, 540, 801, 151))
        self.shape_table.setStyleSheet(self.css.get('master_table'))

        # CSS for the header
        header = self.shape_table.horizontalHeader()
        header.setStyleSheet(
            "QHeaderView::section {background-color: rgb(231, 231, 231); color: rgb(69, 119, 185); border: 1.5px solid rgb(89, 89, 89); border-top: none; border-left: none;border-right: 1px solid rgb(89, 89, 89); padding: 3px;}"
        )
        header.setDefaultSectionSize(150)
        header.setDefaultAlignment(Qt.AlignLeft)
        header.setFont(self.font_for_table_header)
        header.setFixedHeight(35)
        # Change the width of the columns
        self.shape_table.setColumnWidth(0, 67)
        self.shape_table.setColumnWidth(1, 150)
        self.shape_table.setColumnWidth(2, 580)

    def setup_media_frame(self):
        self.media_frame = QFrame(self.content_frame)
        self.media_frame.setObjectName(u"media_frame")
        self.media_frame.setGeometry(QRect(720, 700, 801, 151))
        self.media_frame.setStyleSheet(self.css.get('media_frame'))

        # Horizontal layout
        self.horizontalLayoutWidget = QWidget(self.media_frame)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(9, 10, 781, 131))

        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 0, 0, 0)

        # --================== Download dataset button ==================--
        self.download_dataset_button = QPushButton(self.content_frame)
        self.download_dataset_button.setObjectName(u"download_dataset_button")
        self.download_dataset_button.setGeometry(QRect(1320, 860, 201, 31))
        self.download_dataset_button.setFont(self.filter_label_font)
        self.download_dataset_button.setLayoutDirection(Qt.LeftToRight)
        self.download_dataset_button.setStyleSheet(self.css.get('apply_filter_button'))
        self.download_dataset_button.setText("Download dataset")

    def setup_crud_asset_detail_buttons(self):
        # Add asset button
        self.crud_add_asset_button = ClickableLabel(self.content_frame)
        self.crud_add_asset_button.setObjectName(u"crud_add_asset_button")
        self.crud_add_asset_button.setGeometry(QRect(1529, 80, 21, 21))
        self.crud_add_asset_button.setPixmap(QPixmap(os.path.join(self.buttons_path, 'add.png')))

        # Save/Update asset button
        self.crud_save_asset_button = ClickableLabel(self.content_frame)
        self.crud_save_asset_button.setObjectName(u"crud_save_asset_button")
        self.crud_save_asset_button.setGeometry(QRect(1526, 115, 26, 21))
        self.crud_save_asset_button.setPixmap(QPixmap(os.path.join(self.buttons_path, 'update.png')))

        # Delete asset button
        self.crud_delete_asset_button = ClickableLabel(self.content_frame)
        self.crud_delete_asset_button.setObjectName(u"crud_delete_asset_button")
        self.crud_delete_asset_button.setGeometry(QRect(1530, 150, 19, 21))
        self.crud_delete_asset_button.setPixmap(QPixmap(os.path.join(self.buttons_path, 'delete.png')))

    def setup_crud_attribute_buttons(self):
        # Add attribute button
        self.crud_add_attribute_button = ClickableLabel(self.content_frame)
        self.crud_add_attribute_button.setObjectName(u"crud_add_attribute_button")
        self.crud_add_attribute_button.setGeometry(QRect(1529, 350, 21, 21))
        self.crud_add_attribute_button.setPixmap(QPixmap(os.path.join(self.buttons_path, 'add.png')))

        # Save/Update attribute button
        self.crud_save_attribute_button = ClickableLabel(self.content_frame)
        self.crud_save_attribute_button.setObjectName(u"crud_save_attribute_button")
        self.crud_save_attribute_button.setGeometry(QRect(1526, 385, 26, 21))
        self.crud_save_attribute_button.setPixmap(QPixmap(os.path.join(self.buttons_path, 'update.png')))

        # Delete attribute button
        self.crud_delete_attribute_button = ClickableLabel(self.content_frame)
        self.crud_delete_attribute_button.setObjectName(u"crud_delete_attribute_button")
        self.crud_delete_attribute_button.setGeometry(QRect(1530, 420, 19, 21))
        self.crud_delete_attribute_button.setPixmap(QPixmap(os.path.join(self.buttons_path, 'delete.png')))

    def setup_crud_shape_buttons(self):
        self.crud_add_shape_button = ClickableLabel(self.content_frame)
        self.crud_add_shape_button.setObjectName(u"crud_add_shape_button")
        self.crud_add_shape_button.setGeometry(QRect(1529, 540, 21, 21))
        self.crud_add_shape_button.setPixmap(QPixmap(QPixmap(os.path.join(self.buttons_path, 'add.png'))))

        self.crud_save_shape_button = ClickableLabel(self.content_frame)
        self.crud_save_shape_button.setObjectName(u"crud_save_shape_button")
        self.crud_save_shape_button.setGeometry(QRect(1526, 575, 26, 21))
        self.crud_save_shape_button.setPixmap(QPixmap(QPixmap(os.path.join(self.buttons_path, 'update.png'))))

        self.crud_delete_shape_button = ClickableLabel(self.content_frame)
        self.crud_delete_shape_button.setObjectName(u"crud_delete_shape_button")
        self.crud_delete_shape_button.setGeometry(QRect(1530, 610, 19, 21))
        self.crud_delete_shape_button.setPixmap(QPixmap(QPixmap(os.path.join(self.buttons_path, 'delete.png'))))

    def setup_crud_media_buttons(self):
        self.crud_add_media_button = ClickableLabel(self.content_frame)
        self.crud_add_media_button.setObjectName(u"crud_add_media_button")
        self.crud_add_media_button.setGeometry(QRect(1529, 720, 21, 21))
        self.crud_add_media_button.setPixmap(QPixmap(os.path.join(self.buttons_path, 'add.png')))

        self.crud_delete_media_button = ClickableLabel(self.content_frame)
        self.crud_delete_media_button.setObjectName(u"crud_delete_media_button")
        self.crud_delete_media_button.setGeometry(QRect(1530, 760, 19, 21))
        self.crud_delete_media_button.setPixmap(QPixmap(os.path.join(self.buttons_path, 'delete.png')))

    def setup_sort_button(self):
        # ------------------- Master Table -------------------

        # --================== Sort by asset number button ==================--
        self.sort_asc_asset_number_button = ClickableLabel(self.content_frame)
        self.sort_asc_asset_number_button.setObjectName(u"sort_asc_asset_number_button")
        self.sort_asc_asset_number_button.setGeometry(QRect(306, 170, 13, 14))
        self.sort_asc_asset_number_button.setStyleSheet(u"background-color: rgb(231, 231, 231);")
        self.sort_asc_asset_number_button.setPixmap(QPixmap(os.path.join(self.buttons_path, 'asc.png')))

        self.sort_desc_asset_number_button = ClickableLabel(self.content_frame)
        self.sort_desc_asset_number_button.setObjectName(u"sort_desc_asset_number_button")
        self.sort_desc_asset_number_button.setGeometry(QRect(290, 170, 13, 14))
        self.sort_desc_asset_number_button.setStyleSheet(u"background-color: rgb(231, 231, 231);")
        self.sort_desc_asset_number_button.setPixmap(QPixmap(os.path.join(self.buttons_path, 'desc.png')))

        # --================== Sort by asset name button ==================--
        self.sort_desc_asset_name_button = ClickableLabel(self.content_frame)
        self.sort_desc_asset_name_button.setObjectName(u"sort_desc_asset_name_button")
        self.sort_desc_asset_name_button.setGeometry(QRect(514, 170, 13, 14))
        self.sort_desc_asset_name_button.setStyleSheet(u"background-color: rgb(231, 231, 231);")
        self.sort_desc_asset_name_button.setPixmap(QPixmap(os.path.join(self.buttons_path, 'desc.png')))

        self.sort_asc_asset_name_button = ClickableLabel(self.content_frame)
        self.sort_asc_asset_name_button.setObjectName(u"sort_asc_asset_name_button")
        self.sort_asc_asset_name_button.setGeometry(QRect(530, 170, 13, 14))
        self.sort_asc_asset_name_button.setStyleSheet(u"background-color: rgb(231, 231, 231);")
        self.sort_asc_asset_name_button.setPixmap(QPixmap(os.path.join(self.buttons_path, 'asc.png')))

        # --================== Sort by category button ==================--
        self.sort_desc_asset_category_button = ClickableLabel(self.content_frame)
        self.sort_desc_asset_category_button.setObjectName(u"sort_desc_asset_category_button")
        self.sort_desc_asset_category_button.setGeometry(QRect(664, 170, 13, 14))
        self.sort_desc_asset_category_button.setStyleSheet(u"background-color: rgb(231, 231, 231);")
        self.sort_desc_asset_category_button.setPixmap(QPixmap(os.path.join(self.buttons_path, 'desc.png')))

        self.sort_asc_asset_category_button = ClickableLabel(self.content_frame)
        self.sort_asc_asset_category_button.setObjectName(u"sort_asc_asset_category_button")
        self.sort_asc_asset_category_button.setGeometry(QRect(680, 170, 13, 14))
        self.sort_asc_asset_category_button.setStyleSheet(u"background-color: rgb(231, 231, 231);")
        self.sort_asc_asset_category_button.setPixmap(QPixmap(os.path.join(self.buttons_path, 'asc.png')))

        # ------------------- Attribute Table -------------------
        self.sort_asc_att_number_button = ClickableLabel(self.content_frame)
        self.sort_asc_att_number_button.setObjectName(u"sort_asc_att_number_button")
        self.sort_asc_att_number_button.setGeometry(QRect(806 - 40, 350, 13, 14))
        self.sort_asc_att_number_button.setStyleSheet(u"background-color: rgb(231, 231, 231);")
        self.sort_asc_att_number_button.setPixmap(QPixmap(os.path.join(self.buttons_path, 'asc.png')))

        self.sort_desc_att_number_button = ClickableLabel(self.content_frame)
        self.sort_desc_att_number_button.setObjectName(u"sort_desc_att_number_button")
        self.sort_desc_att_number_button.setGeometry(QRect(790 - 40, 350, 13, 14))
        self.sort_desc_att_number_button.setStyleSheet(u"background-color: rgb(231, 231, 231);")
        self.sort_desc_att_number_button.setPixmap(QPixmap(os.path.join(self.buttons_path, 'desc.png')))

    def retranslate_base_ui(self):
        self.app_name.setText(QCoreApplication.translate("Form", u"ROCKET\nPROJECT", None))
        self.asset_catalogue_button.setText(QCoreApplication.translate("Form", u"Asset catalogue", None))
        self.main_label.setText(QCoreApplication.translate("Form", u"ASSET CATALOGUE", None))
        self.asset_list_label.setText(QCoreApplication.translate("Form", u"ASSET LIST", None))
        self.filter_label.setText(QCoreApplication.translate("Form", u"Filter", None))
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

        # -- Detail Table --
        self.asset_detail_label.setText(QCoreApplication.translate("Form", u"ASSET DETAIL", None))

    def test_action(self):
        print('Button clicked')
