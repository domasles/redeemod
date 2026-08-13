from PySide6.QtWidgets import QWidget, QPushButton, QListWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QApplication, QScroller
from PySide6.QtCore import Qt, QPoint, Signal, QEvent


class Dropdown(QWidget):
    """Custom dropdown component."""

    currentIndexChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("DropdownContainer")
        self._items, self._current_index = [], -1

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.trigger_btn = QPushButton(self, objectName="DropdownTrigger")
        self.trigger_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.trigger_btn.clicked.connect(self._toggle_popup)

        btn_layout = QHBoxLayout(self.trigger_btn)
        btn_layout.setContentsMargins(12, 0, 12, 0)

        self.text_label = QLabel(self, objectName="DropdownTextLabel")
        self.arrow_label = QLabel("▼", self, objectName="DropdownArrowLabel")

        for lbl in (self.text_label, self.arrow_label):
            lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        btn_layout.addWidget(self.text_label)
        btn_layout.addStretch()
        btn_layout.addWidget(self.arrow_label)
        main_layout.addWidget(self.trigger_btn)

        flags = Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint

        self.popup_frame = QFrame(None, flags, objectName="DropdownPopupFrame")
        self.popup_frame.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        popup_layout = QVBoxLayout(self.popup_frame)
        popup_layout.setContentsMargins(0, 0, 0, 0)
        popup_layout.setSpacing(0)

        self.popup_list = QListWidget(self.popup_frame, objectName="DropdownPopup")
        self.popup_list.setMinimumHeight(0)
        self.popup_list.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.popup_list.verticalScrollBar().setSingleStep(12)

        QScroller.ungrabGesture(self.popup_list.viewport())

        self.popup_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.popup_list.itemClicked.connect(self._on_item_clicked)

        popup_layout.addWidget(self.popup_list)

    def addItem(self, text: str, userData=None):
        self._items.append((text, userData))
        self.popup_list.addItem(text)

        if self._current_index == -1:
            self.setCurrentIndex(0)

    def setCurrentIndex(self, index: int):
        if 0 <= index < len(self._items):
            self._current_index = index
            self.text_label.setText(self._items[index][0])
            self.popup_list.setCurrentRow(index)
            self.currentIndexChanged.emit(index)

    def currentIndex(self) -> int:
        return self._current_index

    def currentData(self):
        return self._items[self._current_index][1] if 0 <= self._current_index < len(self._items) else None

    def _toggle_popup(self):
        self._close_popup() if self.popup_frame.isVisible() else self._open_popup()

    def _open_popup(self):
        if not (count := self.popup_list.count()):
            return

        self.popup_list.doItemsLayout()

        row_h = max(0, self.popup_list.sizeHintForRow(0)) or 28
        height = min((count * row_h) + (self.popup_list.frameWidth() * 2) + 2, 154)

        pos = self.trigger_btn.mapToGlobal(QPoint(-1, self.trigger_btn.height() + 4))

        self.popup_list.setFixedHeight(height)
        self.popup_frame.setGeometry(pos.x(), pos.y(), self.trigger_btn.width(), height)
        self.arrow_label.setText("▲")
        self.popup_frame.show()

        if app := QApplication.instance():
            app.installEventFilter(self)

    def _close_popup(self):
        self.arrow_label.setText("▼")
        self.popup_frame.hide()

        if app := QApplication.instance():
            app.removeEventFilter(self)

    def _on_item_clicked(self, item):
        self.setCurrentIndex(self.popup_list.row(item))
        self._close_popup()

    def eventFilter(self, obj, event):
        try:
            if self.popup_frame.isVisible() and event.type() in (QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonDblClick):
                pos = event.globalPosition().toPoint() if hasattr(event, "globalPosition") else event.globalPos()

                if not self.popup_frame.frameGeometry().contains(pos):
                    self._close_popup()

                    if self.trigger_btn.frameGeometry().contains(self.mapFromGlobal(pos)):
                        return True

        except RuntimeError:
            return False

        return super().eventFilter(obj, event)
