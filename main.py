import json
import subprocess
import traceback
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMessageBox, QStackedWidget

import sys
import os

from src.gui.AssetCatalogueGUI import AssetCatelogueGUI


def add_path_to_env():
    # Add PyQt5 path to environment
    new_path = os.path.join(os.getcwd(), '.venv\Lib\site-packages\PyQt5\Qt5\plugins\platforms')
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = new_path


class StackedWidget(QStackedWidget):
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    # Handle the close event
    def closeEvent(self, event):
        self.closed.emit()
        event.accept()


if __name__ == "__main__":
    add_path_to_env()
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Load the config file
    with open(os.path.join(os.getcwd(), 'configuration', 'application.json'), "r") as f:
        config = json.load(f)

    template_folder_images_name = '.temp'
    folder_path = os.path.join(os.getcwd(), template_folder_images_name)
    # Check if the temp folder exists
    if not os.path.exists(os.path.join(os.getcwd(), template_folder_images_name)):
        os.mkdir(folder_path)
        subprocess.run(["attrib", "+h", folder_path], shell=True, check=True)  # Set the .temp folder to be hidden

    # When the application is closed, delete the temp folder
    # def on_close():
    #     os.rmdir(folder_path)

    try:
        app = QApplication(sys.argv)
        main_window = StackedWidget()
        # main_window.closed.connect(on_close)

        # Import all GUIs
        asset_catalogue_gui = AssetCatelogueGUI(main_window)
        main_window.addWidget(asset_catalogue_gui)

        # Set the main window size
        main_window.setFixedHeight(900)
        main_window.setFixedWidth(1820)
        main_window.setWindowTitle(config['window_title'])
        main_window.setCurrentIndex(0)
        main_window.setWindowIcon(QIcon('./assets/icon/logo.jpg'))
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        error_message = f"An error occurred:\n{traceback.format_exc()}"
        QMessageBox.critical(None, "Error", error_message)
        sys.exit(1)
