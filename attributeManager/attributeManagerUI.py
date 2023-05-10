import sys

from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette, QColor




from PySide2.QtWidgets import QApplication, QMainWindow, QSizePolicy, QWidget, QGridLayout, QHBoxLayout, QPushButton,QCheckBox


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.builtLayouts = {}

        self.setWindowTitle("attribute match")

        mainLayout = QGridLayout()
        layoutInputs = {'placeholderLayout' : {'stepLayout':{}}, 'matchLayout' : {'setPositionsLayout':{'axisLayout':{},'attributesLayout':{}}}} 

        self.chainLayout(layoutInputs, mainLayout)

        print (self.builtLayouts)

        self.centerOfSelection = self.button("center of selection")
        self.centerOfEach = self.button("center of each")
        self.centerOfStep= self.button("center of step")

        self.loadSelection = self.button("load selection")
        self.translate = self.button("translate")
        self.rotate = self.button("rotate")
        self.scale = self.button("scale")
        self.checkBoxX = self.checkBox("X")
        self.checkBoxY = self.checkBox("Y")
        self.checkBoxZ = self.checkBox("Z")
                


        self.builtLayouts['stepLayout'].addWidget(self.centerOfStep, 0, 0)

        self.builtLayouts['placeholderLayout'].addWidget(self.centerOfSelection, 1, 0)
        self.builtLayouts['placeholderLayout'].addWidget(self.centerOfEach, 2, 0)

        self.builtLayouts['axisLayout'].addWidget(self.checkBoxX,0,0)
        self.builtLayouts['axisLayout'].addWidget(self.checkBoxY,0,1)
        self.builtLayouts['axisLayout'].addWidget(self.checkBoxZ,0,2)

        
        self.builtLayouts['attributesLayout'].addWidget(self.loadSelection,0,0, 0,1)
        self.builtLayouts['attributesLayout'].addWidget(self.translate,0,1)
        self.builtLayouts['attributesLayout'].addWidget(self.rotate,1,1)
        self.builtLayouts['attributesLayout'].addWidget(self.scale,2,1)
 

        widget = QWidget()
        widget.setLayout( mainLayout )
        self.setCentralWidget(widget)


    @staticmethod
    def button( name):
        pushButton=QPushButton(name)
        pushButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)     
        return pushButton
    
    @staticmethod
    def checkBox(name):
        check = QCheckBox(name)
        check.setChecked(True)
        check.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return check
    


   
    def chainLayout(self, layoutDictionary, parent):
        counter=0

        for layoutName in layoutDictionary:
            grid = QGridLayout()
            self.builtLayouts[layoutName] = grid
            parent.addLayout(grid, counter,0)
            counter+=1    
            
            if layoutDictionary[layoutName]:

                for child in layoutDictionary[layoutName]:   
                    childLayout = self.chainLayout(layoutDictionary[layoutName], grid)
                    self.builtLayouts[child] = childLayout

        
        return grid

    

    

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec_()


