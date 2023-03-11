import pymel.core as pm
import ctrl
import bone


def make(name, positions, poleVectorPosition, shape='circle', side='N'):
    jointList = bone.chain(name, 'IK', positions)
    ikNodes = pm.ikHandle(sj=jointList[0], ee=jointList[-1])

    aimCtrlName = '{}Aim'.format(name)
    ikCtrlName = '{}Ik'.format(name)

    aimCtrl = ctrl.make(side, shape, aimCtrlName, 1, 3)
    ikCtrl = ctrl.make(side, shape, ikCtrlName, 1, 3)

    ctrl.translate(aimCtrl, [poleVectorPosition])
    ctrl.translate(ikCtrl, [positions[-1]])

    constraintNode = pm.poleVectorConstraint(aimCtrl['ctrl'], ikNodes[0])
    pm.parent(ikNodes[0], ikCtrl['ctrl'])

    return {'ik' : ikNodes, 'constraint' : constraintNode, 'joints' : jointList, 'aimControl' : aimCtrl, 'ikControl' : ikCtrl}

































