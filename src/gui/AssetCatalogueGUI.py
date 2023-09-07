from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os
sys.path.append(os.path.join(os.getcwd()))

from src.gui.BaseGUI import BaseGUI
from src.gui.MessageBoxDialog import MessageBox as msg


class AssetCatelogueGUI(BaseGUI):
    def __init__(self, MainWindow) -> None:
        super().__init__(MainWindow)
        self.current_page = 1
        self.current_asset_id = None

        # Initial data from the database
        self.reload_master_table_data_after_crud()
        # Initially, the data in the table is the assets data when the filter is not applied
        self.table_data = self.assets_data
        # Load the master table
        self.load_master_table(self.current_page)

        # Crud buttons
        self.crud_add_asset_button.clicked.connect(self.crud_add_asset_event)
        self.crud_save_asset_button.clicked.connect(self.crud_save_asset_event)
        self.crud_delete_asset_button.clicked.connect(self.crud_delete_asset_event)

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

        # Sort buttons
        self.sort_asc_asset_number_button.clicked.connect(self.sort_asc_asset_number_button_event)
        self.sort_desc_asset_number_button.clicked.connect(self.sort_desc_asset_number_button_event)

        self.sort_asc_asset_name_button.clicked.connect(self.sort_asc_asset_name_button_event)
        self.sort_desc_asset_name_button.clicked.connect(self.sort_desc_asset_name_button_event)

        self.sort_asc_asset_category_button.clicked.connect(self.sort_asc_asset_category_button_event)
        self.sort_desc_asset_category_button.clicked.connect(self.sort_desc_asset_category_button_event)

        self.sort_desc_att_number_button.clicked.connect(self.test_action)
        self.sort_asc_att_number_button.clicked.connect(self.test_action)

        # Cell of master table clicked
        self.master_table.cellClicked.connect(self.master_table_row_clicked_event)

        # Apply filter button
        self.apply_filter_button.clicked.connect(self.apply_filter_button_event)

    def reload_asset_detail_table(self):
        self.asset_number_item.setText("")
        self.asset_name_item.setText("")
        self.asset_variant_value_item.setText("")
        self.asset_description_value_item.setText("")
        self.import_list_header_value_item.setText("")
        self.import_list_2nd_row_value_item.setText("")
        self.import_list_3rd_row_value_item.setText("")

        # Qcombobox
        self.asset_detail_table.setItem(2, 1, QTableWidgetItem(""))

        # Current Asset ID
        self.current_asset_id = None

    def reload_master_table_data_after_crud(self):
        data: dict = self.db.load_master_table()
        self.total_assets = data['total_assets']
        self.total_pages = data['total_pages']
        self.assets_data = data['data']

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

        self.reload_asset_detail_table()

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

            # Get the asset id
            self.current_asset_id = self.db.get_asset_id(int(asset_number), asset_name, asset_category_name)
            print('Current AssetID: ', self.current_asset_id)
            # Get the asset detail
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
            self.asset_detail_table.setItem(2, 1, QTableWidgetItem(asset_category_name))
            # Set the asset description
            self.asset_description_value_item.setText(asset_detail[1])
            # Set the import list header
            self.import_list_header_value_item.setText(asset_detail[2])
            # Set the import list 2nd row
            self.import_list_2nd_row_value_item.setText(asset_detail[3])
            # Set the import list 3rd row
            self.import_list_3rd_row_value_item.setText(asset_detail[4])

    def apply_filter_button_event(self):
        # Get the filter value (number)
        asset_number_filter = self.number_input.text()
        # Get the filter value (name)
        asset_name_filter = self.search_input.text().lower()

        # Apply the filter
        filtered_data = []
        for asset in self.assets_data:
            asset_number = str(asset[0])
            asset_name = asset[1].lower()

            asset_number_cond: bool = True if \
                (asset_number.find(asset_number_filter) != -1 or asset_number_filter == "") else False

            asset_name_cond: bool = True if \
                (asset_name.find(asset_name_filter) != -1 or asset_name_filter == "") else False

            if asset_number_cond and asset_name_cond:
                filtered_data.append(asset)

        self.table_data = filtered_data
        self.total_assets = len(filtered_data)
        self.total_pages = self.total_assets // 10 + 1 if self.total_assets % 10 != 0 else self.total_assets // 10
        self.current_page = 1
        self.load_master_table(self.current_page)

    def _sort_master_table(self, column: int, sort_type: str):
        """
            This is a support function for handle sort button event of master table
        Args:
            column (int): The column to sort in master table: 

            - 0: Asset number
            - 1: Asset name
            - 2: Asset category

            sort_type (str): "asc" or "desc"
        """
        self.table_data.sort(key=lambda x: x[column], reverse=True if sort_type == "desc" else False)

        # Then reload the master table
        self.current_page = 1
        self.load_master_table(self.current_page)

    def sort_asc_asset_number_button_event(self):
        self._sort_master_table(0, "asc")

    def sort_desc_asset_number_button_event(self):
        self._sort_master_table(0, "desc")

    def sort_asc_asset_name_button_event(self):
        self._sort_master_table(1, "asc")

    def sort_desc_asset_name_button_event(self):
        self._sort_master_table(1, "desc")

    def sort_asc_asset_category_button_event(self):
        self._sort_master_table(2, "asc")

    def sort_desc_asset_category_button_event(self):
        self._sort_master_table(2, "desc")

    #######################################################################################################################################

    def crud_delete_asset_event(self):
        # Get the asset number and name
        asset_number = self.asset_number_item.text()
        asset_name = self.asset_name_item.text()
        asset_category_name = self.asset_detail_table.item(2, 1).text()

        if asset_number == "" or asset_name == "" or asset_category_name == "":
            msg.warning_box("Please select an asset to delete!")
            return

        user_choice = msg.yes_no_box("Are you sure to delete this asset? This action cannot be undone!")
        if user_choice == QMessageBox.No:
            return

        # Delete the asset
        success = self.db.delete_asset(int(asset_number), asset_name, asset_category_name)

        if not success:
            msg.warning_box("Error occurred when deleting this asset!")
            return
        # Reload the master table
        self.reload_master_table_data_after_crud()
        self.table_data = self.assets_data
        self.total_assets = len(self.table_data)
        self.total_pages = self.total_assets // 10 + 1 if self.total_assets % 10 != 0 else self.total_assets // 10
        self.current_page = 1
        self.load_master_table(self.current_page)
        self.apply_filter_button.click()
        self.reload_asset_detail_table()

        msg.information_box("Delete asset successfully!")

    def crud_save_asset_event(self):
        user_choice = msg.yes_no_box("Are you sure to save changes of this asset?")
        if user_choice == QMessageBox.No:
            return
        # Get the current asset information
        asset_number = self.asset_number_item.text()
        asset_name = self.asset_name_item.text()
        asset_category_name = self.asset_detail_table.item(2, 1).text()
        asset_variant = self.asset_variant_value_item.text()
        asset_description = self.asset_description_value_item.text()
        import_list_header = self.import_list_header_value_item.text()
        import_list_2nd_row = self.import_list_2nd_row_value_item.text()
        import_list_3rd_row = self.import_list_3rd_row_value_item.text()

        # Update the Asset table
        success = self.db.update_asset_table(self.current_asset_id,
                                             int(asset_number),
                                             asset_name,
                                             asset_variant,
                                             self.db.get_category_id(asset_category_name),
                                             asset_description)

        if not success:
            msg.warning_box("Error occurred when updating information in 'Asset' table!")
            return

        # Update the AssetImportList table
        success = self.db.update_asset_import_list(self.current_asset_id,
                                                   import_list_header,
                                                   import_list_2nd_row,
                                                   import_list_3rd_row)
        if not success:
            msg.warning_box("Error occurred when updating information in 'AssetImportList' table!")
            return

        # Reload the master table
        self.reload_master_table_data_after_crud()
        self.table_data = self.assets_data
        self.total_assets = len(self.table_data)
        self.total_pages = self.total_assets // 10 + 1 if self.total_assets % 10 != 0 else self.total_assets // 10
        self.current_page = 1
        self.load_master_table(self.current_page)
        self.apply_filter_button.click()
        self.reload_asset_detail_table()

        msg.information_box("Save asset information successfully!")

    def crud_add_asset_event(self):
        # Clear filter input
        self.number_input.setText("")
        self.search_input.setText("")
        self.apply_filter_button.click()

        # Move to the last page
        if self.total_assets % 10 == 0:
            self.total_pages += 1
            self.current_page = self.total_pages
            self.load_master_table(self.current_page)
        else:
            self.current_page = self.total_pages
            self.load_master_table(self.current_page)

        print('The new row to insert in master table is: ', len(self.assets_data) % 10 + 1)

        # Create a new asset
        success = self.db.create_new_asset()
        if not success:
            msg.warning_box("Error occurred when creating a new asset!")
            return

        # Reload the master table
        self.reload_master_table_data_after_crud()
        self.table_data = self.assets_data
        self.total_assets = len(self.table_data)
        self.total_pages = self.total_assets // 10 + 1 if self.total_assets % 10 != 0 else self.total_assets // 10
        self.current_page = self.total_pages
        self.load_master_table(self.current_page)
        self.reload_asset_detail_table()
