import maya.cmds as cmds


def createJoint():
    j_number = cmds.intField(jointNumber, q=True, v=True)
    parentJnt = ''
    rootJnt = ''
    curveSelected = cmds.ls(sl=True)[0]
    rad = cmds.radioCollection(orient, q=True, sl=True)

    # flexible estimate
    curveLen = cmds.arclen(curveSelected)
    if cmds.checkBox('flexEst', q=True, v=True): j_number = int(round(curveLen / 0.27))

    for i in range(j_number):
        cmds.select(cl=True)
        newJnt = cmds.joint()
        mp = cmds.pathAnimation(newJnt, c=curveSelected, fm=True)
        cmds.cutKey(mp + '.u', time=())
        cmds.setAttr(mp + '.u', i * (1.0 / (j_number - 1)))
        cmds.delete(newJnt + '.tx', icn=True)
        cmds.delete(newJnt + '.ty', icn=True)
        cmds.delete(newJnt + '.tz', icn=True)
        cmds.delete(mp)

        if i == 0:
            parentJnt = newJnt
            rootJnt = newJnt
            continue

        cmds.parent(newJnt, parentJnt)
        parentJnt = newJnt
        if rad == 'child': cmds.joint(rootJnt, edit=True, oj='xyz', sao='yup', ch=True, zso=True)


if cmds.window('joint_Curve', exists=True):
    cmds.deleteUI('joint_Curve')

cmds.window('joint_Curve', title='Joint Along Curve', w=150)
cmds.columnLayout(adjustableColumn=True)

cmds.frameLayout(label='Select a curve', cll=False, bgc=[0.3, 0, 0.3], w=200)
jointNumber = cmds.intField(v=15, min=2)
cmds.checkBox('flexEst', label='Flexible estimate')

cmds.frameLayout(label='Orientation', cll=False, bgc=[0.3, 0, 0.3], w=200)
orient = cmds.radioCollection()
cmds.radioButton('world', label='World orientation', sl=True)
cmds.radioButton('child', label='Child orientation')

cmds.button('create', c='createJoint()')

cmds.showWindow()
