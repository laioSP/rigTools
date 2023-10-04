import pymel.core as pm
import blueprint
import nurbRig
import ikRig
import controls



class ik:
    def __init__(self, side, name, shape):
        self.side = side
        self.name = name
        self.shape = shape
        self.positions={'translation' : [], 'rotation' : []}        
        self.rig = {}
                
    def placement(self):
        self.rig = nurbRig.stiffRopeRig(self.side, '{}_placement'.format(self.name), 3, 0, self.shape)
        self.rig['aim'] = fk(self.side, self.name, self.shape).placement(translation = (-5,3,0))
                
        return self.rig 

    def inquiry(self):
        for jnt in self.rig['driverJoints']:
            self.positions['translation'].append(jnt.getAttr('t'))    
            self.positions['rotation'].append(jnt.getAttr('r'))   
            
        self.positions['aim'] = self.rig['aim']['driverJoints'][0].getAttr('t')
        
        return self.positions
    
    def build(self):
        self.rig.clear()
        controler =ikRig.make(self.name, self.positions['translation'], self.positions['aim'], self.shape, self.side)
        return controler


class fk:

    def __init__(self, side, name, shape):
        self.side = side
        self.name = name
        self.shape = shape
        self.positions={}        
        self.rig = {}
        
    def placement(self, translation = (0,0,0), rotation = (0,0,0)):
        self.rig = controls.makeFk(self.side, '{}_placement'.format(self.name), self.shape, 3, 1, translation, rotation)
        print(self.rig)
        return self.rig 

    def inquiry(self):
        self.positions['translation'] = self.rig['driverJoints'][0].getAttr('t')    
        self.positions['rotation'] = self.rig['driverJoints'][0].getAttr('r')            
        return self.positions

    def build(self):
        pm.delete(self.rig['group'])
        self.rig.clear()
        self.rig = controls.makeFk(self.side, self.name, self.shape, 3, 1, translation = self.positions['translation'], rotation = self.positions['rotation'])
        print(self.rig)

        return self.rig


























