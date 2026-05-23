from PyQt6.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QLabel, QPushButton

class TaskWidget(QWidget):
    def __init__(self, task_data, list_widget, item, main_window):
        super().__init__()
        self.list_widget = list_widget
        self.item = item
        self.main_window = main_window
        
        self.task_data = task_data 

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)

        self.checkbox = QCheckBox()
        self.checkbox.setStyleSheet("padding: 0px;")
        self.checkbox.setChecked(self.task_data.get("completed", False)) 
        self.checkbox.stateChanged.connect(self.toggle_completed)
        
        self.lbl_title = QLabel(self.task_data["title"]) 
        self.lbl_title.setStyleSheet("color: black; font-weight: bold; background: transparent; padding: 0px;")
        
        self.btn_edit = QPushButton("✎")
        self.btn_edit.setFixedSize(28, 28)
        self.btn_edit.setStyleSheet("background-color: #a29bfe; color: white; border-radius: 5px; padding: 0px; font-size: 14px;")
        self.btn_edit.clicked.connect(self.edit_task)

        self.btn_delete = QPushButton("✖")
        self.btn_delete.setFixedSize(28, 28)
        self.btn_delete.setStyleSheet("background-color: #ff7675; color: white; border-radius: 5px; padding: 0px; font-size: 14px;")
        self.btn_delete.clicked.connect(self.delete_task)

        layout.addWidget(self.checkbox)
        layout.addWidget(self.lbl_title)
        layout.addStretch()
        layout.addWidget(self.btn_edit)
        layout.addWidget(self.btn_delete)

        self.setLayout(layout)
        
        self.update_text_style()

    def update_text_style(self):
        if self.checkbox.isChecked():
            self.lbl_title.setStyleSheet("text-decoration: line-through; color: #7f8c8d; background: transparent; padding: 0px;")
        else:
            self.lbl_title.setStyleSheet("color: black; font-weight: bold; background: transparent; padding: 0px;")

    def toggle_completed(self, state):
        self.task_data["completed"] = self.checkbox.isChecked()
        self.update_text_style()
        self.main_window.save_all_tasks() 

    def delete_task(self):
        row = self.list_widget.row(self.item)
        self.list_widget.takeItem(row)
        
        if self.task_data in self.main_window.tasks:
            self.main_window.tasks.remove(self.task_data)
        self.main_window.save_all_tasks()

    def edit_task(self):
        self.main_window.open_edit(self)