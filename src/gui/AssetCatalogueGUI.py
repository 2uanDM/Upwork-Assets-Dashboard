from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from src.gui.BaseGUI import BaseGUI


class AssetCatelogueGUI(BaseGUI):
    def __init__(self, MainWindow) -> None:
        super().__init__(MainWindow)
        self.current_page = 1

        # Connect for buttons
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

        self.previous_page_button.clicked.connect(self.test_action)
        self.next_page_button.clicked.connect(self.test_action)

        self.download_catalogue_button.clicked.connect(self.test_action)
        self.download_dataset_button.clicked.connect(self.test_action)

    def load_master_table(self, image, asset_id: str, asset_name: str, category: str):
        pass
