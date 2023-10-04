from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QSizePolicy, QWidget, QGridLayout, QPushButton,QCheckBox, QSpinBox, QRadioButton, QDoubleSpinBox
import navigate
import blueprint
import placeholder
import pymel.core as pm
import constants
    
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.builtLayouts = {}
        self.loadedSelection = []

        self.setWindowTitle("attribute match")

        mainLayout = QGridLayout()
        layoutInputs = {'placeholderLayout' : {'spacePositionLayout':{}, 'stepLayout':{}}, 'matchLayout' : {'setPositionsLayout':{'axisLayout':{},'attributesLayout':{}}}, "explodeLayout" : {}} 

        self.chainLayout(layoutInputs, mainLayout)
        
        self.stepValue = self.numberBox(3)

        self.centerOfSelection = self.button("center of \n selection")
        self.centerOfSelection.clicked.connect(lambda: navigate.ofAll(pm.ls(os=True, fl=True)))
        
        self.tie = self.button("tie")
        self.tie.clicked.connect(lambda: navigate.ConstraintRope().tie(pm.ls(os=True, fl=True)))

        self.centerOfEach = self.button("center of \n each")
        self.centerOfEach.clicked.connect(lambda: navigate.ofEach(pm.ls(os=True, fl=True)))
        
        self.centerOfStep= self.button("center of \n step")
        self.centerOfStep.clicked.connect(lambda: navigate.ofStep(pm.ls(os=True, fl=True), int(self.stepValue.value())))
        
        self.subdivide= self.button("subdivide")        
        self.subdivide.clicked.connect(lambda : navigate.subDivide(pm.ls(os=True, fl=True), int(self.stepValue.value()) ))

        self.minLabel = QLabel('min values')
        self.maxLabel = QLabel('max values')
        self.maxExplode = self.numberBox(25)
        self.minExplode = self.numberBox(-25)

        self.startKeyLabel = QLabel('start keyframe')
        self.endKeyLabel = QLabel('end keyframe')
        self.startKeyExplode = self.numberBox(1)
        self.endKeyExplode = self.numberBox(120)
        self.animateExplode = self.checkBox("animate explosion", False)

        self.explodeButton= self.button("explode")        
        self.explodeButton.clicked.connect(lambda : navigate.explode(pm.ls(os=True, fl=True), self.minExplode.value(), self.maxExplode.value(), 
                                                                     self.attributeList(), self.axisList(), self.animateExplode.isChecked(), 
                                                                     self.startKeyExplode.value(), self.endKeyExplode.value()))
        
        self.loadSelectionButton = self.button("load \n selection")
        self.loadSelectionButton.setCheckable(True)
        self.loadSelectionButton.setChecked(False)
        self.loadSelectionButton.clicked.connect(lambda checked: self.unloadSelection() if not checked else self.loadSelection())

        self.worldRadio = QRadioButton("world")
        self.objectRadio = QRadioButton("object")
        self.worldRadio.setChecked(True)
        
        self.checkBoxX = self.checkBox("X")
        self.checkBoxY = self.checkBox("Y")
        self.checkBoxZ = self.checkBox("Z")

        self.checkBoxTranslate = self.checkBox("translate")
        self.checkBoxRotate = self.checkBox("rotate")
        self.checkBoxScale = self.checkBox("scale")    
        self.checkBoxScale.setChecked(False)

        self.match = self.button("match")
        self.match.clicked.connect(lambda: navigate.matchAttributes(pm.ls(os=True, fl=True), self.loadedSelection, self.attributeList(), 
                                                                    self.axisList(), self.spacePostion()))        

        self.importPlaceholders = self.button("import \n placeholders")
        self.importPlaceholders.clicked.connect(lambda : blueprint.importBlueprint())

        self.exportPlaceholders = self.button("export \n placeholders")
        self.exportPlaceholders.clicked.connect(lambda : blueprint.exportBlueprint())

        self.updateAllPlaceholders = self.button("update all \n placeholders")
        self.updateAllPlaceholders.clicked.connect(lambda : placeholder.update(pm.ls(constants.placeholderGroup)[0].listRelatives(s=False)))

        self.updateSelectedPlaceholders = self.button("update \n selected \n placeholders")
        self.updateSelectedPlaceholders.clicked.connect(lambda : placeholder.update(pm.ls(os=True, fl=True)))

        self.resetSelectedPlaceholders = self.button("reset \n selected \n placeholders")
        self.resetSelectedPlaceholders.clicked.connect(lambda : placeholder.reset(pm.ls(os=True, fl=True)))

        self.resetAllPlaceholders = self.button("reset \n all \n placeholders")
        self.resetAllPlaceholders.clicked.connect(lambda : placeholder.reset(pm.ls(constants.placeholderGroup)[0].listRelatives(s=False)))

        self.clean = self.button("clean up")
        self.clean.clicked.connect(lambda : placeholder.deleteGroup())

        self.builtLayouts['spacePositionLayout'].addWidget(self.importPlaceholders, 0, 0, 1, 3)
        self.builtLayouts['spacePositionLayout'].addWidget(self.updateAllPlaceholders, 1, 0)
        self.builtLayouts['spacePositionLayout'].addWidget(self.updateSelectedPlaceholders, 1, 1)
        self.builtLayouts['spacePositionLayout'].addWidget(self.resetAllPlaceholders, 2, 0)
        self.builtLayouts['spacePositionLayout'].addWidget(self.resetSelectedPlaceholders, 2, 1)
        self.builtLayouts['spacePositionLayout'].addWidget(self.exportPlaceholders, 3, 0, 1, 3)
        self.builtLayouts['spacePositionLayout'].addWidget(self.worldRadio, 4, 0)
        self.builtLayouts['spacePositionLayout'].addWidget(self.objectRadio, 4, 1)

        self.builtLayouts['stepLayout'].addWidget(self.stepValue, 1, 0)
        self.builtLayouts['stepLayout'].addWidget(self.centerOfStep, 2, 0)  
        self.builtLayouts['stepLayout'].addWidget(self.subdivide, 1, 1, 2, 1)
        self.builtLayouts['stepLayout'].addWidget(self.tie, 1, 2, 2, 1)
        
        self.builtLayouts['placeholderLayout'].addWidget(self.centerOfSelection, 2, 0)
        self.builtLayouts['placeholderLayout'].addWidget(self.centerOfEach, 3, 0)

        self.builtLayouts['axisLayout'].addWidget(self.checkBoxX,0,0)
        self.builtLayouts['axisLayout'].addWidget(self.checkBoxY,0,1)
        self.builtLayouts['axisLayout'].addWidget(self.checkBoxZ,0,2)

        self.builtLayouts['attributesLayout'].addWidget(self.loadSelectionButton,0,0, 4,1)
        self.builtLayouts['attributesLayout'].addWidget(self.checkBoxTranslate,0,1)
        self.builtLayouts['attributesLayout'].addWidget(self.checkBoxRotate,1,1)
        self.builtLayouts['attributesLayout'].addWidget(self.checkBoxScale,2,1)
        self.builtLayouts['attributesLayout'].addWidget(self.match,3,1)

        self.builtLayouts['explodeLayout'].addWidget(self.minLabel,0,0)
        self.builtLayouts['explodeLayout'].addWidget(self.maxLabel,0,1)
        self.builtLayouts['explodeLayout'].addWidget(self.minExplode,1,0)
        self.builtLayouts['explodeLayout'].addWidget(self.maxExplode,1,1)

        self.builtLayouts['explodeLayout'].addWidget(self.animateExplode, 2,0)
        self.builtLayouts['explodeLayout'].addWidget(self.startKeyLabel, 3,0)
        self.builtLayouts['explodeLayout'].addWidget(self.endKeyLabel, 3,1)
        self.builtLayouts['explodeLayout'].addWidget(self.startKeyExplode, 4,0)
        self.builtLayouts['explodeLayout'].addWidget(self.endKeyExplode, 4,1)
        self.builtLayouts['explodeLayout'].addWidget(self.explodeButton,5,0, 1, 2)

        mainLayout.addWidget(self.clean,3,0)

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

    def spacePostion(self):
        if self.objectRadio.isChecked():
            return 'object'
        
        if self.worldRadio.isChecked():
            return 'world'

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
    
    @staticmethod
    def numberBox(defaultValue, max='noLimit', min = -100000000):
        box = QDoubleSpinBox()
        box.setDecimals(2)
        if max == 'noLimit':
            box.setMaximum(100000000)  
        else:
            box.setMaximum(max)  

        box.setMinimum(min)
        box.setValue(defaultValue)

        return box
      
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