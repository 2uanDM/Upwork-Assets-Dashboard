import shutil
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os
sys.path.append(os.path.join(os.getcwd()))

from src.gui.BaseGUI import BaseGUI
from src.gui.MessageBoxDialog import MessageBox as msg
from src.gui.AddImageGUI import AddImageGUI


class ClickableImage(QLabel):
    clicked = pyqtSignal(object)
    double_clicked = pyqtSignal()

    def __init__(self, parent=None):
        self.parent = parent
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # First, iterate through all the images in the horizontal layout to set the background color to white
            for i in range(self.parent.layout().count()):
                if isinstance(self.parent.layout().itemAt(i).widget(), ClickableImage):
                    self.parent.layout().itemAt(i).widget().setStyleSheet("border: none")

            # Second, set the background color of the image to rgb(89,89,89)
            self.setStyleSheet("border: 1.5px solid red")
            print(self)
            self.clicked.emit(self)

    # Handle double click event
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.double_clicked.emit()


class AssetCatelogueGUI(BaseGUI):
    icon_path: str = './assets/icon/logo.jpg'

    def __init__(self, MainWindow) -> None:
        super().__init__(MainWindow)
        self.current_page = 1
        self.current_asset_id = None
        # Store the information of images of current asset (image: ClickableImage with Pixmap,'image_name', 'image_category_name')
        self.current_asset_images = None
        # Store the current clicked image (image: ClickableImage with Pixmap,'image_name', 'image_category_name')
        self.current_clicked_image: tuple = None

        # Initial data from the database
        self.reload_data_after_crud()
        # Initially, the data in the table is the assets data when the filter is not applied
        self.table_data = self.assets_data
        # Load the master table
        self.fill_in_master_table(self.current_page)

        # Crud buttons
        self.crud_add_asset_button.clicked.connect(self.crud_add_asset_event)
        self.crud_save_asset_button.clicked.connect(self.crud_save_asset_event)
        self.crud_delete_asset_button.clicked.connect(self.crud_delete_asset_event)

        self.crud_add_attribute_button.clicked.connect(self.crud_add_attribute_button_event)
        self.crud_save_attribute_button.clicked.connect(self.crud_save_attribute_button_event)
        self.crud_delete_attribute_button.clicked.connect(self.crud_delete_attribute_button_event)

        self.crud_add_shape_button.clicked.connect(self.crud_add_shape_button_event)
        self.crud_save_shape_button.clicked.connect(self.crud_save_shape_button_event)
        self.crud_delete_shape_button.clicked.connect(self.crud_delete_shape_button_event)

        self.crud_add_media_button.clicked.connect(self.crud_add_image_event)
        self.crud_delete_media_button.clicked.connect(self.crud_delete_image_event)

        # Buttons for master table
        self.previous_page_button.clicked.connect(self.previous_page_button_event)
        self.next_page_button.clicked.connect(self.next_page_button_event)

        # # Download buttons
        # self.download_catalogue_button.clicked.connect(self.test_action)
        # self.download_dataset_button.clicked.connect(self.test_action)

        # Sort buttons
        self.sort_asc_asset_number_button.clicked.connect(self.sort_asc_asset_number_button_event)
        self.sort_desc_asset_number_button.clicked.connect(self.sort_desc_asset_number_button_event)

        self.sort_asc_asset_name_button.clicked.connect(self.sort_asc_asset_name_button_event)
        self.sort_desc_asset_name_button.clicked.connect(self.sort_desc_asset_name_button_event)

        self.sort_asc_asset_category_button.clicked.connect(self.sort_asc_asset_category_button_event)
        self.sort_desc_asset_category_button.clicked.connect(self.sort_desc_asset_category_button_event)

        self.sort_desc_att_number_button.clicked.connect(self.sort_desc_att_number_button_event)
        self.sort_asc_att_number_button.clicked.connect(self.sort_asc_att_number_button_event)

        # Cell of master table clicked
        self.master_table.cellClicked.connect(self.master_table_row_clicked_event)

        # Apply filter button
        self.apply_filter_button.clicked.connect(self.apply_filter_button_event)
        self.number_input.returnPressed.connect(self.apply_filter_button_event)
        self.search_input.returnPressed.connect(self.apply_filter_button_event)

    # --====================== Reload data ======================--

    def reload_data_after_crud(self):
        data: dict = self.db.load_all_assets_data()
        self.total_assets = data['total_assets']
        self.total_pages = data['total_pages']
        self.assets_data = data['data']

    # --====================== Action for sort buttons ======================--

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
        self.fill_in_master_table(self.current_page)

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

    def _sort_attribute_table(self, column: int, sort_type: str):
        """
            This is a support function for handle sort button event of attribute table
        Args:
            column (int): The column to sort in attribute table: 

            - 0: Attribute order number
            - 1: Attribute name
            - 2: Attribute data type
            - 3: Attribute remark

            sort_type (str): "asc" or "desc"
        """
        # Get the current attribute data in the attribute table
        current_attribute_data = []
        for i in range(self.attribute_table.rowCount()):
            current_attribute_data.append([])
            for j in range(self.attribute_table.columnCount()):
                if j == 0:  # AssetAttributeOrderNumber : int
                    current_attribute_data[i].append(int(self.attribute_table.item(i, j).text()))
                else:
                    current_attribute_data[i].append(self.attribute_table.item(i, j).text())

        # Sort the current attribute data
        current_attribute_data.sort(key=lambda x: x[column], reverse=True if sort_type == "desc" else False)

        # Then reload the attribute table
        self.attribute_table.clearContents()
        self.attribute_table.setRowCount(0)

        self.attribute_table.setRowCount(len(current_attribute_data))
        for i, attribute in enumerate(current_attribute_data):
            for j, column in enumerate(attribute):
                self.attribute_table.setItem(i, j, QTableWidgetItem(str(column)))

    def sort_asc_att_number_button_event(self):
        self._sort_attribute_table(0, "asc")

    def sort_desc_att_number_button_event(self):
        self._sort_attribute_table(0, "desc")

    # --====================== Action for master table and asset details ======================--

    def next_page_button_event(self):
        # Renew the page label
        if self.current_page == self.total_pages:
            return
        self.current_page += 1
        # Load the data
        self.fill_in_master_table(self.current_page)

    def previous_page_button_event(self):
        # Renew the page label
        if self.current_page == 1:
            return
        self.current_page -= 1
        # Load the data
        self.fill_in_master_table(self.current_page)

    def master_table_row_clicked_event(self, row, column):
        item = self.master_table.item(row, column)
        if item:
            asset_number = self.master_table.item(row, 1).text()
            asset_name = self.master_table.item(row, 2).text()
            asset_category_name = self.master_table.item(row, 3).text()

            # Get the asset id
            self.current_asset_id = self.db.get_asset_id(int(asset_number), asset_name, asset_category_name)
            print('Current AssetID:', self.current_asset_id)

            # --====================== Load the asset detail table ======================--
            # Get the asset detail from the database
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

            # --====================== Fill the asset attribute table ======================--
            self.fill_attribute_table(self.current_asset_id)
            # --====================== Fill the asset shape table ======================--
            self.fill_shape_table(self.current_asset_id)
            # --====================== Fill in the media frame  ======================--
            self.fill_in_media_frame()

    def fill_in_master_table(self, page: int):
        # Clear the table
        self.master_table.clearContents()

        # Renew the page label
        self.page_label.setText(f"Page {self.current_page} of {self.total_pages}")

        # Load the text data (still not handle the image so j -> j+1)
        if self.total_assets == 0:
            return

        data = self.table_data[(page - 1) * 10: page * 10]  # Ten rows per page
        for i, row in enumerate(data):
            for j, column in enumerate(row):
                self.master_table.setItem(i, j + 1, QTableWidgetItem(str(column)))

        # Clear the asset detail table
        self.clear_asset_detail_table()
        # Clear the horizontal layout
        self.clear_the_horizontal_layout()
        # Clear the Attribute table
        self.clear_the_attribute_table()
        # Clear the Shape table
        self.clear_the_shape_table()
        # Load the image preview of assets in current pages
        self.fill_preview_image_in_master_table(page=page)

    def fill_preview_image_in_master_table(self, page: int):
        if self.total_assets == 0:
            return

        data = self.table_data[(page - 1) * 10: page * 10]  # Ten rows per page

        for i, row in enumerate(data):
            asset_number = row[0]
            asset_name = row[1]
            asset_category_name = row[2]

            # Get the asset id
            asset_id: int = self.db.get_asset_id(asset_number, asset_name, asset_category_name)

            # Get the preview image related to the asset
            preview_image_path = self.get_read_only_image_label(asset_id)
            if preview_image_path is None:
                continue
            else:
                self.master_table.setCellWidget(i, 0, preview_image_path)

    def apply_filter_button_event(self):
        # Get the filter value (number)
        asset_number_filter = self.number_input.text()
        # Get the filter value (name)
        asset_name_filter = self.search_input.text().lower()

        # If the filter is empty
        if asset_number_filter == "" and asset_name_filter == "":
            self.table_data = self.assets_data
            self.total_assets = len(self.table_data)
            self.total_pages = self.total_assets // 10 + \
                1 if (self.total_assets % 10 != 0 or self.total_assets == 0) else self.total_assets // 10
            self.current_page = 1

            self.fill_in_master_table(self.current_page)  # Reload the master table with all data
            self.clear_asset_detail_table()  # Clear the asset detail table
            self.clear_the_horizontal_layout()  # Clear the horizontal layout
            self.clear_the_attribute_table()
            self.clear_the_shape_table()
            return

        # Else apply the filter
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

        # Finally, reload the master table with the filtered data
        self.table_data = filtered_data
        self.total_assets = len(filtered_data)
        self.total_pages = self.total_assets // 10 + \
            1 if (self.total_assets % 10 != 0 or self.total_assets == 0) else self.total_assets // 10
        self.current_page = 1
        self.fill_in_master_table(self.current_page)
        self.clear_asset_detail_table()  # Clear the asset detail table
        self.clear_the_horizontal_layout()  # Clear the horizontal layout
        self.clear_the_attribute_table()
        self.clear_the_shape_table()

    def get_read_only_image_label(self, asset_id: int) -> QLabel:
        """
        Arg:
            asset_id (int): Example: 1
        Return:
            This function return a QLabel with the image_path_resized for master table read only related to the asset_id
        """
        # Get the AssetName from the database
        asset_name = self.db.get_asset_name_frome_asset_id(asset_id)

        asset_image_dir = os.path.join(self.temp_folder_path, f'{asset_id}_{asset_name}')

        if not os.path.exists(asset_image_dir):
            os.mkdir(asset_image_dir)

        has_preview_image = False
        for temp_image in os.listdir(asset_image_dir):
            if temp_image.find('^mastertable') != -1:
                has_preview_image = True
                extension = temp_image.split('.')[1]
                just_image_name = temp_image.split('.')[0]
                break

        if not has_preview_image:
            return None

        image_path_resized = os.path.join(asset_image_dir, f'{just_image_name}.{extension}')

        # Create a QLabel
        image_label = QLabel(self.horizontalLayoutWidget)
        image_label.setPixmap(QPixmap(image_path_resized))
        image_label.setAlignment(Qt.AlignCenter)

        return image_label

    def clear_asset_detail_table(self):
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

    def crud_delete_asset_event(self):
        # Get the asset number and name
        asset_number = self.asset_number_item.text()
        asset_name = self.asset_name_item.text()
        asset_category_name = self.asset_detail_table.item(2, 1).text()

        if asset_number == "" or asset_name == "" or asset_category_name == "":
            msg.warning_box("Please select an asset to delete!", icon_path=self.icon_path)
            return

        user_choice = msg.yes_no_box(
            "Are you sure to delete this asset? This action cannot be undone!", icon_path=self.icon_path)
        if user_choice == QMessageBox.No:
            return

        # Remove the asset folder in the asset pictures folder
        asset_folder_name = f'{self.current_asset_id}_{asset_name}'
        if os.path.exists(os.path.join(self.asset_pictures_path, asset_folder_name)):
            shutil.rmtree(os.path.join(self.asset_pictures_path, asset_folder_name))

        # Remove the asset folder in the temp folder
        if os.path.exists(os.path.join(self.temp_folder_path, asset_folder_name)):
            shutil.rmtree(os.path.join(self.temp_folder_path, asset_folder_name))

        # Delete the asset
        success = self.db.delete_asset(int(asset_number), asset_name, asset_category_name)

        if not success:
            msg.warning_box("Error occurred when deleting this asset!", icon_path=self.icon_path)
            return
        # Reload the master table
        self.reload_data_after_crud()
        self.table_data = self.assets_data
        self.total_assets = len(self.table_data)
        self.total_pages = self.total_assets // 10 + \
            1 if (self.total_assets % 10 != 0 or self.total_assets == 0) else self.total_assets // 10
        self.current_page = 1
        self.fill_in_master_table(self.current_page)
        self.apply_filter_button.click()
        self.clear_asset_detail_table()

        msg.information_box("Delete asset successfully!", icon_path=self.icon_path)

    def crud_save_asset_event(self):
        if self.current_asset_id is None:
            msg.warning_box("Please select an asset to update!", icon_path=self.icon_path)
            return

        # Get the name of asset in the database
        asset_name_in_database = self.db.get_asset_name_frome_asset_id(self.current_asset_id)

        if asset_name_in_database != self.asset_name_item.text():
            old_asset_folder_name = f'{self.current_asset_id}_{asset_name_in_database}'
            if not os.path.exists(os.path.join(self.asset_pictures_path, old_asset_folder_name)):
                os.mkdir(os.path.join(self.asset_pictures_path, old_asset_folder_name))

            new_asset_folder_name = f'{self.current_asset_id}_{self.asset_name_item.text()}'
            # Rename the asset folder in the asset pictures folder
            os.rename(os.path.join(self.asset_pictures_path, old_asset_folder_name),
                      os.path.join(self.asset_pictures_path, new_asset_folder_name))

            # Rename the asset folder in the temp folder
            os.rename(os.path.join(self.temp_folder_path, old_asset_folder_name),
                      os.path.join(self.temp_folder_path, new_asset_folder_name))

        # Get the current asset information
        asset_number = self.asset_number_item.text()
        asset_name = self.asset_name_item.text()
        asset_category_name = self.asset_detail_table.item(2, 1).text()
        asset_variant = self.asset_variant_value_item.text()
        asset_description = self.asset_description_value_item.text()
        import_list_header = self.import_list_header_value_item.text()
        import_list_2nd_row = self.import_list_2nd_row_value_item.text()
        import_list_3rd_row = self.import_list_3rd_row_value_item.text()

        if not asset_number.isdigit():
            msg.warning_box("Asset number must be a number!", icon_path=self.icon_path)
            return

        user_choice = msg.yes_no_box("Are you sure to save changes of this asset?", icon_path=self.icon_path)
        if user_choice == QMessageBox.No:
            return

        # Update the Asset table
        success = self.db.update_asset_table(self.current_asset_id,
                                             int(asset_number),
                                             asset_name,
                                             asset_variant,
                                             self.db.get_category_id(asset_category_name),
                                             asset_description)

        if not success:
            msg.warning_box("Error occurred when updating information in 'Asset' table!", icon_path=self.icon_path)
            return

        # Update the AssetImportList table
        success = self.db.update_asset_import_list(self.current_asset_id,
                                                   import_list_header,
                                                   import_list_2nd_row,
                                                   import_list_3rd_row)
        if not success:
            msg.warning_box("Error occurred when updating information in 'AssetImportList' table!",
                            icon_path=self.icon_path)
            return

        # Reload the master table
        self.reload_data_after_crud()
        self.table_data = self.assets_data
        self.total_assets = len(self.table_data)
        self.total_pages = self.total_assets // 10 + \
            1 if (self.total_assets % 10 != 0 or self.total_assets == 0) else self.total_assets // 10
        self.current_page = 1
        self.fill_in_master_table(self.current_page)
        self.apply_filter_button.click()
        self.clear_asset_detail_table()

        msg.information_box("Save asset information successfully!", icon_path=self.icon_path)

    def crud_add_asset_event(self):
        # Clear filter input
        self.number_input.setText("")
        self.search_input.setText("")
        self.apply_filter_button.click()

        # Move to the last page
        if self.total_assets % 10 == 0:
            self.total_pages += 1
            self.current_page = self.total_pages
            self.fill_in_master_table(self.current_page)
        else:
            self.current_page = self.total_pages
            self.fill_in_master_table(self.current_page)

        print('The new row to insert in master table is: ', len(self.assets_data) % 10 + 1)

        # Create a new asset
        success = self.db.create_new_asset()
        if not success:
            msg.warning_box("Error occurred when creating a new asset!", icon_path=self.icon_path)
            return

        # Reload the master table
        self.reload_data_after_crud()
        self.table_data = self.assets_data
        self.total_assets = len(self.table_data)
        self.total_pages = self.total_assets // 10 + \
            1 if (self.total_assets % 10 != 0 or self.total_assets == 0) else self.total_assets // 10
        self.current_page = self.total_pages
        self.fill_in_master_table(self.current_page)
        self.clear_asset_detail_table()

    # --====================== Action for Attribute table ======================--

    def clear_the_attribute_table(self):
        self.attribute_table.clearContents()
        self.attribute_table.setRowCount(0)

    def fill_attribute_table(self, asset_id: int):
        if asset_id is None:
            return

        # Clear the attribute table
        self.attribute_table.clearContents()
        self.attribute_table.setRowCount(0)

        # Get the attribute data from the database
        attribute_data: list = self.db.load_asset_attribute_table(asset_id)

        if attribute_data == []:
            return

        self.attribute_table.setRowCount(len(attribute_data))

        for i, attribute in enumerate(attribute_data):
            for j, column in enumerate(attribute):
                self.attribute_table.setItem(i, j, QTableWidgetItem(str(column)))

        # Set the height of the row
        for i in range(self.attribute_table.rowCount()):
            self.attribute_table.setRowHeight(i, 40)

    def crud_add_attribute_button_event(self):
        if self.current_asset_id is None:
            msg.warning_box("Please select an asset to add attribute!", icon_path=self.icon_path)
            return

        # Create new attribute in the database
        success = self.db.create_new_attribute(self.current_asset_id)
        if not success:
            msg.warning_box("Error occurred when creating a new attribute!", icon_path=self.icon_path)
            return

        # Reload the attribute table
        self.fill_attribute_table(self.current_asset_id)

        # Scroll to the last row
        self.attribute_table.scrollToBottom()

    def crud_save_attribute_button_event(self):
        if self.current_asset_id is None:
            msg.warning_box("Please select an asset to update attribute!", icon_path=self.icon_path)
            return

        # Get the current attribute data
        new_attribute_data = []
        for i in range(self.attribute_table.rowCount()):
            new_attribute_data.append([])
            for j in range(self.attribute_table.columnCount()):
                if j == 0:  # AssetAttributeOrderNumber : int
                    # If not a number
                    if not self.attribute_table.item(i, j).text().isdigit():
                        msg.warning_box("Attribute order number must be a number!", icon_path=self.icon_path)
                        return
                    new_attribute_data[i].append(int(self.attribute_table.item(i, j).text()))
                else:
                    new_attribute_data[i].append(self.attribute_table.item(i, j).text())

        # Update the the attribute of the current asset in the database
        success = self.db.update_asset_attribute(self.current_asset_id, new_attribute_data)

        if not success:
            msg.warning_box("Error occurred when updating attribute!", icon_path=self.icon_path)
            return

        # Reload the attribute table
        self.fill_attribute_table(self.current_asset_id)

        msg.information_box("Save attribute successfully!", icon_path=self.icon_path)

    def crud_delete_attribute_button_event(self):
        if self.current_asset_id is None:
            msg.warning_box("Please select an asset to delete attribute!", icon_path=self.icon_path)
            return

        # Get the current clicked attribute data row
        current_clicked_attribute_row = self.attribute_table.currentRow()

        if current_clicked_attribute_row == -1:
            msg.warning_box("Please select an attribute to delete!", icon_path=self.icon_path)
            return

        # Get the current clicked data in the attribute table
        current_att_order_number: str = self.attribute_table.item(current_clicked_attribute_row, 0).text()
        current_att_name: str = self.attribute_table.item(current_clicked_attribute_row, 1).text()
        current_att_datatype: str = self.attribute_table.item(current_clicked_attribute_row, 2).text()
        current_att_remark: str = self.attribute_table.item(current_clicked_attribute_row, 3).text()

        if not self.db.check_if_asset_attribute_exists(
                asset_id=self.current_asset_id,
                attribute_order_number=int(current_att_order_number),
                attribute_name=current_att_name,
                data_type_name=current_att_datatype,
                attribute_remark=current_att_remark):
            msg.warning_box("This attribute does not exist! Have you saved the changes yet?", icon_path=self.icon_path)
            return

        user_choice = msg.yes_no_box("Are you sure to delete this attribute?", icon_path=self.icon_path)
        if user_choice == QMessageBox.No:
            return

        # Delete the attribute in the database
        success = self.db.delete_asset_attribute(
            asset_id=self.current_asset_id,
            row_data=(int(current_att_order_number), current_att_name, current_att_datatype, current_att_remark))

        if not success:
            msg.warning_box("Error occurred when deleting attribute!", icon_path=self.icon_path)
            return

        # Reload the attribute table
        self.fill_attribute_table(self.current_asset_id)

        msg.information_box("Delete attribute successfully!", icon_path=self.icon_path)

    # --====================== Action for Shape table ======================--
    def clear_the_shape_table(self):
        self.shape_table.clearContents()
        self.shape_table.setRowCount(0)

    def fill_shape_table(self, asset_id: int):
        if asset_id is None:
            return

        # Clear the attribute table
        self.shape_table.clearContents()
        self.shape_table.setRowCount(0)

        # Get the shape data from the database
        shape_data: list = self.db.load_asset_shape_table(asset_id)

        print(f'Shape data for AssetID {asset_id}:', shape_data)
        if shape_data == []:
            return

        self.shape_table.setRowCount(len(shape_data))

        for i, shape in enumerate(shape_data):
            for j, column in enumerate(shape):
                if j == 0:  # AssetShapeID : int (read only)
                    self.shape_table.setItem(i, j, QTableWidgetItem(str(column)))
                    self.shape_table.item(i, j).setFlags(Qt.ItemIsEnabled)
                else:
                    self.shape_table.setItem(i, j, QTableWidgetItem(str(column)))

        # Set the height of the row
        for i in range(self.shape_table.rowCount()):
            self.shape_table.setRowHeight(i, 40)

    def crud_add_shape_button_event(self):
        if self.current_asset_id is None:
            msg.warning_box("Please select an asset to add shape!", icon_path=self.icon_path)
            return

        # Create new shape in the database
        success = self.db.create_new_shape(self.current_asset_id)
        if not success:
            msg.warning_box("Error occurred when creating a new shape!", icon_path=self.icon_path)
            return

        # Reload the shape table
        self.fill_shape_table(self.current_asset_id)

        # Scroll to the last row
        self.shape_table.scrollToBottom()

    def crud_save_shape_button_event(self):
        if self.current_asset_id is None:
            msg.warning_box("Please select an asset to update shape!", icon_path=self.icon_path)
            return

        # Get the current shape data
        new_shape_data = []
        for i in range(self.shape_table.rowCount()):
            new_shape_data.append([])
            for j in range(self.shape_table.columnCount()):
                if j == 0:  # AssetShapeID : int
                    new_shape_data[i].append(int(self.shape_table.item(i, j).text()))
                else:
                    new_shape_data[i].append(self.shape_table.item(i, j).text())

        # Update the the shape of the current asset in the database
        success = self.db.update_asset_shape(new_shape_data)

        if not success:
            msg.warning_box("Error occurred when updating shape!", icon_path=self.icon_path)
            return

        # Reload the shape table
        self.fill_shape_table(self.current_asset_id)

        msg.information_box("Save shape successfully!", icon_path=self.icon_path)

    def crud_delete_shape_button_event(self):
        if self.current_asset_id is None:
            msg.warning_box("Please select an asset to delete shape!", icon_path=self.icon_path)
            return

        # Get the current clicked shape data row
        current_clicked_shape_row = self.shape_table.currentRow()

        if current_clicked_shape_row == -1:
            msg.warning_box("Please select a shape to delete!", icon_path=self.icon_path)
            return

        user_choice = msg.yes_no_box(
            "Are you sure to delete this shape? This action cannot be undone!", icon_path=self.icon_path)

        if user_choice == QMessageBox.No:
            return

        # Get the current clicked data in the shape table
        current_asset_shape_id: str = self.shape_table.item(current_clicked_shape_row, 0).text()

        # Delete the shape in the database
        success = self.db.delete_asset_shape(asset_shape_id=int(current_asset_shape_id))

        if not success:
            msg.warning_box("Error occurred when deleting shape!", icon_path=self.icon_path)
            return

        # Reload the shape table
        self.fill_shape_table(self.current_asset_id)

        msg.information_box("Delete shape successfully!", icon_path=self.icon_path)

    # --====================== Action for media frame ======================--

    def show_image_detail(self, image_label: ClickableImage):
        for image in self.current_asset_images:
            if image[0] == image_label:
                image_name = image[1]
                image_category_name = image[2]
                self.current_clicked_image: tuple = image
                self.image_category_label.setText(f'Category: {image_category_name}')

    def get_clickable_image_label(self, just_image_name: str, extension: str) -> ClickableImage:
        """
        Arg:
            just_image_name (str): Example: 'image^mediaframe'
            extension (str): Example: 'png'
        Return:
            This function return a ClickableImage with the image_path_resized for media frame and set to the action show the original image when clicked
        """
        # Get the original image name
        orignal_image_name = f"{just_image_name.replace('^mediaframe', '')}.{extension}"

        # Get the current AssetID
        asset_id: int = self.current_asset_id

        image_path_resized = os.path.join(
            self.temp_folder_path, f'{asset_id}_{self.asset_name_item.text()}', f'{just_image_name}.{extension}')
        image_path_original = os.path.join(
            self.asset_pictures_path, f'{asset_id}_{self.asset_name_item.text()}', orignal_image_name)

        # Create a ClickableImage
        image_label = ClickableImage(self.horizontalLayoutWidget)
        image_label.setPixmap(QPixmap(image_path_resized))
        image_label.setAlignment(Qt.AlignCenter)
        image_label.double_clicked.connect(lambda: os.startfile(image_path_original))
        image_label.clicked.connect(self.show_image_detail)

        return image_label

    def clear_the_horizontal_layout(self):
        # Clear the horizontal layouts
        for i in reversed(range(self.horizontalLayout.count())):
            self.horizontalLayout.itemAt(i).widget().setParent(None)  # Auto garbage collection

        # Clear the image category label
        self.image_category_label.setText("")

        # Set the current clicked image to None
        self.current_clicked_image = None

    def fill_in_media_frame(self):
        self.clear_the_horizontal_layout()  # Clear the horizontal layout before adding new images
        self.current_asset_images = []  # Clear the current asset images metadata list

        # Browse the temp folder to get the images of current asset (for media frame)
        asset_folder_name = f'{self.current_asset_id}_{self.asset_name_item.text()}'

        if not os.path.exists(os.path.join(self.temp_folder_path, asset_folder_name)):
            os.mkdir(os.path.join(self.temp_folder_path, asset_folder_name))
            return

        for image_name in os.listdir(os.path.join(self.temp_folder_path, asset_folder_name)):
            if image_name.find('^mediaframe') != -1:
                extension = image_name.split('.')[1]
                just_image_name = image_name.split('.')[0]
                original_image_name = f'{just_image_name.replace("^mediaframe","")}.{extension}'
                # Create a ClickableImage
                image_label: ClickableImage = self.get_clickable_image_label(just_image_name, extension)
                # Get the image category name
                image_category_name = self.db.get_asset_image_category_name(
                    self.current_asset_id, original_image_name)
                # Add the image to the metadata list
                self.current_asset_images.append((image_label, original_image_name, image_category_name))

        # Add the images to the horizontal layout
        for image in self.current_asset_images:
            self.horizontalLayout.addWidget(image[0])

        print('Current asset images: ', self.current_asset_images)

    def resize_newly_added_image(self, asset_id: int, asset_name: str, image_name: str):
        """
        Resize the newly added image to fit the master table and media frame
        Args:
            asset_id (int): Example: 1
            asset_name (str): Example: 'Asset 1'
            image_name (str): Example: 'image.png'
        """
        just_image_name = image_name.split('.')[0]
        extension = image_name.split('.')[1]

        # Check if the folder image of asset is existed. If not, create it and naming it with asset id_asset name
        temp_asset_image_folder = os.path.join(self.temp_folder_path, f'{asset_id}_{asset_name}')
        if not os.path.exists(temp_asset_image_folder):
            os.mkdir(temp_asset_image_folder)

        # Check whether the image contain "mastertable" is existed in the temp folder or not
        existed_mastertable_image = False
        for resized_image_dir in os.listdir(temp_asset_image_folder):
            if resized_image_dir.find('^mastertable') != -1:
                existed_mastertable_image = True
                break
        if not existed_mastertable_image:
            self.resizer.fit_master_table(asset_id, asset_name, image_name)

        # Create the image for media frame
        self.resizer.fit_media_frame(asset_id, asset_name, image_name)

    def crud_add_image_event(self):
        # Show a sub window include choose file button and a ComboBox to choose the image category
        # Then add the image to the database
        if self.current_asset_id is None:
            msg.warning_box("Please select an asset to add image!", icon_path=self.icon_path)
            return

        self.image_window = QMainWindow()
        self.image_window.resize(721, 417)
        self.image_window.setWindowTitle(u"Add Image")
        self.image_window.setWindowIcon(QIcon('./assets/icon/logo.jpg'))

        self.image_window_widget = AddImageGUI(
            asset_name=self.asset_name_item.text(),
            image_categories=self.db.get_list_of_image_categories(),
            MainWindow=self.image_window
        )

        # Add widget to the window
        self.image_window.setCentralWidget(self.image_window_widget)
        self.image_window_widget.add_image_signal.connect(self.store_asset_image_to_database)

        # with self.main_window is a QStackedWidget, when self.main_window is close, close the self.image_window too
        self.main_window.closed.connect(self.image_window.close)

        # Show the window
        self.image_window.show()

    def store_asset_image_to_database(self, image_path: str, image_category: str):
        # Get the image name from image_path
        image_name = image_path.split('/')[-1]

        # Got the name and extension of the image
        just_image_name = image_name.split('.')[0]
        extension = image_name.split('.')[1]

        # If the extension is not png, convert it to png using PIL in the original folder
        if extension != 'png':
            self.resizer.convert_to_png(image_path)
            # Delete the original image
            os.remove(image_path)
            # Rename the extension of the image
            image_name = image_name.split('.')[0] + '.png'
            # Rename the image_path
            image_path = os.path.join(os.path.dirname(image_path), f'{just_image_name}.png')

        # --====================== Add to the original asset image folder ======================--

        # Check if the folder image of asset is existed. If not, create it and naming it with "asset id_asset name"
        list_of_asset_image_folders = os.listdir(self.asset_pictures_path)
        asset_id: int = self.current_asset_id
        asset_folder_name = f'{asset_id}_{self.asset_name_item.text()}'
        if asset_folder_name not in list_of_asset_image_folders:
            os.mkdir(os.path.join(self.asset_pictures_path, asset_folder_name))

        # Check if existing the image with the same name in the asset folder
        list_of_images = os.listdir(os.path.join(self.asset_pictures_path, asset_folder_name))
        if image_name in list_of_images:
            msg.warning_box(
                f'The image: "{image_name}" is already existed in the folder "{asset_folder_name}"!', icon_path=self.icon_path)
            return

        # Check if existing the image with the same name in the database
        if image_name in self.db.get_list_of_asset_images(asset_id=asset_id):
            msg.warning_box(
                f'The image: "{image_name}" is already existed in the database\nwhere AssetID = {asset_id}!', icon_path=self.icon_path)
            return

        # If there is no duplicate, copy the image to the asset folder
        shutil.copy(image_path, os.path.join(self.asset_pictures_path, asset_folder_name))

        # --====================== Add to the temp asset image folder ======================--
        self.resize_newly_added_image(asset_id, self.asset_name_item.text(), image_name)

        # --====================== Insert to the database ======================--
        success = self.db.create_new_image(
            asset_id,
            image_file_name=image_name,
            image_category_name=image_category
        )

        if not success:
            msg.warning_box(f'Error occurred when adding image: "{image_name}" to database!', icon_path=self.icon_path)
            return

        self.image_window_widget.set_result_label_text(
            f'Add image "{image_name}" successfully!')
        print(f'Add image "{image_name}" to the asset with id = {asset_id} successfully!')

        self.fill_in_media_frame()
        self.fill_preview_image_in_master_table(self.current_page)

    def crud_delete_image_event(self):
        if self.current_clicked_image is None:
            msg.warning_box("Please select an asset to delete image!", icon_path=self.icon_path)
            return

        if msg.yes_no_box('Are you sure to delete this image? Action cannot be undone!', icon_path=self.icon_path) == QMessageBox.No:
            return

        # First, try to delete the image in the database
        delete_operation = self.db.delete_asset_image(
            asset_id=self.current_asset_id,
            asset_image_name=self.current_clicked_image[1]
        )

        if not delete_operation:
            msg.warning_box(
                f'Error occurred when deleting image: "{self.current_clicked_image[1]}" in the database!', icon_path=self.icon_path)
            return

        # If the image is deleted in the database, delete the image in the asset folder
        asset_folder_name = f'{self.current_asset_id}_{self.asset_name_item.text()}'
        if os.path.exists(os.path.join(self.asset_pictures_path, asset_folder_name, self.current_clicked_image[1])):
            os.remove(os.path.join(
                self.asset_pictures_path, asset_folder_name, self.current_clicked_image[1]))

        # If the image is deleted in the asset folder, delete the image in the temp folder
        # But we need to check if the image is choosed to be the preview image in the master table or not

        is_preview_image = False
        just_current_image_name = self.current_clicked_image[1].split('.')[0]
        for temp_image in os.listdir(os.path.join(self.temp_folder_path, asset_folder_name)):
            if temp_image.find('^mastertable') != -1 and temp_image.find(just_current_image_name) != -1:
                is_preview_image = True
                break

        # Delete the image in the temp folder
        for temp_image in os.listdir(os.path.join(self.temp_folder_path, asset_folder_name)):
            if temp_image.find(just_current_image_name) != -1:
                os.remove(os.path.join(
                    self.temp_folder_path, asset_folder_name, temp_image))

        if is_preview_image:
            # If the image is choosed to be the preview image in the master table, we need to choose another image to be the preview image
            current_asset_images = os.listdir(os.path.join(self.asset_pictures_path, asset_folder_name))
            if current_asset_images != []:
                # Choose the first image in the list to be the preview image
                self.resize_newly_added_image(
                    self.current_asset_id, self.asset_name_item.text(), current_asset_images[0])

        # Notify the user
        msg.information_box(
            f'Delete image "{self.current_clicked_image[1]}" successfully!', icon_path=self.icon_path)

        # Reload the master table
        self.reload_data_after_crud()
        self.fill_in_master_table(self.current_page)
        self.fill_in_media_frame()
