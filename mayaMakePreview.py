# coding=utf-8
import re,os
import maya.cmds as cmds
import maya.mel as mel
from btpPySide import *
from btpDebugInfo import *

def removeMayaWindow(window):
    try:
        cmds.deleteUI(window, window=1)
        cmds.windowPref(window, remove=1)
    except:
        cmds.windowPref(window, exists=0)
        
# Make Preview
def makePreview(    file, 
                    camera,
                    useDefaultMaterial, 
                    percent, 
                    quality,
                    startFrame, 
                    endFrame, 
                    widthHeight, 
                    showOrnaments=1 ):
    #
    width, height = widthHeight
    #
    widthReduce = width
    heightReduce = height
    # Reduce Width and Height
    checkValue = max(widthHeight)
    if checkValue > 2048:
        if width > height:
            widthReduce = 2048
            heightReduce = 2048 * height / width
        if width < height:
            widthReduce = 2048 * width / height
            heightReduce = 2048
    widthHeightReduce = widthReduce, heightReduce
    #
    filePath = os.path.dirname(file)
    fileName = os.path.basename(file)
    #
    isMov = os.path.splitext(fileName)[-1] == '.mov'
    format = [os.path.splitext(fileName)[-1][1:], u'qt'][isMov]
    compression = [u'IYUV 编码解码器', u'H.264'][isMov]
    #
    prvName = os.path.splitext(file)[0]
    #
    prvWindow = "previewWindowName"
    removeMayaWindow(prvWindow)
    cmds.window(prvWindow, title='Animation Preview')
    paneLayout = cmds.paneLayout(width=widthReduce/2, height=heightReduce/2)
    animationView = cmds.modelPanel(label=prvWindow,
                                    parent=paneLayout,
                                    menuBarVisible=0,
                                    modelEditor=0,
                                    camera=camera)
    cmds.displayRGBColor('background', .25, .25, .25)
    cmds.displayRGBColor('backgroundTop', .25, .25, .25)
    cmds.displayRGBColor('backgroundBottom', .25, .25, .25)
    cmds.showWindow(prvWindow)

    # Set Maye View
    cmds.modelEditor(   animationView,
                        edit=1,
                        activeView=1,
                        useDefaultMaterial=useDefaultMaterial,
                        wireframeOnShaded=0,
                        fogging=0,
                        dl='default',
                        twoSidedLighting=0,
                        allObjects=0,
                        manipulators=0,
                        grid=0,
                        hud=1,
                        sel=0)
    cmds.modelEditor(   animationView,
                        edit=1,
                        activeView=1,
                        polymeshes=1,
                        subdivSurfaces=1,
                        fluids=1,
                        strokes=1,
                        nCloths=1,
                        nParticles=1,
                        pluginShapes=1,
                        pluginObjects=['gpuCacheDisplayFilter', 1],
                        displayAppearance='smoothShaded')
                    # Video Preview
    cmds.playblast( startTime=startFrame,
                    endTime=endFrame,
                    format=format,
                    filename=prvName,
                    clearCache=1,
                    viewer=0,
                    showOrnaments=showOrnaments,
                    offScreen=1,
                    framePadding=4,
                    percent=percent,
                    compression=compression,
                    quality=quality,
                    widthHeight=widthHeightReduce)
    # # Image Preview
    # midFrame = int((endFrame - startFrame) / 2 + startFrame)
    # frameRange = [startFrame, midFrame, endFrame]
    # frameDic = {startFrame: '0000', midFrame: '0001', endFrame: '0002'}
    # for frame in frameRange:
    #     cmds.playblast( startTime=frame,
    #                     endTime=frame,
    #                     format='iff',
    #                     filename=prvName,
    #                     sequenceTime=0,
    #                     clearCache=1,
    #                     viewer=0,
    #                     showOrnaments=0,
    #                     offScreen=0,
    #                     framePadding=4,
    #                     percent=percent,
    #                     compression='jpg',
    #                     quality=quality)
    #     previewFile = prvName + '_' + frameDic[frame] + '.jpg'
    #     if os.path.exists(previewFile):
    #         os.remove(previewFile)
    #     os.rename(prvName + '.' + str(frame).zfill(4) + '.jpg', previewFile)
    # Remove Widow
    removeMayaWindow(prvWindow)
