from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import QDate
from PyQt6 import uic

from deadline import format_date_with_deadline



class BaseTaskWindow(QDialog):
    def validate_and_save(self):
        title = self.titleEdit.text().strip()
        desc = self.descEdit.toPlainText().strip()

        if not title:
            QMessageBox.warning(self, "Ошибка", "Название задачи не может быть пустым!")
            return
            
        if len(title) > 50:
            QMessageBox.warning(self, "Ошибка", "Название слишком длинное! (Максимум 50 символов)")
            return
            
        if len(desc) > 500:
            QMessageBox.warning(self, "Ошибка", "Описание слишком длинное! (Максимум 500 символов)")
            return

        self.accept()

class CreateTaskWindow(BaseTaskWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("UI/create.ui", self)
        
        self.btnSave.clicked.connect(self.validate_and_save) 
        self.btnCancel.clicked.connect(self.reject)
        self.dateEdit.setDate(QDate.currentDate())

class EditTaskWindow(BaseTaskWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("UI/edit.ui", self)
        
        self.btnSave.clicked.connect(self.validate_and_save) 
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

        date_str = task_data.get("date", "")
        completed = task_data.get("completed", False)
        if date_str:
            date_text, date_color = format_date_with_deadline(date_str, completed)
            self.lblDate.setText(f"Дата: {date_text}")
            self.lblDate.setStyleSheet(
                f"color: {date_color}; font-weight: bold; font-size: 14px;"
            )
            self.lblDate.setVisible(True)
        else:
            self.lblDate.clear()
            self.lblDate.setVisible(False)
        

