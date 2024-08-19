import pymel.core as pm
import navigate
import maya.cmds as cmds


class leaf:
    def __init__(self, nAme, rotation=None, constraints=None):
        self.nAme = nAme
        self.location = cmds.getAttr(nAme+'.t')
        self.rotation = rotation
        self.constraints = constraints
        self.parent = cmds.listRelatives(nAme, parent=True)
        self.children = cmds.listRelatives(nAme, children=True)
        self.type = str(cmds.nodeType(nAme))

        if self.type == "joint":
            self.orientation = cmds.getAttr(nAme + ".jointOrient")



def getTree(root, visitedBranches=None):
    if visitedBranches is None:
        visitedBranches = {}

    if isinstance(root, list):
        for branch in root:
            if branch not in visitedBranches:
                visitedBranches[branch] = []
            if cmds.listRelatives(branch, children=True):
                children = cmds.listRelatives(branch, children=True)

                for child in children:
                    if child not in visitedBranches:
                        visitedBranches[branch].append(child)
                        getTree(child, visitedBranches)
    else:
        if root not in visitedBranches:
            visitedBranches[root] = []
            children = cmds.listRelatives(root, children=True)
            if children:
                for child in children:
                    if child not in visitedBranches:
                        visitedBranches[root].append(child)
                        getTree(child, visitedBranches)

    return visitedBranches