from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget


class ModalDialog(QDialog):
    """Modal dialog."""

    def __init__(self, parent: QWidget, title: str, body_widget: QWidget):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(380)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title_lbl = QLabel(title)
        title_lbl.setObjectName("LibraryTitle")

        layout.addWidget(title_lbl)
        layout.addWidget(body_widget)

        self.setFixedSize(self.width(), self.sizeHint().height())

    def _clear_focus_before_close(self):
        focused = self.focusWidget()

        if focused:
            focused.clearFocus()

        if self.parentWidget():
            self.parentWidget().setFocus()

    def closeEvent(self, event):
        self._clear_focus_before_close()
        super().closeEvent(event)

    def reject(self):
        self._clear_focus_before_close()
        super().reject()

    def accept(self):
        self._clear_focus_before_close()
        super().accept()
