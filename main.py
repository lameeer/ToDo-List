import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QDialog, 
                             QListWidgetItem, QWidget, QHBoxLayout, 
                             QLabel, QPushButton, QCheckBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6 import uic

from windows import CreateTaskWindow, ViewTaskWindow, EditTaskWindow
from widgets import TaskWidget



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/main.ui", self)
        
        self.btnAdd.clicked.connect(self.open_create)
        self.listTasks.itemDoubleClicked.connect(self.open_view)
        self.searchEdit.textChanged.connect(self.filter_tasks)

    def open_create(self):
        dialog = CreateTaskWindow(self)
        if dialog.exec():
            title = dialog.titleEdit.text()
            if title:
                item = QListWidgetItem()
                item.setSizeHint(QSize(0, 65))
                self.listTasks.addItem(item)
                
                task_widget = TaskWidget(title, self.listTasks, item, self)
                self.listTasks.setItemWidget(item, task_widget)

    def open_view(self, item):
        widget = self.listTasks.itemWidget(item)
        if widget:
            dialog = ViewTaskWindow(widget.lbl_title.text(), self)
            dialog.exec()

    def open_edit(self, label):
        dialog = EditTaskWindow(self)
        dialog.titleEdit.setText(label.text())
        if dialog.exec():
            new_title = dialog.titleEdit.text()
            if new_title:
                label.setText(new_title)

    def filter_tasks(self, text):
        for i in range(self.listTasks.count()):
            item = self.listTasks.item(i)
            widget = self.listTasks.itemWidget(item)
            if widget:
                item.setHidden(text.lower() not in widget.lbl_title.text().lower())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())