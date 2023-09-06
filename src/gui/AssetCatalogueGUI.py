from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from src.gui.BaseGUI import BaseGUI


class AssetCatelogueGUI(BaseGUI):
    def __init__(self, MainWindow) -> None:
        super().__init__(MainWindow)

        self.add_to_master_table('image', 'asset_id', 'asset_name', 'category')
        self.add_to_master_table('image', 'asset_id', 'asset_name', 'category')
        self.add_to_master_table('image', 'asset_id', 'asset_name', 'category')
        self.add_to_master_table('image', 'asset_id', 'asset_name', 'category')

    def add_to_master_table(self, image, asset_id: str, asset_name: str, category: str):
        # Add these to the master table
        row_count = self.master_table.rowCount()
        self.master_table.insertRow(row_count)
        self.master_table.setRowHeight(row_count, 40)

        # Set the image
        # image_item = QTableWidgetItem()
        # image_item.setData(Qt.DecorationRole, image)
        # self.master_table.setItem(row_count, 0, image_item)

        image_item = QTableWidgetItem()
        image_item.setText(image)
        self.master_table.setItem(row_count, 0, image_item)
        # Set the asset id
        self.master_table.setItem(row_count, 1, QTableWidgetItem(asset_id))
        # Set the asset name
        self.master_table.setItem(row_count, 2, QTableWidgetItem(asset_name))
        # Set the category
        self.master_table.setItem(row_count, 3, QTableWidgetItem(category))
