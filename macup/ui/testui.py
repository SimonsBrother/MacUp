from PyQt6 import QtWidgets, uic

app = QtWidgets.QApplication([])

window = uic.loadUi("modifyfilterwidget.ui")
window.show()
app.exec()
