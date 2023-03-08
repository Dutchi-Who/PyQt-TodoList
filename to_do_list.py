import sys
import os
from CreateNewDatabase import *
from TaskProjectTabs import *


# 自定义的类，表示主窗口。继承了 PyQt5.QtWidgets.QMainWindow
class ToDoWindow(QMainWindow):

    # 构造函数
    def __init__(self):
        super().__init__()  # 调用父类的构造函数

        # 设置窗口标题和大小
        self.setWindowTitle("任务清单")
        self.setMinimumHeight(300)

        # 主菜单 UI
        self.central_widget = TaskProjectTabs()
        self.setCentralWidget(self.central_widget)

        # 断开主菜单的信号槽连接，退出程序
        self.central_widget.task_exit_button.clicked.connect(self.close)
        self.central_widget.project_exit_button.clicked.connect(self.close)


# 程序入口
if __name__ == "__main__":
    # PyQt 框架初始化
    to_do = QApplication(sys.argv)

    # 启动前检查数据库是否存在，不存在则创建
    if not os.path.exists("to_do.db"):
        createNewDatabase("to_do.db")

        # 创建数据库后，显示一个窗口
        new_db = QMessageBox()
        new_db.setWindowTitle("新增数据库")
        new_db.setText("已新建数据库 to_do.db")
        new_db.exec_()

    # 创建主界面
    main_window = ToDoWindow()
    main_window.show()
    main_window.raise_()

    # PyQt 安全退出
    to_do.exec_()
