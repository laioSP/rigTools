import pymel.core as pm
import controls
#import ensemble 
from groupSettings import nurbRigGrp, allGroups

def motionPath(drivenList, Curve, category):

    motionPathOffset = {'rope': 1, 'circle': 0, 'simpleCircle': 0}
    UValueOffset = 1 / float(len(drivenList) - motionPathOffset[category])
    counter = 0
    motionPathList = []

    for drv in drivenList:
        motionPath = pm.pathAnimation(drv, c=Curve, fm=True)
        pm.disconnectAttr("{}.uValue".format(motionPath))
        pm.setAttr("{}.uValue".format(motionPath), min(counter, 1))
        counter += UValueOffset
        motionPathList.append(motionPath)

    return motionPathList

def makeCurve(name, category, pointPositions, degreeAmount = 3):

    def ropeCurve():

        Curve = pm.curve(degree=degreeAmount, point=pointPositions, n='{}_driven_CRV'.format(name))
        return Curve

    def simpleCircle():
        Curve = pm.circle(degree=degreeAmount, s=pointPositions, n='{}_driven_CRV'.format(name), r=5)[0]
        return Curve

    def circleCurve():
        Curve = pm.circle(degree=degreeAmount, s=pointPositions, n='{}_driven_CRV'.format(name), r=5)[0]
        for cv, pos in zip(Curve.cv, pointPositions):
            cv.setPosition(pos)

        return Curve

    curveChoice = {
        'rope': ropeCurve,
        'circle': circleCurve,
        'simpleCircle': simpleCircle}

    Curve = curveChoice[category]()
    grp = nurbRigGrp.flatHierarchy( '{}{}'.format(name, category.upper()), 'NURB', 'N', Curve)
    Curve.setAttr('template', True)

    return Curve

def makeJoints(name, amount, category, radius):
    jointList = []
    digits = len(str(amount))
    for i in range(amount):
        jnt = pm.joint(n='{}_{:0{}d}_{}_JNT'.format(name, i + 1, digits, category), rad=radius)
        pm.parent(jnt, w=True)
        jointList.append(jnt)

    return jointList

def driverJoints(side, name, amount, Curve, category):
    driverJNTs = makeJoints(name, amount, 'driver', 1.5)
    motionNodes = motionPath(driverJNTs, Curve, category)

    positions = list(map(lambda jnt: pm.xform(jnt, q=True, worldSpace=True, translation=True), driverJNTs))
    
    pm.delete(motionNodes)
    pm.skinCluster(driverJNTs, Curve, toSelectedBones=True)
    nurbRigGrp.flatHierarchy(name ,'DRV', side, driverJNTs)
    pm.select(cl=True)
    return driverJNTs

def drivenJoints(side, name, amount, Curve, category, upVector):
    drivenJNTs = makeJoints(name, amount, 'driven', 0.5)
    motionPath(drivenJNTs, Curve, category)

    for jnt in drivenJNTs:
        pm.tangentConstraint(Curve, jnt, wu=upVector)
    
    nurbRigGrp.flatHierarchy(name ,'DRN', side, drivenJNTs)
    
    return  drivenJNTs

def rigIt(side, name, CtrlAmount, DrivenAmount, category, position, upVector, controlShape):
    groupList = []
    curve = makeCurve(name, category, position)
    #Curve = CurveList[-1]; CurveGroups = CurveList[:-1]

    driverJNTs = driverJoints(side, name, CtrlAmount, curve, category)
    drivenJNTs = drivenJoints(side, name, DrivenAmount, curve, category, upVector)
    ctrl = controls.makeControls(side, name, controlShape, 3, 3, driverJNTs)

    nurbRig = {'ctrl' : controls.ctrlsDictionary, 'driverJoints' : driverJNTs, 'drivenJoints' : drivenJNTs}
    
    groupList = [nurbRigGrp.groupDictionary.keys(), allGroups['ctrl'].keys()[-1]]
    
    nurbRigGrp.flatHierarchy(name, '{}rig'.format(category.upper()), side, nurbRigGrp.groupDictionary.keys())
    #groupList.append(CurveGroups[0]);
    #groupList.append(driverJNTs[0]);
    #groupList.append(drivenJNTs[0]);

    return nurbRig


def simpleRopeRig(side, name, shape, CtrlAmount, DrivenAmount, controlShape):
    points=[]
    for i in range(CtrlAmount * 2):
        points.append((0, i, 0))

    return rigIt(side, name, CtrlAmount, DrivenAmount, 'rope', points, (1,0,0), controlShape)

def simpleCircleRig(side, name, shape, CtrlAmount, DrivenAmount, controlShape):
    return rigIt(side, name, CtrlAmount, DrivenAmount, 'simpleCircle', CtrlAmount * 2, (1,0,0), controlShape)

def overSelection(side, name, category, DrivenAmount, positionList, ctrlsPositions, upVector, controlShape):
    groupList = []
    CurveList = makeCurve(name, category, positionList)
    Curve = CurveList[-1]; CurveGroups = CurveList[:-1]

    driverJNTs = driverJoints(name, len(ctrlsPositions), Curve, category, ctrlsPositions)
    drivenJNTs = drivenJoints(name, Curve, DrivenAmount, category, upVector)

    groupList.append(CurveGroups[0]);
    groupList.append(driverJNTs[0]);
    groupList.append(drivenJNTs[0]);

    return main.pyramidHierarchy('{}_ROOT'.format(name), groupList, 'N')

