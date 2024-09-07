from PySide2.QtWidgets import QLabel, QSizePolicy, QWidget, QHBoxLayout, QGridLayout, QPushButton,QCheckBox, QSpinBox, QRadioButton, QDoubleSpinBox
from PySide2.QtCore import Qt
import Schematic

class Blueprint:
    def __init__(self):
        self.grid = QGridLayout()
        self.mainLayout = QGridLayout()
        self.titleLayout = QGridLayout()
        self.blueprintLayout = QGridLayout()

        titleWidget = QWidget()
        titleWidget.setLayout(self.titleLayout)

        BlueprintManager = Schematic.BlueprintManager()
        self.title = QLabel(BlueprintManager.projectPath)
        self.titleLayout.addWidget(self.title, 0, 0)
        self.title.setTextInteractionFlags(Qt.TextBrowserInteraction)


        self.loadBlueprint = button("Load\nBlueprint")
        self.loadBlueprint.clicked.connect(lambda: BlueprintManager.loadBlueprint())

        self.saveBlueprint = button("Save\nBlueprint")
        self.saveBlueprint.clicked.connect(lambda: BlueprintManager.writeBlueprint())

        self.refreshBlueprint = button("Refresh\nBlueprint")
        self.refreshBlueprint.clicked.connect(lambda: BlueprintManager.writeBlueprint(refresh=True))

        self.printBlueprint = button("Print\nBlueprint")
        self.printBlueprint.clicked.connect(lambda: BlueprintManager.toString())


        self.blueprintLayout.addWidget(titleWidget, 0, 0)
        self.blueprintLayout.addWidget(self.loadBlueprint, 1, 0)
        self.blueprintLayout.addWidget(self.refreshBlueprint, 2, 0)
        self.blueprintLayout.addWidget(self.saveBlueprint, 3, 0)
        self.blueprintLayout.addWidget(self.printBlueprint, 3, 1)

        self.mainLayout.addLayout(self.blueprintLayout,0,0)



    def getLayout(self):
        return self.mainLayout


def button(name):
    pushButton = QPushButton(name)
    pushButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return pushButton

def checkBox(name, checked=True):
    check = QCheckBox(name)
    check.setChecked(checked)
    check.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return check

def numberBox(value):
    spinBox = QSpinBox()
    spinBox.setValue(value)
    return spinBox