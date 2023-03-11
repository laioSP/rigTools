import pymel.core as pm


class grouper:
    hierarchy = []

    def __init__(self, hierarchy):
        self.hierarchy = hierarchy
        self.groupDictionary = {}

    def make(self, side, grpName, type):
        nameSide = {'N': '{}_{}', 'C': 'C_{}_{}', 'L': 'L_{}_{}', 'R': 'R_{}_{}'}

        groupName = nameSide[side].format(grpName, type)
        pm.select(cl=True)
        grp = pm.group(n=groupName, em=True)
        return grp

    def delete(self, target):
        pm.delete(target)

    def check(self, target):
        return cmds.objExists(target)

    def sequenceParenting(self, target):
        for grp in range(len(self.groupDictionary[target]) - 1):
            pm.parent(self.groupDictionary[target][grp + 1], self.groupDictionary[target][grp])

    def makeHierarchy(self, target, side):
        self.groupDictionary[target] = []
        for type in self.hierarchy:
            grp = self.make(side, target, type)
            self.groupDictionary[target].append(grp)

        self.groupDictionary[target].append(target)
        self.sequenceParenting(target)
        return self.groupDictionary[target]

    def emptyGroup(self, name, side):
        self.groupDictionary[name] = []
        for type in self.hierarchy:
            grp = self.make(side, name, type)
            self.groupDictionary[name].append(grp)

        self.sequenceParenting(name)
        return self.groupDictionary[name]

    def aggregate(self, name, target, side):
        grp = self.emptyGroup(name, 'N')

        for t in target:
            if t in self.groupDictionary:
                pm.parent(self.groupDictionary[t][0], grp[-1])
            else:
                pm.parent(t, grp[-1])

        return self.groupDictionary[name]
