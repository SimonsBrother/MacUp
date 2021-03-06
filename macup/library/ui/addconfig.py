from PyQt6.QtWidgets import QDialog, QApplication

from macup.ui.addconfig import Ui_addconfig


class AddConfigDialogUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_addconfig()
        self.ui.setupUi(self)
        self.setWindowTitle("Add configuration")


if __name__ == "__main__":
    app = QApplication([])

    window = AddConfigDialogUI()
    window.show()
    app.exec()
