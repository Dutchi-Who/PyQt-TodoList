from PyQt5.QtWidgets import *


# 单选按钮组件（布局）
class RadioButtonWidget(QWidget):
    def __init__(self, button_list):
        super().__init__()

        self.radio_button_group = QButtonGroup()

        self.radio_button_list = []
        for item in button_list:
            self.radio_button_list.append(QRadioButton(item))

        # 第一个 button 默认选中
        self.radio_button_list[0].setChecked(True)

        # 定义一个布局
        self.radio_button_layout = QHBoxLayout()

        # 将 button 添加到 button group 中
        for counter, item in enumerate(self.radio_button_list):
            self.radio_button_layout.addWidget(item)
            self.radio_button_group.addButton(item)
            self.radio_button_group.setId(item, counter)

        self.setLayout(self.radio_button_layout)

    def selected_button(self):
        return self.radio_button_group.checkedId()
