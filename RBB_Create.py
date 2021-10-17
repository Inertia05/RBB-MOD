# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 18:29:34 2021

@author: Administrator
"""
import pandas
import RBB

df = pandas.read_excel("RBB.xlsx", "精度表", header = 1)

静止精度 = df["静止精度"]
移动精度 = df["移动精度"]

##space 0.05
#space   0.1  0.1
#space  0.15 0.15 0.15
#...
#space  0.95 0.95 .... 0.95 (19x 0.95)

def GeneralCreatePatch(table, patchName):
    out = ("""
    <ndfcreate ndf="pc\\ndf\patchable\gfx\everything.ndfbin" table=\""""
        +table+"""\" name=\""""+patchName+"""\" />
    """)

    RBB.xmlOutput += out


totalEntriesCount = 0
catIndexSeps = []

for i in range(19):
    catIndexSeps.append(totalEntriesCount)
    totalEntriesCount+=(2+i)
   
def createHitRollCommands(initialFileName):
    fileNameList = "WGPatcher apply "+initialFileName+".dat "
    initialFileName = initialFileName.lower()
    RBB.xmlOutput += """<wargamepatch>"""    
    generatedCount = 0
    fileIndex = 0
    for i in range(19):
        oneBasedIndex = i+1
        
        start = catIndexSeps[i]+1
        for j in range(oneBasedIndex):
            staAcc = 静止精度[start+j]
            realSta = round(oneBasedIndex*0.05,2)
            movAcc = 移动精度[start+j]
            realMov = round((j+1)*0.05,2)
            
            patchName = str(staAcc)+" "+str(movAcc)+" /"+str(realSta)+" "+str(realMov)
    
            
            table = "TModernWarfareHitRollRule"
            if (pandas.isna(staAcc) or pandas.isna(movAcc)):
                print(patchName)
                GeneralCreatePatch(table, patchName)
                RBB.GeneralPatch(table, patchName, 
                                 conditions = RBB.GeneralConditions(__order = "last"), 
                                 changes = RBB.GeneralChanges(MinimalHitProbability     = ["Float32",0.05],
                                                              MinimalCritProbability    = ["Float32",0.01],
                                                              HitProbability            = ["Float32",realSta],
                                                              HitProbabilityWhileMoving = ["Float32",realMov]))
                #RBB.GeneralPatch(table, "Check existance of "+patchName, 
                 #                conditions = RBB.GeneralConditions(HitProbability            = realSta,
                  #                                                  HitProbabilityWhileMoving = realMov), 
                   #              changes = "")
                generatedCount += 1
                if generatedCount == 5:
                    RBB.xmlOutput += """\n\n</wargamepatch>"""
                    
                    RBB.XMLPatch("RBB-Create-"+str(fileIndex))
                    

                    fileNameList += "RBB-Create-"+str(fileIndex)+".xml \n"
                    fileIndex+=1
                    
                    generatedCount = 0
                    
                    initialFileName += "_patched"
                    fileNameList += "rename "+initialFileName+".dat "
            
                    if not ((i == 18) and (j == oneBasedIndex-1)):
                        initialFileName = "RBB-Create-"+str(fileIndex)
                        fileNameList += initialFileName+".dat\n\n"   
                        
                        fileNameList += "WGPatcher apply "+initialFileName+".dat "
                        RBB.xmlOutput += """<wargamepatch>"""       

                    else:
                        initialFileName = "RBB-Create-Final"
                        fileNameList += initialFileName+".dat\n\n"   
                        
                elif ((i == 18) and (j == oneBasedIndex-1)):
                    RBB.xmlOutput += """\n\n</wargamepatch>"""
                    
                    RBB.XMLPatch("RBB-Create-"+str(fileIndex))
                 
                    fileNameList += "RBB-Create-"+str(fileIndex)+".xml \n"
                    fileIndex+=1   
                    
                    initialFileName += "_patched"
                    fileNameList += "rename "+initialFileName+".dat "
                    initialFileName = "RBB-Create-Final"
                    fileNameList += initialFileName+".dat\n\n"      
                    
                
    RBB.checkXmlOutputIsEmpty()
    return (fileNameList)
#for i in range(totalEntriesCount):
