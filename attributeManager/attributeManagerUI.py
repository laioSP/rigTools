import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QSizePolicy, QWidget, QGridLayout, QHBoxLayout, QPushButton,QCheckBox 

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("attribute match")

        self.mainLayout = QHBoxLayout()
        self.axisLayout = QGridLayout()
        self.attributeButtonsLayout = QGridLayout()
        
    

        self.loadSelection = QPushButton("load selection")
        self.translate = QPushButton("translate")
        self.rotate = QPushButton("rotate")
        self.scale = QPushButton("scale")
        self.checkBoxX = QCheckBox("X")
        self.checkBoxY = QCheckBox("Y")
        self.checkBoxZ = QCheckBox("Z")
                
        self.loadSelection.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        
        self.checkBoxX.setChecked(True)
        self.checkBoxY.setChecked(True)
        self.checkBoxZ.setChecked(True)
        



        self.mainLayout.addWidget(self.loadSelection)
        self.mainLayout.addLayout(self.attributeButtonsLayout)
        self.attributeButtonsLayout.addLayout(self.axisLayout, 0, 0)

        self.axisLayout.addWidget(self.checkBoxX, 0,0)
        self.axisLayout.addWidget(self.checkBoxY, 0,1)
        self.axisLayout.addWidget(self.checkBoxZ, 0,2)

        self.attributeButtonsLayout.addWidget(self.translate, 1,0 )
        self.attributeButtonsLayout.addWidget(self.rotate, 2,0)
        self.attributeButtonsLayout.addWidget(self.scale, 3,0)

        widget = QWidget()
        widget.setLayout(self.mainLayout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()