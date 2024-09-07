from PySide2.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton, QSizePolicy
import pymel.core as pm

def moveCv(selection, axis):
    value = 0.2
    offset = {'x': [value, 0, 0], 'y': [0, value, 0], 'z': [0, 0, value]}
    for i in selection:
        pm.move('{}.cv[*]'.format(i), offset[axis])

def rotateCv(selection, axis):
    value = 15
    offset = {'x': [value, 0, 0], 'y': [0, value, 0], 'z': [0, 0, value]}
    for i in selection:
        pm.rotate('{}.cv[*]'.format(i), offset[axis])

def scaleCv(selection, upDown):
    value = {'+': 1.2, '-': 0.8}
    for i in selection:
        pm.scale('{}.cv[*]'.format(i), value[upDown], value[upDown], value[upDown])

class cvToolUI(QMainWindow):

    def __init__(self):
        super(cvToolUI, self).__init__()

        self.setWindowTitle("cv editor")

        self.mainLayout = QGridLayout()
        self.rotateLayout = QGridLayout()
        self.scaleLayout = QGridLayout()

        self.mainLayout.addLayout(self.rotateLayout, 0, 0)
        self.mainLayout.addLayout(self.scaleLayout, 1, 0)

        self.rotateX = self.button('rotate x')
        self.rotateX.clicked.connect(lambda: rotateCv(pm.ls(os=True, fl=True), 'x'))
        self.rotateLayout.addWidget(self.rotateX, 0, 0)

        self.rotateY = self.button('rotate y')
        self.rotateY.clicked.connect(lambda: rotateCv(pm.ls(os=True, fl=True), 'y'))
        self.rotateLayout.addWidget(self.rotateY, 0, 1)

        self.rotateZ = self.button('rotate z')
        self.rotateZ.clicked.connect(lambda: rotateCv(pm.ls(os=True, fl=True), 'z'))
        self.rotateLayout.addWidget(self.rotateZ, 0, 2)

        self.scaleUp = self.button('scale +')
        self.scaleUp.clicked.connect(lambda: scaleCv(pm.ls(os=True, fl=True), '+'))
        self.scaleLayout.addWidget(self.scaleUp, 0, 0)

        self.scaleDown = self.button('scale -')
        self.scaleDown.clicked.connect(lambda: scaleCv(pm.ls(os=True, fl=True), '-'))
        self.scaleLayout.addWidget(self.scaleDown, 0, 1)

        widget = QWidget()
        widget.setLayout(self.mainLayout)
        self.setCentralWidget(widget)

    @staticmethod
    def button(name):
        pushButton = QPushButton(name)
        pushButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        return pushButton


window = cvToolUI()
window.show()