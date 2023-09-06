from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor
import sys


class CustomTableWidget(QTableWidget):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)

        # Hide the horizontal header
        self.horizontalHeader().hide()

        # Add a custom row with two columns
        self.setRowCount(1)
        self.setColumnCount(2)

        # Set background color for the first row
        first_row_item = QTableWidgetItem()
        first_row_item.setBackground(QColor(231, 231, 231))  # Set your desired background color
        self.setItem(0, 0, first_row_item)

        # Set text for the first row
        first_row_text = "Custom Text"  # Set your desired text
        self.setItem(0, 1, QTableWidgetItem(first_row_text))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    table_widget = CustomTableWidget(3, 3)
    window.setCentralWidget(table_widget)
    window.show()
    sys.exit(app.exec_())
