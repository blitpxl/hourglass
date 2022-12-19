from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QVariantAnimation
from PyQt5.QtGui import QFont, QColor
from datetime import datetime
from util import shadowify


class Clock(QtWidgets.QWidget):
    def __init__(self, p=None):
        super().__init__(p)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint | Qt.WindowTransparentForInput | Qt.SplashScreen)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        shadowify(self, radius=0, color=(0, 0, 0, 64))
        self._main_layout = QtWidgets.QHBoxLayout(self)
        self._clock = QtWidgets.QLabel("00:00", self)
        self._main_layout.addWidget(self._clock, alignment=Qt.AlignCenter)
        self.showMaximized()
        self._current_color = QColor(0, 0, 0)
        self._animation = QVariantAnimation(self)
        self._animation.setDuration(1000)
        self._formatting = "%I:%M"

    def _set_current_color(self, color):
        self._current_color = color

    def set_text(self, text: str):
        self._clock.setText(text)
        self._clock.setAlignment(Qt.AlignCenter)

    def update_time(self):
        self.set_text(datetime.now().strftime(self._formatting))

    @property
    def font_family(self):
        return self._clock.font().family()

    def set_font_family(self, family: str):
        font = QFont(family)
        self._clock.setFont(font)

    @property
    def font_size(self):
        return self._clock.font().pixelSize()

    def set_font_size(self, size: int):
        font = QFont(self._clock.font().family(), size)
        self._clock.setFont(font)

    @property
    def font_bold(self):
        return self._clock.font().bold()

    def set_font_style(self, style: str):
        font = self._clock.font()
        if style == "Bold":
            font.setBold(True)
        else:
            font.setBold(False)
        self._clock.setFont(font)

    @property
    def font_color(self):
        return self._current_color

    def set_font_color(self, color: QColor):
        self._animation.setStartValue(self._current_color)
        self._animation.setEndValue(color)
        self._animation.valueChanged.connect(lambda clr: self._clock.setStyleSheet(f"color: rgba({clr.red()}, "
                                                                                   f"{clr.green()}, {clr.blue()}, "
                                                                                   f"{clr.alpha()})"))
        self._animation.finished.connect(lambda: self._set_current_color(color))
        self._animation.start()

    @property
    def formatting(self):
        return self._formatting

    def set_formatting(self, formatting):
        self._formatting = formatting
