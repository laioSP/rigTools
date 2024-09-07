import pymel.core as pm
import nurbShapes as sh



def ensure_list(item):
    putIntoAlist = {'str': [item], 'Transform': [item], 'list': item}
    listOfTargets = putIntoAlist[category(item).__name__]

    return listOfTargets


def numberedName(name, category, objType, amount):
    digits = len(str(amount))
    nameList=[]
    
    check = lambda x: ('', '_{}'.format(x))[x is not None]

    
    for i in range(amount):        
        numberedName = '{}_{:0{}d}{}{}'.format(name, i + 1, digits, check (category), check(objType))
        nameList.append(numberedName)
    
    
    
    return nameList


def numberedName(name, category, objType, amount):
    digits = len(str(amount))
    nameList=[]
    
    check = lambda x: ('', '_{}'.format(x))[x is not None]
    
    for i in range(amount):        
        numberedName = '{}_{:0{}d}{}{}'.format(name, i + 1, digits, check (category), check(objType))
        nameList.append(numberedName)
    
    return nameList


def alphabetName(name, category, objType, amount):
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    nameList=[]
    
    check = lambda x: ('', '_{}'.format(x))[x is not None]
    
    for i in range(amount):        
        numberedName = '{}_{}{}{}'.format(name, alphabet[i], check (category), check(objType))
        nameList.append(numberedName)
    
    return nameList



class switch:
    def __init__(self, objects, attribute):
        self.objects = objects
        self.attribute = attribute
        self.mayaObject = {True : self.shiftMayaState , False : self.shiftPythonState}
        self.switcher = {True: False, False: True}

    def updateSwitch(self, newSwitch):
        self.switcher = newSwitch
        return self.switcher

    def shiftPythonState(self):
        oldState = self.attribute
        newState = self.switcher[self.attribute]
        self.attribute = newState
        return oldState, newState

    def shiftMayaState(self):
        for obj in pm.ls(self.objects):
            oldState = obj.getAttr(self.attribute)
            newState = self.switcher[oldState]
            obj.setAttr(self.attribute, newState)
            return oldState, newState

    def shift(self):
        oldState, newState = self.mayaObject[pm.objExists(self.objects)]()
        #print '{}_>_{}'.format(oldState, newState)
        return [oldState, newState]


#geoVisibility = switch('RootGeometry_Grp', 'v')











