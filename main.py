import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QDialog, 
                             QListWidgetItem, QWidget, QHBoxLayout, 
                             QLabel, QPushButton, QCheckBox)
from PyQt6.QtCore import QDate, QSize
from PyQt6 import uic

from windows import CreateTaskWindow, ViewTaskWindow, EditTaskWindow
from widgets import TaskWidget
import storage



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/main.ui", self)
        
        self.tasks = storage.load_tasks()
        self.btnAdd.clicked.connect(self.open_create)
        self.listTasks.itemDoubleClicked.connect(self.open_view)
        self.searchEdit.textChanged.connect(self.filter_tasks)

        self.refresh_list()

    def save_all_tasks(self):
        storage.save_tasks(self.tasks)

        self.update_statistics()

    def refresh_list(self):
        self.listTasks.clear()
        for task_data in self.tasks:
            self.add_task_to_list(task_data)
        
        self.update_statistics()

    def add_task_to_list(self, task_data):
        item = QListWidgetItem()
        item.setSizeHint(QSize(0, 65))
        self.listTasks.addItem(item)
        
        task_widget = TaskWidget(task_data, self.listTasks, item, self)
        self.listTasks.setItemWidget(item, task_widget)

    def filter_tasks(self, text):
        for i in range(self.listTasks.count()):
            item = self.listTasks.item(i)
            widget = self.listTasks.itemWidget(item)
            if widget:
                item.setHidden(text.lower() not in widget.lbl_title.text().lower())

    def open_create(self):
        dialog = CreateTaskWindow(self)
        if dialog.exec():
            title = dialog.titleEdit.text()
            if title:
                new_task = {
                    "title": title,
                    "description": dialog.descEdit.toPlainText(),
                    "priority": dialog.priorityCombo.currentText(),
                    "date": dialog.dateEdit.date().toString("dd.MM.yyyy"),
                    "completed": False
                }
                self.tasks.append(new_task)
                self.save_all_tasks()
                self.add_task_to_list(new_task)

    def open_edit(self, task_widget):
        dialog = EditTaskWindow(self)
        task_data = task_widget.task_data
        
        dialog.titleEdit.setText(task_data.get("title", ""))
        dialog.descEdit.setText(task_data.get("description", ""))
        dialog.priorityCombo.setCurrentText(task_data.get("priority", "Низкий"))
        
        date_str = task_data.get("date", "")
        if date_str:
            dialog.dateEdit.setDate(QDate.fromString(date_str, "dd.MM.yyyy"))

        if dialog.exec():
            new_title = dialog.titleEdit.text()
            if new_title:
                task_data["title"] = new_title
                task_data["description"] = dialog.descEdit.toPlainText()
                task_data["priority"] = dialog.priorityCombo.currentText()
                task_data["date"] = dialog.dateEdit.date().toString("dd.MM.yyyy")
                
                self.save_all_tasks()
                task_widget.lbl_title.setText(new_title)

    def open_view(self, item):
        widget = self.listTasks.itemWidget(item)
        if widget:
            dialog = ViewTaskWindow(widget.task_data, self)
            dialog.exec()

    def update_statistics(self):
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.get("completed", False))
        active = total - completed

        self.lblTotal.setText(f"Всего: {total}")
        self.lblActive.setText(f"Активных: {active}")
        self.lblCompleted.setText(f"Завершено: {completed}")

   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())