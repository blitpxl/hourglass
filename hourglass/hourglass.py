from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QTimer
from clock import Clock
from observer import WallpaperObserver, ConfigObserver
from typing import Union
import json
import sys
import os


CONFIG_PATH = config_path = os.path.join(os.path.join(os.getenv("appdata"), "HourGlass"), "hgconf")


class DesktopClock(Clock):
    def __init__(self):
        super(DesktopClock, self).__init__()
        with open(CONFIG_PATH, "r") as file:
            config = json.load(file)

            wallpaper_observer = WallpaperObserver(self)
            wallpaper_observer.setInterval(config["system"]["color_update_interval"])
            wallpaper_observer.ColorPaletteChanged.connect(lambda color: self.set_font_color(color))

            self.set_font_family(config["appearance"]["font_family"])
            self.set_font_size(config["appearance"]["font_size"])
            self.set_font_style(config["appearance"]["font_style"])
            self.set_formatting(config["formatting"]["format"])
            if config["appearance"]["font_color"] == "Static":
                wallpaper_observer.stop()
                self.set_font_color(QColor.fromRgba(config["appearance"]["static_font_color"]))
            else:
                wallpaper_observer.start()

            clock_timer = QTimer(self)
            clock_timer.setInterval(config["system"]["clock_update_interval"])
            clock_timer.timeout.connect(self.update_time)
            clock_timer.start()


clock: Union[DesktopClock, None] = None


def reload_clock():
    global clock
    clock.close()
    clock = DesktopClock()
    clock.show()


def main():
    global clock
    app = QApplication(sys.argv)

    clock = DesktopClock()
    clock.show()

    config_observer = ConfigObserver(config_path=CONFIG_PATH)
    config_observer.setInterval(100)
    config_observer.ConfigChanged.connect(lambda: reload_clock())
    config_observer.start()

    app.exec()


if __name__ == '__main__':
    main()
