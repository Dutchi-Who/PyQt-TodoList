from PyQt5.QtWidgets import *
from DbController import *


# 删除项目对话框
class DeleteProjectDialog(QDialog):
    # 构造函数
    def __init__(self, project_id):
        # 调用父类构造函数
        super().__init__()
        # 获取项目 id
        self.project_id = project_id
        # 连接数据库
        self.controller = DbController("to_do.db")
        # 设置窗口标题
        self.setWindowTitle("删除项目")
        # 弹出对话框提示
        self.delete_project_message_label = QLabel("确定要删除该项目及其相关的任务吗？")

        self.delete_project_tasks_button = QPushButton("删除项目和任务")
        self.delete_project_only_button = QPushButton("仅删除项目")
        self.delete_project_cancel_button = QPushButton("取消")

        self.delete_project_button_layout = QHBoxLayout()
        self.delete_project_button_layout.addWidget(self.delete_project_tasks_button)
        self.delete_project_button_layout.addWidget(self.delete_project_only_button)
        self.delete_project_button_layout.addWidget(self.delete_project_cancel_button)

        self.delete_project_layout = QVBoxLayout()
        self.delete_project_layout.addWidget(self.delete_project_message_label)
        self.delete_project_layout.addLayout(self.delete_project_button_layout)

        self.setLayout(self.delete_project_layout)

        # 绑定信号和槽
        self.delete_project_tasks_button.clicked.connect(self.delete_project_and_tasks)
        self.delete_project_only_button.clicked.connect(self.delete_project_only)
        self.delete_project_cancel_button.clicked.connect(self.close)

    # 删除项目及其相关的任务
    def delete_project_and_tasks(self):
        self.controller.delete_project_and_tasks(self.project_id)
        delete_project_tasks_confirmation = QMessageBox()
        delete_project_tasks_confirmation.setWindowTitle("项目已删除")
        delete_project_tasks_confirmation.setInformativeText("项目及任务已删除")
        delete_project_tasks_confirmation.exec_()
        self.close()

    # 仅删除项目
    def delete_project_only(self):
        self.controller.delete_project_only(self.project_id)
        delete_project_only_confirmation = QMessageBox()
        delete_project_only_confirmation.setWindowTitle("项目已删除")
        delete_project_only_confirmation.setInformativeText("已解除关联的任务")
        delete_project_only_confirmation.exec_()
        self.close()
