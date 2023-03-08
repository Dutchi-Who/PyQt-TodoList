import sqlite3


# 创建数据库
def createNewDatabase(db_name):
    # 创建数据库连接
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        # 创建 Projects 表
        cursor.execute("""CREATE TABLE Projects(
                    ProjectID integer,
                    Description text,
                    Deadline date,
                    Created timestamp,
                    Completed timestamp,
                    PRIMARY KEY(ProjectID));""")
        # 创建 Tasks 表
        cursor.execute("""CREATE TABLE Tasks(
            TaskID integer,
            Description text,
            Deadline date,
            Created timestamp,
            Completed timestamp,
            ProjectID integer,
            PRIMARY KEY(TaskID),
            FOREIGN KEY(ProjectID) REFERENCES Projects(ProjectID));""")

        db.commit()
