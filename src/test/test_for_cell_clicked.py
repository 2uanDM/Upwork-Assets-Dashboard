from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QTableWidget(3, 3)
        self.setCentralWidget(self.table)

        self.table.cellClicked.connect(self.on_cell_clicked)

    def on_cell_clicked(self, row, column):
        item = self.table.item(row, column)
        if item:
            print(f"Cell ({row}, {column}) clicked with text: {item.text()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
