from PyQt5.QtWidgets import *
from DbController import *
from datetime import datetime


# 新建项目/任务对话框
class AddNewDialog(QDialog):
    # 构造函数
    def __init__(self):
        super().__init__()
        # 连接数据库
        self.controller = DbController("to_do.db")
        # 设置窗口UI
        self.description_label = QLabel("描述: ")
        self.description_line_edit = QLineEdit()
        self.deadline_label = QLabel("截止日期: ")
        self.deadline_calendar_widget = QCalendarWidget()
        self.deadline_calendar_widget.setMinimumDate(datetime.today())
        self.no_deadline_checkbox = QCheckBox("无时间限制")

        self.description_deadline_layout = QVBoxLayout()
        self.description_deadline_layout.addWidget(self.description_label)
        self.description_deadline_layout.addWidget(self.description_line_edit)
        self.description_deadline_layout.addWidget(self.deadline_label)
        self.description_deadline_layout.addWidget(self.deadline_calendar_widget)
        self.description_deadline_layout.addWidget(self.no_deadline_checkbox)

        self.save_new_button = QPushButton("保存")
        self.save_new_button.setEnabled(False)
        self.cancel_new_button = QPushButton("取消")

        self.add_new_button_layout = QHBoxLayout()
        self.add_new_button_layout.addWidget(self.save_new_button)
        self.add_new_button_layout.addWidget(self.cancel_new_button)

        # 信号槽
        self.description_line_edit.textEdited.connect(self.enable_save_button)
        self.no_deadline_checkbox.clicked.connect(self.toggle_calendar)
        # 关闭窗口的信号槽
        self.cancel_new_button.clicked.connect(self.close)

    # 保存按钮
    def enable_save_button(self):
        self.save_new_button.setEnabled(True)

    # 日历控件
    def toggle_calendar(self):
        if self.no_deadline_checkbox.isChecked():
            self.deadline_calendar_widget.setEnabled(False)
        else:
            self.deadline_calendar_widget.setEnabled(True)


# 新建任务
class NewTaskDialog(AddNewDialog):
    # 构造函数
    def __init__(self):
        # 调用父类构造函数
        super().__init__()
        # 设置窗口标题
        self.setWindowTitle("新建任务")

        self.project_assign_label = QLabel("分配到项目")
        self.project_assign_combobox = QComboBox()
        self.project_assign_combobox.addItem("无")
        self.project_assign_combobox.addItems(self.get_project_list())

        self.project_assign_layout = QVBoxLayout()
        self.project_assign_layout.addWidget(self.project_assign_label)
        self.project_assign_layout.addWidget(self.project_assign_combobox)

        self.new_task_layout = QVBoxLayout()
        self.new_task_layout.addLayout(self.description_deadline_layout)
        self.new_task_layout.addLayout(self.project_assign_layout)
        self.new_task_layout.addLayout(self.add_new_button_layout)

        self.setLayout(self.new_task_layout)

        # 信号槽
        self.save_new_button.clicked.connect(self.add_new_task)

    # 获取项目列表
    def get_project_list(self):
        project_list = []
        for entry in self.controller.get_all_projects():
            project_list.append(str(entry[0]) + ": " + entry[1])
        return project_list

    # 添加新任务
    def add_new_task(self):
        # 获取描述
        description = self.description_line_edit.text()
        # 任务是否拥有截止日期（时间限制）？
        if self.no_deadline_checkbox.isChecked():
            deadline = None
        else:
            deadline = self.deadline_calendar_widget.selectedDate().toPyDate()
        if self.project_assign_combobox.currentText() == "无":
            project_id = None
        else:
            project_id = int(self.project_assign_combobox.currentText()[0])
        # 插入数据库
        self.controller.add_task(description, deadline, project_id)
        # 添加任务后关闭窗口
        self.close()


# 基于项目新建任务的对话框
class NewProjectTaskDialog(NewTaskDialog):
    # 构造函数
    def __init__(self, project_id):
        super().__init__()
        self.project_id = project_id

        self.project_assign_label.hide()
        self.project_assign_combobox.hide()

    # 添加新任务
    def add_new_task(self):
        description = self.description_line_edit.text()
        if self.no_deadline_checkbox.isChecked():
            deadline = None
        else:
            deadline = self.deadline_calendar_widget.selectedDate().toPyDate()
        self.controller.add_task(description, deadline, self.project_id)
        self.close()


# 新建项目
class NewProjectDialog(AddNewDialog):
    # 构造函数
    def __init__(self):
        super().__init__()
        # 设置窗口标题
        self.setWindowTitle("新建项目")

        self.new_project_layout = QVBoxLayout()
        self.new_project_layout.addLayout(self.description_deadline_layout)
        self.new_project_layout.addLayout(self.add_new_button_layout)

        self.setLayout(self.new_project_layout)
        # 信号槽
        self.save_new_button.clicked.connect(self.add_new_project)

    # 添加新项目
    def add_new_project(self):
        description = self.description_line_edit.text()
        if self.no_deadline_checkbox.isChecked():
            deadline = None
        else:
            deadline = self.deadline_calendar_widget.selectedDate().toPyDate()
        self.controller.add_project(description, deadline)
        self.close()
