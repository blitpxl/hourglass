from PyQt5.QtGui import QColor
from PyQt5.QtCore import QFile, QIODevice
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


def open_qt_resource(url):
    file = QFile(url)
    file.open(QIODevice.ReadOnly)
    bytes_content = file.readAll()
    content = bytes(bytes_content).decode("utf-8")
    return content


def shadowify(widget, xoffset=0, yoffset=4, radius=4, color=(0, 0, 0, 62)):
    shadow = QGraphicsDropShadowEffect(widget.parent())
    shadow.setOffset(xoffset, yoffset)
    shadow.setBlurRadius(radius)
    shadow.setColor(QColor(*color))
    widget.setGraphicsEffect(shadow)
