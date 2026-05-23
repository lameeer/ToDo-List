from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

class CreateTaskWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("UI/create.ui", self)
        self.btnSave.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)

class ViewTaskWindow(QDialog):
    def __init__(self, task_data, parent=None):
        super().__init__(parent)
        uic.loadUi("UI/view.ui", self)
        
        title = task_data.get("title", "Задача")
        self.setWindowTitle(title)
        self.lblTaskName.setText(title)
        
        self.lblDesc.setText(task_data.get("description", ""))
        self.lblPriority.setText(f"Приоритет: {task_data.get('priority', '')}")
        self.lblDate.setText(f"Дата: {task_data.get('date', '')}")
        

class EditTaskWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("UI/edit.ui", self)
        self.btnSave.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)