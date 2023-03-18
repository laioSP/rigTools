import pymel.core as pm


flatGroups ={}

class grouper:
    hierarchy = []

    def __init__(self, hierarchy):
        self.hierarchy = hierarchy
        self.groupDictionary = {}

    # create group and add it to self.groupDictionary
    def make(self, name, category, side):
        nameSide = {'N': '{}_{}', 'C': 'C_{}_{}', 'L': 'L_{}_{}', 'R': 'R_{}_{}'}
        
        groupName = nameSide[side].format(name, category)
        pm.select(cl=True)
        grp = pm.group(n=groupName, em=True)
        return grp

    # remove it from self.groupDictionary
    def delete(self, target):
        del self.groupDictionary[target]

    # check if the group exist and if not, it delete from self.groupDictionary
    def check(self, target): 
        cond = {True : lambda doNothing : doNothing, False : self.delete}             
        cond[pm.objExists(target)](target)  

    # create an empty group sequence following self.groupDictionary
    def emptyGroupPile(self, name, side):
        self.groupDictionary[name] = []
        for category in self.hierarchy:
            grp = self.make(name, category, side)
            self.groupDictionary[name].append(grp)

        self.pileUpParenting(name)
        return self.groupDictionary[name]
    
    # parent a sequence of groups in self.groupDictionary that belongs to the same object
    # |pCube2_a|pCube2_b|pCube2_c
    def pileUpParenting(self, target):
        for grp in range(len(self.groupDictionary[target]) - 1):
            pm.parent(self.groupDictionary[target][grp + 1], self.groupDictionary[target][grp])

    # parent a root group of one object to the lowest object of the previous group sequence
    def linearHierarchy(self, target, side):
        self.groupDictionary[target] = []

        for category in self.hierarchy:
            grp = self.make(target, category, side)
            self.groupDictionary[target].append(grp)

        self.groupDictionary[target].append(target)
        self.pileUpParenting(target)
        
        return self.groupDictionary[target]

    # parent the targetList under one group
    def flatHierarchy(self, name, category, side, targetList):
        grp = self.make(name, category, side) 
        pm.parent(targetList, grp)
        self.groupDictionary[grp] = targetList
        flatGroups[grp] = self.groupDictionary[grp]

        return grp

    # parent the targetList under one group sequence
    def pyramidHierarchy(self, name, targetList, side):
        grp = self.emptyGroupPile(name, 'N')        

        for target in targetList:
            if target in self.groupDictionary:
                pm.parent(self.groupDictionary[target][0], grp[-1])
            else:
                pm.parent(target, grp[-1])

        return self.groupDictionary[name]


def clearflatGroups():
    flatGroups.clear()
    







































