from PySide2.QtWidgets import QLabel, QSizePolicy, QWidget, QHBoxLayout, QGridLayout, QPushButton,QCheckBox, QSpinBox, QRadioButton, QDoubleSpinBox
import navigate
import pymel.core as pm
import placeholder
import constants

class placeholders:
    def __init__(self):
        self.grid = QGridLayout()
        self.mainLayout = QGridLayout()
        self.titleLayout = QGridLayout()
        self.title = QLabel("placeholders")


        self.updateAllPlaceholders = button("update all \n placeholders")
        self.updateAllPlaceholders.clicked.connect( lambda: placeholder.update(pm.ls(constants.placeholderGroup)[0].listRelatives(s=False)))

        self.updateSelectedPlaceholders = button("update \n selected \n placeholders")
        self.updateSelectedPlaceholders.clicked.connect(lambda: placeholder.update(pm.ls(os=True, fl=True)))

        self.resetSelectedPlaceholders = button("reset \n selected \n placeholders")
        self.resetSelectedPlaceholders.clicked.connect(lambda: placeholder.reset(pm.ls(os=True, fl=True)))

        self.resetAllPlaceholders = button("reset \n all \n placeholders")
        self.resetAllPlaceholders.clicked.connect(lambda: placeholder.reset(pm.ls(constants.placeholderGroup)[0].listRelatives(s=False)))

        self.titleLayout.addWidget(self.title, 0, 0)
        self.grid.addWidget(self.updateAllPlaceholders, 1, 0)
        self.grid.addWidget(self.updateSelectedPlaceholders, 1, 1)
        self.grid.addWidget(self.resetSelectedPlaceholders, 2, 1)
        self.grid.addWidget(self.resetAllPlaceholders, 2, 0)

        titleWidget = QWidget()
        titleWidget.setLayout(self.titleLayout)

        gridWidget = QWidget()
        gridWidget.setLayout(self.grid)

        self.mainLayout.addWidget(titleWidget, 0, 0)
        self.mainLayout.addWidget(gridWidget, 1, 0)

    def getLayout(self):
        return self.mainLayout


class position:
    def __init__(self):
        self.grid = QGridLayout()
        self.mainLayout = QGridLayout()
        self.titleLayout = QGridLayout()
        self.firstColumn = QGridLayout()

        self.title = QLabel("position")

        self.title.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.titleLayout.addWidget(self.title, 0, 0)

        titleWidget = QWidget()
        titleWidget.setLayout(self.titleLayout)

        self.stepValue = numberBox(3)

        self.worldRadio = QRadioButton("world")
        self.objectRadio = QRadioButton("object")
        self.worldRadio.setChecked(True)

        self.centerOfSelection = button("center of \n selection")
        self.centerOfSelection.clicked.connect(lambda: navigate.ofAll(pm.ls(os=True, fl=True)))

        self.tie = button("tie")
        self.tie.clicked.connect(lambda: navigate.ConstraintRope().tie(pm.ls(os=True, fl=True)))

        self.centerOfEach = button("center of \n each")
        self.centerOfEach.clicked.connect(lambda: navigate.ofEach(pm.ls(os=True, fl=True)))

        self.centerOfStep = button("center of \n step")
        self.centerOfStep.clicked.connect(lambda: navigate.ofStep(pm.ls(os=True, fl=True), int(self.stepValue.value())))

        self.subdivide = button("subdivide")
        self.subdivide.clicked.connect(lambda: navigate.subDivide(pm.ls(os=True, fl=True), int(self.stepValue.value())))

        firstColumnWidget = QWidget()
        firstColumnWidget.setLayout(self.firstColumn)

        self.titleLayout.addWidget(self.worldRadio, 1, 0)
        self.titleLayout.addWidget(self.objectRadio, 1, 1)

        self.firstColumn.addWidget(self.stepValue, 0, 0)
        self.firstColumn.addWidget(self.centerOfStep, 1, 0)

        self.grid.addWidget(firstColumnWidget, 0,0)
        self.grid.addWidget(self.subdivide, 0, 1)
        self.grid.addWidget(self.tie, 0, 2)

        self.grid.addWidget(self.centerOfSelection, 1, 0, 1 ,3)
        self.grid.addWidget(self.centerOfEach, 2, 0, 1 ,3)
        self.grid.addWidget(self.centerOfStep, 3, 0, 1 ,3)


        gridWidget = QWidget()
        gridWidget.setLayout(self.grid)

        self.mainLayout.addWidget(titleWidget, 0, 0)
        self.mainLayout.addWidget(gridWidget, 1, 0)

        self.mainLayout.setRowStretch(0, 1)
        self.mainLayout.setRowStretch(1, 3)

    def getLayout(self):
        return self.mainLayout

class Match:
    def __init__(self):
        super(Match, self).__init__()

        self.mainLayout = QGridLayout()

        self.titleLayout = QGridLayout()
        self.titleLayoutWidget = QWidget()
        self.titleLayoutWidget.setLayout(self.titleLayout)
        self.mainLayout.addWidget(self.titleLayoutWidget, 0, 0, 1, 2)

        self.matchTitle = QLabel("match position")
        self.titleLayout.addWidget(self.matchTitle, 0, 0)

        self.checkBoxX = checkBox("X")
        self.checkBoxY = checkBox("Y")
        self.checkBoxZ = checkBox("Z")

        self.checkBoxTranslate = checkBox("translate")
        self.checkBoxRotate = checkBox("rotate")
        self.checkBoxScale = checkBox("scale")
        self.checkBoxScale.setChecked(False)

        self.matchButton = QPushButton("match")
        self.matchButton.clicked.connect(
            lambda: navigate.matchAttributes(pm.ls(os=True, fl=True), self.loadedSelection, self.attributeList(),
                                             self.axisList(), self.spacePosition()))

        self.checkBoxLayout = QGridLayout()
        self.checkBoxLayout.addWidget(self.checkBoxX, 0, 0)
        self.checkBoxLayout.addWidget(self.checkBoxY, 0, 1)
        self.checkBoxLayout.addWidget(self.checkBoxZ, 0, 2)

        self.secondColumnLayout = QGridLayout()
        self.selectionLayout = QGridLayout()
        self.secondColumnLayout.addWidget(self.checkBoxTranslate, 1, 0)
        self.secondColumnLayout.addWidget(self.checkBoxRotate, 2, 0)
        self.secondColumnLayout.addWidget(self.checkBoxScale, 3, 0)
        self.secondColumnLayout.addWidget(self.matchButton, 4, 0)

        self.loadSelectionButton = QPushButton("load \n selection")
        self.loadSelectionButton.setCheckable(True)
        self.loadSelectionButton.setChecked(False)
        self.loadSelectionButton.clicked.connect(
            lambda checked: self.unloadSelection() if not checked else self.loadSelection())

        self.selectionLayout.addWidget(self.loadSelectionButton, 0, 0)
        self.selectionLayout.addLayout(self.secondColumnLayout, 0, 1)

        self.minLabel = QLabel('min values')
        self.maxLabel = QLabel('max values')
        self.minExplode = numberBox(-25)
        self.maxExplode = numberBox(25)
        self.minExplode.setValue(-25)
        self.maxExplode.setValue(25)

        self.startKeyLabel = QLabel('start keyframe')
        self.endKeyLabel = QLabel('end keyframe')
        self.startKeyExplode = QSpinBox()
        self.endKeyExplode = QSpinBox()
        self.startKeyExplode.setValue(1)
        self.endKeyExplode.setValue(120)
        self.animateExplode = QCheckBox("animate explosion")

        self.explodeButton = QPushButton("explode")
        self.explodeButton.clicked.connect(
            lambda: navigate.explode(pm.ls(os=True, fl=True), self.minExplode.value(), self.maxExplode.value(),
                                     self.attributeList(), self.axisList(), self.animateExplode.isChecked(),
                                     self.startKeyExplode.value(), self.endKeyExplode.value()))

        self.cleanButton = QPushButton("clean up")
        self.cleanButton.clicked.connect(lambda: placeholder.deleteGroup())

        self.mainLayout.addLayout(self.titleLayout,0,0)
        self.mainLayout.addLayout(self.checkBoxLayout, 1, 0)
        self.mainLayout.addLayout(self.selectionLayout, 2, 0)

        self.firstRow = QGridLayout()
        self.firstRow.addWidget(self.minLabel, 0, 0)
        self.firstRow.addWidget(self.maxLabel, 0, 1)
        self.firstRow.addWidget(self.minExplode, 1, 0)
        self.firstRow.addWidget(self.maxExplode, 1, 1)

        self.secondRow = QGridLayout()
        self.secondRow.addWidget(self.startKeyLabel, 0, 0)
        self.secondRow.addWidget(self.endKeyLabel, 0, 1)
        self.secondRow.addWidget(self.startKeyExplode, 1, 0)
        self.secondRow.addWidget(self.endKeyExplode, 1, 1)

        self.mainLayout.addLayout(self.firstRow, 3, 0)
        self.mainLayout.addWidget(self.animateExplode, 4, 0)
        self.mainLayout.addLayout(self.secondRow, 5, 0)
        self.mainLayout.addWidget(self.explodeButton, 6, 0)
        self.mainLayout.addWidget(self.cleanButton, 7, 0)

    def getLayout(self):
        return self.mainLayout

    def axisList(self):
        chosenList = []
        if self.checkBoxX.isChecked():
            chosenList.append('x')
        if self.checkBoxY.isChecked():
            chosenList.append('y')
        if self.checkBoxZ.isChecked():
            chosenList.append('z')
        return chosenList

    def attributeList(self):
        chosenList = []
        if self.checkBoxTranslate.isChecked():
            chosenList.append('t')
        if self.checkBoxRotate.isChecked():
            chosenList.append('r')
        if self.checkBoxScale.isChecked():
            chosenList.append('s')
        return chosenList

def button(name):
    pushButton = QPushButton(name)
    pushButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return pushButton

def checkBox(name, checked=True):
    check = QCheckBox(name)
    check.setChecked(checked)
    check.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return check


def numberBox(defaultValue, max='noLimit', min=-100000000):
    box = QDoubleSpinBox()
    box.setDecimals(2)
    if max == 'noLimit':
        box.setMaximum(100000000)
    else:
        box.setMaximum(max)

    box.setMinimum(min)
    box.setValue(defaultValue)

    return box
