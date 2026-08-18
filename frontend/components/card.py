from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtCore import QObject, Qt, QRectF

class BannerImageLabel(QLabel):
    """QLabel that center-crops and clips an image."""

    def __init__(self, pixmap: QPixmap | None = None, corner_radius: float = 8.0):
        super().__init__()

        self._pixmap = pixmap
        self._corner_radius = corner_radius

    def set_banner_pixmap(self, pixmap: QPixmap | None):
        self._pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        if self._pixmap and not self._pixmap.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            rect = self.rect()
            w, h = rect.width(), rect.height()

            if w > 0 and h > 0:
                scaled = self._pixmap.scaled(
                    rect.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )

                x = (scaled.width() - w) // 2
                y = (scaled.height() - h) // 2
                
                cropped = scaled.copy(x, y, w, h)

                path = QPainterPath()
                path.addRoundedRect(QRectF(rect), self._corner_radius, self._corner_radius)

                painter.setClipPath(path)
                painter.drawPixmap(0, 0, cropped)
                painter.end()

                return

        super().paintEvent(event)


class Card(QFrame):
    """Base composable Card container."""

    CARD_WIDTH = 200
    CARD_HEIGHT = 250

    def __init__(self, parent: QObject):
        super().__init__(parent)

        self.setFixedSize(self.CARD_WIDTH, self.CARD_HEIGHT)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.card_layout = QVBoxLayout(self)
        self.card_layout.setContentsMargins(12, 12, 12, 12)
        self.card_layout.setSpacing(10)
