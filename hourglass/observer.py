from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QColor
from os import getenv, stat
from glob import glob
from fast_colorthief import get_palette


class ConfigObserver(QTimer):
    ConfigChanged = pyqtSignal()

    def __init__(self, config_path, p=None):
        super().__init__(p)
        self.timeout.connect(self._observe)
        self._config_path = config_path
        self._current_config = None

    def _observe(self):
        config = self._config_path
        if self._current_config is None:
            self._current_config = stat(config).st_mtime
        else:
            if self._current_config != stat(config).st_mtime:
                self.ConfigChanged.emit()
                self._current_config = stat(config).st_mtime


class WallpaperObserver(QTimer):
    ColorPaletteChanged = pyqtSignal(QColor)

    def __init__(self, p=None):
        super().__init__(p)
        self._appdata_env = getenv("appdata")
        self._current_wallpaper = None
        self.timeout.connect(self._observe)

        self.cache_observe_timer = QTimer(self)
        self.cache_observe_timer.setInterval(500)
        self.cache_observe_timer.timeout.connect(self._get_cached_image)
        self.cache_observe_timer.start()

    def start(self, msec: int = 0) -> None:
        self.cache_observe_timer.start()
        super().start()

    def stop(self) -> None:
        self.cache_observe_timer.stop()
        super().stop()

    def _observe(self):
        wallpaper = f"{self._appdata_env}\\Microsoft\\Windows\\Themes\\TranscodedWallpaper"
        if self._current_wallpaper is None:
            self._current_wallpaper = stat(wallpaper).st_mtime
        else:
            if self._current_wallpaper != stat(wallpaper).st_mtime:
                self.cache_observe_timer.start()
                self._current_wallpaper = stat(wallpaper).st_mtime

    def _get_color_from_cache(self):
        image = glob(f"{self._appdata_env}\\Microsoft\\Windows\\Themes\\CachedFiles\\*.jpg")[0]
        return QColor(*get_palette(image, 2, 1)[1])

    def _get_cached_image(self):
        try:
            self.ColorPaletteChanged.emit(self._get_color_from_cache())
            self.cache_observe_timer.stop()
        except IndexError:
            pass
