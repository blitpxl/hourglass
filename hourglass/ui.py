from uilib.window import Window
from uilib.util import shadowify
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
import webbrowser
from res.generated.resources import *   # NOQA


class DropDownField(QtWidgets.QWidget):
    def __init__(self, fieldname, p, dropdown_widget=QtWidgets.QComboBox):
        super(DropDownField, self).__init__(p)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignVCenter)
        self.setFixedHeight(120)

        self.dropdown_label = QtWidgets.QLabel(fieldname, self)
        self.dropdown = dropdown_widget(self)
        self.dropdown.setItemDelegate(QtWidgets.QStyledItemDelegate())
        self.dropdown.setFixedSize(300, 35)
        shadowify(self.dropdown, yoffset=17, radius=32)

        self.main_layout.addWidget(self.dropdown_label)
        self.main_layout.addWidget(self.dropdown)


class LineEditField(QtWidgets.QWidget):
    def __init__(self, fieldname, p, textedit_widget=QtWidgets.QLineEdit):
        super(LineEditField, self).__init__(p)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignVCenter)
        self.setFixedHeight(120)

        self.textedit_label = QtWidgets.QLabel(fieldname, self)
        self.textedit = textedit_widget(self)
        self.textedit.setFixedSize(300, 40)
        shadowify(self.textedit, yoffset=17, radius=32)

        self.main_layout.addWidget(self.textedit_label)
        self.main_layout.addWidget(self.textedit)


class AppearanceTab(QtWidgets.QWidget):
    def __init__(self, p):
        super().__init__(p)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.first_row_layout = QtWidgets.QHBoxLayout()
        self.second_row_layout = QtWidgets.QHBoxLayout()

        self.font_family = DropDownField("Font Family", self)
        self.font_size = DropDownField("Font Size (px)", self)
        self.font_style = DropDownField("Font Style", self)
        self.font_color = DropDownField("Font Color", self)

        self.first_row_layout.addWidget(self.font_family)
        self.first_row_layout.addWidget(self.font_size)
        self.second_row_layout.addWidget(self.font_style)
        self.second_row_layout.addWidget(self.font_color)

        self.main_layout.addLayout(self.first_row_layout)
        self.main_layout.addLayout(self.second_row_layout)


class FormattingTab(QtWidgets.QWidget):
    def __init__(self, p):
        super().__init__(p)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.format_input = QtWidgets.QTextEdit(self)
        self.format_input.setPlaceholderText("Format cannot be empty!")
        self.info_label = QtWidgets.QLabel(self)
        self.info_label.setOpenExternalLinks(True)
        self.info_label.setText("To see more about formatting, see: "
                                "<a style= \"color: #86E9FF\" href=\"https://docs.python.org/3.8/library/datetime.html#"
                                "strftime-and-strptime-format-codes\">Time Format Codes</a>")
        self.main_layout.addWidget(self.format_input)
        self.main_layout.addWidget(self.info_label)


class SystemTab(QtWidgets.QWidget):
    def __init__(self, p):
        super().__init__(p)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.clock_update_interval = LineEditField("Clock Update Interval (ms)", self)
        self.color_update_interval = LineEditField("Dynamic Color Update Interval (ms)", self)
        self.launch_on_startup = QtWidgets.QCheckBox("Launch on startup", self)
        self.launch_on_startup.setFixedHeight(50)
        shadowify(self.launch_on_startup, yoffset=17, radius=32)
        self.main_layout.addWidget(self.clock_update_interval)
        self.main_layout.addSpacing(-14)
        self.main_layout.addWidget(self.color_update_interval)
        self.main_layout.addWidget(self.launch_on_startup)


class AboutTab(QtWidgets.QWidget):
    def __init__(self, p):
        super().__init__(p)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.branding = QtWidgets.QLabel(self)
        self.branding.setPixmap(QPixmap(":/icons/about.svg").scaled(500, 250, transformMode=Qt.SmoothTransformation,
                                                                    aspectRatioMode=Qt.KeepAspectRatio))
        self.version_n_links = QtWidgets.QLabel("v1.0 (18/12/22) "
                                                "<a style= \"color: #86E9FF\" href=\"https://github.com/vinrato\">"
                                                "Github</a> "
                                                "<a style= \"color: #86E9FF\" "
                                                "href=\"https://twitter.com/vinrato\">Twitter</a> ", self)
        self.version_n_links.setOpenExternalLinks(True)
        self.donate_label = QtWidgets.QLabel("Consider Donating")
        self.donate_paypal = QtWidgets.QPushButton(self)
        self.donate_paypal.setIcon(QIcon(":/icons/paypal.png"))
        self.donate_paypal.setObjectName("donate-paypal")
        self.donate_paypal.setIconSize(QSize(200, 50))
        self.donate_paypal.clicked.connect(self.open_paypal)
        self.main_layout.addWidget(self.branding, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.main_layout.addWidget(self.version_n_links, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.donate_label, alignment=Qt.AlignCenter | Qt.AlignBottom)
        self.main_layout.addWidget(self.donate_paypal, alignment=Qt.AlignCenter | Qt.AlignBottom)

    @staticmethod
    def open_paypal():
        webbrowser.open(r"https://www.paypal.com/paypalme/vinrato")


class MainWindow(Window):
    def __init__(self, p):
        super().__init__(p)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.tab_layout = QtWidgets.QHBoxLayout()
        self.tab_layout.setSpacing(15)
        self.tab_layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.bottom_layout = QtWidgets.QHBoxLayout()

        self.appearance_tab_btn = QtWidgets.QPushButton("Appearance", self)
        self.formatting_tab_btn = QtWidgets.QPushButton("Formatting", self)
        self.system_tab_btn = QtWidgets.QPushButton("System", self)
        self.about_tab_btn = QtWidgets.QPushButton("About", self)

        self.appearance_tab_btn.setObjectName("tab-button")
        self.formatting_tab_btn.setObjectName("tab-button")
        self.system_tab_btn.setObjectName("tab-button")
        self.about_tab_btn.setObjectName("tab-button")

        self.tab_layout.addWidget(self.appearance_tab_btn)
        self.tab_layout.addWidget(self.formatting_tab_btn)
        self.tab_layout.addWidget(self.system_tab_btn)
        self.tab_layout.addWidget(self.about_tab_btn)

        self.tab_group = QtWidgets.QButtonGroup(self)
        for child in self.findChildren(QtWidgets.QPushButton):
            if child.objectName() == "tab-button":
                child.setCheckable(True)
                self.tab_group.addButton(child)
        self.appearance_tab_btn.setChecked(True)

        self.main_layout.addLayout(self.tab_layout)

        self.stack_layout = QtWidgets.QStackedLayout()

        self.appearance_tab_btn.clicked.connect(lambda: self.stack_layout.setCurrentIndex(0))
        self.formatting_tab_btn.clicked.connect(lambda: self.stack_layout.setCurrentIndex(1))
        self.system_tab_btn.clicked.connect(lambda: self.stack_layout.setCurrentIndex(2))
        self.about_tab_btn.clicked.connect(lambda: self.stack_layout.setCurrentIndex(3))

        self.appearance_tab = AppearanceTab(self)
        self.formatting_tab = FormattingTab(self)
        self.system_tab = SystemTab(self)
        self.about_tab = AboutTab(self)

        self.stack_layout.addWidget(self.appearance_tab)
        self.stack_layout.addWidget(self.formatting_tab)
        self.stack_layout.addWidget(self.system_tab)
        self.stack_layout.addWidget(self.about_tab)

        self.main_layout.addLayout(self.stack_layout)

        self.apply_button = QtWidgets.QPushButton("Apply", self)
        self.apply_button.setObjectName("generic-button")
        self.start_button = QtWidgets.QPushButton("Start HourGlass", self)
        self.start_button.setObjectName("generic-button")

        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignRight)

        self.button_layout.addWidget(self.start_button, alignment=Qt.AlignRight)
        self.button_layout.addWidget(self.apply_button, alignment=Qt.AlignRight)
        self.main_layout.addLayout(self.button_layout)
        self.stack_layout.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, tab_index):
        # if the user is on the about tab, hide the apply button
        if tab_index == 3:
            self.apply_button.setStyleSheet("background: transparent; color: transparent; border: 1px solid #242424;")
            self.start_button.setStyleSheet("background: transparent; color: transparent; border: 1px solid #242424;")
        else:
            self.apply_button.setStyleSheet("""width: 120px; height: 30px; background: 
            #434343; border: none; border-top: 2px solid #727272; border-radius: 4px; font-family: "Open Sans"; 
            font-weight: bold; font-size: 14px; color: #BEBEBE; } QPushButton#generic-button:hover { border-top: 
            2px solid #86E9FF; color: #FFFFFF; """)
            self.start_button.setStyleSheet("""width: 120px; height: 30px; background: 
            #434343; border: none; border-top: 2px solid #727272; border-radius: 4px; font-family: "Open Sans"; 
            font-weight: bold; font-size: 14px; color: #BEBEBE; } QPushButton#generic-button:hover { border-top: 
            2px solid #86E9FF; color: #FFFFFF; """)

        # the reason im using these stylesheets to hide the apply button instead od just setting it to visible/invisible
        # is that it'll throw an error:
        # "UpdateLayeredWindowIndirect failed for ptDst=(833, 280), size=(894x520), dirty=(902x524 -4, 0)
        # (The parameter is incorrect.)"
