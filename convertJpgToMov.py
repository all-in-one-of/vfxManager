import sys
import nuke

# if __name__ == '__main__':
argList=sys.argv[1].split(" ")
jpgSeq=argList[0]
outMov=argList[1]
projName=argList[4]
artist=argList[5]
task=argList[6]
ver=argList[7]
readNode=nuke.nodes.Read( file = jpgSeq, first=int(argList[2]), last=int(argList[3]) )
msg="Project: %s\nArtist: %s\nTask: %s\nVer: %s\nFrame: [frame] [%s-%s]"%(projName,artist,task,ver,argList[2],argList[3])
txtNode=nuke.nodes.Text2(message=msg, inputs=[readNode])
# print [curKnob.name() for curKnob in txtNode.allKnobs()]
txtNode["global_font_scale"].setValue(0.3)
txtNode["box"].setValue((0,0,800,150))
writeNode=nuke.nodes.Write(file=outMov, inputs=[txtNode])
nuke.execute(writeNode,int(argList[2]),int(argList[3]))