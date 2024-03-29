import pymel.core as pm
import controls
import ensemble

nurbRigGrp = ensemble.grouper(hierarchy=['offset'])

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
    grp = nurbRigGrp.flatHierarchy( '{}{}'.format(name, category.capitalize()), 'NURB', 'N', Curve)
    Curve.setAttr('template', True)

    return Curve



def driverJoints(side, name, amount, Curve, category):
    driverJNTs = controls.makeJoints(name, amount, 'driver', 1.5)
    motionNodes = motionPath(driverJNTs, Curve, category)

    positions = list(map(lambda jnt: pm.xform(jnt, q=True, worldSpace=True, translation=True), driverJNTs))
    
    pm.delete(motionNodes)
    pm.skinCluster(driverJNTs, Curve, toSelectedBones=True)
    nurbRigGrp.flatHierarchy(name ,'DRV', side, driverJNTs)
    pm.select(cl=True)
    return driverJNTs

def drivenJoints(side, name, amount, Curve, category, upVector):
    drivenJNTs = controls.makeJoints(name, amount, 'driven', 0.5)
    motionPath(drivenJNTs, Curve, category)

    for jnt in drivenJNTs:
        pm.tangentConstraint(Curve, jnt, wu=upVector)
    
    nurbRigGrp.flatHierarchy(name ,'DRN', side, drivenJNTs)
    
    return  drivenJNTs

def rigIt(side, name, CtrlAmount, DrivenAmount, category, position, upVector, controlShape, degreeAmount = 3):
    curve = makeCurve(name, category, position, degreeAmount)

    driverJNTs = driverJoints(side, name, CtrlAmount, curve, category)
    drivenJNTs = drivenJoints(side, name, DrivenAmount, curve, category, upVector)
    ctrl = controls.makeControls(side, name, controlShape, 3, 3, driverJNTs)
    nurbRigGrp.flatGroups[ctrl]=[]
    nurbRig = {'ctrl' : ctrl, 'driverJoints' : driverJNTs, 'drivenJoints' : drivenJNTs}
    
    nurbRigGrp.flatHierarchy(name, '{}Rig'.format(category.capitalize()), side, list(nurbRigGrp.flatGroups.keys()))
    nurbRigGrp.clearflatGroups()
    pm.select(cl=True)
    return nurbRig

def simpleRopeRig(side, name, CtrlAmount, DrivenAmount, shape, degreeAmount = 3):
    points=[]
    for i in range(CtrlAmount * 2):
        points.append((0, i, 0))

    return rigIt(side, name, CtrlAmount, DrivenAmount, 'rope', points, (1,0,0), shape, degreeAmount)

def stiffRopeRig(side, name, CtrlAmount, DrivenAmount, shape, degreeAmount = 1):
    points=[]
    for i in range(CtrlAmount):
        points.append((0, i*3, 0))

    return rigIt(side, name, CtrlAmount, DrivenAmount, 'rope', points, (1,0,0), shape, degreeAmount)


def simpleCircleRig(side, name, shape, CtrlAmount, DrivenAmount):
    return rigIt(side, name, CtrlAmount, DrivenAmount, 'simpleCircle', CtrlAmount * 2, (1,0,0), shape)

def customPositions(side, name, category, DrivenAmount, positionList, ctrlsPositions, upVector, controlShape):
    groupList = []
    CurveList = makeCurve(name, category, positionList)
    Curve = CurveList[-1]; CurveGroups = CurveList[:-1]

    driverJNTs = driverJoints(name, len(ctrlsPositions), Curve, category, ctrlsPositions)
    drivenJNTs = drivenJoints(name, Curve, DrivenAmount, category, upVector)

    groupList.append(CurveGroups[0]);
    groupList.append(driverJNTs[0]);
    groupList.append(drivenJNTs[0]);
    
    nurbRigGrp.clearflatGroups()

