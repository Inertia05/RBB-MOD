# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 17:40:12 2021

@author: Administrator
"""



import os
import numpy as np
import pandas 
import numbers

xmlOutput = ""
def XMLPatch(fName = "RBB"):
    global xmlOutput

    txtFile = fName+".txt"
    xmlFile = fName+'.xml'
    if os.access(xmlFile, os.F_OK):
        os.remove(xmlFile)
    file = open(txtFile,"w+", encoding = "utf-8")
    #"//" means /
    file.write(xmlOutput)
    file.close()
    os.rename(txtFile, xmlFile)
    print(xmlFile+" patch file generated.")
    xmlOutput = ""
    
wmiOutput = ""
def WMIPatch():
    global wmiOutput
    fName = "installerConfig"
    txtFile = fName+".txt"
    wmiFile = fName+'.wmi'
    if os.access(wmiFile, os.F_OK):
        os.remove(wmiFile)
    file = open(txtFile,"w+", encoding = "utf-8")
    #"//" means /
    file.write(wmiOutput)
    file.close()
    os.rename(txtFile, wmiFile)
    print(wmiFile+" patch file generated.")
    wmiOutput = ""
    
def WMIAlterDictPatch(language, hashList, valueList, hashRenameList, valueRenameList):
    global wmiOutput
    wmiOutput += """
    <AlterDictionary 
            targetPath="Data\RBB\ZZ_Win.dat"
            targetContentPath="pc\localisation\\"""+language+"""\localisation\\unites.dic">\n"""
    for i in range(len(hashList)):
        hashI = hashList[i]
        valueI = valueList[i]
        if not pandas.isna(valueI):
            wmiOutput += """            <AddEntry hash=\""""+hashI+"""\" value=\""""+valueI+""""/>\n"""
    
    for i in range(len(hashRenameList)):
        hashI = hashRenameList[i]
        valueI = valueRenameList[i]
        checkHashValue(hashI)
        if not pandas.isna(valueI):
            wmiOutput += """            <RenameEntry hash=\""""+str(hashI)+"""\" value=\""""+valueI+""""/>\n"""
            
    wmiOutput += """
		</AlterDictionary>	
    """
    

    
def HashListRenameWeaponFromTable(sheet, fName = "RBB"):
    df = pandas.read_excel(fName+".xlsx", sheet, header = 1)
    hashList = []
    valueList = []
    for i in range(df["武器Hash值"].size):
        武器Hash值 = df["武器Hash值"][i]
        新武器名 = df["新武器名"][i]
        新武器Hash值 = df["新武器Hash值"][i] if "新武器Hash值" in df.keys() else None
        if (not pandas.isna(武器Hash值) and (not pandas.isna(新武器名) and (pandas.isna(新武器Hash值)))):
            checkHashLength(武器Hash值)
            hashList.append(武器Hash值)
            valueList.append(新武器名)
    return hashList,valueList        
    
def HashListAddWeaponFromTable(sheet, fName = "RBB"):
    df = pandas.read_excel(fName+".xlsx", sheet, header = 1)
    hashList = []
    valueList = []
    for i in range(df["新武器Hash值"].size):
        新武器名 = df["新武器名"][i]
        新武器Hash值 = df["新武器Hash值"][i]
        if ((not pandas.isna(新武器名) and (not pandas.isna(新武器Hash值)))):#include line with no 武器Hash值 
            checkHashLength(新武器Hash值)
            hashList.append(新武器Hash值)
            valueList.append(新武器名)
    return hashList,valueList        

def HashListRenameFromTable(sheet, kwdHash = "单位Hash值", newKwdHash = "新单位Hash值", newKwdName = "新单位名", fName = "RBB"):
    df = pandas.read_excel(fName+".xlsx", sheet, header = 1)
    hashList = []
    valueList = []
    for i in range(df[kwdHash].size):
        kwdHashI = df[kwdHash][i]
        newKwdNameI = df[newKwdName][i]

        newKwdHashI = df[newKwdHash][i] if newKwdHash in df.keys() else None
        if (not pandas.isna(kwdHashI) and (not pandas.isna(newKwdNameI) and (pandas.isna(newKwdHashI)))):
            checkHashLength(kwdHashI)
            hashList.append(kwdHashI)
            valueList.append(newKwdNameI)
    return hashList,valueList        
    
def HashListAddNameFromTable(sheet, newKwdHash = "新单位Hash值", newKwdName = "新单位名", fName = "RBB"):
    df = pandas.read_excel(fName+".xlsx", sheet, header = 1)
    hashList = []
    valueList = []
    for i in range(df[newKwdHash].size):
        newKwdNameI = df[newKwdName][i]
        newKwdHashI = df[newKwdHash][i]
        if ((not pandas.isna(newKwdNameI) and (not pandas.isna(newKwdHashI)))):#include line with no kwdHash 
            checkHashLength(newKwdHashI)
            hashList.append(newKwdHashI)
            valueList.append(newKwdNameI)
    return hashList,valueList        

VariableTypeFloat  = "Float32"
VariableTypeHash   = "LocalisationHash"
VariableTypeBool   = "Boolean"
VariableTypeUInt   = "UInt32"
VariableTypeInt    = "Int32"
VariableTypeTableString = "TableString"

TurretTypeUnit = "TTurretUnitDescriptor"
TurretTypeAxis = "TTurretTwoAxisDescriptor"
TurretTypeInf  = "TTurretInfanterieDescriptor"

TUniteAuSolDescriptor = "TUniteAuSolDescriptor"

CatPre1980      = "41E22D4DD9380000"
Cat1981to1985   = "46E22D4DD9380000"
CatPost1986     = "81E22D4DD9380000"

HEBombTypeArme = "A74C330000000000"
RetardedHEBombTypeArme = "A74C33B9CA010000"
LGBTypeArme = "32E3EA116E5A0000"
NapalmBombTypeArme = "A74C33B589010000" 
ATClusterBombTypeArme = "A74C337ADC000000"

HowitzerTypeArme = "B7FAE72E4F4B0000"
MortarTypeArme = "B799DFF405000000"
MLRSTypeArme = "E8AC9B56C95D0000"

ATGMTypeArme = "57E42D0000000000"
AGMTypeArme = "57B4000000000000"
AntiRadarTypeArme = "DC02000000000000"

AAMTypeArme = "D7B2000000000000"
SAMTypeArme = "D7D2010000000000"

NavalGunTypeArme = "B31E95BB89010000"
NavalAutocannonTypeArme = "74AE2FE56E620000"
AutocannonTypeArme = "F46CA274AE2F0000"
TwinAutocannonTypeArme = "74AE2FE5ECF21E00"
QuadAutocannonTypeArme = "74AE2F656AEA1B00"
GatlingGunTypeArme = "ECECC6B919010000"
CIWSTypeArme = "5D38350000000000"

SSMTypeArme = "57D7010000000000"
MainGunTypeArme = "B31E95B36B5E0000"



def generateKeyWordHashDictFromTable(keyword, keywordHash, sheet = "常用Hash表", fName = "RBB"):
    df = pandas.read_excel(fName+".xlsx", sheet, header = 1)
    ret = {}
    for i in range(df[keyword].size):
        kwd = df[keyword][i]
        kwdHash = df[keywordHash][i]
        if (not pandas.isna(kwd)) and (not pandas.isna(kwdHash)):
           ret[kwd] = kwdHash
    return ret

TAmmuCaliber = generateKeyWordHashDictFromTable(keyword = "口径名", keywordHash = "口径Hash值")
TAmmuTypeArme = generateKeyWordHashDictFromTable(keyword = "武器类型名", keywordHash = "武器类型Hash值")

def generateAmountDictForPrice(unitTypeList, sheet = "价格数量临界线", fName = "RBB"):

    df = pandas.read_excel(fName+".xlsx", sheet, header = 1)
    ret = {}
    amountKeys = ["基础数量(菜鸟)", "基础数量(受训)", "基础数量(硬汉)", "基础数量(老兵)", "基础数量(精英)"]
    for unitType in unitTypeList:
        
        priceList = df[unitType+"价格"]
        priceListRet = []
        amountDict = {}
        for i in range(len(priceList)):
            if not pandas.isna(priceList[i]):
                price = int(priceList[i])
                priceListRet.append(price)
                amounts = []
                for amountKey in amountKeys:
                    amounts.append(int(df[unitType+amountKey][i]))
                amountDict[price] = amounts
        ret[unitType] = [priceListRet, amountDict]
    
    return ret

unitTypeList = ["迫击炮", "坦克", "侦察车辆","步战车", "导弹坦歼", "舰艇", "高炮","重防空", "榴弹炮","火箭炮", "攻击直升机"]
UnitAmountDict = generateAmountDictForPrice(unitTypeList)

"""
			<matchcondition type="property" property="TypeArme">A74C330000000000</matchcondition>
"""

def TypeArme(TypeArme):
    out = """<matchcondition type="property" property="TypeArme">"""+TypeArme+"""</matchcondition>"""
    return out

def Name(Name):
    out = """<matchcondition type="property" property="Name">"""+Name+"""</matchcondition>"""
    return out

def SalvoLength(SalvoLength):
    out = """<matchcondition type="property" property="NbTirParSalves">"""+str(SalvoLength)+"""</matchcondition>"""
    return out

def IsSubAmmu(isSubAmmu):
    if isSubAmmu:
        return """<matchcondition type="property" property="IsSubAmmunition">True</matchcondition>"""
    else:
        return """<matchcondition type="property" property="IsSubAmmunition">null</matchcondition>"""

def IsNPLM(isNPLM):
    if isNPLM:
        return """<matchcondition type="property" property="IgnoreInflammabilityConditions">True</matchcondition>"""
    else:
        return """<matchcondition type="property" property="IgnoreInflammabilityConditions">null</matchcondition>"""



    
def setArme(ammoType, AP = 0):
    Arme = {"Bullet":"null", "HMG":"1", "HE":"3"}
    if ammoType == "KE":
        if AP<1 or AP >30:
            raise ValueError("AP Value has to be in range [1,30]")
        return """<change operation="set" property="Arme" type="UInt32">"""+str(4+AP)+"""</change>"""
    elif ammoType == "HEAT":
        if AP<1 or AP >30:
            raise ValueError("AP Value has to be in range [1,30]")
        return """<change operation="set" property="Arme" type="UInt32">"""+str(34+AP)+"""</change>"""  
    else:
        out =  """<change operation="set" property="Arme" type="UInt32">"""+Arme[ammoType]+"""</change>"""
        if AP>0:
            out += """<change operation="set" property="PhysicalDamages" type="Float32">"""+str(AP)+"""</change>"""
        return out        

def setDamages(HE, HERadi, SupRadi):
    out = """<change operation="set" property="RadiusSplashSuppressDamages" type="Float32">"""+str(SupRadi*52)+"""</change>
    			<change operation="set" property="RadiusSplashPhysicalDamages" type="Float32">"""+str(HERadi*52)+"""</change>
    			<change operation="set" property="PhysicalDamages" type="Float32">"""+str(HE)+"""</change>"""
    return out

def setSalvoSupply(supply):
    out = """<change operation="set" property="SupplyCost" type="UInt32">"""+str(supply)+"""</change>"""
    return out

space3 = """			"""

def bombPatch(patchName, bombTypeArme, caliber, HE, HERadi, SupRadi, salvoLength, supply):
    global xmlOutput
    conditions = """
    """
    changes = """
    """

    if bombTypeArme == HEBombTypeArme or RetardedHEBombTypeArme:     
        conditions += """			"""+TypeArme(bombTypeArme)+"""
        		"""                    +TAmmuConditions(Caliber = caliber)+"""
        		"""                    +SalvoLength(salvoLength)
                
        changes += """			"""    +setDamages(HE, HERadi, SupRadi)+"""
        		"""                    +setSalvoSupply(supply)

    elif bombTypeArme == ATClusterBombTypeArme:
        conditions += """			"""+TypeArme(bombTypeArme)+"""
        		"""                    +TAmmuConditions(Caliber = caliber)+"""
        		"""                    +SalvoLength(salvoLength)
                
        changes += """			"""    +setDamages(HE, HERadi, SupRadi)+"""
        		"""                    +setSalvoSupply(supply)+"""
        		"""                    +setArme("HE")#set it to HE
        
    out = """
    <!-- change property of PatchName -->
   	<ndfpatch ndf="pc\\ndf\patchable\gfx\everything.ndfbin" table="TAmmunition" name="PatchName">
       	<matchconditions>"""+conditions+"""
   		</matchconditions>
   		<changes>"""+changes+"""
   		</changes>
   	</ndfpatch>
        """
    out = out.replace("PatchName", patchName)
    xmlOutput += out
        
def bombPatches(HESupplyFactor, HESupRadiFactor, CLUSSupplyFactor, CLUSSupRadiFactor):
    global xmlOutput
    checkXmlOutputIsEmpty()
    xmlOutput += """<wargamepatch>"""    
    CLUSBombWeights = [245,340,450,500]
    CLUSBombDamages = {
                    245:
                        ["2C6C140300000000",8,379],#only Mk 20, 5 ins
                    340:
                        ["2C1C140400000000",9,423],#only 1 ins exist
                    450:
                        ["2C1C180500000000",10,465],#various name and salvo length
                    500:
                        ["2C1C040600000000",11,481]}#only RBK-500, 4 ins
    CLUSsalvoLengths = [2,4,5,6,8,12]
    
    for i in range(len(CLUSBombWeights)):
        for j in range(len(CLUSsalvoLengths)):
            bombData = CLUSBombDamages[CLUSBombWeights[i]]
            supplyRef = bombData[1]
            
            salvoLength = CLUSsalvoLengths[j]
            supply = supplyRef * salvoLength * CLUSSupplyFactor
            
            bombPatch(patchName = str(CLUSBombWeights[i])+" kg CLUS bomb, salvo length "+str(CLUSsalvoLengths[j]), 
                        bombTypeArme = ATClusterBombTypeArme,
                        caliber = bombData[0], 
                        HE = bombData[1], 
                        HERadi = bombData[2], 
                        SupRadi = bombData[2]*CLUSSupRadiFactor, 
                        salvoLength = salvoLength,
                        supply = supply)
            
    CLUSBomb450kg = {"BL-755"       :["8681580C00000000",10],
                     "250-1"        :["42600C8BA5010000",10],
                     "BLG-66 Beluga":["C711590C00000000",11],
                     "TAL-2"        :["83B5780000000000",11],
                     "CBU-87"       :["48F2310D00000000",12],
                     "IBL-755"      :["868158CC04000000",12],
                     "BK90 Mjölner" :["57A0540C00000000",14]}
    
    for salvoLength in [4,6]:
        for name in CLUSBomb450kg.keys():
            patchName = "450kg CLUS Bomb "+name
            HE = CLUSBomb450kg[name][1]
            supply = HE * salvoLength * CLUSSupplyFactor
            conditions = """
    """
            conditions += """			"""+Name(CLUSBomb450kg[name][0])+"""
        		"""                        +SalvoLength(salvoLength)
            changes = """
    """
            changes += """			"""    +setArme("HE", HE)+"""
        		"""                    +setSalvoSupply(supply)
                
            out = """
    <!-- change property of PatchName -->
   	<ndfpatch ndf="pc\\ndf\patchable\gfx\everything.ndfbin" table="TAmmunition" name="PatchName">
       	<matchconditions>"""+conditions+"""
   		</matchconditions>
   		<changes>"""+changes+"""
   		</changes>
   	</ndfpatch>
"""
            out = out.replace("PatchName", patchName)
            xmlOutput += out
    xmlOutput += """</wargamepatch>"""
    xmlOutput = xmlOutput.replace("pc\n","pc\\n")

def priceBuff(price, factor):
    mod =  (price*factor)%5
    newPrice = price*factor-mod if mod<2.5 else price*factor+(5-mod)
    newPrice = 1 if newPrice<1 else int(newPrice)
    return newPrice

def pricePatch(units, priceFactor = 1, amountFactor = 1):

    """
    unitPriceListExample = {"M/727 HAWK"         :["306F4AC8805C0000",40,[0,8,6,0,0]],
                            "AMX-30 ROLAND"      :["0EB6581907000000",45,[0,8,6,0,0]],
                            "TRACKED RAPIER 2000":["4B07DDAA5B9B1C00",55,[0,6,4,0,0]]
                            }
    """
    for unit in units.keys():
        amounts = "\n	   	   	"
        for i in range(5):
            decimalAmount = units[unit][2][i]*amountFactor
            newAmount = int(decimalAmount + (1-decimalAmount%1)) if decimalAmount%1>=0.5 else int(decimalAmount)
            if newAmount < 0:
                raise ValueError("Amount cannot be negative.")
            amounts += GeneralChangeDict(prop = "MaxDeployableAmount", 
                                  key = i, 
                                  typeValuePair = ["Int32", newAmount])
            
        price = str(priceBuff(units[unit][1],priceFactor))
        
        GeneralPatch(table = "TUniteAuSolDescriptor",
                     patchName = " price of "+unit, 
                     conditions = GeneralConditions(NameInMenuToken = units[unit][0]),
                     changes = GeneralChangeDict(prop = "ProductionPrice", 
                                          key = 0, 
                                          typeValuePair = ["Int32",price])+amounts)

        
def pricePatchSingle(patchName, unitData, priceFactor = 1, amountFactor = 1):
    global xmlOutput
    """
    unitData = {"hash"  : "306F4AC8805C0000",
                "price" : 40,
                "amount": [0,8,6,0,0]}
    """
    unitHash = unitData["hash"]
    unitPrice = unitData["price"]
    unitAmountData = unitData["amount"]
    amounts = ""
    for i in range(5):
        decimalAmount = unitAmountData[i]*amountFactor
        newAmount = int(decimalAmount + (1-decimalAmount%1)) if decimalAmount%1>=0.5 else int(decimalAmount)
        if newAmount < 0:
            raise ValueError("Amount cannot be negative.")
        amounts += GeneralChangeDict(prop = "MaxDeployableAmount", 
                              key = i, 
                              typeValuePair = ["Int32", newAmount])
        
    price = str(priceBuff(unitPrice,priceFactor))
    
    GeneralPatch(table = "TUniteAuSolDescriptor",
                 patchName = patchName, 
                 conditions = GeneralConditions(NameInMenuToken = unitHash),
                 changes = GeneralChangeDict(prop = "ProductionPrice", 
                                      key = 0, 
                                      typeValuePair = ["Int32",price])+amounts)
    
def GeneralChangeDict(prop, key, typeValuePair):
    ret = ""

    ret += ("""<change operation="set" property=\""""+prop+"""\" key=\""""+str(key)+
    """\" type=\""""+typeValuePair[0]+"""\">"""+str(typeValuePair[1])+
    """</change>\n	   	   	""")
    
    return ret

def GeneralChangeDictValueObject(prop, key, table, tableConditions):
    ret = ""
    ret += ("""<change operation=\"set\" property=\""""+prop+"""\" key=\""""+str(key)+
    """\" type= \"ObjectReference\">"""+"""
                <reference table=\""""+table+"""\">
					<matchconditions>
                        """+addTabsBetweenLines(string = tableConditions, tabCount = 3)+"""
					</matchconditions>
				</reference>
            </change>\n	   	   	""")
                

    return ret

def GeneralChangeDictValueObjectDelete(prop, key):
    ret = ""
    ret += ("""<change operation=\"delete\" property=\""""+prop+"""\" key=\""""+str(key)+
    """\" ></change>\n	   	   	""")
                

    return ret

def GeneralChangeDictClear(prop):
    ret = ""
    ret += """<change property=\""""+str(prop)+"""\" operation="clear" />\n	   	   	"""
    return ret

def GeneralChangeDictAppend(prop, typeValuePair):
    ret = ""
    
    ret += ("""<change operation="append" property=\""""+prop+"""\" type=\""""+typeValuePair[0]+"""\">"""+str(typeValuePair[1])+
    """</change>\n	   	   	""")

    return ret


def GeneralChangeDictValueObjectAppend(prop, table, tableConditions):
    ret = ""
    ret += ("""<change operation=\"append\" property=\""""+prop+
    """\" type= \"ObjectReference\">"""+"""
                <reference table=\""""+table+"""\">
					<matchconditions>
                        """+addTabsBetweenLines(string = tableConditions, tabCount = 3)+"""
					</matchconditions>
				</reference>
            </change>\n	   	   	""")
    return ret

def GeneralChangeDictValueObjectAppendKey(prop, keyType, key, table, tableConditions):
    ret = ""
    ret += ("""<change operation=\"append\" property=\""""+prop+"\" type=\"map\">"+
            """
                <map>
					<key type=\""""+keyType+"\">"+key+"</key>"+"""
                    <value type="ObjectReference">"""+
                """
                        <reference table=\""""+table+"""\">
        					<matchconditions>
                                """+addTabsBetweenLines(string = tableConditions, tabCount = 5)+"""
        					</matchconditions>
        				</reference>
                    </value>
                </map>    
            </change>\n	   	   	""")
    return ret
        
        
def GeneralChangeDictInDict(prop, keyOut, keyIn, typeValuePair):
   ret = ""
   keyOut = str(keyOut)
   keyIn = str(keyIn)
   
   ret += ("""<change operation="select" property=\""""+prop+"""\" key=\""""+keyOut+"""\" />
            <change operation="set" key=\""""+keyIn+"""\" type=\""""+
            typeValuePair[0]+"""\">"""+typeValuePair[1]+"""</change>
            <change operation="unselect" />\n            """)
   return ret



def GeneralPatch(table, patchName, conditions, changes, path = "everything"):
    global xmlOutput
    
    if path == "everything":
        path = "pc\\ndf\patchable\gfx\everything.ndfbin"
    elif path == "camera":
        path = "pc\\ndf\patchable\misc\\basecamera.ndfbin"
    elif path == "constant":
        path = "pc\\ndf\patchable\gfx\gdconstanteoriginal.ndfbin"
    else:
        raise ValueError("Uncategorized path: "+str(path))
    
    
    out = """
    
    <!-- Patch: PatchName -->
   	<ndfpatch ndf=\""""+path+"""\" table=\""""+table+"""\" name="PatchName">
       	<matchconditions>
           	"""+conditions+"""
   		</matchconditions>
           
   		<changes>
           	"""+changes+"""
   		</changes>
   	</ndfpatch>\n"""
    out = out.replace("PatchName", patchName)
    xmlOutput += out
    
def TAmmuPatch(patchName, conditions, changes):
    global xmlOutput
        
    out = """
    
    <!-- change property of PatchName -->
   	<ndfpatch ndf="pc\\ndf\patchable\gfx\everything.ndfbin" table="TAmmunition" name="PatchName">
       	<matchconditions>
            """+conditions+"""
   		</matchconditions>
           
   		<changes>
            """+changes+"""
   		</changes>
   	</ndfpatch>"""
    out = out.replace("PatchName", patchName)
    xmlOutput += out

maxLength = 185#140 max except model file name condition
def AddSpaceTo2Var(prefix, variable, connec, value, suffix):
    totLength = (len(prefix) + len(variable) + len(connec) + len(str(value)) + len(suffix))
    if totLength <= maxLength:
        space = ""
        for i in range(maxLength-totLength):
            space +=" "
        connec = connec[:-1] + space + connec[-1]
    else:
        raise ValueError("The max length is set too short, current length = "+str(totLength))
    return prefix + variable+ connec + str(value) + suffix

def AddSpaceTo3Var(prefix, variable, connec1, vType, connec2, value, suffix):
    totLength = (len(prefix) + len(variable) + len(connec1) + len(vType) + len(connec2) + len(str(value)) + len(suffix))
    if totLength <= maxLength:
        space = ""
        for i in range(maxLength-totLength):
            space += " "
        connec1 = connec1[:-1] + space + connec1[-1]
    else:
        raise ValueError("The max length is set too short")
    return prefix + variable + connec1 + vType + connec2 + str(value)+ suffix
    
def GeneralConditions(**kwargs):
    ret = ""
    for kwarg in kwargs.keys():
        variable = kwarg #auto convert to string
        value = kwargs[kwarg]
        prefix = """<matchcondition type="property" property=\""""
        connec = """\">"""
        suffix = """</matchcondition>\n      	    """
        
        if isinstance(value, numbers.Number):
            if value%1 == 0:
                if not isinstance(value, int):
                    raise ValueError("Int Condition value = "+str(value)+" cannot have decimal point")
        ret += AddSpaceTo2Var(prefix, variable, connec, value, suffix)
    return ret

def GeneralConditionReference(table, tableConditions):
    ret = ""
    ret += """<matchcondition type="references" table=\""""+table+"""">
				<matchconditions>
                    """+addTabsBetweenLines(string = tableConditions, tabCount = 2)+"""
				</matchconditions>
			</matchcondition>
            
            """
    return ret

def GeneralConditionReferencedBy(table, tableConditions):
    ret = ""
    ret += """<matchcondition type="referencedby" table=\""""+table+"""">
				<matchconditions>
                    """+addTabsBetweenLines(string = tableConditions, tabCount = 2)+"""
				</matchconditions>
			</matchcondition>
            
            """
    return ret

def GeneralChangesObject(prop, table, tableConditions):
    ret = ""
    ret += """<change operation="set" property=\""""+prop+"""\" type="ObjectReference">
				<reference table=\""""+table+"""\">
					<matchconditions>
                        """+addTabsBetweenLines(string = tableConditions, tabCount = 2)+"""
					</matchconditions>
				</reference>
      		</change>
            """
    return ret





def accInputCheck(acc):
    if acc[0] == "空值" and acc[1] == "空值":
        #print("This acc is null acc.")
        pass
    else:
        if acc[0] <0.01 or acc[0]>1:
            raise ValueError("stationary acc[0] must be in interval [0.01,1]")
        if acc[1] > acc[0]:
            raise ValueError("stationary acc[0] must >= movement acc[1]")
        if acc[1] <0.01:
            raise ValueError("movement acc[1] must >=0.01")
            
        if acc[0] <= 0.05:
            if (acc[0] not in [0.01,0.02,0.03,0.04, 0.05]) or (acc[1] not in [0.01,0.02,0.03,0.04, 0.05]):
                raise ValueError("acc smaller than or euqal to 0.05 must be multiple of 0.01: sta = " + str(acc[0])+", mov = "+str(acc[1]))
        else:
            if int(acc[0]*100)%5 != 0 or int(acc[1]*100)%5 != 0:
                raise ValueError("acc must be multiple of 0.05: sta = " + str(acc[0])+", mov = "+str(acc[1]))
            elif len(str(acc[0]))>4 or len(str(acc[1]))>4:
                raise ValueError("acc must be multiple of 0.05: sta = " + str(acc[0])+", mov = "+str(acc[1]))

def TAmmuConditions(acc = None, unitHash = [None,None], **kwargs):
    #5 object reference, the rest = value
    ret = ""
    ret += GeneralConditions(**kwargs)

    if acc:
        accInputCheck(acc)
        ret +="""
			<matchcondition type="references" table="TModernWarfareHitRollRule">
				<matchconditions>
					<matchcondition type="property" property="HitProbability">"""+str(acc[0])+"""</matchcondition>
                    <matchcondition type="property" property="HitProbabilityWhileMoving">"""+str(acc[1])+"""</matchcondition>
				</matchconditions>
            </matchcondition>\n
            """
    if unitHash[0]:
        turretType = {"axis"    :"TTurretTwoAxisDescriptor",
                      "turret"  :"TTurretUnitDescriptor"}
        ret+="""			
            <matchcondition type="referencedby" table="TMountedWeaponDescriptor">
				<matchconditions>
					<matchcondition type="referencedby" table=\""""+turretType[unitHash[1]]+"""\">
						<matchconditions>
							<matchcondition type="referencedby" table="TWeaponManagerModuleDescriptor">
								<matchconditions>
									<matchcondition type="referencedby" table="TModuleSelector">
										<matchconditions>
											<matchcondition type="referencedby" table="TUniteAuSolDescriptor">
												<matchconditions>
													<matchcondition type="property" property="NameInMenuToken">"""+unitHash[0]+"""</matchcondition>
												</matchconditions>
											</matchcondition>
										</matchconditions>
									</matchcondition>
								</matchconditions>
							</matchcondition>
						</matchconditions>
					</matchcondition>
				</matchconditions>
			</matchcondition>\n"""
    return ret



def GeneralChanges(**kwargs):
    ret = ""
    for kwarg in kwargs.keys():
        if kwargs[kwarg] == None:
            ret += """<change operation="null" property=\""""+kwarg+"""\"/>\n   	   	    """
        else:
            prefix = """<change operation="set" property=\""""
            variable = kwarg #auto convert to string
            connec1 = """\" type=\""""
            vType = kwargs[kwarg][0]
            connec2 = """\">"""
            value = kwargs[kwarg][1]
            suffix = """</change>\n   	   	    """
            
            if vType == VariableTypeInt:
                if not isinstance(value, int):
                    raise ValueError("Value has to be a int")
            elif vType == VariableTypeUInt:
                if not isinstance(value, int):
                    raise ValueError("Value has to be a int")
                if value<0:
                    raise ValueError("Value has to be a non-negative int")
            elif vType == VariableTypeHash:
                if not isinstance(value, str):
                    raise ValueError("Value has to be a string")
                checkHashValue(value)
            elif vType == VariableTypeFloat:
                checkNumber(value)
            elif vType == VariableTypeBool:
                if not isinstance(value, bool):
                    raise ValueError("Value has to be a boolean")
                
            
            ret += AddSpaceTo3Var(prefix, variable, connec1, vType, connec2, value, suffix)
    return ret

def TAmmuChanges(acc = None, **kwargs):
    #Float32, UInt32, Boolean
    ret = ""
    ret += GeneralChanges(**kwargs)
    if acc:
        accInputCheck(acc)
        if (acc[0]=="空值") and (acc[1]=="空值"):
            acc[0] = "null"
            acc[1] = "null"
        ret +="""
            <change operation="set" property="HitRollRule">
				<reference table="TModernWarfareHitRollRule">
					<matchconditions>
						<matchcondition type="property" property="HitProbability">"""+str(acc[0])+"""</matchcondition>
                        <matchcondition type="property" property="HitProbabilityWhileMoving">"""+str(acc[1])+"""</matchcondition>
					</matchconditions>
				</reference>
		    </change>
            """
    return ret
                    

def Range(distance):
    return distance/35*2600      

shown = False
def GameDistanceFor(real_distance_km):
    global shown
    #xp = [0,  2.5,   12,   25,    60,   160]
    #fp = [0, 2500, 5000, 6000,  8400, 15000]
    
    xp = [0,  2.5,   12,    40,     60,   160,   460]
    fp = [0, 2500, 5000, 12250,  12950, 16750, 23100]
    if not shown:
        distanceScale = ""
        for i in range(len(xp)):
            distanceScale += str(xp[i])+" real km = "+str(fp[i])+" game m\n"
        print(distanceScale)
        shown = True
            
    if real_distance_km < xp[0]:
        raise ValueError("Input distance out of interpolation boundary(" + str(xp[0])+" km)!")
    interp = np.interp(real_distance_km,xp,fp)
    if real_distance_km <= 13:
        return round(interp/175)*175
    else:
        return round(interp/350)*350
    
def TAmmuChangesRange(shipOnly = False,
                      ground = [None,None], 
                      helo   = [None,None],                 
                      air    = [None,None],
                      projec = [None,None]):
    ret = ""
    if shipOnly:
        if ground[0]:
            ret += TAmmuChanges(PorteeMinimale = None,
                                PorteeMinimaleBateaux    = ["Float32",ground[0]] if ground[0] != "null" else None)
        if ground[1]:
            ret += TAmmuChanges(PorteeMaximale = None,
                                PorteeMaximaleBateaux    = ["Float32",ground[1]] if ground[1] != "null" else None)  
    else:
        if ground[0]:
            ret += TAmmuChanges(PorteeMinimale           = ["Float32",ground[0]] if ground[0] != "null" else None,
                                PorteeMinimaleBateaux    = ["Float32",ground[0]] if ground[0] != "null" else None)
        if ground[1]:
            ret += TAmmuChanges(PorteeMaximale           = ["Float32",ground[1]] if ground[1] != "null" else None,
                                PorteeMaximaleBateaux    = ["Float32",ground[1]] if ground[1] != "null" else None)  
        
    if helo[0]:
        ret += TAmmuChanges(PorteeMinimaleTBA        = ["Float32",helo[0]] if helo[0] != "null" else None)
    if helo[1]:
        ret += TAmmuChanges(PorteeMaximaleTBA        = ["Float32",helo[1]] if helo[1] != "null" else None)  
        
    if air[0]:
        ret += TAmmuChanges(PorteeMinimaleHA         = ["Float32",air[0]] if air[0] != "null" else None)
    if air[1]:
        ret += TAmmuChanges(PorteeMaximaleHA         = ["Float32",air[1]] if air[1] != "null" else None)  
        
    if projec[0]:
        ret += TAmmuChanges(PorteeMinimaleProjectile = ["Float32",projec[0]] if projec[0] != "null" else None)
    if projec[1]:
        ret += TAmmuChanges(PorteeMaximaleProjectile = ["Float32",projec[1]] if projec[1] != "null" else None)  
    return ret

def TAmmuConditionsRange(shipOnly = False,
                      ground = [None,None], 
                      helo   = [None,None],                 
                      air    = [None,None],
                      projec = [None,None]):
    ret = ""
    if shipOnly:
        if ground[0]:
            intCheck(ground[0])
            ret += TAmmuConditions(PorteeMinimaleBateaux    = ground[0])
        if ground[1]:
            intCheck(ground[1])
            ret += TAmmuConditions(PorteeMaximaleBateaux    = ground[1])  
    else:
        if ground[0]:
            intCheck(ground[0])
            ret += TAmmuConditions(PorteeMinimale           = ground[0],
                                   PorteeMinimaleBateaux    = ground[0])
        if ground[1]:
            intCheck(ground[1])
            ret += TAmmuConditions(PorteeMaximale           = ground[1],
                                   PorteeMaximaleBateaux    = ground[1])  
        
    if helo[0]:
        intCheck(helo[0])
        ret += TAmmuConditions(PorteeMinimaleTBA        = helo[0])
    if helo[1]:
        intCheck(helo[1])
        ret += TAmmuConditions(PorteeMaximaleTBA        = helo[1])  
        
    if air[0]:
        intCheck(air[0])
        ret += TAmmuConditions(PorteeMinimaleHA         = air[0])
    if air[1]:
        intCheck(air[1])
        ret += TAmmuConditions(PorteeMaximaleHA         = air[1])  
        
    if projec[0]:
        intCheck(projec[0])
        ret += TAmmuConditions(PorteeMinimaleProjectile = projec[0])
    if projec[1]:
        intCheck(projec[1])
        ret += TAmmuConditions(PorteeMaximaleProjectile = projec[1])  
    return ret

def TAmmuChangesDisp(disp = [None, None], corr = None):
    ret = ""
    if disp[0]:
        if disp[0] == "null":
            ret += TAmmuChanges(DispersionAtMinRange = None)
        else:
            ret += TAmmuChanges(DispersionAtMinRange = ["Float32", disp[0]])
    if disp[1]:
        if disp[1] == "null":
            ret += TAmmuChanges(DispersionAtMaxRange = None)
        else:
            ret += TAmmuChanges(DispersionAtMaxRange = ["Float32", disp[1]])  
    if corr:
            ret += TAmmuChanges(CorrectedShotDispersionMultiplier = ["Float32", corr])  
    return ret

def TAmmuConditionsArme(ammoType, AP = 0):
    Arme = {"Bullet":"null", "HMG":"1", "HE":"3"}
    if ammoType == "KE":
        if AP<1 or AP >30:
            raise ValueError("AP Value has to be in range [1,30]")
        return TAmmuConditions(Arme = 4+int(AP))
    elif ammoType == "HEAT":
        if AP<1 or AP >30:
            raise ValueError("AP Value has to be in range [1,30]")
        return TAmmuConditions(Arme = 34+int(AP))
    else:
        return  TAmmuConditions(Arme = Arme[ammoType])
    
def TAmmuChangesAOE(HE = [None, None], Sup = [None, None]):
    ret = ""
    if HE[0]:
        HEval = HE[0]
        if HEval>=0.95 and HEval <4:
            HEval = round(HEval/0.5)*0.5
        elif HEval >= 4:
            HEval = round(HEval)
        ret += TAmmuChanges(PhysicalDamages             = ["Float32", HEval])
    if HE[1]:
        ret += TAmmuChanges(RadiusSplashPhysicalDamages = ["Float32", HE[1]])
    if Sup[0]:
        SupVal = Sup[0]
        SupVal = round(SupVal)
        ret += TAmmuChanges(SuppressDamages             = ["Float32", SupVal])
    if Sup[1]:
        ret += TAmmuChanges(RadiusSplashSuppressDamages = ["Float32", Sup[1]])
    return ret
    
def TAmmuChangesArme(ammoType, AP = 0):
    """ammoType = (one of the following) 
            Bullet, HMG, HE, KE, HEAT
       AP is used for KE/HEAT ammoType only"""
    Arme = {"HMG":1, "Autocannon":2, "HE":3}
    if ammoType == "KE":
        if AP<1 or AP >30:
            raise ValueError("AP Value has to be in range [1,30]")
        return TAmmuChanges(Arme                    = ["UInt32",  4+int(AP)],
                            EfficaciteSelonPortee   = ["Boolean", True])
    elif ammoType == "HEAT":
        if AP<1 or AP >30:
            raise ValueError("AP Value has to be in range [1,30]")
        return TAmmuChanges(Arme = ["UInt32", 34+int(AP)],
                            EfficaciteSelonPortee = None)
    
    elif ammoType == "Bullet":
        return TAmmuChanges(Arme = None)
    
    else:
        if ammoType:
            return  TAmmuChanges(Arme = ["UInt32", Arme[ammoType]])

def TAmmuConditionsOnTheSameGunWithAmmu(subAmmuConditions):
    ret = ""
    """
    sepStr = subAmmuConditions.split(sep = "\n")
    tab ="""	"""
    tabs = ""
    for i in range(8):
        tabs += tab

    subAmmuConditions = ("\n"+tabs).join(sepStr)
    """
    subAmmuConditions = addTabsBetweenLines(subAmmuConditions, 8)
    ret +=("""
            <matchcondition type="referencedby" table="TMountedWeaponDescriptor">
				<matchconditions>
					<matchcondition type="referencedby" table="TTurretTwoAxisDescriptor">
						<matchconditions>
							<matchcondition type="references" table="TMountedWeaponDescriptor">
								<matchconditions>
									<matchcondition type="references" table="TAmmunition">
										<matchconditions>
                                            """+subAmmuConditions+"""    
										</matchconditions>
									</matchcondition>
								</matchconditions>
							</matchcondition>
						</matchconditions>
					</matchcondition>
				</matchconditions>
			</matchcondition>
    
    """)
    return ret

def addTabsBetweenLines(string, tabCount):
    sepStr = string.split(sep = "\n")
    tab ="""	"""
    tabs = ""
    for i in range(tabCount):
        tabs += tab

    string = ("\n"+tabs).join(sepStr)
    return string


def TAmmuConditionsROF(shotReload = None, shotFxReload  = None, salvoReload = None, 
                       salvoUILength = None, salvoLength = None, 
                       shotSimutane = None, aim = None):
    ret = ""
    if not pandas.isna(shotReload):
        ret += TAmmuConditions(TempsEntreDeuxTirs
                               = convertNumberForCondition(shotReload))
    if not pandas.isna(shotFxReload):
        ret += TAmmuConditions(TempsEntreDeuxFx
                               = convertNumberForCondition(shotFxReload))
    if not pandas.isna(salvoReload):
        ret += TAmmuConditions(TempsEntreDeuxSalves
                               = convertNumberForCondition(salvoReload))
    if not pandas.isna(aim):
        ret += TAmmuConditions(TempsDeVisee
                               = convertNumberForCondition(aim))

    if not pandas.isna(salvoUILength):
        if not salvoUILength%1 == 0:
            raise TypeError("salvoUILength = "+str(salvoUILength)+" must be int")
        ret += TAmmuConditions(AffichageMunitionParSalve
                               = convertNumberForCondition(salvoUILength))
    if not pandas.isna(salvoLength):
        if not salvoLength%1 == 0:
            raise TypeError("salvoLength = "+str(salvoLength)+" must be int")
        ret += TAmmuConditions(NbTirParSalves
                               = convertNumberForCondition(salvoLength))
        
    if not pandas.isna(shotSimutane):
        if not shotSimutane%1 == 0:
            raise TypeError("shotSimutane = "+str(shotSimutane)+" must be int")
        ret += TAmmuConditions(NbrProjectilesSimultanes
                               = convertNumberForCondition(shotSimutane))
    return ret

def TAmmuChangesROF(shotReload = None, shotFxReload  = None, salvoReload = None, 
                    salvoUILength = None, salvoLength = None, 
                    shotSimutane = None, aim = None):
    ret = ""
    if pandas.isna(shotFxReload):
            shotFxReload = shotReload
            
    if pandas.isna(salvoUILength):
            salvoUILength = salvoLength
           
    ###########################################################################
    
    if not pandas.isna(shotReload):
        ret += TAmmuChanges(TempsEntreDeuxTirs
                               = ["Float32", convertNumberForCondition(shotReload)])    
            
    if not pandas.isna(shotFxReload):
        ret += TAmmuChanges(TempsEntreDeuxFx
                               = ["Float32", convertNumberForCondition(shotFxReload)])
    if not pandas.isna(salvoReload):
        ret += TAmmuChanges(TempsEntreDeuxSalves
                               = ["Float32", convertNumberForCondition(salvoReload)])
        
    if not pandas.isna(aim):
        ret += TAmmuChanges(TempsDeVisee
                               = ["Float32", convertNumberForCondition(aim)])

    if not pandas.isna(salvoUILength):
        if not salvoUILength%1 == 0:
            raise TypeError("salvoUILength = "+str(salvoUILength)+" must be int")
        ret += TAmmuChanges(AffichageMunitionParSalve
                            = ["UInt32", convertNumberForCondition(salvoUILength)])
        
    if not pandas.isna(salvoLength):
        if not salvoLength%1 == 0:
            raise TypeError("salvoLength = "+str(salvoLength)+" must be int")
        ret += TAmmuChanges(NbTirParSalves
                            = ["UInt32", convertNumberForCondition(salvoLength)])
        
    if not pandas.isna(shotSimutane):
        if not shotSimutane%1 == 0:
            raise TypeError("shotSimutane = "+str(shotSimutane)+" must be int")
        ret += TAmmuChanges(NbrProjectilesSimultanes
                            = ["UInt32", convertNumberForCondition(shotSimutane)])
      

    return ret

        
def intCheck(*args, **kwargs):
    for arg in args:
        if arg%1 != 0:
            raise TypeError(str(arg)+" must be int type")      
    
    for kwarg in kwargs.keys():
        if kwargs[kwarg]%1 != 0:
            raise TypeError(kwarg+" must be int type")       
            
def floatCheck(*args, **kwargs):
    for arg in args:
        if type(arg) != float:
            raise TypeError(str(arg)+" must be float type")      
    
    for kwarg in kwargs.keys():
        if type(kwargs[kwarg]) != float:
            raise TypeError(kwarg+" must be float type")      
            

    
def convertNumberForCondition(number):
    if number%1 == 0:
        return int(number)
    else:
        return number

def checkXmlOutputIsEmpty():
    global xmlOutput
    if xmlOutput != "":
        raise ValueError("xmlOutput is not empty")
    
def TMountedWeaponPatchReplace(patchName, unitHash, oldAmmuCondition, newAmmuCondition, turretType = TurretTypeUnit):
    GeneralPatch("TMountedWeaponDescriptor", patchName, 
                 GeneralConditionReference("TAmmunition", oldAmmuCondition)+"\n\n			"+
                 
                 GeneralConditionReferencedBy(turretType, 
                     GeneralConditionReferencedBy("TWeaponManagerModuleDescriptor", 
                         GeneralConditionReferencedBy("TModuleSelector", 
                             GeneralConditionReferencedBy("TUniteAuSolDescriptor", 
                                 GeneralConditions(NameInMenuToken = unitHash))))),
                 
                 GeneralChangesObject("Ammunition", "TAmmunition", addTabsBetweenLines(newAmmuCondition,1)))
    
def TMountedWeaponPatchChangeUISlotIndex(patchName, tableConditions, UIIndex):
    intCheck(UIIndex = UIIndex)
    UIIndex = int(UIIndex)
    GeneralPatch("TMountedWeaponDescriptor", "All "+patchName+" go to slot "+str(UIIndex), 
                                         conditions = GeneralConditionReference("TAmmunition", 
                                                                                tableConditions = tableConditions),
                                         changes = GeneralChanges(SalvoStockIndex_ForInterface = ["Int32",UIIndex]))
    


def TMountedWeaponPatchChangeStablizer(patchName, tableConditions, stabChange):
    patchName = "所有 " + patchName +" "+stabChange+"稳定器" 
    if stabChange == "移除":
        changes = GeneralChanges(TirEnMouvement = None)
    elif stabChange == "新增":
        changes = GeneralChanges(TirEnMouvement = [VariableTypeBool, True])
    else:
        raise ValueError("stabChange argument has to be 移除 or 新增")
    GeneralPatch("TMountedWeaponDescriptor", patchName, 
                 conditions = GeneralConditionReference("TAmmunition", 
                                                        tableConditions = tableConditions),
                 changes = changes) 


def TAmmuChangesFire(fireSize = None, fireChance = 1):
    ret = ""
    if fireSize:
        fireNames = {"特小"   :"Fire_Incendie",       #Tiny fire
                     "小"     :"Fire_NapalmLeger",    #NPLM squad
                     "中"     :"Fire_NapalmBuratino", #NPLM MLRS
                     "大"     :"Fire_Napalm",         #NPLM tank
                     "特大"   :"Fire_NapalmLourd"     #NPLM air bomb
                    }

        tUniteDescriptorCondition = GeneralConditions(ClassNameForDebug = fireNames[fireSize])
        ret += GeneralChanges(IgnoreInflammabilityConditions = ["Boolean", True],
                              FireTriggeringProbability      = ["Float32", fireChance])
        
        ret += GeneralChangesObject("FireDescriptor", "TUniteDescriptor", addTabsBetweenLines(tUniteDescriptorCondition,1))
    return ret

def checkHashLength(locHash):
    tpe = type(locHash)
    locHash = str(locHash)
    if len(locHash) != 16:
        print(tpe)
        raise ValueError("loc Hash = ("+locHash+") must be in length 16")
        
def checkHashValue(locHash):
    locHash = str(locHash)
    checkHashLength(locHash)
    if not set(locHash) <= set("0123456789ABCDEF"):
        raise ValueError("loc Hash = ("+locHash+") must not contain characters other than 0-9, A-F")
        
def checkNumber(num):
    if not isinstance(num, numbers.Number):
        raise ValueError("value: "+str(num)+" has to be a number")