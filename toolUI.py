import sys
from PySide2.QtGui import QPalette, QColor
from PySide2.QtWidgets import QApplication, QMainWindow, QSizePolicy, QWidget, QGridLayout, QPushButton,QCheckBox, QSpinBox
import navigate
import pymel.core as pm
dir(QSpinBox())
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.builtLayouts = {}

        self.setWindowTitle("attribute match")

        mainLayout = QGridLayout()
        layoutInputs = {'placeholderLayout' : {'stepLayout':{}}, 'matchLayout' : {'setPositionsLayout':{'axisLayout':{},'attributesLayout':{}}}} 

        self.chainLayout(layoutInputs, mainLayout)
        
        self.intBox = QSpinBox()
        self.centerOfSelection = self.button("center of selection")
        self.centerOfSelection.clicked.connect(lambda: navigate.ofAll(pm.ls(os=True, fl=True)))
        
        self.tie = self.button("tie")
        self.tie.clicked.connect(lambda: navigate.ConstraintRope.tie(pm.ls(os=True, fl=True)))

        self.centerOfEach = self.button("center of each")
        self.centerOfEach.clicked.connect(lambda: navigate.ofEach(pm.ls(os=True, fl=True)))
        
        self.centerOfStep= self.button("center of step")
        self.centerOfStep.clicked.connect(lambda: navigate.ofStep(pm.ls(os=True, fl=True), self.intBox.value()))
        
        self.subdivide= self.button("subdivide")        
        self.subdivide.clicked.connect(lambda : navigate.subDivide(pm.ls(os=True, fl=True), self.intBox.value()))
        
        self.loadSelection = self.button("load selection")
        self.translate = self.button("translate")
        self.rotate = self.button("rotate")
        self.scale = self.button("scale")
        self.allAttributes = self.button("all attributes")
        self.checkBoxX = self.checkBox("X")
        self.checkBoxY = self.checkBox("Y")
        self.checkBoxZ = self.checkBox("Z")      
        
        self.scale.clicked.connect(lambda: pm.ls(os=True, fl=True))

        self.builtLayouts['stepLayout'].addWidget(self.subdivide, 0, 1,2,1)
        self.builtLayouts['stepLayout'].addWidget(self.tie, 0, 2,2,1)
        self.builtLayouts['stepLayout'].addWidget(self.intBox, 0, 0)
        self.builtLayouts['stepLayout'].addWidget(self.centerOfStep, 1, 0)
        

        self.builtLayouts['placeholderLayout'].addWidget(self.centerOfSelection, 1, 0)
        self.builtLayouts['placeholderLayout'].addWidget(self.centerOfEach, 2, 0)

        self.builtLayouts['axisLayout'].addWidget(self.checkBoxX,0,0)
        self.builtLayouts['axisLayout'].addWidget(self.checkBoxY,0,1)
        self.builtLayouts['axisLayout'].addWidget(self.checkBoxZ,0,2)

        
        self.builtLayouts['attributesLayout'].addWidget(self.loadSelection,0,0, 0,1)
        self.builtLayouts['attributesLayout'].addWidget(self.translate,0,1)
        self.builtLayouts['attributesLayout'].addWidget(self.rotate,1,1)
        self.builtLayouts['attributesLayout'].addWidget(self.scale,2,1)
        self.builtLayouts['attributesLayout'].addWidget(self.allAttributes,3,1)

        widget = QWidget()
        widget.setLayout( mainLayout )
        self.setCentralWidget(widget)


    @staticmethod
    def button(name, function=nope, inputs=[]):
        pushButton=QPushButton(name)
        pushButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
  
        return pushButton
    
    @staticmethod
    def checkBox(name, checked = True):
        check = QCheckBox(name)
        check.setChecked(checked)
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

    
window = MainWindow()
window.show()