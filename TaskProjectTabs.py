from RadioButtonWidget import *
from ProjectTasksDialog import *
from DeleteProjectDialog import *


# 任务主窗口，继承自 QWidget
class TaskProjectTabs(QWidget):

    # 构造函数
    def __init__(self):
        # 调用父类的构造函数
        super().__init__()
        # 连接数据库
        self.controller = DbController("to_do.db")

        # --------------设置窗口布局----------------
        self.tabs = QTabWidget()        # 创建一个标签页
        self.tasks_tab = QWidget()      # 创建一个任务标签页
        self.projects_tab = QWidget()   # 创建一个项目标签页

        self.tabs.addTab(self.tasks_tab, "任务")
        self.tabs.addTab(self.projects_tab, "项目")

        # 单选框
        self.tasks_radio_buttons = RadioButtonWidget(['进行中', '已完成', '全部'])
        self.projects_radio_buttons = RadioButtonWidget(['进行中', '已完成', '全部'])

        # 任务-下拉菜单：根据选择的内容排序
        self.tasks_sort_label = QLabel("排序依据:")
        self.tasks_sort_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tasks_sort_combobox = QComboBox()
        self.tasks_sort_combobox.addItems(["任务ID", "描述", "截止日期", "创建日期", "完成日期", "项目ID"])

        # 项目-下拉菜单：根据选择的内容排序
        self.projects_sort_label = QLabel("排序依据:")
        self.projects_sort_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.projects_sort_combobox = QComboBox()
        self.projects_sort_combobox.addItems(["项目ID", "描述", "截止日期", "完成日期", "已完成"])

        # 定义任务标签页的布局（水平布局）
        self.tasks_top_layout = QHBoxLayout()
        self.tasks_top_layout.addWidget(self.tasks_radio_buttons)
        self.tasks_top_layout.addWidget(self.tasks_sort_label)
        self.tasks_top_layout.addWidget(self.tasks_sort_combobox)

        # 定义项目标签页的布局（水平布局）
        self.projects_top_layout = QHBoxLayout()
        self.projects_top_layout.addWidget(self.projects_radio_buttons)
        self.projects_top_layout.addWidget(self.projects_sort_label)
        self.projects_top_layout.addWidget(self.projects_sort_combobox)

        self.tasks_table = TasksTable()
        self.populate_tasks_table()
        self.projects_table = ProjectsTable()
        self.populate_projects_table()

        # 定义任务列表按钮
        self.new_task_button = QPushButton("新建")
        self.task_complete_button = QPushButton("标记已完成")
        self.task_complete_button.setEnabled(False)
        self.task_edit_button = QPushButton("编辑")
        self.task_edit_button.setEnabled(False)
        self.task_delete_button = QPushButton("删除")
        self.task_delete_button.setEnabled(False)
        self.task_exit_button = QPushButton("退出")

        # 定义项目列表按钮
        self.new_project_button = QPushButton("新建")
        self.project_tasks_button = QPushButton("浏览项目任务")
        self.project_tasks_button.setEnabled(False)
        self.project_complete_button = QPushButton("标记已完成")
        self.project_complete_button.setEnabled(False)
        self.project_edit_button = QPushButton("编辑")
        self.project_edit_button.setEnabled(False)
        self.project_delete_button = QPushButton("删除")
        self.project_delete_button.setEnabled(False)
        self.project_exit_button = QPushButton("退出")

        # 定义任务列表按钮布局（水平布局）
        self.tasks_tab_button_layout = QHBoxLayout()
        self.tasks_tab_button_layout.addWidget(self.new_task_button)
        self.tasks_tab_button_layout.addWidget(self.task_complete_button)
        self.tasks_tab_button_layout.addWidget(self.task_edit_button)
        self.tasks_tab_button_layout.addWidget(self.task_delete_button)
        self.tasks_tab_button_layout.addWidget(self.task_exit_button)

        # 定义项目列表按钮布局（水平布局）
        self.projects_tab_button_layout = QHBoxLayout()
        self.projects_tab_button_layout.addWidget(self.new_project_button)
        self.projects_tab_button_layout.addWidget(self.project_tasks_button)
        self.projects_tab_button_layout.addWidget(self.project_complete_button)
        self.projects_tab_button_layout.addWidget(self.project_edit_button)
        self.projects_tab_button_layout.addWidget(self.project_delete_button)
        self.projects_tab_button_layout.addWidget(self.project_exit_button)

        # 定义任务列表标签页的整体布局（垂直布局）
        self.tasks_tab_layout = QVBoxLayout()
        self.tasks_tab_layout.addLayout(self.tasks_top_layout)
        self.tasks_tab_layout.addWidget(self.tasks_table)
        self.tasks_tab_layout.addLayout(self.tasks_tab_button_layout)
        self.tasks_tab.setLayout(self.tasks_tab_layout)

        # 定义项目列表标签页的整体布局（垂直布局）
        self.projects_tab_layout = QVBoxLayout()
        self.projects_tab_layout.addLayout(self.projects_top_layout)
        self.projects_tab_layout.addWidget(self.projects_table)
        self.projects_tab_layout.addLayout(self.projects_tab_button_layout)
        self.projects_tab.setLayout(self.projects_tab_layout)

        # 定义两标签页之间的布局（水平布局）
        self.tab_widget_layout = QVBoxLayout()
        self.tab_widget_layout.addWidget(self.tabs)
        self.setLayout(self.tab_widget_layout)

        # --------------设置信号与槽----------------
        # 任务列表标签页的连接
        self.tabs.currentChanged.connect(self.refresh_tab)

        # 任务、项目单选框的连接
        self.tasks_radio_buttons.radio_button_group.buttonClicked.connect(self.populate_tasks_table)
        self.projects_radio_buttons.radio_button_group.buttonClicked.connect(self.populate_projects_table)

        # 任务、项目排序下拉框的连接
        self.tasks_sort_combobox.currentIndexChanged.connect(self.sort_tasks_table)
        self.projects_sort_combobox.currentIndexChanged.connect(self.sort_projects_table)

        # 任务、项目列表的连接
        self.tasks_table.clicked.connect(self.enable_task_buttons)
        self.projects_table.clicked.connect(self.enable_project_buttons)

        # 任务、项目新建按钮的连接
        self.new_task_button.clicked.connect(self.open_new_task_dialog)
        self.new_project_button.clicked.connect(self.open_new_project_dialog)

        self.project_tasks_button.clicked.connect(self.open_project_tasks_dialog)

        # 任务、项目切换已完成按钮的连接
        self.task_complete_button.clicked.connect(self.mark_task_completed)
        self.project_complete_button.clicked.connect(self.mark_project_completed)

        # 任务、项目编辑按钮的连接
        self.task_edit_button.clicked.connect(self.open_edit_task_dialog)
        self.project_edit_button.clicked.connect(self.open_edit_project_dialog)

        # 任务、项目删除按钮的连接
        self.task_delete_button.clicked.connect(self.open_delete_task_dialog)
        self.project_delete_button.clicked.connect(self.open_delete_project_dialog)

    # 刷新任务表格
    def populate_tasks_table(self):
        table_type = self.tasks_radio_buttons.selected_button()
        table_items = self.tasks_table.get_tasks(table_type)
        self.tasks_table.show_items(table_items)

    # 刷新项目表格
    def populate_projects_table(self):
        table_type = self.projects_radio_buttons.selected_button()
        table_items = self.projects_table.get_projects(table_type)
        self.projects_table.show_items(table_items)

    # 刷新当前页
    def refresh_tab(self):
        if self.tabs.currentIndex() == 0:
            self.populate_tasks_table()
        else:
            self.populate_projects_table()

    # 排序任务表格
    def sort_tasks_table(self):
        sort_by = self.tasks_sort_combobox.currentIndex()
        self.tasks_table.sortByColumn(sort_by, Qt.AscendingOrder)

    # 排序项目表格
    def sort_projects_table(self):
        sort_by = self.projects_sort_combobox.currentIndex()
        self.projects_table.sortByColumn(sort_by, Qt.AscendingOrder)

    # 激活任务按钮
    def enable_task_buttons(self):
        if not self.tasks_table.check_completed():
            self.task_complete_button.setEnabled(True)
        else:
            self.task_complete_button.setEnabled(False)
        self.task_edit_button.setEnabled(True)
        self.task_delete_button.setEnabled(True)

    # 激活项目按钮
    def enable_project_buttons(self):
        self.project_tasks_button.setEnabled(True)

        # 如果项目已完成，则禁用“切换已完成”按钮
        if not self.projects_table.check_completed():
            self.project_complete_button.setEnabled(True)
        else:
            self.project_complete_button.setEnabled(False)
        self.project_edit_button.setEnabled(True)
        self.project_delete_button.setEnabled(True)

    # 打开新建任务对话框
    def open_new_task_dialog(self):
        new_task_dialog = NewTaskDialog()
        new_task_dialog.exec_()
        self.populate_tasks_table()

    # 打开新建项目对话框
    def open_new_project_dialog(self):
        new_project_dialog = NewProjectDialog()
        new_project_dialog.exec_()
        self.populate_projects_table()

    # 打开编辑任务对话框
    def open_edit_task_dialog(self):
        task_id = self.tasks_table.get_id()
        edit_task_dialog = EditTaskDialog(task_id)
        edit_task_dialog.exec_()
        self.populate_tasks_table()

    # 打开编辑项目对话框
    def open_edit_project_dialog(self):
        project_id = self.projects_table.get_id()
        edit_project_dialog = EditProjectDialog(project_id)
        edit_project_dialog.exec_()
        self.populate_projects_table()

    # 标记任务为已完成
    def mark_task_completed(self):
        task_id = self.tasks_table.get_id()
        self.controller.mark_task_completed(task_id)
        project_id = self.check_project_tasks_completed()
        # 如果项目中的所有任务都已完成，则标记项目为已完成
        if project_id:
            mark_project_complete_dialog = MarkProjectCompleteDialog(project_id)
            mark_project_complete_dialog.exec_()
        self.populate_tasks_table()

    # 标记项目和任务为已完成
    def check_project_tasks_completed(self):
        project_id = self.tasks_table.get_task_project_id()
        if project_id:
            if self.controller.check_project_tasks_completed(project_id):
                return project_id
            else:
                return False

    # 标记项目为已完成（有问题）
    def mark_project_completed(self):
        project_id = self.projects_table.get_id()
        self.controller.mark_project_completed(project_id)
        # 如果项目中的所有任务都已完成，则标记项目为已完成
        if not self.check_project_tasks_completed():
            mark_project_tasks_complete_dialog = MarkProjectTasksCompleteDialog(project_id)
            mark_project_tasks_complete_dialog.exec_()
        self.populate_projects_table()

    # 打开删除任务对话框
    def open_delete_task_dialog(self):
        task_id = self.tasks_table.get_id()
        delete_task_dialog = DeleteTaskDialog(task_id)
        delete_task_dialog.exec_()
        self.populate_tasks_table()

    # 打开删除项目对话框
    def open_delete_project_dialog(self):
        project_id = self.projects_table.get_id()
        delete_project_dialog = DeleteProjectDialog(project_id)
        delete_project_dialog.exec_()
        self.populate_projects_table()

    # 打开项目任务对话框
    def open_project_tasks_dialog(self):
        project_id = self.projects_table.get_id()
        project_tasks_dialog = ProjectTasksDialog(project_id)
        project_tasks_dialog.exec_()
        self.populate_projects_table()
