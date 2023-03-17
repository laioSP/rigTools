import pymel.core as pm
import controls
import basicTools as bt
import ensemble

JntGrp = ensemble.grouper(hierarchy=['offset'])
ctrlGrp = ensemble.grouper(hierarchy=['main', 'position', 'offset', 'ctrl', 'constraint'])
main = ensemble.grouper(hierarchy=['main'])


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
        Curve = pm.circle(degree=degreeAmount, s=len(pointPositions), n='{}_driven_CRV'.format(name), r=5)[0]
        return Curve

    def circleCurve():
        Curve = pm.circle(degree=degreeAmount, s=len(pointPositions), n='{}_driven_CRV'.format(name), r=5)[0]
        for cv, pos in zip(Curve.cv, pointPositions):
            cv.setPosition(pos)

        return Curve

    curveChoice = {
        'rope': ropeCurve,
        'circle': circleCurve,
        'simpleCircle': simpleCircle}

    Curve = curveChoice[category]()
    grp = JntGrp.flatHierarchy( '{}{}'.format(name, category), 'NURB', 'N', Curve)
    Curve.setAttr('template', True)

    return grp

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

    #ctrlList = ctrl(side, name, shape, name, 10, 3, JointList, positions)

    pm.delete(motionNodes)
    pm.skinCluster(driverJNTs, Curve, toSelectedBones=True)
    group = JntGrp.flatHierarchy(name ,'DRV', side, driverJNTs)
    pm.select(cl=True)
    return group

def drivenJoints(side, name, amount, Curve, category, upVector):
    drivenJNTs = makeJoints(name, amount, 'driven', 0.5)
    motionPath(drivenJNTs, Curve, category)

    for jnt in drivenJNTs:
        pm.tangentConstraint(Curve, jnt, wu=upVector)
    
    return JntGrp.flatHierarchy(name ,'DRN', side, drivenJNTs)

def ctrl(side, name, shape, size, amountOfSubCtrls, JointList, positions):

    ctrlsDictionary = {}
    counter = 1
    for jnt, pos in zip(JointList, positions):
        ctrls = controls.make(side, shape, name, size, amountOfSubCtrls)
        controls.translate(ctrls, [pos])

        pm.parentConstraint(ctrls['ctrl'], jnt)
        pm.scaleConstraint(ctrls['ctrl'], jnt)

        ctrlsDictionary['{}_{}'.format(name, counter)] = ctrls 
        counter +=1

    return ctrlsDictionary


def rigIt(side, name, CtrlAmount, DrivenAmount, category, position, upVector, controlShape):
    groupList = []
    curve = makeCurve(name, category, position)
    #Curve = CurveList[-1]; CurveGroups = CurveList[:-1]

    driverJNTs = driverJoints(side, name, CtrlAmount, curve, category)
    drivenJNTs = drivenJoints(side, name, DrivenAmount, curve, category, upVector)
    ctrl = controls.makeControls(side, name, controlShape, 3, 3, driverJNTs)

    nurbRig = {'ctrl' : ctrl, 'driverJoints' : driverJNTs, 'drivenJoints' : drivenJNTs}
    #groupList.append(CurveGroups[0]);
    #groupList.append(driverJNTs[0]);
    #groupList.append(drivenJNTs[0]);

    #return nurbRig


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

