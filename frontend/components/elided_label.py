from PySide6.QtGui import QPainter, QFontMetrics
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class ElidedLabel(QLabel):
    """Label component that elides text."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumWidth(0)

    def paintEvent(self, event):
        painter = QPainter(self)
        metrics = QFontMetrics(self.font())

        rect = self.contentsRect()
        elided_text = metrics.elidedText(self.text(), Qt.TextElideMode.ElideRight, rect.width())

        painter.drawText(rect, self.alignment(), elided_text)
