import pymel.core as pm
import os


class AiPBR:
    def __init__(self,*args):
        self.location=[]
        self.files=[]
        self.name=""
        self.makeGUI()
        
    def folderPicker(self,*args):
        
        self.location=pm.fileDialog2(fileMode=2)[0]

    def filePicker(self,*args):
        
        self.files=pm.fileDialog2(fileMode=4)
    
    def go(self,*args):
        
        self.name=pm.textField(self.matName,query=True,text=True)
        
        fileAlias={}
        fileAlias["baseColor"]=["baseColor","diffuse","color"]
        fileAlias["specularColor"]=["specular","specularColor"]
        fileAlias["specularRoughness"]=["roughness","glossiness"]
        fileAlias["opacity"]=["opacity","transparency"]
        fileAlias["metalness"]=["metallic","metal"]
        fileAlias["normalCamera"]=["normal","bump","height"]
        fileAlias["emissionColor"]=["emission"]
        fileAlias["transmission"]=["transmission","translucence"]


        texturePath={}
        texturePath["baseColor"]=[]
        texturePath["specularColor"]=[]
        texturePath["specularRoughness"]=[]
        texturePath["opacity"]=[]
        texturePath["metalness"]=[]
        texturePath["normalCamera"]=[]
        texturePath["emissionColor"]=[]
        texturePath["transmission"]=[]

        textureNode={}
        textureNode["baseColor"]=[]
        textureNode["specularColor"]=[]
        textureNode["specularRoughness"]=[]
        textureNode["opacity"]=[]
        textureNode["metalness"]=[]
        textureNode["normalCamera"]=[]
        textureNode["emissionColor"]=[]
        textureNode["transmission"]=[]

        shader=pm.shadingNode("aiStandardSurface",asShader=True,name=self.name+"_Mat")

    
        if self.location:
            for texture in os.listdir(self.location):
                for refName,keyword in fileAlias.items():
                    for alias in keyword:
                        if alias in texture:
                            if os.path.splitext(texture)[1] !=".tx":
                                texturePath[refName]=os.path.join(self.location,texture)

        placerName=NodeName+"_placer"
        placer=pm.shadingNode("place2dTexture",name=placerName+"place",asUtility=True)

        for key, value in texturePath.items():
            print(key,value)
            
            if value:
                textureName=NodeName+key
                texture=pm.shadingNode("file",name=textureName,isColorManaged=True,asTexture=True)
                pm.connectAttr(placer+".coverage",texture+".coverage",force=True)
                pm.connectAttr(placer+".translateFrame",texture+".translateFrame",force=True)
                pm.connectAttr(placer+".rotateFrame",texture+".rotateFrame",force=True)
                pm.connectAttr(placer+".mirrorU",texture+".mirrorU",force=True)
                pm.connectAttr(placer+".mirrorV",texture+".mirrorV",force=True)
                pm.connectAttr(placer+".stagger",texture+".stagger",force=True)
                pm.connectAttr(placer+".wrapU",texture+".wrapU",force=True)
                pm.connectAttr(placer+".wrapV",texture+".wrapV",force=True)
                pm.connectAttr(placer+".repeatUV",texture+".repeatUV",force=True)
                pm.connectAttr(placer+".rotateUV",texture+".rotateUV",force=True)
                pm.connectAttr(placer+".noiseUV",texture+".noiseUV",force=True)
                pm.connectAttr(placer+".vertexUvOne",texture+".vertexUvOne",force=True)
                pm.connectAttr(placer+".vertexUvTwo",texture+".vertexUvTwo",force=True)
                pm.connectAttr(placer+".vertexUvThree",texture+".vertexUvThree",force=True)
                pm.connectAttr(placer+".vertexCameraOne",texture+".vertexCameraOne",force=True)
                pm.connectAttr(placer+".outUV",texture+".uv",force=True)
                pm.connectAttr(placer+".outUvFilterSize",texture+".uvFilterSize",force=True)
                # print(type(texture))
                pm.setAttr(textureName+".fileTextureName",value)
                if "roughness" in key.lower() or "metalness" in key.lower() or "transmission" in key.lower():
                    rgb2Float=pm.shadingNode("aiRgbaToFloat",asUtility=True,name=textureName+"_float")
                    pm.setAttr(texture+".ignoreColorSpaceFileRules",1)
                    pm.setAttr(texture+".colorSpace","Raw")
                    pm.connectAttr(texture+".outColor",rgb2Float+".input",force=True)
                    textureNode[key]=rgb2Float
                    
                elif "normal" in key.lower():
                    bump=pm.shadingNode("bump2d",asUtility=True,name=textureName+"_normal")
                    pm.setAttr(textureName+"_normal.bumpInterp",1)
                    pm.setAttr(texture+".ignoreColorSpaceFileRules",1)
                    pm.setAttr(texture+".colorSpace","Raw")
                    pm.connectAttr(texture+".outAlpha",bump+".bumpValue")
                    textureNode[key]=bump
                    
                else:
                    textureNode[key]=texture
                

        for key,value in textureNode.items():
            print(key,value)
            if value:
                textureName=NodeName+key
                if "roughness" in key.lower() or "metalness" in key.lower() or "transmission" in key.lower():
                    
                    pm.connectAttr(value+".outValue",shader+"."+key,force=True)
                
                elif "normal" in key.lower():
                    pm.connectAttr(value+".outNormal",shader+"."+key,force=True)
            
                else:
                    pm.connectAttr(value+".outColor",shader+"."+key,force=True)
                    
    def makeGUI(self):
        self.win = pm.window(title="Standard Surface Builder",width=450,h=300,rtf=True,sizeable=0)
        layout = pm.columnLayout()

        self.matName=pm.textField(it="Material Name",w=450,h=50,fn='boldLabelFont',bgc=(.7,.7,.7))

        self.matName.setAnnotation(val="Material Name")
                
        pm.separator(h=10,w=450,st='doubleDash')

        self.folderBtn = pm.button(w=450,bgc=(0.0,0.7,0.1),h=60)
        self.folderBtn.setLabel("Choose Source Folder \n (keep textures one material per folder!)")
        self.folderBtn.setCommand(self.folderPicker)
        
        # self.fileBtn = pm.button(w=450,bgc=(0.0,0.7,0.1),h=60)
        # self.fileBtn.setLabel("Choose Source File")
        # self.fileBtn.setCommand(self.filePicker)

        self.goBtn = pm.button(w=450,bgc=(0.0,0.7,0.6),h=60)
        self.goBtn.setLabel("Create Ai Standard Surface")
        self.goBtn.setCommand(self.go)
       
        pm.showWindow()  


if __name__== "__main__":
    AiPBR()
