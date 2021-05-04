import sys
from PyQt5 import QtWidgets, QtCore
from MainForm import Ui_Form

#(25, -14);(16, 8);(8, 24);(-30, 11);(50, -12);(-60, 11);(25, 25);(11, -11);(-20, 20)
#
#(10, 8);(-5, 15) -- Евклид тест
#(10, 8);(0, 15) -- Манхэттен тест


app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QWidget()
app2 = Ui_Form(widget)
widget.setWindowTitle("Network")
widget.setFixedWidth(795)
widget.setFixedHeight(520)
widget.show()

exit(app.exec_())