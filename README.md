# Python程序设计 大作业报告
 
## 1. 目的与要求

本次课程设计要求自拟题目，设计一个能够独立运行的程序，代码量不少于200行。

### 1.1 评分要求

- 文档（格式，描述，术语，图表，规范） 30%
- 代码（加注释） 30%
- 功能（实用，新颖） 20%
- 加分项（使用课堂未讲过的知识，并在文档重点突出）20%

## 2. 题目

基于PyQt5的简单任务清单（To Do List）实现

### 2.1 概要设计

使用Python实现一个拥有GUI界面的简易任务清单桌面APP。该APP包含：
- 一个主窗口，展示正在进行的各项任务
- 添加/编辑任务的窗口：可以自定义每个任务的截止时间、描述信息等等
- 实现任务、项目两种清单模式。任务包含在项目之中，一个项目可以有很多任务。可以为项目设置截止时间。
- 尽量美观，简洁。

### 2.2 详细设计

#### 1. 程序入口

程序入口负责启动程序，初始化GUI框架和连接数据库的功能。

#### 2. 程序主菜单

程序主菜单中按标签页分别展示任务和项目。任务和项目的展示和设置页面互相独立。单个标签页包含：
- 显示现有的任务、项目
- 可以按类别切换显示：未完成、已完成、全部
- 排序任务、项目
- 用于改变状态的按钮：新建、标记为已完成、编辑、删除、退出（程序）

#### 3. 新建任务、项目的窗口

新建窗口将添加任务或者项目到数据库中。在新建时，用户先给定项目、任务的描述，而后在日历控件上选择想要添加的截止日期（也可以选择不添加截止日期）。

#### 4. 编辑任务、项目的窗口

编辑窗口读取数据库中已有的该项目的信息，并允许用户对其进行修改。可以编辑的内容和“新建窗口”部分一致。

#### 5. 删除任务、项目的窗口

删除窗口允许用户删除一个任务或者项目。如果删除的任务附属于项目，则需要提醒用户在删除后该项目中将不包含此任务；如果删除的是含有任务的项目，则需要提醒用户在删除后，项目下的任务将不属于任何项目。

#### 6. 标记项目、任务已完成

允许用户切换项目和任务的状态为已完成。已完成的任务不会显示在“已完成的任务”列表筛选条件下。

#### 7. 日历控件

日历控件用于新建窗口和编辑窗口，允许用户选择任务、项目的截止日期。如果用户勾选了“无时间限制”选项，则禁用整个日历控件。

#### 8. 底部按钮控件

底部按钮负责控制项目的状态，允许新增、编辑、删除和标记为已完成。

#### 9. 连接数据库

该程序的数据存储于数据库，需要实现与数据库的连接。

## 3. 程序实现

本程序使用Python 3.11实现。需要自行安装[SQLite3](https://www.sqlite.org/download.html)运行环境和工具集，以及使用 `pip install` 安装[PyQt5](https://doc.qt.io/qtforpython/)库。

本程序基于桌面端开发，请使用Windows 10及以上版本的桌面平台打开PyCharm等IDE并运行 `to_do_list.py` 及其附属源文件，并确保 `to_do.db` 数据库文件存在。

### 3.1 需求分析

本程序需要设计GUI，为了轻量化考虑，使用了PyQt作为GUI框架。同样地，使用SQLite而不是 MySQL 作为数据库。

此外，考虑到整体的代码量将会比较庞大，因此使用了面向对象设计思想，并包含众多Python新版本的特性。

### 3.2 使用技术介绍

除了Python本身，本次使用到框架、库和插件有：
- PyQt5
- SQLite3
- Pandoc
- ...

#### Python面向对象

为了更好地配合PyQt框架进行程序设计，我深入研究了Python的面向对象机制。
和其它编程语言相似，Python可以定义一个类 `class`：

```python
class MyClass:
	def __init__(self):
		self.name = "Bob"
		
	def myPublicMethod(self):
		print(f"Hello, {self.name}.")


c = MyClass()
c.myPublicMethod() # output: Hello, Bob.
```

使用 `__init__` 定义类的构造函数，而在构造函数中定义的 `self.name` 等等以 `self.` 开头的变量，都是类的私有数据成员。

而在构造函数外部定义的，不以双下划线 `__` 开头的函数，皆为公有方法（如果以双下划线开头，如 `__insert()` 则为私有方法）。

Python的类也支持继承。类继承自父类后，将可以调用父类的所有方法和数据成员。

```python
class Base:
	# ...
	def foo(self):
		print("base")

class Derived(Base):
	# ...

d = Derived()
d.foo()      # output: base
```

#### PyQt5实现GUI和程序框架

本次大作业我选用 PyQt5 作为前端框架进行开发。其中一个理由是，PyQt5无需 HTML，CSS，JavaScript 等语言实现前端的页面布局和交互逻辑，它直接使用Python本身来编写这些元素。

对于每一个 PyQt 的窗口类（继承自 `QWidget` 类的自定义类）它的构造函数中将调用设定窗口布局的方法完成实例化。

以本程序中 `EditDialog` 类为例，该类对应的窗口在用户新建或者修改任务时调用，允许用户设置任务的具体信息：

```python
# 编辑任务/项目对话框  
class EditDialog(QDialog):  
  
    def __init__(self):  
        super().__init__()  
        
		# ...
		
		# 定义控件类型
        self.description_label = QLabel("描述: ")  
        self.description_line_edit = QLineEdit()  
        self.deadline_label = QLabel("截止日期: ")  
        self.deadline_calendar_widget = QCalendarWidget()  
        
        # ...
        
        self.no_deadline_checkbox = QCheckBox("无时间限制")  
        
		# 定义窗口布局
        self.description_deadline_layout = QVBoxLayout()  
        self.description_deadline_layout.addWidget(self.description_label)  
        self.description_deadline_layout.addWidget(self.description_line_edit)  
        self.description_deadline_layout.addWidget(self.deadline_label)  
        self.description_deadline_layout.addWidget(self.deadline_calendar_widget)  
        self.description_deadline_layout.addWidget(self.no_deadline_checkbox)
```

可以看到，在构造函数内定义完每一个窗口内的控件后，又定义了一个布局类型的变量：

```python
self.description_deadline_layout = QVBoxLayout()
```

这里接收的类 `QVBoxLayout` ，拆解开来的含义是：
- `Q`：代表这是一个 `Qt` 库的类型；
- `V`：`Vertical` 的缩写，代表垂直布局（从上到下依次排列）；
- `Box`：代表窗口的布局是使用正方形的盒子约束的（还有其它不同的定义方式）；
- `Layout`：顾名思义，代表布局。

在此之后，将布局内容一个一个按顺序 `addWidget` 加入 `Layout` 对象即可。

#### Qt的设计模式：信号与槽

承接上段，了解完 Qt 定义GUI的方式后，接下来需要明白 Qt 是如何定义程序的逻辑的。

PyQt5 是 Qt 公司的产品。而 Qt 公司早在1990年就为 C++ 语言开发框架（那时还没有 Python 这门语言），在那个“设计模式”一词都颇为新鲜，MVC，MVVM等设计模式都还没被验证的时候，Qt 公司提出了“信号-槽”模型（signals and slots)，并一直沿用至今（Qt6 for C++）。

在 Python 这门语言发布后，Qt 也迅速跟进了在 Python 上的 PyQt 框架。

信号与槽是 PyQt 的核心设计思想。简单来说，当用户在界面上按下一个按钮时，它将触发一个信号。而在用户界面的窗口（和后台数据库等）之中，会有一个或者几个控件会接收这个信号，称之为“槽”。当一个信号进入一个槽时，用户按下的按钮触发了相应事件，这个过程称之为连接。

在编写Python代码的时候，继承自 `QObject` 顶层类的所有控件都默认具有槽和接口。我们在编程时需要做的仅仅是将它们连接起来：

```python
# TaskProjectTabs.py
self.tabs.currentChanged.connect(self.refresh_tab)
```

这个 `connect` 方法，将对象自己（`self`）与 `refresh_tab()` 相连接，使得前端窗口产生了变化。

这样的连接在程序中随处可见，是程序设计核心中的核心。

#### SQLite3轻量数据库

碍于本人对数据库了解不深，为了尽快完成大作业的要求，我只好选择相对轻量的 SQLite3 数据库系统作为本程序的数据库。

安装好 SQLite 3 环境和控制台后，使用 Python 调用 SQLite3 时需要先将其导入进来：

```python
import sqlite3
```

因此，最好的方式是将所有操作数据库的方式集中到一个 `.py` 文件，并提供 Python 的接口供其它函数调用。

在本程序中，`DbController` 类就承担了这样的工作。碍于篇幅限制，请在“3.4 核心代码”部分查看有关 `DbController` 类的具体设计。

#### Python `with` 关键字

在连接数据库与访问本地文件时，需要使用异常处理模块将代码包裹起来，预防错误的数据流干扰程序的正常运行。

自 Python 2.5 起，`with` 关键字被加入了 Python。对于控制外部的文件流、数据流（如读写文件，访问数据库，连接网络等），一般我们都需要用一个异常处理模块将它们包裹起来，处理意想不到的情况：

```python
try:
	a = file.read() # 打开文件
	# ... 执行代码
except:
	# 处理异常
finally:
	a.close()       # 关闭文件
```

在比较复杂的使用场合，这种写法过于冗长。Python 使用了 `with` 关键字提供了对此类 `try-except` 场合的语法糖：

```python
with file.read() as a:
	# ... 执行代码
```

上文 `with` 语句是先前 `try-except` 的等价写法。当一个数据流能够提供打开、关闭的方法，并在使用过程中会抛出异常时，就可以使用 `with` 语句对其进行简化。让开发者**专注于业务的实现**，并让代码的阅读者能够更好地**关注程序逻辑本身**。

#### 使用 Markdown to Docx 插件统一文档格式

众所周知，Markdown 是一种轻量级的文本文档格式，它能够用类似 HTML 的标签和语法约定对纯文本构成的文档赋予结构，从而让格式统一，让编写者专注于内容。

在本次大作业文档中，使用了 Pandoc on Obsidian 插件（Obsidian 是一款笔记软件，能够编辑 Markdown 文档），将 `.md` 文档转化成 `.docx` 文档。生成的文档内容不会出现格式错误。

从 Markdown 文件转到 docx 文档后，保留了段落、正文、标题、注释、脚注等等核心的文本内容。并且可以通过 Word 文档“样式”模块进行修改，做到修改一处，全局应用。

### 3.3 运行界面

#### 主菜单

![Pasted image 20221121143641.png](screenshots/Pasted%20image%2020221121143641.png)

#### 新增任务

![Pasted image 20221121143750.png](screenshots/Pasted%20image%2020221121143750.png)

#### 删除任务

![Pasted image 20221121143812.png](screenshots/Pasted%20image%2020221121143812.png)

#### 展示全部任务

![Pasted image 20221121143836.png](screenshots/Pasted%20image%2020221121143836.png)

#### 按截止日期排序

![Pasted image 20221121143910.png](screenshots/Pasted%20image%2020221121143910.png)

### 3.4 核心代码

#### 主程序入口

```python
import sys  
import os  
from CreateNewDatabase import *  
from TaskProjectTabs import *  
  
  
# 自定义的类，表示主窗口。继承了 PyQt5.QtWidgets.QMainWindowclass ToDoWindow(QMainWindow):  
  
    # 构造函数  
    def __init__(self):  
        super().__init__()  # 调用父类的构造函数  
  
        # 设置窗口标题和大小  
        self.setWindowTitle("任务清单")  
        self.setMinimumHeight(300)  
  
        # 主菜单 UI        self.central_widget = TaskProjectTabs()  
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
```

#### 任务、项目窗口显示信息（基类方法）

```python
class TableWidget(QTableWidget):  
  
    def __init__(self):  
        super().__init__()  
        self.controller = DbController("to_do.db")  
  
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)  
        self.setSelectionBehavior(QTableView.SelectRows)  
        self.setShowGrid(False)  
  
    # 显示任务  
    def show_items(self, item_list):  
        if len(item_list) == 0:  
            self.setRowCount(0)  
        else:  
            row = 0  
            for entry in item_list:  
                if entry[4] == None:  
                    active = True  
                else:  
                    active = False  
                self.setRowCount(row + 1)  
                column = 0  
                for item in entry:  
                    if item == None:  
                        item = ""  
                    elif column == 3 or column == 4:  
                        item = str(item[:-7])  
                    table_item = QTableWidgetItem(str(item))  
                    if column == 2 and item != "" and active:  
                        if check_overdue(item):  
                            table_item.setForeground(QColor(255, 0, 0))  
                    self.setItem(row, column, table_item)  
                    column += 1  
                row += 1
```

#### 日历控件

```python
# 编辑任务/项目对话框  
class EditDialog(QDialog):  
  
    def __init__(self):  
        super().__init__()  
        
        # ...
        
		# 新建日历组件
        self.deadline_calendar_widget = QCalendarWidget()
        # 设置可用的最小日期为今天（过期的不能选择）
		self.deadline_calendar_widget.setMinimumDate(datetime.today())
		# ...
	
	# ...
	
	# 日历控件  
	def toggle_calendar(self):  
	    if self.no_deadline_checkbox.isChecked():  
	        self.deadline_calendar_widget.setEnabled(False)  
	    else:  
	        self.deadline_calendar_widget.setEnabled(True)
```

#### 数据库连接类：`DbController`

```python
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
```

### 3.5 代码调试过程中遇到的问题

#### 连接数据库失败

在初期调试时，遇到过几十次数据库连接失败的问题。我一边想借助 PyCharm Professional 优秀的IDE工具帮助我操作数据库，但是我会写Python，会写一点SQL语句，对于这个工具我还是很不熟悉。

后来，我新建了一个 `test.py` 测试这个数据库相关的信息，才慢慢解决了这个问题。

#### 在“任务”视图返回主菜单时异常退出

在调试这个返回功能时，每当我点击“完成”按钮后程序都会闪退。后来发现是我没有将变量连接到正确的槽导致的。

在这个过程中，使用 PyCharm 单步调试分析给了我很大帮助。

## 4. 自我评价

### 4.1 学习过程中的收获

我想到做一个“任务清单”APP，是因为我生活中经常使用的一款时间管理软件：滴答清单。在这段学习过后，我也深刻理解到，做一个看似简单的任务清单APP背后有这么多需要设计的注意点，而我的实现距离市面上商用的任务清单还有非常大的距离，跟他们相比，我做的仅仅是一个玩具级的项目。

在本次学习中，我更多地接触了Python的框架。起初看到PyQt的时候我是十分疑惑的，就是因为这个名字。我以前学过 Qt for C++，当时还不知道 Qt 为 Python 也做了 GUI 框架。经过不断学习，我发现Python 这门语言本身的简洁和高效让Qt的GUI设计能够更有效率。也正因如此，可以使用 Python 作为脚本设计GUI（这换成其它低级语言绝对做不到）。

比较可惜的是，在后来上网学习和查询时，我发现Qt 公司后来推出的 PySide6 相比 PyQt5 的编程体验更加优秀，做出来GUI的效果也更好。可惜了解到这一点的时候已经进入了项目的晚期，我已经不可能将它们全部推翻重做了。

另外，我很喜欢 Python 的装饰器功能。装饰器可以在用户进入一个函数之前对参数进行检查，相比普通的返回值和异常抛出，用装饰器进行书写更加便捷和美观。同样地，很多参数合理性检查都由PyQt框架帮我执行了，导致我没有什么机会使用装饰器。

### 4.2 项目可改进的地方

1. 可以支持提醒，通过windows 系统通知发送到桌面；
2. 任务清单的截止日期设置可以增加对一天中具体时间的支持，让用户一天内的突发事件也可以使用这个系统进行管理；
3. 任务清单可以设置循环任务，比如背单词，每天都需要有截止日期，每天都需要提醒。

### 4.3 总结

通过本次学习，我进一步巩固了已经掌握的Python知识，并且学习了新的框架和数据库使用方法。我会在日后的编程和学习中进一步利用Python的优势，写出我自己的程序。