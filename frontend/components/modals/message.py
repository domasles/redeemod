from collections.abc import Callable

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QDialog
from PySide6.QtCore import Signal, Qt

from frontend.components.modal_dialog import ModalDialog


class MessageModalBody(QWidget):
    confirmed = Signal()

    def __init__(self, message: str):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        message_label = QLabel(message)
        message_label.setObjectName("CardTitleLabel")
        message_label.setWordWrap(True)

        layout.addWidget(message_label)
        layout.addStretch()

        btn_ok = QPushButton("OK")
        btn_ok.setObjectName("LaunchBtn")
        btn_ok.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ok.clicked.connect(self.confirmed.emit)

        layout.addWidget(btn_ok)


def show_error_modal(message: str, parent: QWidget | None = None) -> None:
    show_info_modal("Something went wrong", message, parent)


def show_info_modal(title: str, message: str, parent: QWidget | None = None) -> None:
    body = MessageModalBody(message)
    modal = ModalDialog(title, body, parent)
    body.confirmed.connect(modal.accept)

    modal.exec()


def show_setup_modal(title: str, message: str, on_confirm: Callable[[], None], parent: QWidget | None = None) -> bool:
    body = MessageModalBody(message)
    modal = ModalDialog(title, body, parent)
    body.confirmed.connect(modal.accept)

    confirmed = modal.exec() == QDialog.DialogCode.Accepted

    if confirmed:
        on_confirm()

    return confirmed
