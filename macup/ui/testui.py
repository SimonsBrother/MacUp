from PyQt6 import QtWidgets, uic

app = QtWidgets.QApplication([])

window = uic.loadUi("addconfig.ui")
window.show()
app.exec()
