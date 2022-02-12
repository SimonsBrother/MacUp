from PyQt6 import QtWidgets, uic

app = QtWidgets.QApplication([])

window = uic.loadUi("mainwindow.ui")
window.show()
app.exec()
