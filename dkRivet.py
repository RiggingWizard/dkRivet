# SELECT 2 EDGES OF A POLYGON OBJECT AND RUN THE SCRIPT #

import maya.cmds as cmds

def dkRivet():
	sel = cmds.ls(sl = 1)
	
	# SPLIT THE SELECTION NAME #
	splitNameA = sel[0].split('.')
	splitNameB = sel[1].split('.')
	
	# GET THE OBJECT NAME #
	obj = splitNameA[0] 
	
	# GET THE VERTEX NUMBER #
	vertexA = splitNameA[1].replace('e', '').replace('[', '').replace(']', '') 
	vertexB = splitNameB[1].replace('e', '').replace('[', '').replace(']', '')
	
	# GET THE SHAPE NODE OF THE SELECTED OBJECT #
	shape = cmds.listRelatives(obj, shapes = 1)[0]
	
	# CREATE AND CONNECT curveFromMeshEdge Node #
	curveFromMeshEdgeA = cmds.createNode('curveFromMeshEdge', name = 'curveFromEdgeA_rivet1')
	curveFromMeshEdgeB = cmds.createNode('curveFromMeshEdge', name = 'curveFromEdgeB_rivet1')
	cmds.connectAttr(shape + '.w', curveFromMeshEdgeA + '.im')
	cmds.connectAttr(shape + '.w', curveFromMeshEdgeB + '.im')
	cmds.setAttr(curveFromMeshEdgeA + '.ei[0]', int(vertexA))
	cmds.setAttr(curveFromMeshEdgeB + '.ei[0]', int(vertexB))
	
	# CREATE pointOnSurfaceInfo Node #
	pointOnSurfaceInfoNode = cmds.createNode('pointOnSurfaceInfo', name = 'pointOnSurfaceInfo1')
	cmds.setAttr(pointOnSurfaceInfoNode + '.turnOnPercentage', 1)
	cmds.setAttr(pointOnSurfaceInfoNode + '.parameterU', 0.5)
	cmds.setAttr(pointOnSurfaceInfoNode + '.parameterV', 0.5)
	
	# CREATE AND CONNECT LOFT NODE #
	loftSurface = cmds.createNode('loft', name = 'loftSurfaceFromEdge1')
	cmds.connectAttr(curveFromMeshEdgeA + '.oc', loftSurface + '.ic[0]')
	cmds.connectAttr(curveFromMeshEdgeB + '.oc', loftSurface + '.ic[1]')
	cmds.connectAttr(loftSurface + '.os', pointOnSurfaceInfoNode + '.is')
	
	 # CREATE THE RIVET LOCATOR #
	rivetLoc = cmds.spaceLocator(name = 'rivet1')[0]
	
	# MATHS #
	vectorProduct = cmds.createNode('vectorProduct', name = 'vectorProduct_rivet1')
	cmds.connectAttr(pointOnSurfaceInfoNode + '.normal', vectorProduct + '.input1')
	cmds.connectAttr(pointOnSurfaceInfoNode + '.tangentU', vectorProduct + '.input2')
	cmds.setAttr(vectorProduct + '.operation', 2)
	
	fourByFourMatrix = cmds.createNode('fourByFourMatrix', name = 'fourByFourMatrix_rivet1')
	
	cmds.connectAttr(pointOnSurfaceInfoNode + '.normalX', fourByFourMatrix + '.in00')
	cmds.connectAttr(pointOnSurfaceInfoNode + '.normalY', fourByFourMatrix + '.in01')
	cmds.connectAttr(pointOnSurfaceInfoNode + '.normalZ', fourByFourMatrix + '.in02')
	
	cmds.connectAttr(pointOnSurfaceInfoNode + '.tangentUx', fourByFourMatrix + '.in10')
	cmds.connectAttr(pointOnSurfaceInfoNode + '.tangentUy', fourByFourMatrix + '.in11')
	cmds.connectAttr(pointOnSurfaceInfoNode + '.tangentUz', fourByFourMatrix + '.in12')
	
	cmds.connectAttr(vectorProduct + '.outputX', fourByFourMatrix + '.in20')
	cmds.connectAttr(vectorProduct + '.outputY', fourByFourMatrix + '.in21')
	cmds.connectAttr(vectorProduct + '.outputZ', fourByFourMatrix + '.in22')
	
	cmds.connectAttr(pointOnSurfaceInfoNode + '.positionX', fourByFourMatrix + '.in30')
	cmds.connectAttr(pointOnSurfaceInfoNode + '.positionY', fourByFourMatrix + '.in31')
	cmds.connectAttr(pointOnSurfaceInfoNode + '.positionZ', fourByFourMatrix + '.in32')
	
	multMatrix = cmds.createNode('multMatrix', name = 'multMatrix_rivet1')
	cmds.connectAttr(fourByFourMatrix + '.output', multMatrix + '.matrixIn[0]')
	cmds.connectAttr(rivetLoc + '.pim[0]', multMatrix + '.matrixIn[1]')
	
	decomposeMatrix = cmds.createNode('decomposeMatrix', name = 'decomposeMatrix_rivet1')
	cmds.connectAttr(multMatrix + '.matrixSum', decomposeMatrix + '.inputMatrix')
	
	cmds.connectAttr(decomposeMatrix + '.outputTranslateX', rivetLoc + '.translateX')
	cmds.connectAttr(decomposeMatrix + '.outputTranslateY', rivetLoc + '.translateY')
	cmds.connectAttr(decomposeMatrix + '.outputTranslateZ', rivetLoc + '.translateZ')
	
	cmds.connectAttr(decomposeMatrix + '.outputRotateX', rivetLoc + '.rotateX')
	cmds.connectAttr(decomposeMatrix + '.outputRotateY', rivetLoc + '.rotateY')
	cmds.connectAttr(decomposeMatrix + '.outputRotateZ', rivetLoc + '.rotateZ')
dkRivet()