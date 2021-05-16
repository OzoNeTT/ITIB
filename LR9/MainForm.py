import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QGraphicsView
import sys

class Ui_Form(object):

    def __init__(self, obj):
        super().__init__()
        self.setupUi(obj)
        self.retranslateUi(obj)
        self.graphicsView = QGraphicsView(obj)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 500, 500))
        self.graphicsView.setObjectName("graphicsView")
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        pen = QtGui.QPen(QtCore.Qt.GlobalColor.black)
        for i in range(-248, 248):
            r1 = QtCore.QRectF(QtCore.QPointF(0, i), QtCore.QSizeF(1, 1))
            r2 = QtCore.QRectF(QtCore.QPointF(i, 0), QtCore.QSizeF(1, 1))
            self.scene.addRect(r1, pen)
            self.scene.addRect(r2, pen)

        self.cordinates = None
        self.centers = None
        self.clasters = []

    def setupUi(self, Form):
        Form.setObjectName("Form")

        self.euclidButton = QPushButton(Form)
        self.euclidButton.clicked.connect(self.euclidButtonClicked)
        self.euclidButton.setGeometry(QtCore.QRect(560, 10, 211, 41))
        self.euclidButton.setObjectName("euclidButton")

        self.manhetButton = QPushButton(Form)
        self.manhetButton.clicked.connect(self.manhetButtonClicked)
        self.manhetButton.setGeometry(QtCore.QRect(560, 60, 211, 41))
        self.manhetButton.setObjectName("manhetButton")

        #self.polygonQ = QPolygon()


        self.stepButton = QPushButton(Form)
        self.stepButton.clicked.connect(self.stepButtonClicked)
        self.stepButton.setGeometry(QtCore.QRect(560, 110, 211, 41))
        self.stepButton.setObjectName("stepButton")

        self.resetButton = QPushButton(Form)
        self.resetButton.clicked.connect(self.resetButtonClicked)
        self.resetButton.setGeometry(QtCore.QRect(560, 160, 211, 41))
        self.resetButton.setObjectName("resetButton")


        self.cordsTextBox = QtWidgets.QPlainTextEdit(Form)
        self.cordsTextBox.setGeometry(QtCore.QRect(560, 230, 211, 71))
        self.cordsTextBox.setObjectName("cordsTextBox")

        self.cordsButton = QPushButton(Form)
        self.cordsButton.clicked.connect(self.cordsButtonClicked)
        self.cordsButton.setGeometry(QtCore.QRect(560, 310, 211, 31))
        self.cordsButton.setObjectName("cordsButton")


        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(560, 210, 200, 21))
        self.label.setObjectName("label")

        self.centersTextBox = QtWidgets.QPlainTextEdit(Form)
        self.centersTextBox.setGeometry(QtCore.QRect(560, 380, 211, 71))
        self.centersTextBox.setObjectName("centersTextBox")

        self.centersButton = QPushButton(Form)
        self.centersButton.clicked.connect(self.centersButtonClicked)
        self.centersButton.setGeometry(QtCore.QRect(560, 460, 211, 31))
        self.centersButton.setObjectName("centersButton")

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(560, 350, 200, 21))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.euclidButton.setText(_translate("Form", "Евклид"))
        self.stepButton.setText(_translate("Form", "Шаг"))
        self.manhetButton.setText(_translate("Form", "Манхэттен"))
        self.resetButton.setText(_translate("Form", "RESET"))
        self.cordsButton.setText(_translate("Form", "Add cords"))
        self.label.setText(_translate("Form", "Format: (x1, y1);(x2, y2);(x3, y3);..."))
        self.centersButton.setText(_translate("Form", "Add Centers"))
        self.label_2.setText(_translate("Form", "Format: (x1, y1);(x2, y2);(x3, y3);..."))

    def addCordsToGraph(self, cords, f):
        pen = None
        brush = None
        if f == 'm':
            pen = QtGui.QPen(QtCore.Qt.GlobalColor.blue)
            brush = QtGui.QBrush(QtCore.Qt.GlobalColor.blue)
        else:
            pen = QtGui.QPen(QtCore.Qt.GlobalColor.red)
            brush = QtGui.QBrush(QtCore.Qt.GlobalColor.red)
        side = 3
        for i in cords:
            self.scene.addEllipse(i[0] * side - 3, -1* i[1] * side - 3, 7, 7, pen, brush)

    def parseStringToCords(self, s, tb):
        cords_l = None
        try:
            cords_string_array = s.split(';')
            cords_l = []
            for i in cords_string_array:
                l = [float(k) for k in i.strip('()').split(',')]
                cords_l.append(l)
        except:
            if tb == 'c':
                self.cordsTextBox.clear()
            else:
                self.centersTextBox.clear()

            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Format Error")
            msg.setInformativeText('Follow the format!')
            msg.setWindowTitle("Error")
            msg.setStyleSheet("QLabel{font-size: 20px;}")
            msg.exec_()
            pass
        return cords_l

    def cordsButtonClicked(self):
        cords = self.cordsTextBox.toPlainText()
        cords_list = self.parseStringToCords(cords, 'c')
        if cords_list is not None:
            self.cordinates = cords_list.copy()
            print (cords_list)
            self.addCordsToGraph(cords_list, 'm')

    def centersButtonClicked(self):
        cords = self.centersTextBox.toPlainText()
        cords_list = self.parseStringToCords(cords, 'm')
        if cords_list is not None:
            self.centers = cords_list.copy()
            print (cords_list)
            self.addCordsToGraph(cords_list, 'c')

    def drawLineToDot(self):
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.red)

        brush = QtGui.QBrush(QtCore.Qt.GlobalColor.red)
        pen.setWidth(2)
        pen.setColor(QtCore.Qt.GlobalColor.green)


        for i in range(len(self.clasters)):
            for j in self.clasters[i]:
                self.scene.addLine(QtCore.QLineF(3* j[0], -3* j[1], 3*self.centers[i][0], -3*self.centers[i][1]), pen)


    def euclidButtonClicked(self):
        if self.centers is None or self.cordinates is None:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Empty Error")
            msg.setInformativeText('Not enough dots!')
            msg.setWindowTitle("Error")
            msg.setStyleSheet("QLabel{font-size: 20px;}")
            msg.exec_()
            return
        for _ in range(len(self.centers)):
            self.clasters.append([])

        for i in self.cordinates:
            range_l = []
            for c in self.centers:
                range_l.append(math.sqrt((i[0]-c[0])**2 + (i[1]-c[1])**2))

            minindex = range_l.index(min(range_l))
            self.clasters[minindex].append(i)
        self.drawLineToDot()
        self.euclidButton.setEnabled(False)
        self.manhetButton.setEnabled(False)
        self.cordsButton.setEnabled(False)
        self.centersButton.setEnabled(False)

    def manhetButtonClicked(self):
        if self.centers is None or self.cordinates is None:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Empty Error")
            msg.setInformativeText('Not enough dots!')
            msg.setWindowTitle("Error")
            msg.setStyleSheet("QLabel{font-size: 20px;}")
            msg.exec_()
            return
        for _ in range(len(self.centers)):
            self.clasters.append([])

        for i in self.cordinates:
            range_l = []
            for c in self.centers:
                range_l.append(abs((c[0]-i[0])) + abs(c[1]-i[1]))

            minindex = range_l.index(min(range_l))
            self.clasters[minindex].append(i)
        self.drawLineToDot()
        self.euclidButton.setEnabled(False)
        self.manhetButton.setEnabled(False)
        self.cordsButton.setEnabled(False)
        self.centersButton.setEnabled(False)

    def stepButtonClicked(self):

        if self.centers is None or self.cordinates is None:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Empty Error")
            msg.setInformativeText('Not enough dots!')
            msg.setWindowTitle("Error")
            msg.setStyleSheet("QLabel{font-size: 20px;}")
            msg.exec_()
            return

        claster_backup = self.clasters.copy()

        new_centers = []

        for i in self.clasters:
            new_x = 0
            new_y = 0
            for k in i:
                new_x += k[0]
                new_y += k[1]

            new_x /= len(i)
            new_y /= len(i)
            new_centers.append([new_x, new_y])

        self.centers = new_centers.copy()
        self.redrow(False)
        self.addCordsToGraph(new_centers, 'c')
        self.clasters.clear()
        for _ in range(len(self.centers)):
            self.clasters.append([])

        for i in self.cordinates:
            range_l = []
            for c in new_centers:
                range_l.append(math.sqrt((i[0]-c[0])**2 + (i[1]-c[1])**2))

            minindex = range_l.index(min(range_l))
            self.clasters[minindex].append(i)
        self.drawLineToDot()
        new_back_clasters = self.clasters.copy()

        if claster_backup == new_back_clasters:
            self.stepButton.setEnabled(False)
            self.stepButton.clearFocus()

    def redrow(self, full):
        self.scene.clear()
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.black)
        for i in range(-248, 248):
            r1 = QtCore.QRectF(QtCore.QPointF(0, i), QtCore.QSizeF(1, 1))
            r2 = QtCore.QRectF(QtCore.QPointF(i, 0), QtCore.QSizeF(1, 1))
            self.scene.addRect(r1, pen)
            self.scene.addRect(r2, pen)
        if not full:

            pen2 = QtGui.QPen(QtCore.Qt.GlobalColor.blue)
            brush2 = QtGui.QBrush(QtCore.Qt.GlobalColor.blue)

            side = 3
            for i in self.cordinates:
                self.scene.addEllipse(i[0] * side - 3, -1 * i[1] * side - 3, 7, 7, pen2, brush2)

    def resetButtonClicked(self):
        self.euclidButton.setEnabled(True)
        self.manhetButton.setEnabled(True)
        self.cordsButton.setEnabled(True)
        self.centersButton.setEnabled(True)
        self.stepButton.setEnabled(True)
        self.redrow(True)

        self.cordinates = None
        self.centers = None
        self.clasters.clear()

if __name__ == '__main__':
    # (25, -14);(16, 8);(8, 24);(-30, 11);(50, -12);(-60, 11);(25, 25);(11, -11);(-20, 20)
    #
    # (10, 8);(-5, 15);(0, 0) -- Евклид тест
    # (10, 8);(0, 15) -- Манхэттен тест

    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    app2 = Ui_Form(widget)
    widget.setWindowTitle("Network")
    widget.setFixedWidth(795)
    widget.setFixedHeight(520)
    widget.show()

    exit(app.exec_())