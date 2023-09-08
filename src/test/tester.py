import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QComboBox, QVBoxLayout, QWidget, QStyledItemDelegate
from PyQt5.QtCore import Qt


class ComboBoxDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        row = index.row()
        column = index.column()

        # Specify the desired cell where the delegate should be applied
        target_row = 1
        target_column = 1

        if row == target_row and column == target_column:
            editor = QComboBox(parent)
            editor.addItem("Option 1")
            editor.addItem("Option 2")
            editor.addItem("Option 3")
            return editor

        # Use the default editor for other cells
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        current_text = index.model().data(index, Qt.EditRole)
        # If the editor is a QComboBox, this will select the current text
        if isinstance(editor, QComboBox):
            editor.setCurrentText(current_text)
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(editor, QComboBox):
            model.setData(index, editor.currentText(), Qt.EditRole)
        else:
            super().setModelData(editor, model, index)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QTableWidget with ComboBox")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create a QTableWidget
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(3)

        # Set the custom delegate
        combo_delegate = ComboBoxDelegate()
        self.tableWidget.setItemDelegate(combo_delegate)

        self.tableWidget.setItem(1, 1, QTableWidgetItem("Option 2"))

        layout.addWidget(self.tableWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
