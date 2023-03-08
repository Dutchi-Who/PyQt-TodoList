import sqlite3
from datetime import datetime

# 用这个类集中处理操作数据库
class DbController:
    # 构造函数
    def __init__(self, db_name):
        # 数据库名称作为私有属性
        self.db_name = db_name

    # 用于执行增删改操作
    def query(self, sql, data):
        # 连接数据库
        with sqlite3.connect(self.db_name) as db:
            # 将db数据库流传给cursor
            cursor = db.cursor()
            # 开启外键约束
            cursor.execute("PRAGMA Foreign_Keys = ON")
            cursor.execute(sql, data)
            # 提交数据库（thread关闭）
            db.commit()

    # 用于执行查询操作
    def select_query(self, sql, data=None):
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            if data:
                cursor.execute(sql, data)
            else:
                cursor.execute(sql)

        # 返回查询结果（按列表）
        return cursor.fetchall()

    # 添加任务到数据库表
    def add_task(self, description, deadline, project_id):
        # 获取当前时间
        created = datetime.now()
        # 用一个str类型变量存储sql语句
        sql_add_task = "INSERT INTO Tasks (Description, Deadline, Created, ProjectID) VALUES (?,?,?,?)"
        # 执行sql语句（第一个参数是sql语句（str类型），第二个参数是一个tuple类型的数据，用于替换sql语句中的问号）
        self.query(sql_add_task, (description, deadline, created, project_id))

    # 添加项目到数据库表
    def add_project(self, description, deadline):
        created = datetime.now()
        sql_add_project = "INSERT INTO Projects (Description, Deadline, Created) VALUES (?,?,?)"
        self.query(sql_add_project, (description, deadline, created))

    # 删除任务
    def delete_task(self, task_id):
        self.query("DELETE FROM Tasks WHERE TaskID = ?", (task_id,))

    # 仅删除项目
    def delete_project_only(self, project_id):
        self.query("UPDATE Tasks SET ProjectID = NULL WHERE ProjectID = ?", (project_id,))
        self.query("DELETE FROM Projects WHERE ProjectID = ?", (project_id,))

    # 删除任务和项目
    def delete_project_and_tasks(self, project_id):
        self.query("DELETE FROM Tasks WHERE ProjectID = ?", (project_id,))
        self.query("DELETE FROM Projects WHERE ProjectID = ?", (project_id,))

    # 标记任务为已完成
    def mark_task_completed(self, task_id):
        completed = datetime.now()
        sql_mark_completed = "UPDATE Tasks SET Completed = ? WHERE TaskID = ?"
        self.query(sql_mark_completed, (completed, task_id))

    # 标记项目为已完成
    def mark_project_completed(self, project_id):
        completed = datetime.now()
        sql_mark_completed = "UPDATE Projects SET Completed = ? WHERE ProjectID = ?"
        self.query(sql_mark_completed, (completed, project_id))

    # 标记项目和任务为已完成
    def mark_project_tasks_completed(self, project_id):
        completed = datetime.now()
        sql_mark_completed = "UPDATE Tasks SET Completed = ? WHERE ProjectID = ?"
        self.query(sql_mark_completed, (completed, project_id))

    # 获取任务和项目ID
    def get_task_project_id(self, task_id):
        sql_get_project_id = "SELECT ProjectID FROM Tasks WHERE TaskID = ?"
        results = self.select_query(sql_get_project_id, (task_id,))
        return results[0][0]

    # 检查项目和任务是否已完成
    def check_project_tasks_completed(self, project_id):
        sql_check_project = "SELECT TaskID FROM Tasks WHERE ProjectID = ? AND Completed IS NULL"
        results = self.select_query(sql_check_project, (project_id,))
        if not results:
            return True
        return False

    # 编辑任务描述
    def edit_task_description(self, task_id, description):
        sql_edit_descr = "UPDATE Tasks SET Description = ? WHERE TaskID = ?"
        self.query(sql_edit_descr, (description, task_id))

    # 设置任务截止日期
    def set_task_deadline(self, task_id, deadline):
        sql_set_deadline = "UPDATE Tasks SET Deadline = ? WHERE TaskID = ?"
        self.query(sql_set_deadline, (deadline, task_id))

    # 分配任务到项目
    def assign_task_to_project(self, task_id, project_id):
        sql_assign_task = "UPDATE Tasks SET ProjectID = ? WHERE TaskID = ?"
        self.query(sql_assign_task, (project_id, task_id))

    # 设置项目截止日期
    def set_project_deadline(self, project_id, deadline):
        sql_set_deadline = "UPDATE Projects SET Deadline = ? WHERE ProjectID = ?"
        self.query(sql_set_deadline, (deadline, project_id))

    # 编辑项目描述
    def edit_project_description(self, project_id, description):
        sql_edit_descr = "UPDATE Projects SET Description = ? WHERE ProjectID = ?"
        self.query(sql_edit_descr, (description, project_id))

    # 获取所有任务
    def get_all_tasks(self):
        results = self.select_query("SELECT * FROM Tasks")
        return results

    # 获取未完成的任务
    def get_active_tasks(self):
        results = self.select_query("SELECT * FROM Tasks WHERE Completed IS NULL")
        return results

    # 获取已完成的任务
    def get_completed_tasks(self):
        results = self.select_query("SELECT * FROM Tasks WHERE Completed IS NOT NULL")
        return results

    # 获取单个任务
    def get_single_task(self, task_id):
        results = self.select_query("SELECT * FROM Tasks WHERE TaskID = ?", (task_id,))
        return results

    # 获取所有项目
    def get_all_projects(self):
        results = self.select_query("SELECT * FROM Projects")
        return results

    # 获取未完成的项目
    def get_active_projects(self):
        results = self.select_query("SELECT * FROM Projects WHERE Completed IS NULL")
        return results

    # 获取已完成的项目
    def get_completed_projects(self):
        results = self.select_query("SELECT * FROM Projects WHERE Completed IS NOT NULL")
        return results

    # 获取单个项目
    def get_single_project(self, project_id):
        results = self.select_query("SELECT * FROM Projects WHERE ProjectID = ?", (project_id,))
        return results

    # 获取项目中的任务
    def get_project_tasks(self, project_id):
        results = self.select_query("SELECT * FROM Tasks WHERE ProjectID = ?", (project_id,))
        return results
