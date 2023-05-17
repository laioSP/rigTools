import pymel.core as pm



class ConstraintRope:
    def __init__(self):
        self.groupManager={}

    def makeGroup(self, knot, direction):
        grp=cmds.group(n='{}_{}_Grp'.format(knot, direction), em=True)
        return grp

    def constraintIt(self, linksList, direction):
        anchor, hood = self.groupManager[direction]
        weight=0.33
        for link in range(len(linksList) - 1):
            pm.parentConstraint(linksList[link], linksList[link + 1], mo=True, w=weight)
            pm.scaleConstraint(linksList[link], linksList[link + 1], mo=True, w=weight)
            pm.parentConstraint(anchor, linksList[link], mo=True, w=weight)
            pm.scaleConstraint(anchor, linksList[link], mo=True, w=weight)

    def chain(self,knotsList, direction):
        groupList=[]
        for knot in knotsList:
            groupList.append(self.makeGroup(knot, direction))

        anchor = self.makeGroup('anchor', direction)
        hood = self.makeGroup('hood', direction)
        self.groupManager[direction]= [ anchor, hood]

        pm.parent(anchor, hood)
        for grp in groupList:
            pm.parent(grp,hood)

        return groupList

    def tie(self, knotsList):

        driven = self.chain(knotsList, 'driven')
        forward = self.chain(knotsList, 'forward')
        backward = self.chain(knotsList, 'backward')

        self.constraintIt(forward, 'forward')
        backward.reverse()
        self.constraintIt(backward, 'backward')
        backward.reverse()
        weight = 0.33
        ctrlGrp = self.makeGroup('ctrl', 'ctrl')

        for up, down, drv, knot in zip(forward, backward, driven, knotsList):
            pm.parentConstraint(up, drv, mo=True, w=0.5)
            pm.parentConstraint(down, drv, mo=True, w=0.5)
            pm.scaleConstraint(up, drv, mo=True, w=0.5)
            pm.scaleConstraint(down, drv, mo=True, w=0.5)

            pm.parent(knot, drv)

            ctrl=pm.circle(nr=(0, 0, 1), c=(0, 0, 0))[0]
            pm.addAttr(ctrl, ln='offset', k=True, at='float')
            grp=pm.group(n='{}_offset_grp'.format(knot))
            pm.parent(grp, ctrlGrp)
            pm.matchTransform(grp, knot)
                        
            UpParent = pm.parentConstraint(ctrl, up, mo=True, w=weight)
            UpScale = pm.scaleConstraint(ctrl, up, mo=True, w=weight)
            DownParent = pm.parentConstraint(ctrl, down, mo=True, w=weight)
            DownScale = pm.scaleConstraint(ctrl, down, mo=True, w=weight)
            
            WeightDistribution = lambda node : pm.listAttr(node, k=True)[-1]
            
            ctrl.connectAttr('offset','{}.{}'.format(UpParent, WeightDistribution(UpParent)))
            ctrl.connectAttr('offset','{}.{}'.format(UpScale, WeightDistribution(UpScale)))
            ctrl.connectAttr('offset','{}.{}'.format(DownParent, WeightDistribution(DownParent)))
            ctrl.connectAttr('offset','{}.{}'.format(DownScale, WeightDistribution(DownScale)))
            
            ctrl.setAttr('offset', 0.34)
           


