from pathlib import Path

from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QLabel


class Image(QLabel):
    """A lightweight image label."""

    def __init__(self, path: str | Path, size: QSize = QSize(48, 48), parent=None):
        super().__init__(parent)

        self.path = path
        self.image_size = size

        self.setFixedSize(self.image_size)

    def paintEvent(self, event):
        if type(self) is not Image:
            super().paintEvent(event)
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        dpr = self.devicePixelRatio()
        pixmap = QPixmap(self.path)

        scaled = pixmap.scaled(
            self.image_size * dpr,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )

        scaled.setDevicePixelRatio(dpr)
        painter.drawPixmap(0, 0, scaled)
        painter.end()

        super().paintEvent(event)
