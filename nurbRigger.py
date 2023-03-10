import pymel.core as pm
import basicTools as bt


JntGrp = bt.groupMaker(hierarchy=['main', 'position', 'offset', 'ctrl', 'constraint'])
main = bt.groupMaker(hierarchy=['main'])


class nurbRig:

    def motionPath(self, drivenList, Curve, type):

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

    def createCurve(self, name, type, pointPositions):
        def ropeCurve():

            Curve = pm.curve(degree=3, point=pointPositions, n='{}_driven_CRV'.format(name))
            grp = JntGrp.createHierarchy(Curve, 'N')
            return grp

        def simpleCircle():
            Curve = pm.circle(degree=3, s=pointPositions, n='{}_driven_CRV'.format(name), r=5)[0]
            grp = JntGrp.createHierarchy(Curve, 'N')
            return grp

        def circleCurve():
            Curve = pm.circle(degree=3, s=len(pointPositions), n='{}_driven_CRV'.format(name), r=5)[0]

            for cv, pos in zip(Curve.cv, pointPositions):
                cv.setPosition(pos)

            grp = JntGrp.createHierarchy(Curve, 'N')
            return grp

        curveChoice = {
            'rope': ropeCurve,
            'circle': circleCurve,
            'simpleCircle': simpleCircle}

        return curveChoice[type]()

    def makeJoints(self, name, amount, type, radius):
        jointList = []
        digits = len(str(amount))
        for i in range(amount):
            jnt = pm.joint(n='{}_{:0{}d}_{}_JNT'.format(name, i + 1, digits, type), rad=radius)
            pm.parent(jnt, w=True)
            jointList.append(jnt)

        return jointList

    def driverJoints(self, name, amount, Curve, type, ctrlsPositions=[]):
        JointList = self.makeJoints(name, amount, 'driver', 1.5)
        motionNodes = self.motionPath(JointList, Curve, type)
        groupList = []

        if len(ctrlsPositions) > 1:
            positions = ctrlsPositions

        else:
            positions = list(map(lambda jnt: pm.xform(jnt, q=True, worldSpace=True, translation=True), JointList))

        pm.delete(motionNodes)

        counter = 1
        for jnt, pos in zip(JointList, positions):
            groupList.append(JntGrp.createHierarchy(jnt, 'N')[-1])
            jnt.setAttr('t', pos)

            ctrlList = bt.ctrl().makeCtrl('N', 'cube', name, 1, 3, counter)
            ctrlList[0][0].setAttr('t', pos)

            pm.parentConstraint(ctrlList[-1][-1], jnt)
            pm.scaleConstraint(ctrlList[-1][-1], jnt)

            counter +=1

        pm.skinCluster(JointList, Curve, toSelectedBones=True)
        grp = JntGrp.aggregate('{}_DRV'.format(name), groupList, 'N')
        return grp

    def drivenJoints(self, name, Curve, amount, type):
        drivenJNTs = self.makeJoints(name, amount, 'driven', 0.5)
        self.motionPath(drivenJNTs, Curve, type)
        groupList = []

        for jnt in drivenJNTs:
            groupList.append(JntGrp.createHierarchy(jnt, 'N')[-1])
            pm.tangentConstraint(Curve, jnt)


        grp = JntGrp.aggregate('{}_DRN'.format(name), groupList, 'N')
        return grp

    def rigIt(self, name, CtrlAmount, DrivenAmount, type, position):
        groupList = []
        CurveList = self.createCurve(name, type, position)
        Curve = CurveList[-1]; CurveGroups = CurveList[:-1]

        driverJNTs = self.driverJoints(name, CtrlAmount, Curve, type)
        drivenJNTs = self.drivenJoints(name, Curve, DrivenAmount, type)


        groupList.append(CurveGroups[0]);
        groupList.append(driverJNTs[0]);
        groupList.append(drivenJNTs[0]);

        return main.aggregate('{}_ROOT'.format(name), groupList, 'N')


    def simpleRopeRig(self, name, CtrlAmount, DrivenAmount):
        points=[]
        for i in range(CtrlAmount * 2):
            points.append((0, i, 0))

        return self.rigIt(name, CtrlAmount, DrivenAmount, 'rope', points)

    def simpleCircleRig(self, name, CtrlAmount, DrivenAmount):
        return self.rigIt(name, CtrlAmount, DrivenAmount, 'simpleCircle', CtrlAmount * 2)

    def overSelection(self, name, type, DrivenAmount, positionList, ctrlsPositions):
        groupList = []
        CurveList = self.createCurve(name, type, positionList)
        Curve = CurveList[-1]; CurveGroups = CurveList[:-1]

        driverJNTs = self.driverJoints(name, len(ctrlsPositions), Curve, type, ctrlsPositions)
        drivenJNTs = self.drivenJoints(name, Curve, DrivenAmount, type)


        groupList.append(CurveGroups[0]);
        groupList.append(driverJNTs[0]);
        groupList.append(drivenJNTs[0]);

        return main.aggregate('{}_ROOT'.format(name), groupList, 'N')

