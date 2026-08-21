from pathlib import Path

from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtCore import QRectF, Qt

from frontend.components.image import Image


class BannerImageLabel(Image):
    """Image label that center-crops and clips an image."""

    def __init__(self, path: str | Path | None = None, corner_radius: float = 8.0, parent=None):
        super(Image, self).__init__(parent)

        self.path = path
        self._corner_radius = corner_radius

    def paintEvent(self, event):
        pixmap = QPixmap(str(self.path)) if self.path else QPixmap()

        if not pixmap.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

            rect = self.rect()
            w, h = rect.width(), rect.height()

            if w > 0 and h > 0:
                dpr = self.devicePixelRatio()

                scaled = pixmap.scaled(
                    rect.size() * dpr,
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation,
                )

                x = (scaled.width() - int(w * dpr)) // 2
                y = (scaled.height() - int(h * dpr)) // 2

                cropped = scaled.copy(x, y, int(w * dpr), int(h * dpr))
                cropped.setDevicePixelRatio(dpr)

                clip_path = QPainterPath()
                clip_path.addRoundedRect(QRectF(rect), self._corner_radius, self._corner_radius)

                painter.setClipPath(clip_path)
                painter.drawPixmap(0, 0, cropped)
                painter.end()

                return

        super().paintEvent(event)
