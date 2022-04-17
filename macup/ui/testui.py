from PyQt6 import QtWidgets, uic

app = QtWidgets.QApplication([])

window = uic.loadUi("modifyfilter.ui")
window.show()
app.exec()
