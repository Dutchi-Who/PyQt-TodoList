from TableWidget import *
from AddNewDialog import *
from MarkCompleteDialog import *
from EditDialog import *
from DeleteTaskDialog import *


# 展示任务和项目列表
class ProjectTasksDialog(QDialog):

    def __init__(self, project_id):
        super().__init__()
        self.project_id = project_id
        self.controller = DbController("to_do.db")

        self.setWindowTitle("项目中的任务")

        self.project_label = QLabel("<b>项目:</b>")
        self.tasks_label = QLabel("<b>任务:</b>")

        self.project_labels_list = ["项目ID", "描述", "截止日期", "创建日期", "完成日期"]
        self.project_details = self.get_project_details()

        self.project_details_layout = QGridLayout()
        col = 0
        for label in self.project_labels_list:
            self.project_details_layout.addWidget(QLabel(label), 0, col)
            col += 1
        col = 0
        for item in self.project_details:
            self.project_details_layout.addWidget(QLabel(item), 1, col)
            col += 1

        self.project_tasks_table = ProjectTasksTable(self.project_id)
        self.populate_project_tasks_table()

        # 按钮排列
        self.add_task_button = QPushButton("新增任务")
        self.mark_task_complete_button = QPushButton("标记为已完成")
        self.mark_task_complete_button.setEnabled(False)
        self.edit_task_button = QPushButton("编辑任务")
        self.edit_task_button.setEnabled(False)
        self.delete_task_button = QPushButton("删除任务")
        self.delete_task_button.setEnabled(False)
        self.close_window_button = QPushButton("关闭")

        self.project_tasks_button_layout = QHBoxLayout()
        self.project_tasks_button_layout.addWidget(self.add_task_button)
        self.project_tasks_button_layout.addWidget(self.mark_task_complete_button)
        self.project_tasks_button_layout.addWidget(self.edit_task_button)
        self.project_tasks_button_layout.addWidget(self.delete_task_button)
        self.project_tasks_button_layout.addWidget(self.close_window_button)

        self.project_tasks_layout = QVBoxLayout()
        self.project_tasks_layout.addWidget(self.project_label)
        self.project_tasks_layout.addLayout(self.project_details_layout)
        self.project_tasks_layout.addWidget(self.tasks_label)
        self.project_tasks_layout.addWidget(self.project_tasks_table)
        self.project_tasks_layout.addLayout(self.project_tasks_button_layout)

        self.setLayout(self.project_tasks_layout)

        # 信号和槽
        self.project_tasks_table.clicked.connect(self.enable_buttons)

        self.add_task_button.clicked.connect(self.open_new_project_task_dialog)
        self.mark_task_complete_button.clicked.connect(self.mark_task_completed)
        self.edit_task_button.clicked.connect(self.open_edit_task_dialog)
        self.delete_task_button.clicked.connect(self.open_delete_task_dialog)
        self.close_window_button.clicked.connect(self.close)

    # 获取项目的详细信息
    def get_project_details(self):
        project_details = []
        controller_results = self.controller.get_single_project(self.project_id)
        # 将项目的详细信息添加到列表中
        for item in controller_results[0][:3]:
            if item is None:
                item = ""
            project_details.append(str(item))

        # 将日期转换为字符串
        for item in controller_results[0][3:]:
            if item is None:
                item = ""
                project_details.append(item)
            else:
                project_details.append(str(item[:-7]))
        # 返回项目详细信息列表
        return project_details

    # 打开编辑任务对话框
    def populate_project_tasks_table(self):
        table_items = self.project_tasks_table.get_project_tasks()
        self.project_tasks_table.show_items(table_items)

    # 启动按钮
    def enable_buttons(self):
        # 如果任务已完成，则禁用编辑和删除按钮
        if not self.project_tasks_table.check_completed():
            self.mark_task_complete_button.setEnabled(True)
        else:
            self.mark_task_complete_button.setEnabled(False)
        self.edit_task_button.setEnabled(True)
        self.delete_task_button.setEnabled(True)

    # 打开新增任务对话框
    def open_new_project_task_dialog(self):
        new_project_task_dialog = NewProjectTaskDialog(self.project_id)
        new_project_task_dialog.exec_()
        self.populate_project_tasks_table()

    # 标记任务为已完成
    def mark_task_completed(self):
        task_id = self.project_tasks_table.get_id()
        self.controller.mark_task_completed(task_id)
        # 如果任务已完成，则禁用编辑和删除按钮
        if self.check_project_tasks_completed():
            mark_project_complete_dialog = MarkProjectCompleteDialog(self.project_id)
            mark_project_complete_dialog.exec_()
        self.populate_project_tasks_table()

    # 检查项目中的任务是否已全部完成
    def check_project_tasks_completed(self):
        # 获取项目中的任务是否已全部完成
        if self.controller.check_project_tasks_completed(self.project_id):
            return True
        else:
            return False

    # 打开编辑任务对话框
    def open_edit_task_dialog(self):
        task_id = self.project_tasks_table.get_id()
        edit_task_dialog = EditTaskDialog(task_id)
        edit_task_dialog.exec_()
        self.populate_project_tasks_table()

    # 打开删除任务对话框
    def open_delete_task_dialog(self):
        task_id = self.project_tasks_table.get_id()
        delete_task_dialog = DeleteTaskDialog(task_id)
        delete_task_dialog.exec_()
        self.populate_project_tasks_table()
