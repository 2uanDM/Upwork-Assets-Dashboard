import json
import traceback
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox, QStackedWidget

import sys
import os

from src.gui.AssetCatalogueGUI import AssetCatelogueGUI


def add_path_to_env():
    # Add PyQt5 path to environment
    new_path = os.path.join(os.getcwd(), '.venv\Lib\site-packages\PyQt5\Qt5\plugins\platforms')
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = new_path


if __name__ == "__main__":
    add_path_to_env()
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Load the config file
    with open(os.path.join(os.getcwd(), 'configuration', 'application.json'), "r") as f:
        config = json.load(f)

    try:
        app = QApplication(sys.argv)
        main_window = QStackedWidget()

        # Import all GUIs
        asset_catalogue_gui = AssetCatelogueGUI(main_window)
        main_window.addWidget(asset_catalogue_gui)

        # Set the main window size
        main_window.setFixedHeight(900)
        main_window.setFixedWidth(1820)
        main_window.setWindowTitle(config['window_title'])
        main_window.setCurrentIndex(0)
        main_window.setWindowIcon(QIcon('./assets/logo.jpg'))
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        error_message = f"An error occurred:\n{traceback.format_exc()}"
        QMessageBox.critical(None, "Error", error_message)
        sys.exit(1)
