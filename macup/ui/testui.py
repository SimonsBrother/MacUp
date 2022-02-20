from PyQt6 import QtWidgets, uic

app = QtWidgets.QApplication([])

window = uic.loadUi("addconfigwidget.ui")
window.show()
app.exec()
