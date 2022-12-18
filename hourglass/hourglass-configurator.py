from PyQt5 import QtWidgets
from PyQt5.QtGui import QFontDatabase, QIcon
from uilib.window import WindowContainer
from util import open_qt_resource
from ui import MainWindow
import subprocess
import json
import sys
import os

from winreg import (
    OpenKey,
    SetValueEx,
    DeleteValue,
    KEY_SET_VALUE,
    REG_SZ,
    HKEY_LOCAL_MACHINE
)


class Application(MainWindow):
    def __init__(self, p):
        super().__init__(p)
        # populate options
        self.appearance_tab.font_family.dropdown.addItems(["Default"] + QFontDatabase().families())
        self.appearance_tab.font_size.dropdown.addItems([str(size) for size in range(100, 501)])
        self.appearance_tab.font_style.dropdown.addItems(["Normal", "Bold"])
        self.appearance_tab.font_color.dropdown.addItems(["Dynamic", "Static"])

        # set default states
        self.appearance_tab.font_size.dropdown.setCurrentText("200")
        self.appearance_tab.font_size.dropdown.setCurrentText("Bold")
        self.formatting_tab.format_input.insertPlainText("%I:%M")
        self.system_tab.clock_update_interval.textedit.setText("100")
        self.system_tab.color_update_interval.textedit.setText("500")
        self.system_tab.launch_on_startup.setChecked(False)

        self.appearance_tab.font_color.dropdown.view().pressed.connect(self.on_color_mode_changed)
        self.system_tab.launch_on_startup.clicked.connect(self.auto_launch_changed)
        self.apply_button.clicked.connect(self.generate_configuration)
        self.start_button.clicked.connect(self.on_start_hourglass)
        self.static_font_color = None
        self.config_path = os.path.join(os.getenv("appdata"), "HourGlass")
        if not os.path.exists(self.config_path):
            os.mkdir(self.config_path)
            self.generate_configuration()
        self.load_configuration()

    @staticmethod
    def auto_launch_changed(state):
        key = OpenKey(HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, KEY_SET_VALUE)
        with key:
            if state:
                SetValueEx(key, "HourGlassAutoLaunch", 0, REG_SZ, str(__file__).replace("hourglass-configurator.py",
                                                                                        "hourglass.exe"))
            else:
                DeleteValue(key, "HourGlassAutoLaunch")

    @staticmethod
    def on_start_hourglass():
        subprocess.Popen(str(__file__).replace("hourglass-configurator.py", "hourglass.exe"))

    def on_color_mode_changed(self, index):
        index = self.appearance_tab.font_color.dropdown.model().itemFromIndex(index).row()
        if index == 1:
            color_picker = QtWidgets.QColorDialog(self)
            self.static_font_color = color_picker.getColor(options=QtWidgets.QColorDialog.ShowAlphaChannel).rgba()
            self.appearance_tab.font_color.dropdown.setCurrentIndex(index)

    def load_configuration(self):
        with open(os.path.join(self.config_path, "hgconf"), "r") as file:
            config = json.load(file)
            self.appearance_tab.font_family.dropdown.setCurrentText(config["appearance"]["font_family"])
            self.appearance_tab.font_size.dropdown.setCurrentText(str(config["appearance"]["font_size"]))
            self.appearance_tab.font_style.dropdown.setCurrentText(config["appearance"]["font_style"])
            self.appearance_tab.font_color.dropdown.setCurrentText(config["appearance"]["font_color"])
            self.static_font_color = config["appearance"]["static_font_color"]

            self.formatting_tab.format_input.clear()
            self.formatting_tab.format_input.insertPlainText(config["formatting"]["format"])

            self.system_tab.clock_update_interval.textedit.setText(str(config["system"]["clock_update_interval"]))
            self.system_tab.color_update_interval.textedit.setText(str(config["system"]["color_update_interval"]))
            self.system_tab.launch_on_startup.setChecked(config["system"]["launch_on_startup"])

    def generate_configuration(self):
        with open(os.path.join(self.config_path, "hgconf"), "w") as file:
            json.dump(
                {
                    "appearance":
                        {
                            "font_family": self.appearance_tab.font_family.dropdown.currentText(),
                            "font_size": int(self.appearance_tab.font_size.dropdown.currentText()),
                            "font_style": self.appearance_tab.font_style.dropdown.currentText(),
                            "font_color": self.appearance_tab.font_color.dropdown.currentText(),
                            "static_font_color": self.static_font_color
                        },

                    "formatting":
                        {
                            "format": self.formatting_tab.format_input.toPlainText()
                        },

                    "system":
                        {
                            "clock_update_interval": int(self.system_tab.clock_update_interval.textedit.text()),
                            "color_update_interval": int(self.system_tab.color_update_interval.textedit.text()),
                            "launch_on_startup": self.system_tab.launch_on_startup.isChecked()
                        }
                },
                file, indent=4)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    retcode = QFontDatabase.addApplicationFont(":/font/opensans.ttf")
    if retcode < 0:
        print("Failed to load default font.")

    wc = WindowContainer(window=Application)
    wc.setWindowIcon(QIcon(":/icons/hourglass.ico"))
    wc.setWindowTitle("HourGlass Configurator")
    wc.setStyleSheet(open_qt_resource(":/style/style.qss"))
    wc.show()

    app.exec()
