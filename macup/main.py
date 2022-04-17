from PyQt6 import QtWidgets
from macup.library.ui.mainwindow import MainWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
