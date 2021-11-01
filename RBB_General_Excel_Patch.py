# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 00:06:10 2021

@author: Administrator
"""
import RBB
import pandas
import numpy as np
import subprocess
import os

def checkValues(df, i, directKeys):
    directValues = {}
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
                else:
                    if ("Hash" in key):
                        RBB.checkHashValue(value)
                    elif key in ["原版武器类型", "原版武器子类型", "武器管理器名"]:
                        pass
                    else:
                        RBB.checkNumber(value)
                    directValues[key] = value
    return directValues




def WriteTAmmuPatchFromTable(sheet, typeArme = None, xlsx = "RBB.xlsx", newestWeaponHashConditionOnly = False):
    df = pandas.read_excel(xlsx, sheet, header = 1)
    firstTime = []
    #有武器Hash即默认改变武器性质

        
    for i in range(df["武器名"].size):
        武器Hash值 = df["武器Hash值"][i]
        if not pandas.isna(武器Hash值):
            patchName = df["武器名"][i] + "(weapon), weapon hash = " +str(武器Hash值)
            repeatedCombo = False
            if patchName in firstTime:
                repeatedCombo = True
            else:
                firstTime.append(patchName)
            
            hashOnly = False            
            if "武器Hash值即唯一条件" in df.keys():
                if df["武器Hash值即唯一条件"][i] == "Y":
                    hashOnly = True
 
            
            tAmmuConditions = (WriteTAmmuConditionsFromDF(df, i, hashOnly, newestWeaponHashConditionOnly)+
                              (RBB.TAmmuConditions(TypeArme = typeArme) if typeArme else ""))
            
            tAmmuChanges    = WriteTAmmuChangesFromDF(df, i)
            
            #if newestWeaponHashConditionOnly:
            if "UI格子优先级" in df.keys():
                UI格子优先级 = df["UI格子优先级"][i]
                if not pandas.isna(UI格子优先级):
                    RBB.intCheck(UI格子优先级 = UI格子优先级)
                    RBB.TMountedWeaponPatchChangeUISlotIndex(patchName, 
                                                             tableConditions = tAmmuConditions, 
                                                             UIIndex = UI格子优先级)

            RBB.TAmmuPatch(patchName,
                           tAmmuConditions,
                           tAmmuChanges)
            if repeatedCombo:
                if "武器Hash值即唯一条件" in df.keys():
                    if df["武器Hash值即唯一条件"][i] == "Y":
                        print("Warning: repeated Weapon Name/Weapon Hash combo at line "+str(i+3)+" in sheet = "+sheet)
            

            if "稳定器改动" in df.keys():
                稳定器改动 = df["稳定器改动"][i]
                if not pandas.isna(稳定器改动):
                    RBB.TMountedWeaponPatchChangeStablizer(patchName, 
                                                           tableConditions = tAmmuConditions, 
                                                           stabChange = 稳定器改动)
                    
            directKeys = ["武器管理器名","武器管理器SalvoIndex","武器管理器SalvoCount"]       
            directValues = checkValues(df, i, directKeys)
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
                
                
def WriteTAmmuConditionsFromDF(df, i, hashOnly = True, newestWeaponHashConditionOnly = False):
    tAmmuConditions = ""

    directKeys = ["原版对地射程(m)", "最小原版对地射程(m)",  
                  "原版对直升机射程(m)",     "原版对空射程(m)",        "原版反舰射程(m)",     "原版反导射程(m)",
                  "最小原版对直升机射程(m)", "最小原版对空射程(m)",     "最小原版反舰射程(m)", "最小原版反导射程(m)",
                  "武器Hash值",  "原版静止精度(%)", "原版移动精度(%)","原版HEAT", "原版KE", "新武器Hash值",
                  "原版连发数", "原版面板连发数", "原版齐射数", "原版短装填", "原版短装填Fx", "原版长装填","原版瞄准时间",
                  "原版初速度",
                  "原版武器类型","原版武器子类型", "原版口径"]
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
                else:
                    if ("Hash" in key):
                        if value == "HashDoesNotMatter":
                            HashDoesNotMatter = True
                        else:
                            RBB.checkHashValue(value)
                    elif key in ["原版武器类型", "原版武器子类型", "原版口径"]:
                        pass
                    else:
                        RBB.checkNumber(value)
                    directValues[key] = value
                    
    if newestWeaponHashConditionOnly:
        if directValues["新武器Hash值"]:
            tAmmuConditions += RBB.TAmmuConditions(Name = directValues["新武器Hash值"]) 
            return tAmmuConditions
        elif directValues["武器Hash值"]:
            if not HashDoesNotMatter:
                tAmmuConditions += RBB.TAmmuConditions(Name = directValues["武器Hash值"])
            return tAmmuConditions
        else:
            raise ValueError("Line "+str(i)+" has no hash available for newest hash only condition")
            
    if directValues["武器Hash值"]:#always true because WriteTAmmuPatchFromTable has checked it before calling the function
        if not HashDoesNotMatter:    
            tAmmuConditions += RBB.TAmmuConditions(Name = directValues["武器Hash值"])
    if hashOnly:
        return tAmmuConditions
    
    shipOnly = False
    ground = [directValues["最小原版对地射程(m)"],     directValues["原版对地射程(m)"]]
    if (directValues["原版反舰射程(m)"] != None) or (directValues["最小原版反舰射程(m)"]!= None):       
        if (directValues["原版对地射程(m)"] != None) or (directValues["最小原版对地射程(m)"]!= None):
            raise ValueError("原版反舰射程和原版对地射程同时存在(反舰射程存在时默认该武器只能反舰)")
        shipOnly = True
        ground = [directValues["最小原版反舰射程(m)"],     directValues["原版反舰射程(m)"]]
        
    tAmmuConditions += RBB.TAmmuConditionsRange(shipOnly=shipOnly, ground = ground,
                             helo   = [directValues["最小原版对直升机射程(m)"],     directValues["原版对直升机射程(m)"]],
                             air    = [directValues["最小原版对空射程(m)"],         directValues["原版对空射程(m)"]],
                             projec = [directValues["最小原版反导射程(m)"],         directValues["原版反导射程(m)"]])
    
    tAmmuConditions += RBB.TAmmuConditionsROF(shotReload = directValues["原版短装填"], 
                       shotFxReload  = directValues["原版短装填Fx"], salvoReload = directValues["原版长装填"], 
                       salvoUILength = directValues["原版面板连发数"], salvoLength = directValues["原版连发数"], 
                       shotSimutane = directValues["原版齐射数"], aim = directValues["原版瞄准时间"])
    
    if directValues["原版HEAT"]:
        tAmmuConditions += RBB.TAmmuConditionsArme("HEAT", directValues["原版HEAT"])
        if directValues["原版KE"]:
            raise ValueError("原版KE和原版HEAT不能同时存在")
    elif directValues["原版KE"]:
        tAmmuConditions += RBB.TAmmuConditionsArme("KE", directValues["原版KE"])
        
    if directValues["原版初速度"]:
        tAmmuConditions += RBB.TAmmuConditions(FX_vitesse_de_depart = RBB.convertNumberForCondition(directValues["原版初速度"]))
      
    if directValues["原版口径"]:
        tAmmuConditions += RBB.TAmmuConditions(Caliber = RBB.TAmmuCaliber[directValues["原版口径"]])
        
    if directValues["原版武器类型"]:
        原版武器类型 = directValues["原版武器类型"]
        if "燃烧弹" in 原版武器类型:
            tAmmuConditions += RBB.TAmmuConditions(IgnoreInflammabilityConditions = True)
        elif "子母弹" in 原版武器类型:
            tAmmuConditions += RBB.TAmmuConditions(IsSubAmmunition = True)
        elif "动能弹" in 原版武器类型:
            tAmmuConditions += RBB.TAmmuConditions(EfficaciteSelonPortee = True)
        elif "重机枪" in 原版武器类型:
            tAmmuConditions += RBB.TAmmuConditions(Arme = 1)
        elif "SAM" in 原版武器类型:
            tAmmuConditions += RBB.TAmmuConditions(TypeArme = RBB.SAMTypeArme)
            
    if directValues["原版武器子类型"]:
        原版武器子类型 = directValues["原版武器子类型"]
        if "纯烟雾弹" in 原版武器子类型:
            tAmmuConditions += RBB.TAmmuConditions(Arme = 3,
                                                   PhysicalDamages = "null",
                                                   IgnoreInflammabilityConditions = "null")
            #IgnoreInflam is for NPLM bomb only, which fit the first 2 conditions but not IgnoreInfla
        elif "纯高爆弹" in 原版武器子类型:
            tAmmuConditions += RBB.TAmmuConditions(Arme = 3,
                                                   SmokeDescriptor = "null",
                                                   IsSubAmmunition = "null",
                                                   IgnoreInflammabilityConditions = "null")
        elif "雷达" in 原版武器子类型:
            tAmmuConditions += RBB.TAmmuConditions(Guidance = 1)
        elif "光电" in 原版武器子类型:
            tAmmuConditions += RBB.TAmmuConditions(Guidance = "null")

    
    if directValues["原版静止精度(%)"]:
        tAmmuConditions += RBB.TAmmuConditions(acc = [directValues["原版静止精度(%)"],directValues["原版移动精度(%)"]])

    
    return tAmmuConditions





def WriteTAmmuChangesFromDF(df, i):
    tAmmuChanges = ""

    directKeys = ["新武器Hash值", "HE", "HE半径", "压制", "压制半径","HEAT", "KE", "静止精度(%)", "移动精度(%)", 
                  "连发数", "面板连发数", "齐射数", "短装填", "短装填Fx", "长装填", "瞄准时间",
                  "最小散布", "最大散布", "修正系数",
                  "弹链补给量", "初速度", "散布角",
                  "对空射程(km)", "对直升机射程(km)", "对地射程(km)", "反舰射程(km)", "反导射程(km)", 
                  "最小对空射程(km)", "最小对直升机射程(km)",	"最小对地射程(km)", "最小反舰射程(km)", "最小反导射程(km)",
                  "火", "口径", "武器类型", "TypeArme"
                  #武器类型可选关键词： 
                  #     射后不理， 手动曲射， 自动曲射， 手动直射，自动直射， 步兵， 飞机， 
                  #     高爆，重机枪，枪
                  #武器类型完全匹配词：SEAD, AGM
                  ]
    directValues = {}
    for key in directKeys:
        directValues[key] = None
        if key in df.keys():
            value = df[key][i]
            if not pandas.isna(value):

                if (key == "HE半径") or (key == "压制半径"):
                    directValues[key] = round(value)*52
                elif ("(%)" in key):
                    directValues[key] = value/100
                elif ("(km)" in key):
                    directValues[key] = RBB.Range(RBB.GameDistanceFor(value))
                elif key in ["最小散布", "最大散布"]:
                    directValues[key] = value/18.2*52#game ui dispersion is auto rounded to int
                else:
                    if ("Hash" in key):
                        RBB.checkHashValue(value)
                    elif key in ["火", "口径", "武器类型","TypeArme"]:
                        pass
                    else:
                        RBB.checkNumber(value)
                    directValues[key] = value
    
    shipOnly = False
    ground = [directValues["最小对地射程(km)"],     directValues["对地射程(km)"]]
    if (directValues["反舰射程(km)"] != None) or (directValues["最小反舰射程(km)"]!= None):
        if ((directValues["对地射程(km)"] != None) or (directValues["最小对地射程(km)"]!= None)):
            raise ValueError("反舰射程和对地射程同时存在(反舰射程存在时默认该武器只能反舰)")
        shipOnly=True
        ground = [directValues["最小反舰射程(km)"],     directValues["反舰射程(km)"]]
    #https://www.zhihu.com/question/22770770    De Morgan's laws
    tAmmuChanges += RBB.TAmmuChangesRange(shipOnly=shipOnly, ground = ground,
                                          helo   = [directValues["最小对直升机射程(km)"], directValues["对直升机射程(km)"]],
                                          air    = [directValues["最小对空射程(km)"],     directValues["对空射程(km)"]],
                                          projec = [directValues["最小反导射程(km)"],     directValues["反导射程(km)"]])
    
    tAmmuChanges += RBB.TAmmuChangesROF(directValues["短装填"], directValues["短装填Fx"], directValues["长装填"],
                                        directValues["面板连发数"], directValues["连发数"],
                                        directValues["齐射数"], directValues["瞄准时间"])
    
    tAmmuChanges += RBB.TAmmuChangesDisp(disp = [directValues["最小散布"], directValues["最大散布"]], 
                                         corr = directValues["修正系数"])
    
    tAmmuChanges += RBB.TAmmuChangesFire(fireSize = directValues["火"], fireChance = 1)
    
    ammoTypeSet = False
    if "武器类型" in df.keys():
       武器类型 = df["武器类型"][i]
       if not pandas.isna(武器类型):   
           if 武器类型 in ["SEAD", "AGM"]:
               tAmmuChanges += RBB.TAmmuChangesArme("HE")+RBB.TAmmuChanges(TirIndirect = ["Boolean", True])
           elif "非射后不理" in 武器类型:
               tAmmuChanges += RBB.TAmmuChanges(IsFireAndForget = None)
           elif "射后不理" in 武器类型:
               tAmmuChanges += RBB.TAmmuChanges(IsFireAndForget = ["Boolean", True])
           if "手动曲射" in 武器类型:
               tAmmuChanges += RBB.TAmmuChanges(TirIndirect = [RBB.VariableTypeBool, True])
               tAmmuChanges += RBB.TAmmuChanges(TirReflexe  = [RBB.VariableTypeBool, False])
               tAmmuChanges += RBB.TAmmuChanges(ProjectileType  = [RBB.VariableTypeUInt, 1])
           elif "自动曲射" in 武器类型:
               tAmmuChanges += RBB.TAmmuChanges(TirIndirect = [RBB.VariableTypeBool, True])
               tAmmuChanges += RBB.TAmmuChanges(TirReflexe  = [RBB.VariableTypeBool, True])
               if (not "步兵" in 武器类型) and (not "飞机" in 武器类型):
                   tAmmuChanges += RBB.TAmmuChanges(ProjectileType  = [RBB.VariableTypeUInt, 2])
           elif "自动直射" in 武器类型:
               tAmmuChanges += RBB.TAmmuChanges(TirIndirect = [RBB.VariableTypeBool, False])
               tAmmuChanges += RBB.TAmmuChanges(TirReflexe  = [RBB.VariableTypeBool, True])
           elif "手动直射" in 武器类型:
               tAmmuChanges += RBB.TAmmuChanges(TirIndirect = [RBB.VariableTypeBool, False])
               tAmmuChanges += RBB.TAmmuChanges(TirReflexe  = [RBB.VariableTypeBool, False])          
           else:
               pass  
           
           if "非子母弹" in 武器类型:
               tAmmuChanges += RBB.TAmmuChanges(IsSubAmmunition = None)
           elif "子母弹" in 武器类型:
               tAmmuChanges += RBB.TAmmuChanges(IsSubAmmunition = [RBB.VariableTypeBool, True])
            

           if "高爆" in 武器类型:
               tAmmuChanges += RBB.TAmmuChangesArme(ammoType = "HE")
               ammoTypeSet = True
           elif "重机枪" in 武器类型:
               tAmmuChanges += RBB.TAmmuChangesArme(ammoType = "HMG")   
               ammoTypeSet = True
           elif "枪" in 武器类型:
               tAmmuChanges += RBB.TAmmuChangesArme(ammoType = "Bullet")    
               ammoTypeSet = True
               

               
    if directValues["HEAT"]:
        if ammoTypeSet:
            raise ValueError("Ambiguous ammo type at line "+str(i+3)+" in sheet")
        tAmmuChanges += RBB.TAmmuChangesArme("HEAT", directValues["HEAT"])
    elif directValues["KE"]:
        if ammoTypeSet:
            raise ValueError("Ambiguous ammo type at line "+str(i+3)+" in sheet")
        tAmmuChanges += RBB.TAmmuChangesArme("KE", directValues["KE"])
        
    if directValues["口径"]:
        tAmmuChanges += RBB.TAmmuChanges(Caliber = [RBB.VariableTypeHash, RBB.TAmmuCaliber[directValues["口径"]]])
        
    if directValues["静止精度(%)"]:
        tAmmuChanges += RBB.TAmmuChanges(acc = [directValues["静止精度(%)"],directValues["移动精度(%)"]])
        
    if directValues["新武器Hash值"]:
        tAmmuChanges += RBB.TAmmuChanges(Name = ["LocalisationHash", directValues["新武器Hash值"]])
        
    if directValues["TypeArme"]:
        tAmmuChanges += RBB.TAmmuChanges(Name = [RBB.VariableTypeHash, RBB.TAmmuTypeArme[directValues["TypeArme"]]])
        
    if directValues["初速度"]:
        tAmmuChanges += RBB.TAmmuChanges(FX_vitesse_de_depart = [RBB.VariableTypeFloat, directValues["初速度"]])
        
    if directValues["散布角"]:
        tAmmuChanges += RBB.TAmmuChanges(AngleDispersion = [RBB.VariableTypeFloat, directValues["散布角"]])

    
    if directValues["弹链补给量"]:
        tAmmuChanges += RBB.TAmmuChanges(SupplyCost = [RBB.VariableTypeUInt, int(directValues["弹链补给量"])])
           
    tAmmuChanges += RBB.TAmmuChangesAOE(HE = [directValues["HE"], directValues["HE半径"]], Sup = [directValues["压制"], directValues["压制半径"]])
    return tAmmuChanges


#######################################################################################
#######################################################################################

def WriteUnitConditionsFromDF(df, i, hashOnly):
    unitConditions = ""
    directKeys = ["单位Hash值"]
    directValues = {}
    for key in directKeys:
        directValues[key] = None
        if key in df.keys():
            value = df[key][i]
            if not pandas.isna(value):
                if ("Hash" in key):
                    RBB.checkHashValue(value)
                directValues[key] = value
                
    if directValues["单位Hash值"]:
        unitConditions += RBB.GeneralConditions(NameInMenuToken = directValues["单位Hash值"])
    return unitConditions

def WriteTTypeUnitConditionsFromDF(df, i, hashOnly):
    unitConditions = ""
    directKeys = ["单位Hash值"]
    directValues = {}
    for key in directKeys:
        directValues[key] = None
        if key in df.keys():
            value = df[key][i]
            if not pandas.isna(value):
                if ("Hash" in key):
                    RBB.checkHashValue(value)
                directValues[key] = value
            
    if directValues["单位Hash值"]:
        unitConditions += RBB.GeneralConditions(NameInMenuToken = directValues["单位Hash值"],
                                                GenerateName = True)
    return unitConditions
    

def WriteUnitChangesFromDF(df, i):
    unitChanges = ""
    amountKeys = ["基础数量(菜鸟)", "基础数量(受训)", "基础数量(硬汉)", "基础数量(老兵)", "基础数量(精英)"]
    directKeys = ["价格", "年代", "单位类型","原型", "卡数"] + amountKeys
    
    amountChangesSet = False
    directValues = {}
    for key in directKeys:
        directValues[key] = None
        if key in df.keys():
            value = df[key][i]
            if not pandas.isna(value):   
                directValues[key] = value
                
    if directValues["卡数"]:
        unitChanges += RBB.GeneralChanges(MaxPacks = [RBB.VariableTypeUInt, int(directValues["卡数"])])
              
    if directValues["价格"]:   
        price = int(directValues["价格"])
        unitChanges += RBB.GeneralChangeDict(prop = "ProductionPrice", 
                                              key = 0, 
                                              typeValuePair = [RBB.VariableTypeUInt, price])
        if directValues["单位类型"]:
            单位类型 = directValues["单位类型"]
            if 单位类型 == "主炮坦歼":
                单位类型 = "坦克"
            
            if 单位类型 in RBB.unitTypeList:# "坦克歼击车", 
                priceLine = RBB.UnitAmountDict[单位类型][0]
                amountDict = RBB.UnitAmountDict[单位类型][1]
                amounts = None
                for i, line in enumerate(priceLine):
                    if price>=line:
                        amounts = amountDict[line]
                if amounts == None:
                    raise ValueError("price return no matched amount")
                for i, amount in enumerate(amounts):
                    unitChanges += RBB.GeneralChangeDict(prop = "MaxDeployableAmount", 
                                                         key = i, 
                                                         typeValuePair = [RBB.VariableTypeUInt, amount])
                amountChangesSet = True
            if 单位类型 == "迫击炮":
                unitChanges += RBB.GeneralChanges(Factory = ["Int32",8])

            
    if not amountChangesSet:    
        for i, key in enumerate(amountKeys):
            if (directValues[key] != None):
                amount = int(directValues[key])
                unitChanges += RBB.GeneralChangeDict(prop = "MaxDeployableAmount", 
                                                     key = i, 
                                                     typeValuePair = [RBB.VariableTypeUInt, amount])

    if directValues["原型"]:
        原型 = directValues["原型"]
        if 原型 == "移除":
            unitChanges += RBB.GeneralChanges(IsPrototype = None)
        elif 原型 == "新增":
            unitChanges += RBB.GeneralChanges(IsPrototype = [RBB.VariableTypeBool, True])
        else:
            raise ValueError("原型 argument has to be 移除 or 新增")

    if directValues["年代"]:
        年代 = directValues["年代"]
        RBB.intCheck(年代 = 年代)
        年代 = int(年代)
        unitChanges += RBB.GeneralChanges(ProductionYear = [RBB.VariableTypeUInt, 年代])        
        
    return unitChanges

class FilterChange():
    def __init__(self):
        self.TUnitMainType = RBB.generateKeyWordHashDictFromTable(keyword = "单位主要类型", keywordHash = "单位主要类型Hash值")
    
    def mainTypeChange(self, mainTypeHash):
        return RBB.GeneralChangeDictInDict(prop = "Filters", keyOut = 1, keyIn = 0, 
                                        typeValuePair= [RBB.VariableTypeHash, mainTypeHash])
    
    def yearTypeChange(self, yearTypeHash):
        return RBB.GeneralChangeDictInDict(prop = "Filters", keyOut = 2, keyIn = 0, 
                                        typeValuePair= [RBB.VariableTypeHash, yearTypeHash])  
FC = FilterChange()

def WriteTTypeUnitChangesFromDF(df, i):
    unitChanges = ""
    directKeys = ["年代", "单位类型", "价格"]
    directValues = {}
    for key in directKeys:
        directValues[key] = None
        if key in df.keys():
            value = df[key][i]
            if not pandas.isna(value):   
                directValues[key] = value
       
    ############################################################
    ####################unit filter changes#####################
    unitFilterChanges = ""
    if directValues["单位类型"]:
        单位类型 = directValues["单位类型"]
        if 单位类型 == "坦克": 
            if directValues["价格"]:   
                price = int(directValues["价格"])
                if price <45:
                    unitFilterChanges += FC.mainTypeChange(FC.TUnitMainType["MBT:<45"])
                elif price <= 85:
                    unitFilterChanges += FC.mainTypeChange(FC.TUnitMainType["MBT:45-85"])
                else:
                    unitFilterChanges += FC.mainTypeChange(FC.TUnitMainType["MBT:>85"])
        elif 单位类型 in ["主炮坦歼", "导弹坦歼"]:
            pass

    if directValues["年代"]:
        年代 = directValues["年代"]
        RBB.intCheck(年代 = 年代)
        if 年代<=1980:
            unitFilterChanges += FC.yearTypeChange(RBB.CatPre1980)
        elif 年代<=1985:
            unitFilterChanges += FC.yearTypeChange(RBB.Cat1981to1985)
        else:
            unitFilterChanges += FC.yearTypeChange(RBB.CatPost1986)      
    unitChanges += unitFilterChanges 
    ####################end of unit filter changes##############  
    ############################################################
    
    return unitChanges




def WriteGeneralPatchFromTable(sheet, dataClass = "TUniteAuSolDescriptor", keyProperty = "单位Hash值", keyPropertyName = "单位名", xlsx = "RBB.xlsx",
                               WriteConditionsFromDF    = WriteUnitConditionsFromDF,
                               WriteChangesFromDF       = WriteUnitChangesFromDF):
    df = pandas.read_excel(xlsx, sheet, header = 1)
    firstTime = []
    #检查keyProperty 不为 nan的每一行 
    
    connec = "(关键名称), 关键过滤值 = "
    if keyProperty == "单位Hash值":
        connec = "(单位), 单位Hash值 = "
    
    for i in range(df[keyProperty].size):
        关键过滤值 = df[keyProperty][i]
        if not pandas.isna(关键过滤值):
            patchName = df[keyPropertyName][i] + connec +str(keyProperty)
            if patchName in firstTime:
                print("Warning: repeated 关键名称/关键过滤值 combo at line "+str(i+3)+" in sheet = "+sheet)
            else:
                firstTime.append(patchName)
            
            hashOnly = False     
            keyPropertyOnly = keyProperty+"即唯一条件"
            if keyPropertyOnly in df.keys():
                if df[keyPropertyOnly][i] == "Y":
                    hashOnly = True
 
            
            conditions = WriteConditionsFromDF(df, i, hashOnly)
            changes    = WriteChangesFromDF(df, i)
            RBB.GeneralPatch(dataClass,
                             patchName,
                             conditions,
                             changes)
            
def WriteUnitPatchFromTable(sheet, changeTTypeUnit = False):
    WriteGeneralPatchFromTable(sheet)
    if changeTTypeUnit:
        WriteGeneralPatchFromTable(sheet, dataClass = "TTypeUnitModuleDescriptor",
                                   WriteConditionsFromDF = WriteTTypeUnitConditionsFromDF,
                                   WriteChangesFromDF = WriteTTypeUnitChangesFromDF)
"""
template
def WriteGeneralConditionsFromDF(df, i, hashOnly):
    generalConditions = ""
    directKeys = []
    directValues = {}
    for key in directKeys:
        directValues[key] = None
        if key in df.keys():
            value = df[key][i]
            if not pandas.isna(value):
                directValues[key] = value
    return generalConditions
    
    
def WriteGeneralChangesFromDF(df, i):
    generalChanges = ""
    directKeys = []
    directValues = {}
    for key in directKeys:
        directValues[key] = None
        if key in df.keys():
            value = df[key][i]
            if not pandas.isna(value):   
                directValues[key] = value
    return generalChanges

"""
    