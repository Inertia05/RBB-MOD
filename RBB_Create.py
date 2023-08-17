# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 18:29:34 2021

@author: Administrator
"""
import pandas
import RBB
import RBB_General_Excel_Patch as GEP

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
    
def createTAmmuCommands(initialFileName, sheet, xlsx = "RBB.xlsx"):
    RBB.checkXmlOutputIsEmpty()
    fileNameList = "WGPatcher apply "+initialFileName+".dat "
    initialFileName = initialFileName.lower()
    RBB.xmlOutput += """<wargamepatch>"""    
    generatedCount = 0
    fileIndex = 0
    df = pandas.read_excel(xlsx, sheet, header = 1)
    firstTime = []


    for i in range(df["新建"].size):
        新建 = df["新建"][i]
        end = False
        if not pandas.isna(新建):
            #####################################################################
            directKeys = ["武器管理器名","武器管理器SalvoIndex","武器管理器SalvoCount"]       
            directValues = GEP.checkValues(df, i, directKeys)
            武器管理器名 = directValues["武器管理器名"]
            武器管理器SalvoIndex = directValues["武器管理器SalvoIndex"]
            武器管理器SalvoCount = directValues["武器管理器SalvoCount"]
            if 武器管理器名 and (武器管理器SalvoIndex != None) and 武器管理器SalvoCount:
                RBB.GeneralPatch(table = "TWeaponManagerModuleDescriptor", 
                                 patchName = 武器管理器名+" Weapon Manager", 
                                 conditions = RBB.GeneralConditions(_ShortDatabaseName = "WeaponDescriptor_Unit_"+武器管理器名), 
                                 changes = RBB.GeneralChangeDict(prop = "Salves", 
                                                                 key = int(武器管理器SalvoIndex), 
                                                                 typeValuePair = [RBB.VariableTypeInt,int(武器管理器SalvoCount)]))
            ######################################################################
            directKeys = ["炮塔所属武器Hash值","武器Hash值","新武器Hash值",
                          "炮塔所属武器名","武器名","炮塔类型",
                          "炮塔所属武器SalvoIndex",
                          "静止精度(%)", "移动精度(%)"]
            directValues = {}
            #默认或nan时， 值均为None 
            HashDoesNotMatter = False
            for key in directKeys:
                directValues[key] = None
                if key in df.keys():
                    value = df[key][i]
                    if not pandas.isna(value):
                        if ("(%)" in key):
                            directValues[key] = value/100
                        elif ("(m)" in key):
                            if (value %175) != 0:
                                raise ValueError("vanilla range is not multiple of 175 at line "+str(i+3)+" in the sheet used")
                            directValues[key] = int(RBB.Range(value))
                        elif key in ["炮塔所属武器SalvoIndex"]:
                                if value == "空值":
                                    directValues[key] = "null"
                                else:
                                    RBB.checkNumber(value)
                                    directValues[key] = value
                        else:
                            if ("Hash" in key):
                                if value == "HashDoesNotMatter":
                                    HashDoesNotMatter = True
                                else:
                                    RBB.checkHashValue(value)
                            elif key in ["炮塔所属武器名","武器名","炮塔类型"]:
                                pass
                            else:
                                RBB.checkNumber(value)
                            directValues[key] = value
            
            
            patchName = str(df["武器名"][i]) + "(weapon), weapon hash = " +str(df["新武器Hash值"][i])
            repeatedCombo = False
            if patchName in firstTime:
                repeatedCombo = True
            else:
                firstTime.append(patchName)
            
            hashOnly = False            
            if "武器Hash值即唯一条件" in df.keys():
                if df["武器Hash值即唯一条件"][i] == "Y":
                    hashOnly = True
                    
            
                    
            if "武器" in df["新建"][i]:
                GeneralCreatePatch("TAmmunition","Create TAmmu instance: "+patchName)
                tAmmuConditions = RBB.GeneralConditions(__order = "last")
                generatedCount += 1
            else:
                tAmmuConditions = (GEP.WriteTAmmuConditionsFromDF(df, i, hashOnly, newestWeaponHashConditionOnly = False))
                   
             
            tAmmuChanges    = GEP.WriteTAmmuChangesFromDF(df, i)
            

            if ("修改现有" in df["新建"][i]) or (("武器" in df["新建"][i])):
                RBB.TAmmuPatch(patchName,
                               tAmmuConditions,
                               tAmmuChanges)
            
            fileNameList, initialFileName, fileIndex, generatedCount = createPatchCountCheck(fileNameList, 
                                                                                             initialFileName, 
                                                                                             fileIndex, 
                                                                                             "RBB-CreateTAmmu-", 
                                                                                             generatedCount, 
                                                                                             end)
            if ("MountedWD" in df["新建"][i]):
                GeneralCreatePatch("TMountedWeaponDescriptor","Create TMountedWeaponD instance")
                tMountedConditions = RBB.GeneralConditions(__order = "last")
                generatedCount += 1
                RBB.GeneralPatch("TMountedWeaponDescriptor",
                                  "Change TMountedWeaponD for TAmmu instance: "+patchName,
                           conditions = tMountedConditions,
                           changes = (GEP.WriteTMountedChangesFromDF(df, i))
                                      +RBB.GeneralChangesObject(prop = "Ammunition", 
                                                                table = "TAmmunition", 
                                                                tableConditions = RBB.addTabsBetweenLines(tAmmuConditions,1)))
                
                prop = "MountedWeaponDescriptorList"
                
                changes=RBB.GeneralChangeDictValueObjectAppend(prop, table = "TMountedWeaponDescriptor", 
                                                       tableConditions=tMountedConditions)
                if ("添加至现有炮塔" in df["新建"][i]):
                    if directValues["炮塔所属武器Hash值"]:
                        炮塔类型 = directValues["炮塔类型"]
                        if 炮塔类型:
                            conditions = RBB.GeneralConditionReference(table = "TMountedWeaponDescriptor", 
                       tableConditions = RBB.GeneralConditionReference(table = "TAmmunition", 
                       tableConditions = RBB.GeneralConditions(Name = directValues["炮塔所属武器Hash值"])))
                            if 炮塔类型 =="双轴":
                                RBB.GeneralPatch(table=RBB.TurretTypeAxis, patchName="Change Turret for TMounted for TAmmu instance: "+patchName, 
                                         conditions=conditions, changes = changes)
                            else:
                                raise ValueError("炮塔类型 not specfied")
                        else:
                            raise ValueError("炮塔类型 not specfied")
                    else:
                        raise ValueError("现有炮塔 not specfied")
                elif ("添加至现有特定炮塔" in df["新建"][i]):
                    if directValues["炮塔所属武器Hash值"]:
                        炮塔类型 = directValues["炮塔类型"]
                        if 炮塔类型:
                            extraTMountedConditions = RBB.GeneralConditions(SalvoStockIndex = directValues["炮塔所属武器SalvoIndex"])
                            conditions = RBB.GeneralConditionReference(table = "TMountedWeaponDescriptor", 
                       tableConditions = extraTMountedConditions+
                                         RBB.GeneralConditionReference(table = "TAmmunition", 
                       tableConditions = RBB.GeneralConditions(Name = directValues["炮塔所属武器Hash值"])))
                            if 炮塔类型 =="双轴":
                                RBB.GeneralPatch(table=RBB.TurretTypeAxis, patchName="Add TMounted for TAmmu instance: "+patchName+" to existing turret", 
                                         conditions=conditions, changes = changes)
                            else:
                                raise ValueError("炮塔类型 not specfied")
                        else:
                            raise ValueError("炮塔类型 not specfied")
                    else:
                        raise ValueError("现有炮塔 not specfied")
                    
                

                
                fileNameList, initialFileName, fileIndex, generatedCount = createPatchCountCheck(fileNameList, 
                                                                                                 initialFileName, 
                                                                                                 fileIndex, 
                                                                                                 "RBB-CreateTAmmu-", 
                                                                                                 generatedCount, 
                                                                                                 end)
                
                
            if "精度" in df["新建"][i]:
                GeneralCreatePatch("TModernWarfareHitRollRule","Create HitRoll instance")
                generatedCount += 1
                
                realSta = directValues["静止精度(%)"]
                realMov = directValues["移动精度(%)"]
                RBB.GeneralPatch(table = "TModernWarfareHitRollRule", 
                                 patchName = "Set acc for created instance", 
                                 conditions = RBB.GeneralConditions(__order = "last"), 
                                 changes = RBB.GeneralChanges(MinimalHitProbability     = ["Float32",0.05],
                                                              MinimalCritProbability    = ["Float32",0.01],
                                                              HitProbability            = ["Float32",realSta],
                                                              HitProbabilityWhileMoving = ["Float32",realMov]))
            
                fileNameList, initialFileName, fileIndex, generatedCount = createPatchCountCheck(fileNameList, 
                                                                                                 initialFileName, 
                                                                                                 fileIndex, 
                                                                                                 "RBB-CreateTAmmu-", 
                                                                                                 generatedCount, 
                                                                                                 end)
    end = (i == df["新建"].size-1)       
    fileNameList, initialFileName, fileIndex, generatedCount = createPatchCountCheck(fileNameList, 
                                                                                    initialFileName, 
                                                                                    fileIndex, 
                                                                                    "RBB-CreateTAmmu-", 
                                                                                    generatedCount, 
                                                                                    end)        
        
        
        
    RBB.checkXmlOutputIsEmpty()
    return (fileNameList)

    
def createPatchCountCheck(fileNameList, initialFileName, fileIndex, fileName, generatedCount, end):
    if generatedCount == 5:
        RBB.xmlOutput += """\n\n</wargamepatch>"""
        
        RBB.XMLPatch(fileName+str(fileIndex))
        

        fileNameList += fileName+str(fileIndex)+".xml \n"
        fileIndex+=1
        
        generatedCount = 0
        
        initialFileName += "_patched"
        fileNameList += "rename "+initialFileName+".dat "

        if not (end):
            initialFileName = fileName+str(fileIndex)
            fileNameList += initialFileName+".dat\n\n"   
            
            fileNameList += "WGPatcher apply "+initialFileName+".dat "
            RBB.xmlOutput += """<wargamepatch>"""       
            
        else:
            initialFileName = fileName+"Final"
            fileNameList += initialFileName+".dat\n\n"   
            
    elif (end):
        RBB.xmlOutput += """\n\n</wargamepatch>"""
        
        RBB.XMLPatch(fileName+str(fileIndex))
     
        fileNameList += fileName+str(fileIndex)+".xml \n"
        fileIndex+=1   
        
        initialFileName += "_patched"
        fileNameList += "rename "+initialFileName+".dat "
        initialFileName = fileName+"Final"
        fileNameList += initialFileName+".dat\n\n"   
        
    return fileNameList, initialFileName, fileIndex, generatedCount

#压制伤害效果只有2套
#TSuppressDamagesEffects，一套4个是步兵的，一套4个是载具的
#物理伤害效果只有1套
#TPhysicalDamagesEffects, 全体通用
#士气测试有8套,但99%的单位用1套
#TModernWarfareTestMoralRollRule
#def createArmorCommands()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
