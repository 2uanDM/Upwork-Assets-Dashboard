from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os
sys.path.append(os.path.join(os.getcwd()))

from src.gui.BaseGUI import BaseGUI
from src.utils.database_crud import CrudDB


class AssetCatelogueGUI(BaseGUI):
    def __init__(self, MainWindow) -> None:
        super().__init__(MainWindow)
        self.current_page = 1

        # Init the database
        self.db = CrudDB()
        self.reload_master_table_data_after_crud()
        self.load_master_table(self.current_page)

        # Crud buttons
        self.crud_add_asset_button.clicked.connect(self.test_action)
        self.crud_save_asset_button.clicked.connect(self.test_action)
        self.crud_delete_asset_button.clicked.connect(self.test_action)

        self.crud_add_attribute_button.clicked.connect(self.test_action)
        self.crud_save_attribute_button.clicked.connect(self.test_action)
        self.crud_delete_attribute_button.clicked.connect(self.test_action)

        self.crud_add_shape_button.clicked.connect(self.test_action)
        self.crud_save_shape_button.clicked.connect(self.test_action)
        self.crud_delete_shape_button.clicked.connect(self.test_action)

        self.crud_add_media_button.clicked.connect(self.test_action)
        self.crud_delete_media_button.clicked.connect(self.test_action)

        # Buttons for master table
        self.previous_page_button.clicked.connect(self.previous_page_button_event)
        self.next_page_button.clicked.connect(self.next_page_button_event)

        # Download buttons
        self.download_catalogue_button.clicked.connect(self.test_action)
        self.download_dataset_button.clicked.connect(self.test_action)

        # Cell of master table clicked
        self.master_table.cellClicked.connect(self.master_table_row_clicked_event)

    def reload_master_table_data_after_crud(self):
        data: dict = self.db.load_master_table()
        self.total_assets = data['total_assets']
        self.total_pages = data['total_pages']
        self.table_data = data['data']

    def load_master_table(self, page: int):
        # Clear the table
        self.master_table.clearContents()

        # Renew the page label
        self.page_label.setText(f"Page {self.current_page} of {self.total_pages}")

        # Load the data (still not handle the image so j -> j+1)
        if self.total_assets == 0:
            return

        data = self.table_data[(page - 1) * 10: page * 10]
        for i, row in enumerate(data):
            for j, column in enumerate(row):
                self.master_table.setItem(i, j + 1, QTableWidgetItem(str(column)))

    def next_page_button_event(self):
        # Renew the page label
        if self.current_page == self.total_pages:
            return
        self.current_page += 1
        # Load the data
        self.load_master_table(self.current_page)

    def previous_page_button_event(self):
        # Renew the page label
        if self.current_page == 1:
            return
        self.current_page -= 1
        # Load the data
        self.load_master_table(self.current_page)

    def master_table_row_clicked_event(self, row, column):
        item = self.master_table.item(row, column)
        if item:
            asset_number = self.master_table.item(row, 1).text()
            asset_name = self.master_table.item(row, 2).text()
            asset_category_name = self.master_table.item(row, 3).text()

            asset_detail: tuple = self.db.load_asset_detail_table(int(asset_number), asset_name, asset_category_name)

            if asset_detail is None:
                return

            # Set the asset number
            self.asset_number_item.setText(asset_number)
            # Set the asset name
            self.asset_name_item.setText(asset_name)
            # Set the asset variant
            self.asset_variant_value_item.setText(asset_detail[0])
            # Set the asset category
            self.asset_category_value_item.setText(asset_category_name)
            # Set the asset description
            self.asset_description_value_item.setText(asset_detail[1])
            # Set the import list header
            self.import_list_header_value_item.setText(asset_detail[2])
            # Set the import list 2nd row
            self.import_list_2nd_row_value_item.setText(asset_detail[3])
            # Set the import list 3rd row
            self.import_list_3rd_row_value_item.setText(asset_detail[4])
