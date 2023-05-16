import sys
from PySide2.QtGui import QPalette, QColor
from PySide2.QtWidgets import QApplication, QMainWindow, QSizePolicy, QWidget, QGridLayout, QPushButton,QCheckBox, QSpinBox
import navigate
import pymel.core as pm
from random import uniform
    
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.builtLayouts = {}
        self.loadedSelection = []

        self.setWindowTitle("attribute match")

        mainLayout = QGridLayout()
        layoutInputs = {'placeholderLayout' : {'stepLayout':{}}, 'matchLayout' : {'setPositionsLayout':{'axisLayout':{},'attributesLayout':{}}}} 

        self.chainLayout(layoutInputs, mainLayout)
        
        self.stepValue = QSpinBox()
        self.stepValue.setValue(3)
        self.centerOfSelection = self.button("center of selection")
        self.centerOfSelection.clicked.connect(lambda: navigate.ofAll(pm.ls(os=True, fl=True)))
        
        self.tie = self.button("tie")
        self.tie.clicked.connect(lambda: navigate.ConstraintRope().tie(pm.ls(os=True, fl=True)))

        self.centerOfEach = self.button("center of each")
        self.centerOfEach.clicked.connect(lambda: navigate.ofEach(pm.ls(os=True, fl=True)))
        
        self.centerOfStep= self.button("center of step")
        self.centerOfStep.clicked.connect(lambda: navigate.ofStep(pm.ls(os=True, fl=True), self.stepValue.value()))
        
        self.subdivide= self.button("subdivide")        
        self.subdivide.clicked.connect(lambda : navigate.subDivide(pm.ls(os=True, fl=True), self.stepValue.value()))

        self.maxExplode = QSpinBox()
        self.minExplode = QSpinBox()
        self.maxExplode.setValue(25)
        self.minExplode.setValue(4)

        self.explodeButton= self.button("explode")        
        self.explodeButton.clicked.connect(lambda : navigate.explode(pm.ls(os=True, fl=True), self.minExplode.value(), self.maxExplode.value(), self.attributeList(), self.axisList()))
        
        self.loadSelectionButton = self.button("load selection")
        self.loadSelectionButton.setCheckable(True)
        self.loadSelectionButton.setChecked(False)
        self.loadSelectionButton.clicked.connect(lambda checked: self.unloadSelection() if not checked else self.loadSelection())
        
        self.checkBoxX = self.checkBox("X")
        self.checkBoxY = self.checkBox("Y")
        self.checkBoxZ = self.checkBox("Z")

        self.checkBoxTranslate = self.checkBox("translate")
        self.checkBoxRotate = self.checkBox("rotate")
        self.checkBoxScale = self.checkBox("scale")    

        self.match = self.button("match")
        self.match.clicked.connect(lambda: navigate.matchAttributes(pm.ls(os=True, fl=True), self.loadedSelection, self.attributeList(), self.axisList()))        

        self.builtLayouts['stepLayout'].addWidget(self.subdivide, 0, 1,2,1)
        self.builtLayouts['stepLayout'].addWidget(self.tie, 0, 2,2,1)
        self.builtLayouts['stepLayout'].addWidget(self.stepValue, 0, 0)
        self.builtLayouts['stepLayout'].addWidget(self.centerOfStep, 1, 0)        

        self.builtLayouts['placeholderLayout'].addWidget(self.centerOfSelection, 1, 0)
        self.builtLayouts['placeholderLayout'].addWidget(self.centerOfEach, 2, 0)

        self.builtLayouts['axisLayout'].addWidget(self.checkBoxX,0,0)
        self.builtLayouts['axisLayout'].addWidget(self.checkBoxY,0,1)
        self.builtLayouts['axisLayout'].addWidget(self.checkBoxZ,0,2)

        
        self.builtLayouts['attributesLayout'].addWidget(self.loadSelectionButton,0,0, 5,1)
        self.builtLayouts['attributesLayout'].addWidget(self.checkBoxTranslate,0,1)
        self.builtLayouts['attributesLayout'].addWidget(self.checkBoxRotate,1,1)
        self.builtLayouts['attributesLayout'].addWidget(self.checkBoxScale,2,1)
        self.builtLayouts['attributesLayout'].addWidget(self.match,3,1)


        self.explodeLayout = QGridLayout()
        self.builtLayouts['attributesLayout'].addLayout(self.explodeLayout, 4,1)
        self.explodeLayout.addWidget(self.minExplode,0,0)
        self.explodeLayout.addWidget(self.maxExplode,0,1)
        self.explodeLayout.addWidget(self.explodeButton,1,0, 1, 2)

        widget = QWidget()
        widget.setLayout( mainLayout )
        self.setCentralWidget(widget)

    def axisList(self):        
        chosenList=[]
        if self.checkBoxX.isChecked():
            chosenList.append('x')
        if self.checkBoxY.isChecked():
            chosenList.append('y')
        if self.checkBoxZ.isChecked():
            chosenList.append('z')

        return chosenList
    
    def attributeList(self):        
        chosenList=[]
        if self.checkBoxTranslate.isChecked():
            chosenList.append('t')
        if self.checkBoxRotate.isChecked():
            chosenList.append('r')
        if self.checkBoxScale.isChecked():
            chosenList.append('s')

        return chosenList

    def loadSelection(self):
        for obj in pm.ls(os=True, fl=True):
            self.loadedSelection.append(obj)

        return self.loadedSelection

    def unloadSelection(self):
        del self.loadedSelection[:]

    @staticmethod
    def button(name):
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