# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 17:40:12 2021

@author: Administrator
"""



import os
import numpy as np
import pandas 

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
    
def WMIAlterDictPatch(language, hashList, valueList):
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
    
    wmiOutput += """
		</AlterDictionary>	
    """
    



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
NavalAutocannon = "74AE2FE56E620000"
AutocannonTypeArme = "F46CA274AE2F0000"
TwinAutocannonTypeArme = "74AE2FE5ECF21E00"
QuadAutocannonTypeArme = "74AE2F656AEA1B00"
GatlingGunTypeArme = "ECECC6B919010000"
CIWSTypeArme = "5D38350000000000"

SSMTypeArme = "57D7010000000000"

MainGunTypeArme = "B31E95B36B5E0000"


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

def Caliber(caliber):
    out = """<matchcondition type="property" property="Caliber">"""+caliber+"""</matchcondition>"""
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
        		"""                    +Caliber(caliber)+"""
        		"""                    +SalvoLength(salvoLength)
                
        changes += """			"""    +setDamages(HE, HERadi, SupRadi)+"""
        		"""                    +setSalvoSupply(supply)

    elif bombTypeArme == ATClusterBombTypeArme:
        conditions += """			"""+TypeArme(bombTypeArme)+"""
        		"""                    +Caliber(caliber)+"""
        		"""                    +SalvoLength(salvoLength)
                
        changes += """			"""    +setDamages(HE, HERadi, SupRadi)+"""
        		"""                    +setSalvoSupply(supply)+"""
        		"""                    +setArme("HE")#set it to HE
        
    out = """
    <!-- change property of PatchName -->
   	<ndfpatch ndf="pc\ndf\patchable\gfx\everything.ndfbin" table="TAmmunition" name="PatchName">
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
    xmlOutput += """<wargamepatch>"""

    HEBombWeights = [227,250,340,400,500]
    HEBombDamages = {
                    227:
                        ["2C8C0C0300000000",16,370],
                    250:
                        ["2C1C180300000000",17,382],
                    340:
                        ["2C1C140400000000",19,423],
                    400:
                        ["2C1C040500000000",20,447],
                    500:
                        ["2C1C040600000000",21,481]}
    HEsalvoLengths = [2,3,4,5,6,8,10,12,14,25,30]
    
    CLUSBombWeights = [245,340,450,500]
    CLUSBombDamages = {
                    245:
                        ["2C6C140300000000",8,379],
                    340:
                        ["2C1C140400000000",9,423],
                    450:
                        ["2C1C180500000000",10,465],
                    500:
                        ["2C1C040600000000",11,481]}
    CLUSsalvoLengths = [2,4,5,6,8,12]
    
    for i in range(len(HEBombWeights)):
        for j in range(len(HEsalvoLengths)):
            bombData = HEBombDamages[HEBombWeights[i]]
            supplyRef = HEBombWeights[i]

            salvoLength = HEsalvoLengths[j]
            supply = supplyRef * salvoLength * HESupplyFactor
            bombPatch(patchName = str(HEBombWeights[i])+" kg HE bomb, salvo length "+str(HEsalvoLengths[j]), 
                        bombTypeArme = HEBombTypeArme,
                        caliber = bombData[0], 
                        HE = bombData[1], 
                        HERadi = bombData[2], 
                        SupRadi = bombData[2]*HESupRadiFactor, 
                        salvoLength = salvoLength,
                        supply = supply)
            
    bombPatch("Retarded 227kg HE Bomb, salvo length 2", 
              RetardedHEBombTypeArme,
              HEBombDamages[227][0], 
              HEBombDamages[227][1],
              HEBombDamages[227][2],
              HEBombDamages[227][2]*2,
              2,
              227*2*3)
    
    bombPatch("Retarded 227kg HE Bomb, salvo length 12", 
              RetardedHEBombTypeArme,
              HEBombDamages[227][0], 
              HEBombDamages[227][1],
              HEBombDamages[227][2],
              HEBombDamages[227][2]*2,
              12,
              227*12*3)
    
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
   	<ndfpatch ndf="pc\ndf\patchable\gfx\everything.ndfbin" table="TAmmunition" name="PatchName">
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
    global xmlOutput
    """
    unitPriceListExample = {"M/727 HAWK"         :["306F4AC8805C0000",40,[0,8,6,0,0]],
                            "AMX-30 ROLAND"      :["0EB6581907000000",45,[0,8,6,0,0]],
                            "TRACKED RAPIER 2000":["4B07DDAA5B9B1C00",55,[0,6,4,0,0]]
                            }
    """
    for unit in units.keys():
        amounts = ""
        for i in range(5):
            decimalAmount = units[unit][2][i]*amountFactor
            newAmount = int(decimalAmount + (1-decimalAmount%1)) if decimalAmount%1>=0.5 else int(decimalAmount)
            if newAmount < 0:
                raise ValueError("Amount cannot be negative.")
            amounts += """<change operation="set" property="MaxDeployableAmount" key=\""""
            amounts += str(i)
            amounts += """\" type="Int32">"""+str(newAmount)+"""</change>
            """
        price = str(priceBuff(units[unit][1],priceFactor))
        out = """
    <!-- change price of PatchName-->
	<ndfpatch ndf="pc\ndf\patchable\gfx\everything.ndfbin" table="TUniteAuSolDescriptor" name="PatchName">
		<matchconditions>
			<matchcondition type="property" property="NameInMenuToken">"""+units[unit][0]+"""</matchcondition>
		</matchconditions>
		<changes>
			<change operation="set" property="ProductionPrice" key="0" type="Int32">"""+price+"""</change>
            """+amounts+"""		
        </changes>
	</ndfpatch>\n"""
        out = out.replace("PatchName", unit)
        xmlOutput += out
        
def tankAmount(price):
    priceLine = [5,25,40,   50,60,70,   90,110,125,     140,150,165,    180]
    amountCat = [[0,24,18,0,0],#5
                 [0,20,16,0,0],#25
                 [0,16,12,0,0],#40
                 
                 [0,14,10,0,0],#50
                 [0,12,8,0,0],#60
                 [0,10,7,0,0],#70
                 
                 [0,8,6,0,0],#90 
                 [0,7,5,0,0],#110 #None in Vanilla
                 [0,6,4,0,0],#125 #110 in Vanilla
                 
                 [0,5,4,0,0],#140 #125 in Vanilla
                 [0,4,3,0,0],#150 #140 in Vanilla
                 [0,3,2,0,0],#165 #150 in Vanilla
                 
                 [0,2,0,1,0]]#180 #165 in Vanilla
    amount = None
    for i, line in enumerate(priceLine):
        if price>=line:
            amount = amountCat[i]
    if amount == None:
        raise ValueError("price return no matched amount")
    return amount

def GeneralPatch(table, patchName, conditions, changes):
    global xmlOutput
        
    out = """
    
    <!-- change property of PatchName -->
   	<ndfpatch ndf="pc\ndf\patchable\gfx\everything.ndfbin" table=\""""+table+"""\" name="PatchName">
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
   	<ndfpatch ndf="pc\ndf\patchable\gfx\everything.ndfbin" table="TAmmunition" name="PatchName">
       	<matchconditions>
            """+conditions+"""
   		</matchconditions>
           
   		<changes>
            """+changes+"""
   		</changes>
   	</ndfpatch>"""
    out = out.replace("PatchName", patchName)
    xmlOutput += out

maxLength = 130
def AddSpaceTo2Var(prefix, variable, connec, value, suffix):
    totLength = (len(prefix) + len(variable) + len(connec) + len(str(value)) + len(suffix))
    if totLength <= maxLength:
        space = ""
        for i in range(maxLength-totLength):
            space +=" "
        connec = connec[:-1] + space + connec[-1]
    else:
        raise ValueError("The max length is set too short")
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
        ret += AddSpaceTo2Var(prefix, variable, connec, value, suffix)
    return ret

def ReferenceCondition(table, tableConditions):
    ret = ""
    ret += """<matchcondition type="references" table=\""""+table+"""">
				<matchconditions>
                    """+addTabsBetweenLines(string = tableConditions, tabCount = 2)+"""
				</matchconditions>
			</matchcondition>
    
    """
    return ret

def accInputCheck(acc):
    if acc[0] <0.05 or acc[0]>1:
        raise ValueError("stationary acc[0] must be in interval [0.05,1]")
    if acc[1] > acc[0]:
        raise ValueError("stationary acc[0] must >= movement acc[1]")
    if acc[1] <0.05:
        raise ValueError("movement acc[1] must >=0.05")
    if int(acc[0]*100)%5 != 0 or int(acc[1]*100)%5 != 0:
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
            </matchcondition>\n"""
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

def DictChange(prop, key, typeValuePair):
    ret = ""
    ret += """<change operation="set" property=\""""+prop+"""\" key=\""""+key+"""\" type=\""""+typeValuePair[0]+"""\">"""+str(typeValuePair[1])+"""</change>"""
    return ret

def GeneralChanges(**kwargs):
    ret = ""
    for kwarg in kwargs.keys():
        prefix = """<change operation="set" property=\""""
        variable = kwarg #auto convert to string
        connec1 = """\" type=\""""
        vType = kwargs[kwarg][0]
        connec2 = """\">"""
        value = kwargs[kwarg][1]
        suffix = """</change>\n   	   	    """
        ret += AddSpaceTo3Var(prefix, variable, connec1, vType, connec2, value, suffix)
    return ret

def TAmmuChanges(acc = None, **kwargs):
    #Float32, UInt32, Boolean
    ret = ""
    ret += GeneralChanges(**kwargs)
    if acc:
        accInputCheck(acc)
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
    xp = [0,  2.5,   12,   25,    60,   160]
    fp = [0, 2500, 5000, 6000,  8400, 15000]
    if not shown:
        distanceScale = ""
        for i in range(len(xp)):
            distanceScale += str(xp[i])+" real km = "+str(fp[i])+" game m\n"
        print(distanceScale)
        shown = True
            
    if real_distance_km < xp[0]:
        raise ValueError("Input distance out of interpolation boundary(" + str(xp[0])+" km)!")
    interp = np.interp(real_distance_km,xp,fp)
    if real_distance_km <= 12:
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
            ret += TAmmuChanges(PorteeMinimaleBateaux    = ["Float32",ground[0]])
        if ground[1]:
            ret += TAmmuChanges(PorteeMaximaleBateaux    = ["Float32",ground[1]])  
    else:
        if ground[0]:
            ret += TAmmuChanges(PorteeMinimale           = ["Float32",ground[0]],
                                PorteeMinimaleBateaux    = ["Float32",ground[0]])
        if ground[1]:
            ret += TAmmuChanges(PorteeMaximale           = ["Float32",ground[1]],
                                PorteeMaximaleBateaux    = ["Float32",ground[1]])  
        
    if helo[0]:
        ret += TAmmuChanges(PorteeMinimaleTBA        = ["Float32",helo[0]])
    if helo[1]:
        ret += TAmmuChanges(PorteeMaximaleTBA        = ["Float32",helo[1]])  
        
    if air[0]:
        ret += TAmmuChanges(PorteeMinimaleHA         = ["Float32",air[0]])
    if air[1]:
        ret += TAmmuChanges(PorteeMaximaleHA         = ["Float32",air[1]])  
        
    if projec[0]:
        ret += TAmmuChanges(PorteeMinimaleProjectile = ["Float32",projec[0]])
    if projec[1]:
        ret += TAmmuChanges(PorteeMaximaleProjectile = ["Float32",projec[1]])  
    return ret

def TAmmuChangesDisp(disp = [None, None]):
    ret = ""
    if disp[0]:
            ret += TAmmuChanges(DispersionAtMinRange = ["Float32", disp[0]])
    if disp[1]:
            ret += TAmmuChanges(DispersionAtMaxRange = ["Float32", disp[1]])  
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
        if HEval>=1:
            HEval = round(HEval/0.5)*0.5
        ret += TAmmuChanges(PhysicalDamages             = ["Float32", HEval])
    if HE[1]:
        ret += TAmmuChanges(RadiusSplashPhysicalDamages = ["Float32", HE[1]])
    if Sup[0]:
        ret += TAmmuChanges(SuppressDamages             = ["Float32", Sup[0]])
    if Sup[1]:
        ret += TAmmuChanges(RadiusSplashSuppressDamages = ["Float32", Sup[1]])
    return ret
    
def TAmmuChangesArme(ammoType, AP = 0):
    """ammoType = (one of the following) 
            Bullet, HMG, HE, KE, HEAT
       AP is used for KE/HEAT ammoType only"""
    Arme = {"Bullet":"null", "HMG":"1", "HE":"3"}
    if ammoType == "KE":
        if AP<1 or AP >30:
            raise ValueError("AP Value has to be in range [1,30]")
        return TAmmuChanges(Arme = ["UInt32", 4+int(AP)])
    elif ammoType == "HEAT":
        if AP<1 or AP >30:
            raise ValueError("AP Value has to be in range [1,30]")
        return TAmmuChanges(Arme = ["UInt32", 34+int(AP)])
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






