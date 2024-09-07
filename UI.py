from PySide2.QtWidgets import QApplication,QTabWidget,QVBoxLayout, QLabel, QMainWindow, QSizePolicy, QWidget, QHBoxLayout, QGridLayout, QPushButton,QCheckBox, QSpinBox, QRadioButton, QDoubleSpinBox
import sys
import attributeToolsUi
import BlueprintUi

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("rig tools")
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        centralLayout = QVBoxLayout(centralWidget)
        tabWidget = QTabWidget()
        firstTab = QWidget()
        firstTabLayout = QVBoxLayout()

        placeholdersLayout = attributeToolsUi.placeholders().getLayout()
        positionLayout = attributeToolsUi.position().getLayout()
        matchLayout = attributeToolsUi.Match().getLayout()

        blueprint = BlueprintUi.Blueprint().getLayout()

        firstTabLayout.addLayout(placeholdersLayout)
        firstTabLayout.addLayout(positionLayout)
        firstTabLayout.addLayout(matchLayout)
        firstTab.setLayout(firstTabLayout)

        secondTab = QWidget()
        secondTabLayout = QVBoxLayout()
        secondTab.setLayout(secondTabLayout)

        secondTabLayout.addLayout(blueprint)

        tabWidget.addTab(firstTab, "attribute tools")
        tabWidget.addTab(secondTab, "blueprint")

        centralLayout.addWidget(tabWidget)

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

# app = QApplication(sys.argv)
window = MainWindow()
window.show()
# sys.exit(app.exec_())
