from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from DbController import *
from datetime import datetime


# 编辑任务/项目对话框
class EditDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.controller = DbController("to_do.db")

        self.description_label = QLabel("描述: ")
        self.description_line_edit = QLineEdit()
        self.deadline_label = QLabel("截止日期: ")
        self.deadline_calendar_widget = QCalendarWidget()
        # 限制最小日期，不允许选择今天之前的日期
        self.deadline_calendar_widget.setMinimumDate(datetime.today())
        self.no_deadline_checkbox = QCheckBox("无时间限制")

        self.description_deadline_layout = QVBoxLayout()
        self.description_deadline_layout.addWidget(self.description_label)
        self.description_deadline_layout.addWidget(self.description_line_edit)
        self.description_deadline_layout.addWidget(self.deadline_label)
        self.description_deadline_layout.addWidget(self.deadline_calendar_widget)
        self.description_deadline_layout.addWidget(self.no_deadline_checkbox)

        self.save_edit_button = QPushButton("保存")
        self.save_edit_button.setEnabled(False)
        self.cancel_edit_button = QPushButton("取消")

        self.edit_button_layout = QHBoxLayout()
        self.edit_button_layout.addWidget(self.save_edit_button)
        self.edit_button_layout.addWidget(self.cancel_edit_button)

        self.description_line_edit.textEdited.connect(self.enable_save_button)
        self.deadline_calendar_widget.clicked.connect(self.enable_save_button)
        self.no_deadline_checkbox.clicked.connect(self.toggle_calendar)
        self.no_deadline_checkbox.clicked.connect(self.enable_save_button)
        self.cancel_edit_button.clicked.connect(self.close)

    # 启用保存按钮
    def enable_save_button(self):
        self.save_edit_button.setEnabled(True)

    # 切换日历控件的可用状态
    def toggle_calendar(self):
        # 如果勾选了无时间限制，日历控件不可用
        if self.no_deadline_checkbox.isChecked():
            self.deadline_calendar_widget.setEnabled(False)
        else:
            self.deadline_calendar_widget.setEnabled(True)


# 编辑任务对话框
class EditTaskDialog(EditDialog):

    def __init__(self, task_id):
        super().__init__()
        self.task_id = task_id

        self.setWindowTitle("编辑任务")

        self.task_details = self.get_task_details()

        self.description_line_edit.setText(self.task_details[0][1])
        if self.task_details[0][2] == None:
            self.no_deadline_checkbox.setChecked(True)
            self.deadline_calendar_widget.setEnabled(False)
        else:
            self.deadline_calendar_widget.setSelectedDate(QDate.fromString(self.task_details[0][2], "yyyy-MM-dd"))

        self.project_assign_label = QLabel("分配到任务")
        self.project_assign_combobox = QComboBox()
        self.project_assign_combobox.addItem("无")
        project_list = self.get_project_list()
        self.current_index = 0
        for project in project_list:
            self.project_assign_combobox.addItem(project)
            if int(project[0]) == self.task_details[0][5]:
                self.current_index = project_list.index(project) + 1
        self.project_assign_combobox.setCurrentIndex(self.current_index)

        self.project_assign_layout = QVBoxLayout()
        self.project_assign_layout.addWidget(self.project_assign_label)
        self.project_assign_layout.addWidget(self.project_assign_combobox)

        self.edit_task_layout = QVBoxLayout()
        self.edit_task_layout.addLayout(self.description_deadline_layout)
        self.edit_task_layout.addLayout(self.project_assign_layout)
        self.edit_task_layout.addLayout(self.edit_button_layout)

        self.setLayout(self.edit_task_layout)

        self.project_assign_combobox.activated.connect(self.enable_save_button)
        self.save_edit_button.clicked.connect(self.edit_task)

    def get_task_details(self):
        task_details = self.controller.get_single_task(self.task_id)
        return task_details

    def get_project_list(self):
        project_list = []
        for entry in self.controller.get_all_projects():
            project_list.append(str(entry[0]) + ": " + entry[1])
        return project_list

    def edit_task(self):
        if self.description_line_edit.textEdited:
            description = self.description_line_edit.text()
            self.controller.edit_task_description(self.task_id, description)
        if self.deadline_calendar_widget.selectionChanged:
            if self.no_deadline_checkbox.isChecked():
                deadline = None
            else:
                deadline = self.deadline_calendar_widget.selectedDate().toPyDate()
            self.controller.set_task_deadline(self.task_id, deadline)
        if self.project_assign_combobox.currentIndex() != self.current_index:
            if self.project_assign_combobox.currentText() == "无":
                project_id = None
            else:
                project_id = int(self.project_assign_combobox.currentText()[0])
            self.controller.assign_task_to_project(self.task_id, project_id)
        self.close()


# 编辑项目对话框
class EditProjectDialog(EditDialog):

    def __init__(self, project_id):
        super().__init__()
        self.project_id = project_id

        self.setWindowTitle("编辑项目")

        self.project_details = self.get_project_details()

        self.description_line_edit.setText(self.project_details[0][1])
        if self.project_details[0][2] == None:
            self.no_deadline_checkbox.setChecked(True)
            self.deadline_calendar_widget.setEnabled(False)
        else:
            self.deadline_calendar_widget.setSelectedDate(QDate.fromString(self.project_details[0][2], "yyyy-MM-dd"))

        self.edit_project_layout = QVBoxLayout()
        self.edit_project_layout.addLayout(self.description_deadline_layout)
        self.edit_project_layout.addLayout(self.edit_button_layout)

        self.setLayout(self.edit_project_layout)

        self.save_edit_button.clicked.connect(self.edit_project)

    def get_project_details(self):
        project_details = self.controller.get_single_project(self.project_id)
        return project_details

    def edit_project(self):
        if self.description_line_edit.textEdited:
            description = self.description_line_edit.text()
            self.controller.edit_project_description(self.project_id, description)
        if self.deadline_calendar_widget.selectionChanged:
            if self.no_deadline_checkbox.isChecked():
                deadline = None
            else:
                deadline = self.deadline_calendar_widget.selectedDate().toPyDate()
            self.controller.set_project_deadline(self.project_id, deadline)
        self.close()
