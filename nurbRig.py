import pymel.core as pm
import controls
import basicTools as bt
import ensemble

JntGrp = ensemble.grouper(hierarchy=['main', 'position', 'offset', 'ctrl', 'constraint'])
main = ensemble.grouper(hierarchy=['main'])


def motionPath(drivenList, Curve, type):

    motionPathOffset = {'rope': 1, 'circle': 0, 'simpleCircle': 0}
    UValueOffset = 1 / float(len(drivenList) - motionPathOffset[type])
    counter = 0
    motionPathList = []

    for drv in drivenList:
        motionPath = pm.pathAnimation(drv, c=Curve, fm=True)
        pm.disconnectAttr("{}.uValue".format(motionPath))
        pm.setAttr("{}.uValue".format(motionPath), min(counter, 1))
        counter += UValueOffset
        motionPathList.append(motionPath)

    return motionPathList

def makeCurve(name, type, pointPositions, degreeAmount = 3):

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

    Curve = curveChoice[type]()

    grp = JntGrp.makeHierarchy(Curve, 'N')
    Curve.setAttr('template', True)

    return grp

def makeJoints(name, amount, type, radius):
    jointList = []
    digits = len(str(amount))
    for i in range(amount):
        jnt = pm.joint(n='{}_{:0{}d}_{}_JNT'.format(name, i + 1, digits, type), rad=radius)
        pm.parent(jnt, w=True)
        jointList.append(jnt)

    return jointList

def driverJoints(side, name, amount, Curve, type, ctrlsPositions=[]):
    JointList = makeJoints(name, amount, 'driver', 1.5)
    motionNodes = motionPath(JointList, Curve, type)
    groupList = []

    if len(ctrlsPositions) > 1:
        positions = ctrlsPositions

    else:
        positions = list(map(lambda jnt: pm.xform(jnt, q=True, worldSpace=True, translation=True), JointList))

    #ctrlList = ctrl(side, name, shape, name, 10, 3, JointList, positions)

    pm.delete(motionNodes)

    pm.skinCluster(JointList, Curve, toSelectedBones=True)
    grp = JntGrp.aggregate('{}_DRV'.format(name), groupList, 'N')
    return [grp]

def drivenJoints(name, Curve, amount, type, upVector):
    drivenJNTs = makeJoints(name, amount, 'driven', 0.5)
    motionPath(drivenJNTs, Curve, type)
    groupList = []

    for jnt in drivenJNTs:
        groupList.append(JntGrp.makeHierarchy(jnt, 'N')[-1])
        pm.tangentConstraint(Curve, jnt, wu=upVector)


    grp = JntGrp.aggregate('{}_DRN'.format(name), groupList, 'N')
    return grp

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


def rigIt(side, name, CtrlAmount, DrivenAmount, type, position, upVector):
    groupList = []
    CurveList = makeCurve(name, type, position)
    Curve = CurveList[-1]; CurveGroups = CurveList[:-1]

    driverJNTs = driverJoints(side, name, CtrlAmount, Curve, type)
    drivenJNTs = drivenJoints(side, name, Curve, DrivenAmount, type, upVector)


    groupList.append(CurveGroups[0]);
    groupList.append(driverJNTs[0]);
    groupList.append(drivenJNTs[0]);

    return main.aggregate('{}_ROOT'.format(name), groupList, 'N')


def simpleRopeRig(side, name, shape, CtrlAmount, DrivenAmount):
    points=[]
    for i in range(CtrlAmount * 2):
        points.append((0, i, 0))

    return rigIt(side, name, shape, CtrlAmount, DrivenAmount, 'rope', points, (1,0,0))

def simpleCircleRig(side, name, shape, CtrlAmount, DrivenAmount):
    return rigIt(side, name, shape, CtrlAmount, DrivenAmount, 'simpleCircle', CtrlAmount * 2, (1,0,0))

def overSelection(side, name, type, DrivenAmount, positionList, ctrlsPositions, upVector):
    groupList = []
    CurveList = makeCurve(name, type, positionList)
    Curve = CurveList[-1]; CurveGroups = CurveList[:-1]

    driverJNTs = driverJoints(name, len(ctrlsPositions), Curve, type, ctrlsPositions)
    drivenJNTs = drivenJoints(name, Curve, DrivenAmount, type, upVector)


    groupList.append(CurveGroups[0]);
    groupList.append(driverJNTs[0]);
    groupList.append(drivenJNTs[0]);

    return main.aggregate('{}_ROOT'.format(name), groupList, 'N')

