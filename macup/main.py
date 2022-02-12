from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QSize
from macup.ui.MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("MacUp")

        self.filter_listw.addItems(['test', 'test2'])
        self.filter_listw.itemClicked.connect(self.item_clicked)

    def item_clicked(self):
        item = self.filter_listw.currentItem()
        print(item.text())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
