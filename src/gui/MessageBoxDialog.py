from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
import sys
import os
sys.path.append(os.path.join(os.getcwd()))


class MessageBox():
    @staticmethod
    def information_box(content: str, icon_path: str):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Information)
        message_box.setWindowIcon(QIcon(icon_path))
        message_box.setWindowTitle("Information")
        message_box.setText(content)
        message_box.exec_()

    @staticmethod
    def warning_box(content: str, icon_path: SyntaxError):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Warning)
        message_box.setWindowTitle("Warning")
        message_box.setWindowIcon(QIcon(icon_path))
        message_box.setText(content)
        message_box.exec_()

    @staticmethod
    def warning_box_with_button(content: str, button_name: str, icon_path: str, button_action: callable):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Warning)
        message_box.setWindowTitle("Warning")
        message_box.setWindowIcon(QIcon(icon_path))
        message_box.setText(content)
        # This button can be set action and name by the caller
        button = message_box.addButton(button_name, QMessageBox.YesRole)
        # set the button at the bottom center of the message box
        button.setFixedWidth(120)
        button.move(400, 200)
        # If the button is clicked, the action will be executed
        message_box.buttonClicked.connect(lambda: button_action())
        message_box.exec_()

    @staticmethod
    def yes_no_box(content: str, icon_path: str):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Question)
        message_box.setWindowTitle("Question")
        message_box.setWindowIcon(QIcon(icon_path))
        message_box.setText(content)
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = message_box.exec_()
        return result
