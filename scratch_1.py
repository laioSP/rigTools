def motionPath(drivenList, Curve):
    UValueOffset = 1 / float(len(drivenList) - 1)
    counter = 0
    motionPathList = []

    for drv in drivenList:
        motionPath = pm.pathAnimation(drv, c=Curve, fm=True)
        pm.disconnectAttr("{}.uValue".format(motionPath))
        pm.setAttr("{}.uValue".format(motionPath), counter)
        counter += UValueOffset
        motionPathList.append(motionPath)

    return motionPathList


def subDivide(firstPosition, lastPosition, amount):
    incrementPostion = []
    subDividedPositions = []

    if sum(firstPosition) - sum(lastPosition) < 0:
        startPosition = firstPosition
        endPosition = lastPosition

    else:
        startPosition = lastPosition
        endPosition = firstPosition

    for s, e in zip(startPosition, endPosition):
        incrementPostion.append((s - e) / float(amount + 1))

    for a in range(1, amount + 1):
        newPosition = []
        for s, i in zip(startPosition, incrementPostion):
            newPosition.append(s - i * a)
        subDividedPositions.append(newPosition)

    return subDividedPositions


def createCurve(name, type, pointAmount):
    def ropeCurve():
        points = []
        for i in range(pointAmount):
            points.append((0, 0 + i + 1, 0))

        return pm.curve(degree=3, point=points, n='{}_driven_CRV'.format(name))

    def circleCurve():
        return pm.circle(degree=3, s=pointAmount, n='{}_driven_CRV'.format(name))[0]

    curveChoice = {
        'rope': ropeCurve,
        'circle': circleCurve
    }

    return curveChoice[type]()


def makeJoints(name, amount, type, radius):
    jointList = []
    digits = len(str(amount))
    for i in range(amount):
        jnt = pm.joint(n='{}_{:0{}d}_{}_JNT'.format(name, i + 1, digits, type), rad=radius)
        pm.parent(jnt, w=True)
        jointList.append(jnt)
    return jointList


def driverJoints(name, amount, Curve):
    JointList = makeJoints(name, amount, 'driver', 1.5)
    startPoint = Curve.cv[0].getPosition()
    endPoint = Curve.cv[-1].getPosition()

    JointsPositions = [startPoint]
    for i in subDivide(startPoint, endPoint, amount - 2):
        JointsPositions.append(i)
    JointsPositions.append(endPoint)
    print(JointsPositions)
    for jnt, pos in zip(JointList, JointsPositions):
        jnt.setAttr('t', pos)
    pm.skinCluster(JointList, Curve, toSelectedBones=True)

    return JointList


def drivenJoints(name, Curve, amount):
    drivenJNTs = makeJoints(name, amount, 'driven', 0.5)
    motionPath(drivenJNTs, Curve)

    return drivenJNTs


def rope(name, CtrlAmount, DrivenAmount):
    Curve = createCurve(name, 'rope', CtrlAmount * 2)
    driverJNTs = driverJoints(name, CtrlAmount, Curve)
    drivenJNTs = drivenJoints(name, Curve, DrivenAmount)
