from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import QObject, Signal, Qt

from frontend.components.modal_dialog import ModalDialog


class ErrorModalBody(QWidget):
    dismissed = Signal()

    def __init__(self, message: str):
        super().__init__()

        self.setObjectName("ErrorModalBody")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        error_label = QLabel(message)
        error_label.setObjectName("CardTitleLabel")
        error_label.setWordWrap(True)

        layout.addWidget(error_label)
        layout.addStretch()

        btn_ok = QPushButton("OK")
        btn_ok.setObjectName("LaunchBtn")
        btn_ok.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ok.clicked.connect(self.dismissed.emit)

        layout.addWidget(btn_ok)


def show_error_modal(message: str, parent: QObject | None = None) -> None:
    body = ErrorModalBody(message)
    modal = ModalDialog("Something went wrong", body, parent)
    body.dismissed.connect(modal.accept)

    modal.exec()
