from PyQt5.QtWidgets import *
from DbController import *


# 删除任务对话框
class DeleteTaskDialog(QDialog):
    # 构造函数
    def __init__(self, task_id):
        # 调用父类构造函数
        super().__init__()
        # 获取任务 id
        self.task_id = task_id
        # 连接数据库
        self.controller = DbController("to_do.db")
        # 设置窗口标题
        self.setWindowTitle("删除任务")
        # 弹出对话框提示
        self.delete_task_message_label = QLabel("确定要删除该任务吗？")

        self.yes_button = QPushButton("是")
        self.no_button = QPushButton("否")
        # 窗口布局
        self.delete_task_button_layout = QHBoxLayout()
        self.delete_task_button_layout.addWidget(self.yes_button)
        self.delete_task_button_layout.addWidget(self.no_button)

        self.delete_task_layout = QVBoxLayout()
        self.delete_task_layout.addWidget(self.delete_task_message_label)
        self.delete_task_layout.addLayout(self.delete_task_button_layout)

        self.setLayout(self.delete_task_layout)
        # 信号与槽
        self.yes_button.clicked.connect(self.delete_task)
        self.no_button.clicked.connect(self.close)

    # 删除任务
    def delete_task(self):
        self.controller.delete_task(self.task_id)
        delete_task_confirmation = QMessageBox()
        delete_task_confirmation.setWindowTitle(" ")
        delete_task_confirmation.setInformativeText("任务已删除")
        delete_task_confirmation.exec_()
        self.close()

