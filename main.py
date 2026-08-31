import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QMenu
from PyQt6.QtCore import QDate, QSize
from PyQt6 import uic

from windows import CreateTaskWindow, ViewTaskWindow, EditTaskWindow
from widgets import TaskWidget
import storage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/main.ui", self)

        self.setMinimumSize(400, 600)

        self.tasks = storage.load_tasks()
        self.completion_filter = "all"
        self.btnAdd.clicked.connect(self.open_create)
        self.listTasks.itemDoubleClicked.connect(self.open_view)
        self.searchEdit.textChanged.connect(self.apply_filters)
        self._setup_filter_menu()

        self.refresh_list()

    def _setup_filter_menu(self):
        menu = QMenu(self)
        menu.addAction("Все задачи", lambda: self.set_completion_filter("all"))
        menu.addAction("Активные", lambda: self.set_completion_filter("active"))
        menu.addAction("Завершённые", lambda: self.set_completion_filter("completed"))
        self.btnSort.setMenu(menu)

    def save_all_tasks(self):
        storage.save_tasks(self.tasks)
        self.update_statistics()

    def refresh_list(self):
        self.listTasks.clear()
        for task_data in self.tasks:
            self.add_task_to_list(task_data)
        self.update_statistics()
        self.apply_filters()

    def add_task_to_list(self, task_data):
        item = QListWidgetItem()
        item.setSizeHint(QSize(0, 72))
        self.listTasks.addItem(item)

        task_widget = TaskWidget(task_data, self.listTasks, item, self)
        self.listTasks.setItemWidget(item, task_widget)

    def set_completion_filter(self, filter_type):
        self.completion_filter = filter_type
        self.apply_filters()

    def apply_filters(self, _text=None):
        query = self.searchEdit.text().lower()
        for i in range(self.listTasks.count()):
            item = self.listTasks.item(i)
            widget = self.listTasks.itemWidget(item)
            if not widget:
                continue

            matches_search = query in widget.lbl_title.text().lower()
            completed = widget.task_data.get("completed", False)

            if self.completion_filter == "active":
                matches_completion = not completed
            elif self.completion_filter == "completed":
                matches_completion = completed
            else:
                matches_completion = True

            item.setHidden(not (matches_search and matches_completion))

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
                    "completed": False,
                }
                self.tasks.append(new_task)
                self.save_all_tasks()
                self.add_task_to_list(new_task)
                self.apply_filters()

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
                task_widget.refresh_display()

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
