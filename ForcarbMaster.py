from IPython import get_ipython
get_ipython().magic('reset -sf')

#from operator import add
#from collections import Counter
import matrixFunctions
import numpy as np
np.set_printoptions(threshold=np.nan)
import csv
import os
import pandas as pd
import math
from pandas import DataFrame
from datetime import datetime
import winsound
#from __future__ import division

startTime = datetime.now()     
   
   
######## user input
# list items here that require changing depending on objective:   targets, age_cf, AR rate, spp mix, hwp factors  
# check trailing zeros commenting!
#   soil = 81
#   HWP for FM ask kb
#    Ci=FM user-defined, It equals 0 in AR  == pools 32 & 33
    
######## file management
    
#os.chdir("D:\\Data\\Cloudstation\\Notes & work\\IrishLandUSes\\Matrix")
os.chdir("D:\\Documents\\Cloudstation\\Notes & work\\IrishLandUSes\\Matrix")

######## main input file
#df = pd.read_csv("Files/FinalAR_Actual_newCai.csv", names = ['FT', 'YC','Age', 'Area', 'Litter', 'Stump', 'DW', 'Volha','CAI'])
df = pd.read_csv("Test7\\AR_fgb_400_nosmooth.csv", names = ['FT', 'YC','Age', 'Area', 'Litter', 'Stump', 'DW', 'Volha','CAI',' BiomassAG', ' MerchBark', ' OtherWood', ' Foliage', 'AreaAffor'])

######## new Affor Area
#afforArea = pd.read_csv("Test3/afforArea.csv", names = ['cohort','step','afforArea'])

######## Harvest targets, Clearfell & Thinning rules by year
with open('Test3\HarvestTargets.csv', mode='r') as infile:
    reader = csv.reader(infile)
    HarvTHparm = dict((rows[0],rows[1]) for rows in reader)   #p2
with open('Test3\\HarvestTargets.csv', mode='r') as infile:
    reader = csv.reader(infile)    
    HarvCFparm = dict((rows[0],rows[2]) for rows in reader) 
#with open('HarvestTargets.csv', mode='r') as infile:
#    reader = csv.reader(infile)     
#    HarvTHparm = dict((rows[0],rows[3]) for rows in reader) 
#with open('HarvestTargets.csv', mode='r') as infile:
#    reader = csv.reader(infile)     
#    HarvCFparm = dict((rows[0],rows[4]) for rows in reader)  
##        mydict = {rows[0]:rows[1] for rows in reader}   #p3    

with open('Test3\\newClearfellRules.csv', mode='r') as infile:
    reader = csv.reader(infile)
    CF_AGE_MIN = dict((rows[0],rows[1]) for rows in reader)
with open('Test3\\newClearfellRules.csv', mode='r') as infile:
    reader = csv.reader(infile)
    CF_VOLHA = dict((rows[0],rows[3]) for rows in reader)
    
with open('Test3\\newThinningHarvestRules.csv', mode='r') as infile:
    reader = csv.reader(infile)
    TH_AGE_MIN = dict((rows[0],rows[1]) for rows in reader)
with open('Test3\\newThinningHarvestRules.csv', mode='r') as infile:
    reader = csv.reader(infile)
    TH_FREQ = dict((rows[0],rows[3]) for rows in reader)    
#    TH_VOLHA = dict((rows[0],rows[3]) for rows in reader)


######## Biomass parameters
inParm1 = pd.read_csv("Files\\BmEq1.csv", names = ['cohort','1a','1b','vlim', 'minlim'])
inParm2 = pd.read_csv("Files\\BmEq2.csv", names = ['cohort','2k','2a','2b','fbnlim'])
inParm3 = pd.read_csv("Files\\BmEq3.csv", names = ['cohort','3k','3a','3b','fbslim'])
inParm4 = pd.read_csv("Files\\BmEq4.csv", names = ['cohort','4a','4b'])  #,'fbslim'])
inParm5 = pd.read_csv("Files\\BmEq5.csv", names = ['cohort','a1','a2','a3','b1','b2','b3','c1','c2','c3','volLimit'])  
inParm6 = pd.read_csv("Files\\BmEq6.csv", names = ['cohort','6a','6b', 'biomassab'])  
    
    
######## disturbance files 
with open('Files\\disturbance_matrices\\fire.csv', mode = 'r') as infile:
    firematrix = infile.readlines()     
with open('Files\\disturbance_matrices\\thin.csv', mode = 'r') as infile:
    thinmatrix = infile.readlines() 
with open('Files\\disturbance_matrices\\cf.csv', mode = 'r') as infile:
    cfmatrix = infile.readlines() 
with open('Files\\disturbance_matrices\\affor.csv', mode = 'r') as infile:
    afformatrix = infile.readlines() 
with open('Files\\disturbance_matrices\\defor.csv', mode = 'r') as infile:
    deformatrix = infile.readlines() 

   
######## DOM parameters
DOM = pd.read_csv("Files\\DOMparams.csv", names = ['DOM_FoliageSW','DOM_FoliageHW', 'DOM_STO', 'DOM_BranchSW', 'DOM_BranchHW', 'DOM_StemSnagSW', 'DOM_StemSnagHW', 'DOM_BranchSnagSW', 'DOM_BranchSnagHW','DOM_CoarseRoot','DOM_FRTO'])  #, 'DOM_CoarseRoot','DOM_FRTO','DOM_OWTO',''])
  
######## DisturbancEvent parameters
TARG = pd.read_csv("Test3\\targetsFileNewCF.csv", names = ['Species','Amount', 'Step'])  #, 'DOM_BranchSW', 'DOM_BranchHW', 'DOM_StemSnagSW', 'DOM_StemSnagHW', 'DOM_BranchSnagSW', 'DOM_BranchSnagHW'])  #, 'DOM_CoarseRoot','DOM_FRTO','DOM_OWTO',''])
TARGth = pd.read_csv("Test3\\targetsFileNewTH.csv", names = ['Species','Amount', 'Step'])  #, 'DOM_BranchSW', 'DOM_BranchHW', 'DOM_StemSnagSW', 'DOM_StemSnagHW', 'DOM_BranchSnagSW', 'DOM_BranchSnagHW'])  #, 'DOM_CoarseRoot','DOM_FRTO','DOM_OWTO',''])

######## HWP parameters
HWP = pd.read_csv("Files\\HWPparams.csv", names = ['dummy', 'halfLife', 'frac_th', 'frac_cf', 'carb_frac'])


#sp = 'IE_Cmix'
#step = 4
#fist = TARG[(TARG['Species'] == sp) & (TARG['Step'] == step)]
#targetVolume = fist.iloc[[0],[1]]
#
#def cftarget(TARG, species, step):
#    sp = species
#    step = step
#    line = TARG[(TARG['Species'] == sp) & (TARG['Step'] == step)]
#    targetcf = line.iloc[[0],[1]]
#    return targetcf
    
########  output file(s)
commaout = open('Test7\\Output_Test7_affor_nodist_fgb_400ha_noSmooth_ucd2.csv',mode='w', newline = '')
a = csv.writer(commaout, dialect='excel', delimiter=',')  
#prevout = open('Files/prevarea_out.csv',mode='wb')
#b = csv.writer(prevout, dialect='excel', delimiter=',')  
headers = 'Cohort', ' Year', ' Age', ' Area', ' VolPerHa', ' StandingVol', ' Thin/CF volume (if any)'  #' Standing Vol',
a.writerow(headers)
output = (["____________________________________________________________________"])        
a.writerow(output)
output = ([" "])        
a.writerow(output)
    
    
######## cohort managment
PA = DataFrame(df, columns = ['FT', 'YC','Age', 'Area', 'Litter', 'Stump', 'DW', 'Volha','CAI',' BiomassAG', ' MerchBark', ' OtherWood', ' Foliage', 'AreaAffor'])
PA12 = PA[PA.FT == 'PA12']
endpoint_PA12 = len(PA12.index)
PA12 = PA12.values
PA16 = PA[PA.FT == 'PA16']
endpoint_PA16 = len(PA16.index)
PA16 = PA16.values
PA20 = PA[PA.FT == 'PA20']
endpoint_PA20 = len(PA20.index)
PA20 = PA20.values
PA24 = PA[PA.FT == 'PA24']
endpoint_PA24 = len(PA24.index)
PA24 = PA24.values
PA30 = PA[PA.FT == 'PA30']
endpoint_PA30 = len(PA30.index)
PA30 = PA30.values
OC = PA[PA.FT == 'OC']
endpoint_OC = len(OC.index)
OC = OC.values
FGB = PA[PA.FT == 'FGB']
endpoint_FGB = len(FGB.index)
FGB = FGB.values
SGB = PA[PA.FT == 'SGB']
endpoint_SGB = len(SGB.index)
SGB = SGB.values
CBmix = PA[PA.FT == 'CBmix']
endpoint_CBmix = len(CBmix.index)
CBmix = CBmix.values
Cmix = PA[PA.FT == 'Cmix']
endpoint_Cmix = len(Cmix.index)
Cmix = Cmix.values
PS12 = PA[PA.FT == 'PS12']
endpoint_PS12 = len(PS12.index)
PS12 = PS12.values
PS20 = PA[PA.FT == 'PS20']
endpoint_PS20 = len(PS20.index)
PS20 = PS20.values

CBmixp = PA[PA.FT == 'CBmixp']
endpoint_CBmixp = len(CBmixp.index)
CBmixp = CBmixp.values
Cmixp = PA[PA.FT == 'Cmixp']
endpoint_Cmixp = len(Cmixp.index)
Cmixp = Cmixp.values
PA12p = PA[PA.FT == 'PA12p']
endpoint_PA12p = len(PA12p.index)
PA12p = PA12p.values
PA16p = PA[PA.FT == 'PA16p']
endpoint_PA16p = len(PA16p.index)
PA16p = PA16p.values
PA20p = PA[PA.FT == 'PA20p']
endpoint_PA20p = len(PA20p.index)
PA20p = PA20p.values
PA24p = PA[PA.FT == 'PA24p']
endpoint_PA24p = len(PA24p.index)
PA24p = PA24p.values
PA30p = PA[PA.FT == 'PA30p']
endpoint_PA30p = len(PA30p.index)
PA30p = PA30p.values
OCp = PA[PA.FT == 'OCp']
endpoint_OCp = len(OCp.index)
OCp = OCp.values
FGBp = PA[PA.FT == 'FGBp']
endpoint_FGBp = len(FGBp.index)
FGBp = FGBp.values
SGBp = PA[PA.FT == 'SGBp']
endpoint_SGBp = len(SGBp.index)
SGBp = SGBp.values
PS12p = PA[PA.FT == 'PS12p']
endpoint_PS12p = len(PS12p.index)
PS12p = PS12p.values
PS20p = PA[PA.FT == 'PS20p']
endpoint_PS20p = len(PS20p.index)
PS20p = PS20p.values



######## more cohort management
######## begin cohort re-naming:
cohortlist = 24 #(1,2)   # PA12, PA16, etc.
for cohort in range(1):  # cohortlist
    if cohort == 0: 
        prevarea_FGB = [None]*endpoint_FGB
        prevvol_FGB = [None]*endpoint_FGB
        prev_volha_FGB = [None]*endpoint_FGB
        prevarea_FGB, prevvol_FGB, prev_volha_FGB = matrixFunctions.previous(FGB, endpoint_FGB, prevarea_FGB, prevvol_FGB, prev_volha_FGB)   
#        prev_volha_FGB = prevvol_FGB / prevarea_FGB  
        bm_cohort = 3        
#        prevarea_PA12 = [None]*endpoint_PA12
#        prevvol_PA12 = [None]*endpoint_PA12
#        prev_volha_PA12 = [None]*endpoint_PA12
#        prevarea_PA12, prevvol_PA12, prev_volha_PA12 = matrixFunctions.previous(PA12, endpoint_PA12, prevarea_PA12, prevvol_PA12, prev_volha_PA12)
#        bm_cohort = 0
#    if cohort == 1: 
#        prevarea_PA16 = [None]*endpoint_PA16
#        prevvol_PA16 = [None]*endpoint_PA16
#        prev_volha_PA16 = [None]*endpoint_PA16
#        prevarea_PA16, prevvol_PA16, prev_volha_PA16 = matrixFunctions.previous(PA16, endpoint_PA16, prevarea_PA16, prevvol_PA16, prev_volha_PA16) 
##        prev_volha_PA16 = prevvol_PA16 / prevarea_PA16        
#        bm_cohort = 0
#    if cohort == 2:  
#        prevarea_PA20 = [None]*endpoint_PA20
#        prevvol_PA20 = [None]*endpoint_PA20
#        prev_volha_PA20 = [None]*endpoint_PA20
#        prevarea_PA20, prevvol_PA20, prev_volha_PA20 = matrixFunctions.previous(PA20, endpoint_PA20, prevarea_PA20, prevvol_PA20, prev_volha_PA20)  
##        prev_volha_PA20 = prevvol_PA20 / prevarea_PA20
#        bm_cohort = 0
#    if cohort == 3: 
#        prevarea_PA24 = [None]*endpoint_PA24
#        prevvol_PA24 = [None]*endpoint_PA24
#        prev_volha_PA24 = [None]*endpoint_PA24
#        prevarea_PA24, prevvol_PA24, prev_volha_PA24 = matrixFunctions.previous(PA24, endpoint_PA24, prevarea_PA24, prevvol_PA24, prev_volha_PA24)  
##        prev_volha_PA24 = prevvol_PA24 / prevarea_PA24
#        bm_cohort = 0
#    if cohort == 4: 
#        prevarea_PA30 = [None]*endpoint_PA30
#        prevvol_PA30 = [None]*endpoint_PA30
#        prev_volha_PA30 = [None]*endpoint_PA30
#        prevarea_PA30, prevvol_PA30, prev_volha_PA30 = matrixFunctions.previous(PA30, endpoint_PA30, prevarea_PA30, prevvol_PA30, prev_volha_PA30)  
##        prev_volha_PA30 = prevvol_PA30 / prevarea_PA30
#        bm_cohort = 0  
#    if cohort == 5: 
#        prevarea_PS12 = [None]*endpoint_PS12
#        prevvol_PS12 = [None]*endpoint_PS12
#        prev_volha_PS12 = [None]*endpoint_PS12
#        prevarea_PS12, prevvol_PS12, prev_volha_PS12 = matrixFunctions.previous(PS12, endpoint_PS12, prevarea_PS12, prevvol_PS12, prev_volha_PS12)  
##        prev_volha_PS12 = prevvol_PS12 / prevarea_PS12      
#        bm_cohort = 1        
#    if cohort == 6:
#        prevarea_PS20 = [None]*endpoint_PS20
#        prevvol_PS20 = [None]*endpoint_PS20
#        prev_volha_PS20 = [None]*endpoint_PS20
#        prevarea_PS20, prevvol_PS20, prev_volha_PS20 = matrixFunctions.previous(PS20, endpoint_PS20, prevarea_PS20, prevvol_PS20, prev_volha_PS20)  
##        prev_volha_PS20 = prevvol_PS20 / prevarea_PS20
#        bm_cohort = 1 
#    if cohort == 7:  
#        prevarea_OC = [None]*endpoint_OC
#        prevvol_OC = [None]*endpoint_OC
#        prev_volha_OC = [None]*endpoint_OC
#        prevarea_OC, prevvol_OC, prev_volha_OC = matrixFunctions.previous(OC, endpoint_OC, prevarea_OC, prevvol_OC, prev_volha_OC)  
##        prev_volha_OC = prevvol_OC / prevarea_OC
#        bm_cohort = 2
#    if cohort == 8:
#        prevarea_Cmix = [None]*endpoint_Cmix
#        prevvol_Cmix = [None]*endpoint_Cmix
#        prev_volha_Cmix = [None]*endpoint_Cmix
#        prevarea_Cmix, prevvol_Cmix, prev_volha_CBmix = matrixFunctions.previous(Cmix, endpoint_Cmix, prevarea_Cmix, prevvol_Cmix, prev_volha_Cmix)  
##        prev_volha_Cmix = prevvol_Cmix / prevarea_Cmix
#        bm_cohort = 2
#    if cohort == 9:
#        prevarea_CBmix = [None]*endpoint_CBmix
#        prevvol_CBmix = [None]*endpoint_CBmix
#        prev_volha_CBmix = [None]*endpoint_CBmix
#        prevarea_CBmix, prevvol_CBmix, prev_volha_CBmix = matrixFunctions.previous(CBmix, endpoint_CBmix, prevarea_CBmix, prevvol_CBmix, prev_volha_CBmix)  
##        prev_volha_CBmix = prevvol_CBmix / prevarea_CBmix
#        bm_cohort = 3
#    if cohort == 10:
#        prevarea_FGB = [None]*endpoint_FGB
#        prevvol_FGB = [None]*endpoint_FGB
#        prev_volha_FGB = [None]*endpoint_FGB
#        prevarea_FGB, prevvol_FGB, prev_volha_FGB = matrixFunctions.previous(FGB, endpoint_FGB, prevarea_FGB, prevvol_FGB, prev_volha_FGB)   
##        prev_volha_FGB = prevvol_FGB / prevarea_FGB
#        bm_cohort = 3
#    if cohort == 11:
#        prevarea_SGB = [None]*endpoint_SGB
#        prevvol_SGB = [None]*endpoint_SGB
#        prev_volha_SGB = [None]*endpoint_SGB
#        prevarea_SGB, prevvol_SGB, prev_volha_SGB = matrixFunctions.previous(SGB, endpoint_SGB, prevarea_SGB, prevvol_SGB, prev_volha_SGB)  
##        prev_volha_SGB = prevvol_SGB / prevarea_SGB
#        bm_cohort = 4
#                
#    if cohort == 12: 
#        prevarea_PA12p = [None]*endpoint_PA12p
#        prevvol_PA12p = [None]*endpoint_PA12p
#        prev_volha_PA12p = [None]*endpoint_PA12p
#        prevarea_PA12p, prevvol_PA12p, prev_volha_PA12p = matrixFunctions.previous(PA12p, endpoint_PA12p, prevarea_PA12p, prevvol_PA12p, prev_volha_PA12p)
#        bm_cohort = 0
#    if cohort == 13: 
#        prevarea_PA16p = [None]*endpoint_PA16p
#        prevvol_PA16p = [None]*endpoint_PA16p
#        prev_volha_PA16p = [None]*endpoint_PA16p
#        prevarea_PA16p, prevvol_PA16p, prev_volha_PA16p = matrixFunctions.previous(PA16p, endpoint_PA16p, prevarea_PA16p, prevvol_PA16p, prev_volha_PA16p) 
##        prev_volha_PA16 = prevvol_PA16 / prevarea_PA16        
#        bm_cohort = 0
#    if cohort == 14:  
#        prevarea_PA20p = [None]*endpoint_PA20p
#        prevvol_PA20p = [None]*endpoint_PA20p
#        prev_volha_PA20p = [None]*endpoint_PA20p
#        prevarea_PA20p, prevvol_PA20p, prev_volha_PA20p = matrixFunctions.previous(PA20p, endpoint_PA20p, prevarea_PA20p, prevvol_PA20p, prev_volha_PA20p)  
##        prev_volha_PA20 = prevvol_PA20 / prevarea_PA20
#        bm_cohort = 0
#    if cohort == 15: 
#        prevarea_PA24p = [None]*endpoint_PA24p
#        prevvol_PA24p = [None]*endpoint_PA24p
#        prev_volha_PA24p = [None]*endpoint_PA24p
#        prevarea_PA24p, prevvol_PA24p, prev_volha_PA24p = matrixFunctions.previous(PA24p, endpoint_PA24p, prevarea_PA24p, prevvol_PA24p, prev_volha_PA24p)  
##        prev_volha_PA24 = prevvol_PA24 / prevarea_PA24
#        bm_cohort = 0
#    if cohort == 16: 
#        prevarea_PA30p = [None]*endpoint_PA30p
#        prevvol_PA30p = [None]*endpoint_PA30p
#        prev_volha_PA30p = [None]*endpoint_PA30p
#        prevarea_PA30p, prevvol_PA30p, prev_volha_PA30p = matrixFunctions.previous(PA30p, endpoint_PA30p, prevarea_PA30p, prevvol_PA30p, prev_volha_PA30p)  
##        prev_volha_PA30 = prevvol_PA30 / prevarea_PA30
#        bm_cohort = 0  
#    if cohort == 17: 
#        prevarea_PS12p = [None]*endpoint_PS12p
#        prevvol_PS12p = [None]*endpoint_PS12p
#        prev_volha_PS12p = [None]*endpoint_PS12p
#        prevarea_PS12p, prevvol_PS12p, prev_volha_PS12p = matrixFunctions.previous(PS12p, endpoint_PS12p, prevarea_PS12p, prevvol_PS12p, prev_volha_PS12p)  
##        prev_volha_PS12 = prevvol_PS12 / prevarea_PS12      
#        bm_cohort = 1        
#    if cohort == 18:
#        prevarea_PS20p = [None]*endpoint_PS20p
#        prevvol_PS20p = [None]*endpoint_PS20p
#        prev_volha_PS20p = [None]*endpoint_PS20p
#        prevarea_PS20p, prevvol_PS20p, prev_volha_PS20p = matrixFunctions.previous(PS20p, endpoint_PS20p, prevarea_PS20p, prevvol_PS20p, prev_volha_PS20p)  
##        prev_volha_PS20 = prevvol_PS20 / prevarea_PS20
#        bm_cohort = 1 
#    if cohort == 19:  
#        prevarea_OCp = [None]*endpoint_OCp
#        prevvol_OCp = [None]*endpoint_OCp
#        prev_volha_OCp = [None]*endpoint_OCp
#        prevarea_OCp, prevvol_OCp, prev_volha_OCp = matrixFunctions.previous(OCp, endpoint_OCp, prevarea_OCp, prevvol_OCp, prev_volha_OCp)  
##        prev_volha_OC = prevvol_OC / prevarea_OC
#        bm_cohort = 2
#    if cohort == 20:
#        prevarea_Cmixp = [None]*endpoint_Cmixp
#        prevvol_Cmixp = [None]*endpoint_Cmixp
#        prev_volha_Cmixp = [None]*endpoint_Cmixp
#        prevarea_Cmixp, prevvol_Cmixp, prev_volha_CBmixp = matrixFunctions.previous(Cmixp, endpoint_Cmixp, prevarea_Cmixp, prevvol_Cmixp, prev_volha_Cmixp)  
##        prev_volha_Cmix = prevvol_Cmix / prevarea_Cmix
#        bm_cohort = 2
#    if cohort == 21:
#        prevarea_CBmixp = [None]*endpoint_CBmixp
#        prevvol_CBmixp = [None]*endpoint_CBmixp
#        prev_volha_CBmixp = [None]*endpoint_CBmixp
#        prevarea_CBmixp, prevvol_CBmixp, prev_volha_CBmixp = matrixFunctions.previous(CBmixp, endpoint_CBmixp, prevarea_CBmixp, prevvol_CBmixp, prev_volha_CBmixp)  
##        prev_volha_CBmix = prevvol_CBmix / prevarea_CBmix
#        bm_cohort = 3
#    if cohort == 22:
#        prevarea_FGBp = [None]*endpoint_FGBp
#        prevvol_FGBp = [None]*endpoint_FGBp
#        prev_volha_FGBp = [None]*endpoint_FGBp
#        prevarea_FGBp, prevvol_FGBp, prev_volha_FGBp = matrixFunctions.previous(FGBp, endpoint_FGBp, prevarea_FGBp, prevvol_FGBp, prev_volha_FGBp)   
##        prev_volha_FGB = prevvol_FGB / prevarea_FGB
#        bm_cohort = 3
#    if cohort == 23:
#        prevarea_SGBp = [None]*endpoint_SGBp
#        prevvol_SGBp = [None]*endpoint_SGBp
#        prev_volha_SGBp = [None]*endpoint_SGBp
#        prevarea_SGBp, prevvol_SGBp, prev_volha_SGBp = matrixFunctions.previous(SGBp, endpoint_SGBp, prevarea_SGBp, prevvol_SGBp, prev_volha_SGBp)  
##        prev_volha_SGB = prevvol_SGB / prevarea_SGB
#        bm_cohort = 4        

######## initialise variables
thinvolume = 0
prevthinvol = 0
defor = 0 # 1000
deforYear = 350
affor = 0 # 500
afforYear = 250
remainvol = 0
newcohortvol = 0
new_area = 0
thinTotal = 0
sum_sv = 0
sum_hv = 0
annual_sv = 0
annual_hv = 0
areaFelled = 0
clearfell_nextcycle_PA12 = 0 
clearfell_nextcycle_PA16 = 0 
clearfell_nextcycle_PA20 = 0 
clearfell_nextcycle_PA24 = 0 
clearfell_nextcycle_PA30 = 0 
clearfell_nextcycle_PS12 = 0 
clearfell_nextcycle_PS20 = 0 
clearfell_nextcycle_OC = 0
clearfell_nextcycle_Cmix = 0 
clearfell_nextcycle_CBmix = 0 
clearfell_nextcycle_FGB = 0 
clearfell_nextcycle_SGB = 0 
clearfell_nextcycle_PA12p = 0 
clearfell_nextcycle_PA16p = 0 
clearfell_nextcycle_PA20p = 0 
clearfell_nextcycle_PA24p = 0 
clearfell_nextcycle_PA30p = 0 
clearfell_nextcycle_PS12p = 0 
clearfell_nextcycle_PS20p = 0 
clearfell_nextcycle_OCp = 0
clearfell_nextcycle_Cmixp = 0 
clearfell_nextcycle_CBmixp = 0 
clearfell_nextcycle_FGBp = 0 
clearfell_nextcycle_SGBp = 0 
#cohortratio = 0.0833 # 1.0/(cohortlist+1)
#cohortratio_cf = 0.0833 
#inventoryCheck = 0   # this check is used to reset the pools when there is no species eg. SGBp
increment = 1
newatm = 0

######### Biomass & DOM pools (FM) file
#pooldict = {}
#with open("Files/poolinitialisation_input.csv", mode = 'r') as infile:    
#    for line in infile:
#        (key, val) = line.split(',')
#        pooldict[key] = float(val)

# biomass pools initialisation (AR)
pooldict_temp = {}
pooldict_temp['pool01'] = 0  # sw merch
pooldict_temp['pool02'] = 0  # sw foliage
pooldict_temp['pool03'] = 0  # sw other
pooldict_temp['pool04'] = 0  # sw sub-merch
pooldict_temp['pool05'] = 0  # sw coarse roots
pooldict_temp['pool06'] = 0  # sw fine roots
pooldict_temp['pool07'] = 0  # hw merch
pooldict_temp['pool08'] = 0  # hw foliage
pooldict_temp['pool09'] = 0  # hw others
pooldict_temp['pool10'] = 0 # hw sub-merch
pooldict_temp['pool11'] = 0 # hw coarse
pooldict_temp['pool12'] = 0 # hw fine
pooldict_temp['pool13'] = 0 # ag very fast
pooldict_temp['pool14'] = 0 # bg very fast
pooldict_temp['pool15'] = 0 # ag fast
pooldict_temp['pool16'] = 0 # bg fast
pooldict_temp['pool17'] = 0 # medium
pooldict_temp['pool18'] = 0 # ag slow
pooldict_temp['pool19'] = 92 # bg slow    IF PEAT THIS IS 0 ZERO!
pooldict_temp['pool20'] = 0 # sw stem snag
pooldict_temp['pool21'] = 0 # sw branch snag
pooldict_temp['pool22'] = 0 # hw stem snag
pooldict_temp['pool23'] = 0 # hw stem branch
pooldict_temp['pool24'] = 0 # black C
pooldict_temp['pool25'] = 0 # peat
pooldict_temp['pool26'] = 0 # co2
pooldict_temp['pool27'] = 0 # ch4
pooldict_temp['pool28'] = 0 # co 
pooldict_temp['pool29'] = 0 # n20
pooldict_temp['pool30'] = 0 # products
pooldict_temp['pool31'] = 0  # atm
pooldict_temp['pool32'] = 0  # sw_saw
pooldict_temp['pool33'] = 0  # sw_wbp

#pooldict = pooldict_temp.copy()
fullpool = pooldict_temp.copy()
PA12pool = pooldict_temp.copy()
PA16pool = pooldict_temp.copy()
PA20pool = pooldict_temp.copy()
PA24pool =  pooldict_temp.copy()
PA30pool =  pooldict_temp.copy()
PS12pool = pooldict_temp.copy()
PS20pool = pooldict_temp.copy()
OCpool = pooldict_temp.copy()
SGBpool = pooldict_temp.copy()
FGBpool = pooldict_temp.copy()
CBmixpool = pooldict_temp.copy()
Cmixpool = pooldict_temp.copy()
PA12ppool = pooldict_temp.copy()
PA16ppool = pooldict_temp.copy()
PA20ppool = pooldict_temp.copy()
PA24ppool =  pooldict_temp.copy()
PA30ppool =  pooldict_temp.copy()
PS12ppool = pooldict_temp.copy()
PS20ppool = pooldict_temp.copy()
OCppool = pooldict_temp.copy()
SGBppool = pooldict_temp.copy()
FGBppool = pooldict_temp.copy()
CBmixppool = pooldict_temp.copy()
Cmixppool = pooldict_temp.copy()


PA12ppool['pool19'] = 0
PA16ppool['pool19'] = 0
PA20ppool['pool19'] = 0
PA24ppool['pool19'] = 0
PA30ppool['pool19'] = 0
PS12ppool['pool19'] = 0
PS20ppool['pool19'] = 0
OCppool['pool19'] = 0
SGBppool['pool19'] = 0
FGBppool['pool19'] = 0
CBmixppool['pool19'] = 0
Cmixppool['pool19'] = 0

#distReturnInterval = 75
merchBark = 0
otherWoodBark = 0
foliage = 0
fineRoot = 0
coarseRoot = 0
agbiomass = 0
biomassbg = 0
#standAgbiomass = 0
standPool01 = 0
standPool02 = 0
standPool03 = 0
standPool07 = 0
standPool08 = 0
standPool09 = 0
annualAgbiomass = 0
annualBgbiomass = 0 
#  switches
sthin = 0  # 1 if thinning has taken place
sclear = 0 # 1 if clearfell has taken place
sthin_out = 0 # as above except specifically for output
sclear_out = 0
peat = 1   # if peat = 0, then it's mineral
# harwood = 0   if SW, 1 if HW

newStandPA12 = np.zeros([1,14],dtype = int)
newStandPA16 = np.zeros([1,14],dtype = int)
newStandPA20 = np.zeros([1,14],dtype = int)
newStandPA24 = np.zeros([1,14],dtype = int)
newStandPA30 = np.zeros([1,14],dtype = int)
newStandPS12 = np.zeros([1,14],dtype = int)
newStandPS20 = np.zeros([1,14],dtype = int)
newStandOC = np.zeros([1,14],dtype = int)
newStandSGB = np.zeros([1,14],dtype = int)
newStandFGB = np.zeros([1,14],dtype = int)
newStandCmix = np.zeros([1,14],dtype = int)
newStandCBmix = np.zeros([1,14],dtype = int)
newStandPA12p = np.zeros([1,14],dtype = int)
newStandPA16p = np.zeros([1,14],dtype = int)
newStandPA20p = np.zeros([1,14],dtype = int)
newStandPA24p = np.zeros([1,14],dtype = int)
newStandPA30p = np.zeros([1,14],dtype = int)
newStandPS12p = np.zeros([1,14],dtype = int)
newStandPS20p = np.zeros([1,14],dtype = int)
newStandOCp = np.zeros([1,14],dtype = int)
newStandSGBp = np.zeros([1,14],dtype = int)
newStandFGBp = np.zeros([1,14],dtype = int)
newStandCmixp = np.zeros([1,14],dtype = int)
newStandCBmixp = np.zeros([1,14],dtype = int)

oldsumSlow = 0
diffpc = 3000.0

year = 1990   #1906
#startYear = year
standAge = 0
step = 1
targAge = 0

while year < 2060:
    standAge += 1
    targAge += 1
    fullpool = pooldict_temp.copy()
    fullpool['pool19'] = 0
    annualAgbiomass = 0
    annualBgbiomass = 0    
    for cohort in range(1):  # cohortlist    
        ######## stores each cohort's respective variables    
#        pooldict = {}
#        standPool01 = 0
#        standPool02 = 0
#        standPool03 = 0
#        standPool07 = 0
#        standPool08 = 0
#        standPool09 = 0   
#        standAgbiomass = 0
        if cohort == 0:  
            cht = FGB   
            newStand = newStandFGB
            clearfell_nextcycle_cht = clearfell_nextcycle_FGB
            prevarea_cht = prevarea_FGB
            prevvol_cht = prevvol_FGB 
            prev_volha_cht = prev_volha_FGB
            hardwood = 1
            pooldict = FGBpool            
#            cht = PA12
#            newStand = newStandPA12
#            clearfell_nextcycle_cht = clearfell_nextcycle_PA12
#            prevarea_cht = prevarea_PA12
#            prevvol_cht = prevvol_PA12
#            prev_volha_cht = prev_volha_PA12
#            hardwood = 0
#            pooldict = PA12pool
##            TARG.loc[1,cht]
#        elif cohort == 1:  
#            cht = PA16  
#            newStand = newStandPA16
#            clearfell_nextcycle_cht = clearfell_nextcycle_PA16   
#            prevarea_cht = prevarea_PA16
#            prevvol_cht = prevvol_PA16
#            prev_volha_cht = prev_volha_PA16 
#            hardwood = 0
#            pooldict = PA16pool
#        elif cohort == 2: 
#            cht = PA20    
#            newStand = newStandPA20
#            clearfell_nextcycle_cht = clearfell_nextcycle_PA20 
#            prevarea_cht = prevarea_PA20
#            prevvol_cht = prevvol_PA20
#            prev_volha_cht = prev_volha_PA20
#            hardwood = 0
#            pooldict = PA20pool
#        elif cohort == 3: 
#            cht = PA24     
#            newStand = newStandPA24
#            clearfell_nextcycle_cht = clearfell_nextcycle_PA24
#            prevarea_cht = prevarea_PA24
#            prevvol_cht = prevvol_PA24 
#            prev_volha_cht = prev_volha_PA24
#            hardwood = 0
#            pooldict = PA24pool
#        elif cohort == 4:
#            cht = PA30     
#            newStand = newStandPA30
#            clearfell_nextcycle_cht = clearfell_nextcycle_PA30
#            prevarea_cht = prevarea_PA30
#            prevvol_cht = prevvol_PA30 
#            prev_volha_cht = prev_volha_PA30
#            hardwood = 0
#            pooldict = PA30pool
#        elif cohort == 5:
#            cht = PS12       
#            newStand = newStandPS12
#            clearfell_nextcycle_cht = clearfell_nextcycle_PS12
#            prevarea_cht = prevarea_PS12
#            prevvol_cht = prevvol_PS12      
#            prev_volha_cht = prev_volha_PS12   
#            hardwood = 0
#            pooldict = PS12pool
#        elif cohort == 6:
#            cht = PS20  
#            newStand = newStandPS20
#            clearfell_nextcycle_cht = clearfell_nextcycle_PS20
#            prevarea_cht = prevarea_PS20
#            prevvol_cht = prevvol_PS20 
#            prev_volha_cht = prev_volha_PS20
#            hardwood = 0
#            pooldict = PS20pool
#        elif cohort == 7:
#            cht = OC  
#            newStand = newStandOC
#            clearfell_nextcycle_cht = clearfell_nextcycle_OC
#            prevarea_cht = prevarea_OC
#            prevvol_cht = prevvol_OC 
#            prev_volha_cht = prev_volha_OC
#            hardwood = 0
#            pooldict = OCpool
#        elif cohort == 8:
#            cht = Cmix  
#            newStand = newStandCmix
#            clearfell_nextcycle_cht = clearfell_nextcycle_Cmix
#            prevarea_cht = prevarea_Cmix
#            prevvol_cht = prevvol_Cmix 
#            prev_volha_cht = prev_volha_Cmix
#            hardwood = 0
#            pooldict = Cmixpool
#        elif cohort == 9:
#            cht = CBmix       
#            newStand = newStandCBmix
#            clearfell_nextcycle_cht = clearfell_nextcycle_CBmix
#            prevarea_cht = prevarea_CBmix
#            prevvol_cht = prevvol_CBmix 
#            prev_volha_cht = prev_volha_CBmix
#            hardwood = 1
#            pooldict = CBmixpool
#        elif cohort == 10:
#            cht = FGB   
#            newStand = newStandFGB
#            clearfell_nextcycle_cht = clearfell_nextcycle_FGB
#            prevarea_cht = prevarea_FGB
#            prevvol_cht = prevvol_FGB 
#            prev_volha_cht = prev_volha_FGB
#            hardwood = 1
#            pooldict = FGBpool
#        elif cohort == 11:
#            cht = SGB       
#            newStand = newStandSGB
#            clearfell_nextcycle_cht = clearfell_nextcycle_SGB
#            prevarea_cht = prevarea_SGB
#            prevvol_cht = prevvol_SGB 
#            prev_volha_cht = prev_volha_SGB
#            hardwood = 1
#            pooldict = SGBpool
#            
#        if cohort == 12:  
#            cht = PA12p
#            newStand = newStandPA12p
#            clearfell_nextcycle_cht = clearfell_nextcycle_PA12p
#            prevarea_cht = prevarea_PA12p
#            prevvol_cht = prevvol_PA12p
#            prev_volha_cht = prev_volha_PA12p
#            hardwood = 0
#            pooldict = PA12ppool
##            TARG.loc[1,cht]
#        elif cohort == 13:  
#            cht = PA16p     
#            newStand = newStandPA16p
#            clearfell_nextcycle_cht = clearfell_nextcycle_PA16p
#            prevarea_cht = prevarea_PA16p
#            prevvol_cht = prevvol_PA16p
#            prev_volha_cht = prev_volha_PA16p
#            hardwood = 0
#            pooldict = PA16ppool
#        elif cohort == 14: 
#            cht = PA20p 
#            newStand = newStandPA20p
#            clearfell_nextcycle_cht = clearfell_nextcycle_PA20p
#            prevarea_cht = prevarea_PA20p
#            prevvol_cht = prevvol_PA20p
#            prev_volha_cht = prev_volha_PA20p
#            hardwood = 0
#            pooldict = PA20ppool
#        elif cohort == 15: 
#            cht = PA24p
#            newStand = newStandPA24p
#            clearfell_nextcycle_cht = clearfell_nextcycle_PA24p
#            prevarea_cht = prevarea_PA24p
#            prevvol_cht = prevvol_PA24p 
#            prev_volha_cht = prev_volha_PA24p
#            hardwood = 0
#            pooldict = PA24ppool
#        elif cohort == 16:
#            cht = PA30p 
#            newStand = newStandPA30p
#            clearfell_nextcycle_cht = clearfell_nextcycle_PA30p
#            prevarea_cht = prevarea_PA30p
#            prevvol_cht = prevvol_PA30p
#            prev_volha_cht = prev_volha_PA30p
#            hardwood = 0
#            pooldict = PA30ppool
#        elif cohort == 17:
#            cht = PS12p
#            newStand = newStandPS12p
#            clearfell_nextcycle_cht = clearfell_nextcycle_PS12p
#            prevarea_cht = prevarea_PS12p
#            prevvol_cht = prevvol_PS12p   
#            prev_volha_cht = prev_volha_PS12p
#            hardwood = 0
#            pooldict = PS12ppool
#        elif cohort == 18:
#            cht = PS20p
#            newStand = newStandPS20p
#            clearfell_nextcycle_cht = clearfell_nextcycle_PS20p
#            prevarea_cht = prevarea_PS20p
#            prevvol_cht = prevvol_PS20p
#            prev_volha_cht = prev_volha_PS20p
#            hardwood = 0
#            pooldict = PS20ppool
#        elif cohort == 19:
#            cht = OCp
#            newStand = newStandOCp
#            clearfell_nextcycle_cht = clearfell_nextcycle_OCp
#            prevarea_cht = prevarea_OCp
#            prevvol_cht = prevvol_OCp
#            prev_volha_cht = prev_volha_OCp
#            hardwood = 0
#            pooldict = OCppool
#        elif cohort == 20:
#            cht = Cmixp
#            newStand = newStandCmixp
#            clearfell_nextcycle_cht = clearfell_nextcycle_Cmixp
#            prevarea_cht = prevarea_Cmixp
#            prevvol_cht = prevvol_Cmixp
#            prev_volha_cht = prev_volha_Cmixp
#            hardwood = 0
#            pooldict = Cmixppool
#        elif cohort == 21:
#            cht = CBmixp
#            newStand = newStandCBmixp
#            clearfell_nextcycle_cht = clearfell_nextcycle_CBmixp
#            prevarea_cht = prevarea_CBmixp
#            prevvol_cht = prevvol_CBmixp
#            prev_volha_cht = prev_volha_CBmixp
#            hardwood = 1
#            pooldict = CBmixppool
#        elif cohort == 22:
#            cht = FGBp
#            newStand = newStandFGBp
#            clearfell_nextcycle_cht = clearfell_nextcycle_FGBp
#            prevarea_cht = prevarea_FGBp
#            prevvol_cht = prevvol_FGBp
#            prev_volha_cht = prev_volha_FGBp
#            hardwood = 1
#            pooldict = FGBppool
#        elif cohort == 23:
#            cht = SGBp
#            newStand = newStandSGBp
#            clearfell_nextcycle_cht = clearfell_nextcycle_SGBp
#            prevarea_cht = prevarea_SGBp
#            prevvol_cht = prevvol_SGBp
#            prev_volha_cht = prev_volha_SGBp
#            hardwood = 1   
#            pooldict = SGBppool
        standPool01 = 0
        standPool02 = 0
        standPool03 = 0
        standPool07 = 0
        standPool08 = 0
        standPool09 = 0       
        
        ########  affor preparation        
        age_cf = 9999999# int(CF_AGE_MIN[cht[0,0]])  #  9999999
        rotation = age_cf
        age_th =  9999999 #int(TH_AGE_MIN[cht[0,0]])  # 9999999
        thinfreq = 1  #int(TH_FREQ[cht[0,0]])
        volha_cf = int(CF_VOLHA[cht[0,0]])
        age_th_upper = 9999999 #age_cf    #     99999999
        YC_cht = cht[0,1]
        thin_intensity_cht = matrixFunctions.thin_intensity(YC_cht)        
        afforarea = cht[standAge-1,13]   
        afforarea2 = afforarea 
        newarea = 0
#        endpoint_cht = len(cht)
        endpoint_cht = len(newStand)
        endpoint_inv = endpoint_cht
        if clearfell_nextcycle_cht == "NoCF":
            clearfell_nextcycle_cht = 0
        else:
            clearfell_nextcycle_cht = clearfell_nextcycle_cht
#        This line deals with issue when new line is added (stacked)
#        if sstack == 1:
#            standAge -= 1
#            sstack = 0        
        area = [None]*endpoint_cht     
        ageClass = [None]*endpoint_cht 
        volha = [None]*endpoint_cht     
        availablevolume = [None]*endpoint_cht  
        folinc = [None]*endpoint_cht
        owinc = [None]*endpoint_cht
        merchinc = [None]*endpoint_cht
        sumvolcheck1 = 0  
        remainvol = 0
        volIncPostHarvest = 0
        volIncPreHarvest = 0
        volIncNotFelled = 0
        volIncFelled = 0
        volIncFelled2 = 0
        thinvolumecheck = [None]*endpoint_cht
        check_inc = [0]*endpoint_cht
        species = matrixFunctions.speciesLookup(cht[0,0])
        targetthin = 940846  # matrixFunctions.targets(TARGth, species, step) #  940846
        if targAge >= age_cf and targAge <= 45:
            targetvol = matrixFunctions.targets(TARG, species, targAge)
        else:
            targetvol = 0
        targetThVolume = 999999999999 # targetthin*cohortratio   
        area = [None]*endpoint_cht          
########  affor prep
#        for z in range(endpoint_cht):
#            if z == standAge: 
#                afforarea = afforarea
#            else:
#                afforarea = 0              
########  thinning preparation         
        for z in range(endpoint_cht):       
            ageClass[z] = cht[z,2]
            standingvol = [None]*endpoint_cht
            if ageClass[z] == 1: # standAge-1:
                area[z] = prevarea_cht[z] + afforarea
                standingvol[z] = prevvol_cht[z]
                if area[z] == 0:
                    prev_volha_cht[z] = 0
                else:
                    prev_volha_cht[z] = standingvol[z] / area[z]
                afforarea = 0
            else:
                area[z] = prevarea_cht[z]
            availablevolume[z] = matrixFunctions.availthvol(area[z], thin_intensity_cht, thinfreq)
            if ageClass[z] < age_th:
                thinvolume = 0
            if age_th <= ageClass[z] < age_th_upper:
                thinvolume = (prevthinvol + availablevolume[z])
            prevthinvol = thinvolume   
            sumvolcheck1 += newStand[z,7] * newStand[z,3]
            thinswitch = 'YES'
        originalvoltotal = sumvolcheck1    
        ageClass = [None]*endpoint_cht    
        for z in range(endpoint_cht):
            volha = [None]*endpoint_cht
            cai = [None]*endpoint_cht       
            availablevolume = [None]*endpoint_cht
            harvested = [None]*endpoint_cht
            actualthinvol = [None]*endpoint_cht
            standingvol = [None]*endpoint_cht
            teststanding = [None]*endpoint_cht
            newstandingvol = [None]*endpoint_cht       
            adjvol = [None]*endpoint_cht
            ageClass[z] = cht[z,2]       
            volha[z] = cht[z,7]  
            cai[z] = cht[z,8] 
            standingvol[z] = prevvol_cht[z]            
            adjvol[z] = standingvol[z]
            printvol = 0
########  more thinning preparation       
            availablevolume[z] = matrixFunctions.availthvol(area[z], thin_intensity_cht, thinfreq)
            actualthinvol[z] = matrixFunctions.thincheck2(availablevolume[z], ageClass[z], age_th, age_th_upper, targetThVolume, thinvolume)
#            pooldict = matrixFunctions.disturbanceMatrix(thinmatrix, pooldict)
            if age_th <= ageClass[z] < age_th_upper:            
                if standingvol[z] == 0.0:
                    adjvol[z] = 0.0
                    actualthinvol[z] = 0.0
                    printvol = 0.0    
                else:
                    adjvol[z] = standingvol[z] - actualthinvol[z]
                    if adjvol[z] < 0.0:
                        adjvol[z] = 0.0
                        actualthinvol[z] = standingvol[z]
                    printvol = actualthinvol[z]
                    pooldict = matrixFunctions.disturbanceMatrix(thinmatrix, pooldict)
                    sthin = 1
                    cats9 = 999
            else:
                adjvol[z] = standingvol[z]
########   clearfell 
            availablevolume_cf = 0
            availablearea_cf = 0   
            ageClassCount = 0                
            for y in range(age_cf, endpoint_cht):
                availablevolume_cf += (newStand[y,7] * newStand[y,3])   
                availablearea_cf += newStand[y,3]
                ageClassCount += 1                
            if ageClass[z] >= (age_cf - 1) and availablevolume_cf > 0 and targetvol > 0: #  and volha[z] >= volha_cf   !!!! Uncomment for Full FM
                runVolCheck = 0
#                availablevolume_cf = 0
#                availablearea_cf = 0   
#                ageClassCount = 0
#                if cht[-1, 2] > endpoint_cht - 1: # OR cht[-1, 2] == endpoint_cht:
#                    for y in range(endpoint_cht):
#                        availablevolume_cf += (cht[y,7] * cht[y,3])   
#                        availablearea_cf += cht[y,3]
#                        ageClassCount += 1
#                else:
#                if year == 2019:                    
#                    cats = input()   
#                    dog = 88888888888                      
#                for y in range(z, endpoint_cht):
#                    availablevolume_cf += (newStand[y,7] * newStand[y,3])   
#                    availablearea_cf += newStand[y,3]
#                    ageClassCount += 1
#                if availablevolume_cf == 0:
#                    break
#                print(availablevolume_cf)
                if targetvol < availablevolume_cf and targetvol > 0:
                    print("%.d -  target < available" % year)
                    that_check_inc = 0
                    standingvollist = [None]*endpoint_cht  
                    standingarealist = [None]*endpoint_cht
                    for y in range(endpoint_cht):        
                        standingvollist[y] =  newStand[y,7] * newStand[y,3]  
                        sss = standingvollist[::-1]                        
                    rollingSumSSS = np.cumsum(sss)             
                    sss = np.delete(sss, [0])
                    target_age = matrixFunctions.targetage(sss, targetvol)
                    remainvol = target_age[1]
                    targetIndex = target_age[0]                  
                    print(targetIndex)
                    cohortFelled = target_age[2]
                    prev_volha_cht[z] = standingvollist[y-1] / prevarea_cht[standAge - 1]
                    remainarea = remainvol / prev_volha_cht[z] # newStand[endpoint_cht-targetIndex-2,7]                   
                    volclearfelled = targetvol   
                    cfVolCheck = volclearfelled 
                    clearedArea2 = 0 
                    newAreaFelled = 0
                    sclear = 1
                    sclear_out = 1   
                    pooldict = matrixFunctions.disturbanceMatrix(cfmatrix, pooldict)
                    for z in range(z, endpoint_cht-targetIndex-1):  
                        cai[z] = cht[z,8]
                        area[z] = newStand[z,3]
                        ageClass[z] = cht[z,2] 
                        area[z] = prevarea_cht[z]                           
                        prevarea_cht[z] = newStand[z-1,3] 
                        adjvol[z] = prevvol_cht[z]
                        volha[z] = matrixFunctions.volinc(cai[z], area[z], adjvol[z])
                        newstandingvol[z] = volha[z]*area[z] 
                        check_inc[z] = newstandingvol[z] - newStand[z,7] * newStand[z,3]
                        prevvol_cht[z] = newStand[z-1,3]*newStand[z-1,7]  
                        output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.4F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " Not clearfelled"])
                        a.writerow(output)
                        newStand[z,3] = area[z]
                        newStand[z,7] = volha[z]
                        volIncNotFelled += check_inc[z]                                 
                        print('one')
                    for z in range(endpoint_cht - targetIndex -1, endpoint_cht - targetIndex):
                        cai[z] = cht[z,8]
                        newarea = prevarea_cht[z]  # newStand[z-1,3]
                        prevarea_cht[z] = newStand[z-1,3] 
                        clearedArea1 = newarea - remainarea
                        ageClass[z] = cht[z,2]
                        adjvol[z] = prevvol_cht[z] # + remainvol                        
                        partHarvested = newStand[z,3]*newStand[z,7] - remainvol
                        OtherClAreaCheck = partHarvested / newStand[endpoint_cht -targetIndex - 1,7]                          
                        newvolha = matrixFunctions.volinc(cai[z], remainarea, remainvol) 
                        newstandingvol[z] =  newvolha*newarea
                        area[z] = newarea
                        del newarea
######### new cohort added
                        if targetIndex == 0:
                            nextarea = remainarea
                            prevarea_cht.insert(z+1,remainarea)  
                            prevvol_cht.insert(z+1,remainvol)                            
                            prevvol_cht[z] = newStand[z-1,3]*newStand[z-1,7]
                            newrow = np.array((cht[0,0], YC_cht, (ageClass[z]+increment), nextarea, 0, 0, 0, newvolha, (cai[z]-1)), dtype = object)
                            cats = 7777                                                   
#                            output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z], " doh1 - not cf"])   # , " %.2F" % check_inc[z]])
#                            a.writerow(output)
                            output = (['nextrow', " %.d" % year, " %.d" % (ageClass[z]), " %.4F" % nextarea, " %.2F" % newvolha,  " %.2F" % remainvol, " part felling"])   # , " %.2F" % check_inc[z]])
                            a.writerow(output)                            
                            partAreaHarvest = 0
                            volha[z] = newvolha
                            print('two')
                        elif targetIndex != 0:
                            nextarea = remainarea # prevarea_cht[z] #cht[z+1,3]
                            partAreaHarvest = prevarea_cht[z] - nextarea
                            partHarvested = newStand[z,3]*newStand[z,7] - remainvol
                            newvolha = matrixFunctions.volinc(cai[z], remainarea, remainvol) 
                            prevarea_cht.insert(z,remainarea)  #cht[z,3])
                            prevvol_cht.insert(z+1,remainvol)                            
                            prevvol_cht[z] = newStand[z-1,3]*newStand[z-1,7]
                            nextrow = np.array((cht[0,0], YC_cht, (ageClass[z]+increment), nextarea, 0, 0, 0, newvolha, (cai[z]-1)), dtype = object)
                            eagle = 7777                                                   
                            output = (['nextrow', " %.d" % year, " %.d" % (ageClass[z]), " %.4F" % nextarea, " %.2F" % newvolha,  " %.2F" % remainvol, " partial fell"])   # , " %.2F" % check_inc[z]])
                            a.writerow(output)   
                            print('three')
                            
                        check_inc[z] = newstandingvol[z] - newStand[z,7] * newStand[z,3]       
    
                        newStand[z,3] = nextarea  # area[z]
                        newStand[z,7] = volha[z]         
                        volIncFelled += check_inc[z] 
                    for z in range(endpoint_cht-targetIndex, endpoint_cht):
########  THIS loop only qualifies when targetIndex > 0
                        cai[z] = cht[z,8] 
                        area[z] = newStand[z,3] 
                        clearedArea2 += newStand[z,3] 
                        newAreaFelled += newStand[z,3]
                        ageClass[z] = cht[z,2]                      
                        adjvol[z] = prevvol_cht[z]                       
                        harvested[z] = adjvol[z]
                        area[z] = 0
                        adjvol[z] = 0  
                        volha[z] = matrixFunctions.volinc(cai[z], area[z], adjvol[z])                     
                        newstandingvol[z] = volha[z]*area[z] 
                            
                        check_inc[z] = newstandingvol[z] - newStand[z,7] * newStand[z,3]       
                        newStand[z,2] = ageClass[z]
                        newStand[z,3] = nextarea
                        newStand[z,7] = newvolha
                        volIncFelled += check_inc[z]  
                        print('four')
########  volume checks throughout re: "volIncFelled"   
                    newrow6 = np.zeros([1,14])
                    newStand = np.vstack([newStand, newrow6]) 
#                    if 'volIncFelled' in locals():
                    volIncPostHarvest = volIncNotFelled + volIncFelled # + volIncPreHarvest
                    volIncNotFelled = 0
                    volIncFelled = 0
#                    if 'volIncFelled2' in locals():
#                        volIncPostHarvest = volIncPostHarvest + volIncFelled2
                    clearfell_nextcycle_cht = clearedArea2 +  clearedArea1   
                    remainarea = 0
                    clearedArea1 = 0                    
                    clearedArea2 = 0  
                    break
                elif targetvol >= availablevolume_cf:
                    areafelled = availablearea_cf #0 
                    that_check_inc = 0
                    print("%.d - target > availab" % year)
                    volclearfelled  = availablevolume_cf  
                    for z in range(z, endpoint_cht):  
                        sclear = 1
                        sclear_out = 1
                        cai[z] = cht[z,8]
                        ageClass[z] = cht[z,2] 
                        adjvol[z] = prevvol_cht[z]                                 
                        harvested[z] = cht[z,3]*cht[z,7] 
                        pooldict = matrixFunctions.disturbanceMatrix(cfmatrix, pooldict)
                        if ageClass[z] == endpoint_cht - ageClassCount:
                            area[z] = prevarea_cht[z] 
                            prevarea_cht[z] = cht[z-1,3] 
                            volha[z] = matrixFunctions.volinc(cai[z], area[z], adjvol[z])
                            newstandingvol[z] = volha[z]*area[z]                        
                            prevvol_cht[z] =  newStand[z-1,3]*newStand[z-1,7]                             
                        else:
                            area[z] = 0 
                            prevarea_cht[z] = 0
                            adjvol[z] = 0 
                            prevvol_cht[z] = 0                   
                            volha[z] = matrixFunctions.volinc(cai[z], area[z], adjvol[z])
                            newstandingvol[z] = volha[z]*area[z] 
                        if area[z] > 0:
                            check_inc[z] = newstandingvol[z] - newStand[z,7] * newStand[z,3]
                            output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.4F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],  " %.2F" % harvested[z]])  # " 0.000000000" ])  #
                            a.writerow(output)
#                            output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
#                            b.writerow(output)
                        check_inc[z] = newstandingvol[z] - newStand[z,7] * newStand[z,3]
                        newStand[z,3] = area[z]
                        newStand[z,7] = volha[z]                    
                        volIncPostHarvest += check_inc[z]                       
                        clearfell_nextcycle_cht = areafelled 
                        break
                    
                if 'holder4' in locals():
                    cht = np.vstack([cht, newrow4])
                    sstack = 1
                    output = (["newrow4", " %.d" % year, " %.d" % cht[(z+1),2], " %.4F" % cht[z+1,3], " %.2F" % cht[z+1,7],  " %.2F" % (cht[z+1,3]*cht[z+1,7]),   " 0.000"])
                    a.writerow(output)
                    if prevarea_cht[z+1] == 0:
                        prev_volha_cht.append(0.0)
                    else:                        
                        prev_volha_cht.append(prevvol_cht[z+1] / prevarea_cht[z+1])
                    del holder4  
                    del newrow4       
            else:
######## area & volume modification = pre-thin & pre-cf and no clearfells              
                ageClass[z] = cht[z,2]                                    
                if z == 0:
                    area[z] = 0  #clearfell_nextcycle_cht # + prevarea_cht[z] 
                    volha[z] = matrixFunctions.volinc(cai[z], area[z], adjvol[z])
                    newstandingvol[z] = area[z]*volha[z]
                    prevvol_cht[z] = 0  # cht[z-1,7]  #cht[z-1,3]*cht[z-1,7] 
                    if year == 1990:
                        newrow5 = np.zeros([1,14], dtype = int)
                        newStand = np.vstack([newStand, newrow5])                     
                elif ageClass[z] == endpoint_cht-1:
######### new cohort added                    
                    if ageClass[z] == 1:
                        area[z] =  afforarea2 + prevarea_cht[z]
                        afforarea2 = 0             
                    else:
                        area[z] = prevarea_cht[z] 
                    prevarea_cht.insert(z+1,area[z])
                    volha[z] = matrixFunctions.volinc(cai[z], area[z], adjvol[z])
                    newstandingvol[z] = area[z]*volha[z]
                    prevvol_cht[z] = newStand[z-1,3]*newStand[z-1,7]                     
                    newadjvol = newstandingvol[z] # adjvol[z]
                    prevvol_cht.insert(z+1,area[z]*volha[z]) # newarea*newvolha)# area[z]*cht[z,7])      
                    newrow5 = np.zeros([1,14])
                    newStand = np.vstack([newStand, newrow5])     
                else:   
                    if ageClass[z] == 1:
                        area[z] = afforarea2 + clearfell_nextcycle_cht  # prevarea_cht[z]
                        clearfell_nextcycle_cht = 0
                        afforarea2 = 0             
                    else:
                        area[z] = prevarea_cht[z] 
                        prevarea_cht[z] = newStand[z-1,3]                    
                    volha[z] = matrixFunctions.volinc(cai[z], area[z], newStand[z,3]*newStand[z,7])                                         
                    newstandingvol[z] = area[z]*volha[z]
                    prevvol_cht[z] = newStand[z-1,3]*newStand[z-1,7]
                check_inc[z] = newstandingvol[z] - newStand[z,7] * newStand[z,3]
                newStand[z,3] = area[z]
                newStand[z,7] = volha[z]  
                prevarea_cht[z] = newStand[z-1,3]                    
                if ageClass[z] >= age_th_upper:
                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.4F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " 0.0"])
                    a.writerow(output)  
                elif age_th <= ageClass[z] < age_th_upper:
                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.4F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],  " %.2F" % printvol]) #actualthinvol[z]])
                    a.writerow(output) 
                else:
                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.4F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " 0.0000"])
                    a.writerow(output)                      
#                check_inc[z] = newstandingvol[z] - newStand[z,7] * newStand[z,3]
                newStand[z,2] = ageClass[z]
                newStand[z,3] = area[z]
                newStand[z,7] = volha[z] 
                volIncPreHarvest += check_inc[z]                                 
                thinTotal += printvol #actualthinvol[z] 
                printvol = 0 #actualthinvol[z] = 0   

                
            if z <= standAge - 1:
                if hardwood == 0:
                    standPool01 += area[z]*cht[z,10]
                    standPool03 += area[z]*cht[z,11]
                    standPool02 += area[z]*cht[z,12]
                else:
                    standPool07 += area[z]*cht[z,10]
                    standPool09 += area[z]*cht[z,11]
                    standPool08 += area[z]*cht[z,12] 
                    
        agbiomassINC = (standPool07 + standPool08 + standPool09)
        biomassbgINC = matrixFunctions.sbiombg(agbiomassINC, hardwood)
        pf = 0.072 + (0.354*(math.exp(-0.06*biomassbgINC)))
        fineRoot_mass = pf*biomassbgINC
        coarseRoot_mass = biomassbgINC - fineRoot_mass
        fineRoot = fineRoot_mass 
        coarseRoot = coarseRoot_mass 
        
        if hardwood == 0:
            pooldict['pool06'] += fineRoot 
            pooldict['pool05'] += coarseRoot 
        else:
            pooldict['pool12'] += fineRoot
            pooldict['pool11'] += coarseRoot    
                    
        if hardwood == 0: 
            pooldict['pool01'] += standPool01
            pooldict['pool03'] += standPool03
            pooldict['pool02'] += standPool02
        else:
            pooldict['pool07'] += standPool07
            pooldict['pool09'] += standPool09
            pooldict['pool08'] += standPool08
            
        if hardwood == 0:            
            agbiomass = pooldict['pool01'] + pooldict['pool02'] + pooldict['pool03']
        else:
            agbiomass = pooldict['pool07'] + pooldict['pool08'] + pooldict['pool09']            
            
#        biomassbg = matrixFunctions.sbiombg(agbiomass, hardwood )   
#        pf = 0.072 + (0.354*(math.exp(-0.06*biomassbg)))
#        fineRoot = pf*biomassbg
#        coarseRoot = biomassbg - fineRoot   # (1-pf)*biomassbg 
#        if hardwood == 0:
#            pooldict['pool06'] = fineRoot
#            pooldict['pool05'] = coarseRoot
#        else:
#            pooldict['pool12'] = fineRoot
#            pooldict['pool11'] = coarseRoot 
#     
        newPool15 = 0
        newPool17 = 0
        newPool18 = 0
        newPool19 = 0                          
                
        ####  Turnover amounts  - Table 3 Kurz
        if hardwood == 0:
            sto = pooldict['pool01'] * DOM.loc[0,'DOM_STO']            
            branchto = pooldict['pool03'] * DOM.loc[0,'DOM_BranchSW']    
            foliageto = pooldict['pool02'] * DOM.loc[0,'DOM_FoliageSW'] 
            frto = pooldict['pool06'] * DOM.loc[0,'DOM_FRTO']
            crto = pooldict['pool05'] * DOM.loc[0,'DOM_CoarseRoot']  
        else:
            sto = pooldict['pool07'] * DOM.loc[0,'DOM_STO']            
            branchto = pooldict['pool09'] * DOM.loc[0,'DOM_BranchHW']  
            foliageto = pooldict['pool08'] * DOM.loc[0,'DOM_FoliageHW']   
            frto = pooldict['pool12'] * DOM.loc[0,'DOM_FRTO']
            crto = pooldict['pool11'] * DOM.loc[0,'DOM_CoarseRoot']   
                             
        #####  DOM pools receiving
        if hardwood == 0:
            pooldict['pool20'] += sto   # receiving snag stem
            pooldict['pool21'] += branchto * 0.25    # receiving snag branch
        else:
            pooldict['pool22'] += sto     # receiving snag stem        
            pooldict['pool23'] += branchto * 0.25  # receiving snag branch
        pooldict['pool15'] += branchto * 0.75   # receiving ag fast
        pooldict['pool13'] += foliageto   # ag very fast              
        pooldict['pool13'] += 0.5 * frto    # ag very fast
        pooldict['pool14'] += 0.5 *  frto    #  bg very fast
        pooldict['pool15'] += crto * 0.5   # ag fast
        pooldict['pool16'] += crto * 0.5    # bg fast  
                     
        #####  Decay transfers dynamics                      
        decaycollection = 0
        newatm = 0
        for key in pooldict:
            if key == 'pool20':
                decaycollection = matrixFunctions.decayFunction(pooldict['pool20'], 0.0187, 0.83, 0.17, 0.032)   # snag stem (sw & hw)
                pooldict['pool20'] -= (decaycollection[4] + decaycollection[5])
                newPool18 += decaycollection[2]  # pt agslow
                newPool17 += decaycollection[5]  # physical xfer
                newatm += decaycollection[1]
            if key == 'pool21':    
                decaycollection = matrixFunctions.decayFunction(pooldict['pool21'], 0.07175, 0.83, 0.17, 0.1)   # snag branch (sw & hw)
                pooldict['pool21'] -= (decaycollection[4] + decaycollection[5])
                newPool18 += decaycollection[2]  # pt agslow   
                newPool15 += decaycollection[5]  # physical xfer
                newatm += decaycollection[1]
            if key == 'pool22':
                decaycollection = matrixFunctions.decayFunction(pooldict['pool22'], 0.0187, 0.83, 0.17, 0.032)   # snag stem (sw & hw)
                pooldict['pool22'] -= (decaycollection[4] + decaycollection[5])
                newPool18 += decaycollection[2]  # pt agslow 
                newPool17 += decaycollection[5]  # physical xfer
                newatm += decaycollection[1]
            if key == 'pool23':
                decaycollection = matrixFunctions.decayFunction(pooldict['pool23'], 0.07175, 0.83, 0.17, 0.1)   # snag branch (sw & hw)
                pooldict['pool23'] -= (decaycollection[4] + decaycollection[5])
                newPool18 += decaycollection[2]  # pt agslow 
                newPool15 += decaycollection[5]  # physical xfer
                newatm += decaycollection[1]
            if key == 'pool17':
                decaycollection = matrixFunctions.decayFunction(pooldict['pool17'], 0.0374, 0.83, 0.17, 0)   # medium
                pooldict['pool17'] -= decaycollection[4]
                newPool18 += decaycollection[2]  # pt agslow   
                newatm += decaycollection[1]
            if key == 'pool15':
                decaycollection = matrixFunctions.decayFunction(pooldict['pool15'], 0.214, 0.9, 0.1, 0)   # ag fast
                pooldict['pool15'] -= decaycollection[4]
                newPool18 += decaycollection[2]  # pt agslow 
                newatm += decaycollection[1]
            if key == 'pool13':
                decaycollection = matrixFunctions.decayFunction(pooldict['pool13'], 0.423, 0.888, 0.112, 0)  # ag very fast
                pooldict['pool13'] -= decaycollection[4]
                newPool18 += decaycollection[2]  # pt agslow
                newatm += decaycollection[1]
            if key == 'pool18':
                decaycollection = matrixFunctions.decayFunction2(pooldict['pool18'], 0.19, 0.815, 0.185, 0.006)          # ag slow  0.19, 1, 0, 0.006) 
                pooldict['pool18'] -= (decaycollection[4] + decaycollection[5])   
#                newPool19 += decaycollection[3]  # pt bgslow - guess???
                newPool19 += decaycollection[5]  # physical xfer 
                newatm += decaycollection[1]
            if key == 'pool16':
                decaycollection = matrixFunctions.decayFunction2(pooldict['pool16'], 0.1435, 0.83, 0.17, 0)   # bg fast
                pooldict['pool16'] -= decaycollection[4]
                newPool19 += decaycollection[3]  # pt bgslow  
                newatm += decaycollection[1]
            if key == 'pool14':
                decaycollection = matrixFunctions.decayFunction2(pooldict['pool14'], 0.403, 0.815, 0.185, 0)   # bg very fast
                pooldict['pool14'] -= decaycollection[4]
                newPool19 += decaycollection[3]  # pt bgslow
                newatm += decaycollection[1]
            if key == 'pool19':
                decaycollection = matrixFunctions.decayFunction2(pooldict['pool19'], 0.0033, 1, 0, 0)   # bg slow
                pooldict['pool19'] -= decaycollection[4]   
                newatm += decaycollection[1]
      
        pooldict['pool18'] += newPool18
        pooldict['pool17'] += newPool17 
        pooldict['pool15'] += newPool15
        pooldict['pool19'] += newPool19
        pooldict['pool26'] = newatm
    
    ######## above ground biomass - after dynamics
        if hardwood == 0:            
            agbiomass = pooldict['pool01'] + pooldict['pool02'] + pooldict['pool03']
        else:
            agbiomass = pooldict['pool07'] + pooldict['pool08'] + pooldict['pool09']
        biomassbg = matrixFunctions.sbiombg(agbiomass, hardwood )
        
        
    ######## Harvest Wood Products
        Pool30vol = matrixFunctions.svol(inParm1.loc[bm_cohort,'1a'], inParm1.loc[bm_cohort,'1b'], pooldict['pool30']) # pool30 is populated by dist matrices                   
        if sthin == 0 and sclear == 1:
            inflow_saw_cf = Pool30vol*HWP.loc[0,'frac_cf']*HWP.loc[0,'carb_frac'] 
            pooldict['pool32'] = matrixFunctions.harvWoodProd(inflow_saw_cf, pooldict['pool32'], HWP.loc[0,'halfLife'])            
            inflow_wbp_cf = Pool30vol * HWP.loc[1,'frac_cf'] * HWP.loc[1,'carb_frac']  
            pooldict['pool33'] = matrixFunctions.harvWoodProd(inflow_wbp_cf, pooldict['pool33'], HWP.loc[1,'halfLife'])        
        elif sclear == 0 and sthin == 1:
            inflow_saw_th = Pool30vol*HWP.loc[0,'frac_th']*HWP.loc[0,'carb_frac'] 
            pooldict['pool32'] = matrixFunctions.harvWoodProd(inflow_saw_th, pooldict['pool32'], HWP.loc[0,'halfLife'])            
            inflow_wbp_th = Pool30vol*HWP.loc[1,'frac_th']*HWP.loc[1,'carb_frac']  
            pooldict['pool33'] = matrixFunctions.harvWoodProd(inflow_wbp_th, pooldict['pool33'], HWP.loc[1,'halfLife'])
        elif sclear == 0 and sthin == 0:
            pooldict['pool32'] += 0
            pooldict['pool33'] += 0            
        elif sclear == 1 and sthin == 1:
            inflow_saw_cf = Pool30vol*HWP.loc[0,'frac_cf']*HWP.loc[0,'carb_frac']  
            inflow_saw_th = Pool30vol*HWP.loc[0,'frac_th']*HWP.loc[0,'carb_frac'] 
            pooldict['pool32'] = matrixFunctions.harvWoodProd(inflow_saw_cf + inflow_saw_th, pooldict['pool32'], HWP.loc[0,'halfLife'])            
            
            inflow_wbp_cf = Pool30vol*HWP.loc[1,'frac_cf']*HWP.loc[1,'carb_frac']  
            inflow_wbp_th = Pool30vol*HWP.loc[1,'frac_th']*HWP.loc[1,'carb_frac']  
            pooldict['pool33'] = matrixFunctions.harvWoodProd(inflow_wbp_cf + inflow_wbp_th, pooldict['pool33'], HWP.loc[1,'halfLife'])    
            
#        if inventoryCheck == 0:
#            pooldict = pooldict_temp.copy()
#            pooldict['pool19'] = 0
#        inventoryCheck = 0
#        d.iterkeys() -> iter(pooldict.keys())
        for key in sorted(iter(pooldict.keys())):    
            output = (["%s, %.12f" % (key, pooldict[key])])
            a.writerow(output) 
#        output = (["standPool01 = %.4f" % standPool01])
#        a.writerow(output)
#        output = (["standPool02 = %.4f" % standPool02])
#        a.writerow(output)
#        output = (["standPool03 = %.4f" % standPool03])
#        a.writerow(output)            
        output = (["annual above ground biomass = %.4f" % agbiomass])
        a.writerow(output)
        output = (["annual below ground biomass = %.4f" % biomassbg])
        a.writerow(output) 

########  more volume checks
        volumeIncrement = volIncPostHarvest + volIncPreHarvest  
        finalvoltotal = 0
        sumarea = 0
        presum = 0
        finalvol = [None]*endpoint_cht        
        volumeCheck2 = 0
        
########  area check        
        for z in range(endpoint_cht):       
            volumeCheck2 += newStand[z,7] * newStand[z,3] 
            presum += newStand[z,3]
        if 'newarea' in locals():
            sumarea = presum # + newarea
            del newarea
        elif 'nextarea' in locals():
            sumarea = presum #+ nextarea
            del nextarea
        else:
            sumarea = presum                                 
        areaTotal = sumarea  + clearfell_nextcycle_cht  
        
########    Output code     
        output = (["Year = "," %.d" % year])
        a.writerow(output)
        output = (["Species cohort = %s" % cht[0,0]])
        a.writerow(output)
        volumeCheck1 = originalvoltotal + volumeIncrement 
        output = (["VolCheck1 = "," %.2F" % volumeCheck1])
        a.writerow(output)    
        output = (["VolCheck2 = %.2F" % volumeCheck2] )   
        a.writerow(output)      
        output = (["Area check = "," %.2F" % areaTotal ])
        a.writerow(output) 
#        output = (["VolHa check = %.2F" % (volumeCheck1 / areaTotal ) ])
#        a.writerow(output)         
        output = (["CF Volume Target = %.d" % targetvol ])    
        a.writerow(output)  
        if sclear_out == 1:
            output = (["Volume Felled = %.2F" % volclearfelled ])    
            a.writerow(output)         
        output = (["TH Volume Target = %.d" % targetThVolume ])    
        a.writerow(output)  
        if sthin_out == 1:
            output = (["Volume Thinned = %.d" % thinTotal ])    
            a.writerow(output) 
        output = ([" "])  
        a.writerow(output)         
        if type(clearfell_nextcycle_cht) == str:
            output = (["cf_area_nextcycle = NoCf"])  
            a.writerow(output)
        else:        
            output = (["cf_area_nextcycle = %.2F" % clearfell_nextcycle_cht])
            a.writerow(output) 
        if year > 2:
            sum_sv = volumeCheck1
#            sum_hv += thinTotal + volclearfelled
#            output = (["summary_st_vol = %.2f" % sum_sv])
#            a.writerow(output)
            
########  These two lines removing lines of trailing zeros     
#        n = np.sum((np.where(cht[:,3] >0),np.where(cht[:,5]>0)),axis = 1)[0][-1]
#        cht = cht[:(n+1)]   
                 
                 
#    holder refers to the addition of new lines which occur when there is no cf
        if 'holder1' in locals():
#            n = np.sum((np.where(cht[:,3] >0),np.where(cht[:,5]>0)),axis = 1)[0][-1]
#            cht = cht[:(n+1)]            
            cht = np.vstack([cht, newrow]) 
            del holder1   
            del newrow        
        if 'holder2' in locals():
#            n = np.sum((np.where(cht[:,3] >0),np.where(cht[:,5]>0)),axis = 1)[0][-1]
#            cht = cht[:(n+1)]            
#            cht = np.vstack([cht, nextrow]) 
            del holder2   
            del nextrow      

            
#        if 'volclearfelled' in locals():
        if sclear_out == 1:
            sum_hv = thinTotal + volclearfelled            
#            output = (["Volume Clearfelled = %.2f" % volclearfelled ])    
#            a.writerow(output)    
########  These lines keep the prev* lists in line with the cht matrix            
            while len(prevarea_cht) > len(cht)  :
                prevarea_cht.pop()         
            while len(prevvol_cht) > len(cht) :
                prevvol_cht.pop()     
            del volclearfelled
        else:
            sum_hv = thinTotal
#            print("%.d -  nope to cf" % year)
            del targetvol


########  This step deals with issue when a row of zeros is removed but the 
########      ages aren't monotonic, which causes probs down the line
#        endpoint_cht = len(cht)
#        if cht[endpoint_cht-1,2] - cht[endpoint_cht-2,2]>1:
#            cht[endpoint_cht-1,2] = cht[endpoint_cht-2,2] + 1        
#        endpoint_cht = len(cht)
        
        fullpool['pool01'] += pooldict['pool01']
        fullpool['pool02'] += pooldict['pool02']
        fullpool['pool03'] += pooldict['pool03']
        fullpool['pool04'] += pooldict['pool04']
        fullpool['pool05'] += pooldict['pool05']
        fullpool['pool06'] += pooldict['pool06']
        fullpool['pool07'] += pooldict['pool07']
        fullpool['pool08'] += pooldict['pool08']
        fullpool['pool09'] += pooldict['pool09']
        fullpool['pool10'] += pooldict['pool10']
        fullpool['pool11'] += pooldict['pool11']
        fullpool['pool12'] += pooldict['pool12']
        fullpool['pool13'] += pooldict['pool13']
        fullpool['pool14'] += pooldict['pool14']
        fullpool['pool15'] += pooldict['pool15']
        fullpool['pool16'] += pooldict['pool16']
        fullpool['pool17'] += pooldict['pool17']
        fullpool['pool18'] += pooldict['pool18']
        fullpool['pool19'] += pooldict['pool19']
        fullpool['pool20'] += pooldict['pool20']
        fullpool['pool21'] += pooldict['pool21']
        fullpool['pool22'] += pooldict['pool22']
        fullpool['pool23'] += pooldict['pool23']
        fullpool['pool24'] += pooldict['pool24']
        fullpool['pool25'] += pooldict['pool25']
        fullpool['pool26'] += pooldict['pool26']
        fullpool['pool27'] += pooldict['pool27']
        fullpool['pool28'] += pooldict['pool28']
        fullpool['pool29'] += pooldict['pool29']
        fullpool['pool30'] += pooldict['pool30']
        fullpool['pool31'] += pooldict['pool31']
        fullpool['pool32'] += pooldict['pool32']
        fullpool['pool33'] += pooldict['pool33']     
#        for key, value in pooldict.iteritems():
#            fullpool[key] = value           
#        annualAgbiomass += agbiomass  
        annualBgbiomass += biomassbg         

######## end cohort re-naming:
        if cohort == 0: 
            FGB = cht
            newStandFGB = newStand
            FGBpool = pooldict
            endpoint_FGB = endpoint_cht
            clearfell_nextcycle_FGB = clearfell_nextcycle_cht            
            prevarea_FGB = prevarea_cht
            prevvol_FGB = prevvol_cht
            annual_sv = sum_sv + annual_sv
            annual_hv = sum_hv + annual_hv               
#            PA12 = cht
#            newStandPA12 = newStand
#            PA12pool = pooldict
#            endpoint_PA12 = endpoint_cht
#            clearfell_nextcycle_PA12 = clearfell_nextcycle_cht     
#            prevarea_PA12 = prevarea_cht
#            prevvol_PA12 = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv 
#        elif cohort == 1:
#            PA16 = cht
#            newStandPA16 = newStand
#            PA16pool = pooldict
#            endpoint_PA16 = endpoint_cht
#            clearfell_nextcycle_PA16 = clearfell_nextcycle_cht            
#            prevarea_PA16 = prevarea_cht
#            prevvol_PA16 = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv   
#        elif cohort == 2:
#            PA20 = cht
#            newStandPA20 = newStand
#            PA20pool = pooldict
#            endpoint_PA20 = endpoint_cht
#            clearfell_nextcycle_PA20 = clearfell_nextcycle_cht            
#            prevarea_PA20 = prevarea_cht
#            prevvol_PA20 = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv  
#        elif cohort == 3:
#            PA24 = cht
#            newStandPA24 = newStand
#            PA24pool = pooldict
#            endpoint_PA24 = endpoint_cht
#            clearfell_nextcycle_PA24 = clearfell_nextcycle_cht            
#            prevarea_PA24 = prevarea_cht
#            prevvol_PA24 = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv             
#        elif cohort == 4:
#            PA30 = cht
#            newStandPA30 = newStand
#            PA30pool = pooldict
#            endpoint_PA30 = endpoint_cht
#            clearfell_nextcycle_PA30 = clearfell_nextcycle_cht            
#            prevarea_PA30 = prevarea_cht
#            prevvol_PA30 = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv          
#        elif cohort == 5:
#            PS12 = cht
#            newStandPS12 = newStand
#            PS12pool = pooldict
#            endpoint_PS12 = endpoint_cht
#            clearfell_nextcycle_PS12 = clearfell_nextcycle_cht            
#            prevarea_PS12 = prevarea_cht
#            prevvol_PS12 = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv              
#        elif cohort == 6:
#            PS20 = cht
#            newStandPS20 = newStand
#            PS20pool = pooldict
#            endpoint_PS20 = endpoint_cht
#            clearfell_nextcycle_PS20 = clearfell_nextcycle_cht            
#            prevarea_PS20 = prevarea_cht
#            prevvol_PS20 = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv  
#        elif cohort == 7:
#            OC = cht
#            newStandOC = newStand
#            OCpool = pooldict
#            endpoint_OC = endpoint_cht
#            clearfell_nextcycle_OC = clearfell_nextcycle_cht            
#            prevarea_OC = prevarea_cht
#            prevvol_OC = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv  
#        elif cohort == 8:
#            Cmix = cht
#            newStandCmix = newStand
#            Cmixpool = pooldict
#            endpoint_Cmix = endpoint_cht
#            clearfell_nextcycle_Cmix = clearfell_nextcycle_cht            
#            prevarea_Cmix = prevarea_cht
#            prevvol_Cmix = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv  
#        elif cohort == 9:
#            CBmix = cht
#            newStandCBmix = newStand
#            CBmixpool = pooldict
#            endpoint_CBmix = endpoint_cht
#            clearfell_nextcycle_CBmix = clearfell_nextcycle_cht            
#            prevarea_CBmix = prevarea_cht
#            prevvol_CBmix = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv  
#        elif cohort == 10:  
#            FGB = cht
#            newStandFGB = newStand
#            FGBpool = pooldict
#            endpoint_FGB = endpoint_cht
#            clearfell_nextcycle_FGB = clearfell_nextcycle_cht            
#            prevarea_FGB = prevarea_cht
#            prevvol_FGB = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv              
#        elif cohort == 11:
#            SGB = cht
#            newStandSGB = newStand
#            SGBpool = pooldict
#            endpoint_SGB = endpoint_cht
#            clearfell_nextcycle_SGB = clearfell_nextcycle_cht            
#            prevarea_SGB = prevarea_cht
#            prevvol_SGB = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv  
#
#        if cohort == 12:                 
#            PA12p = cht
#            newStandPA12p = newStand
#            PA12ppool = pooldict
#            endpoint_PA12p = endpoint_cht
#            clearfell_nextcycle_PA12p = clearfell_nextcycle_cht     
#            prevarea_PA12p = prevarea_cht
#            prevvol_PA12p = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv 
#        elif cohort == 13:
#            PA16p = cht
#            newStandPA16p = newStand
#            PA16ppool = pooldict
#            endpoint_PA16p = endpoint_cht
#            clearfell_nextcycle_PA16p = clearfell_nextcycle_cht            
#            prevarea_PA16p = prevarea_cht
#            prevvol_PA16p = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv   
#        elif cohort == 14:
#            PA20p = cht
#            newStandPA20p = newStand
#            PA20ppool = pooldict
#            endpoint_PA20p = endpoint_cht
#            clearfell_nextcycle_PA20p = clearfell_nextcycle_cht            
#            prevarea_PA20p = prevarea_cht
#            prevvol_PA20p = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv  
#        elif cohort == 15:
#            PA24p = cht
#            newStandPA24p = newStand
#            PA24ppool = pooldict
#            endpoint_PA24p = endpoint_cht
#            clearfell_nextcycle_PA24p = clearfell_nextcycle_cht            
#            prevarea_PA24p = prevarea_cht
#            prevvol_PA24p = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv             
#        elif cohort == 16:
#            PA30p = cht
#            newStandPA30p = newStand
#            PA30ppool = pooldict
#            endpoint_PA30p = endpoint_cht
#            clearfell_nextcycle_PA30p = clearfell_nextcycle_cht            
#            prevarea_PA30p = prevarea_cht
#            prevvol_PA30p = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv          
#        elif cohort == 17:
#            PS12p = cht
#            newStandPS12p = newStand
#            PS12ppool = pooldict
#            endpoint_PS12p = endpoint_cht
#            clearfell_nextcycle_PS12p = clearfell_nextcycle_cht            
#            prevarea_PS12p = prevarea_cht
#            prevvol_PS12p = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv              
#        elif cohort == 18:
#            PS20p = cht
#            newStandPS20p = newStand
#            PS20ppool = pooldict
#            endpoint_PS20p = endpoint_cht
#            clearfell_nextcycle_PS20p = clearfell_nextcycle_cht            
#            prevarea_PS20p = prevarea_cht
#            prevvol_PS20p = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv  
#        elif cohort == 19:
#            OCp = cht
#            newStandOCp = newStand
#            OCppool = pooldict
#            endpoint_OCp = endpoint_cht
#            clearfell_nextcycle_OCp = clearfell_nextcycle_cht            
#            prevarea_OCp = prevarea_cht
#            prevvol_OCp = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv  
#        elif cohort == 20:
#            Cmixp = cht
#            newStandCmixp = newStand
#            Cmixppool = pooldict
#            endpoint_Cmixp = endpoint_cht
#            clearfell_nextcycle_Cmixp = clearfell_nextcycle_cht            
#            prevarea_Cmixp = prevarea_cht
#            prevvol_Cmixp = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv  
#        elif cohort == 21:
#            CBmixp = cht
#            newStandCBmixp = newStand
#            CBmixppool = pooldict
#            endpoint_CBmixp = endpoint_cht
#            clearfell_nextcycle_CBmixp = clearfell_nextcycle_cht            
#            prevarea_CBmixp = prevarea_cht
#            prevvol_CBmixp = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv  
#        elif cohort == 22:  
#            FGBp = cht
#            newStandFGBp = newStand
#            FGBppool = pooldict
#            endpoint_FGBp = endpoint_cht
#            clearfell_nextcycle_FGBp = clearfell_nextcycle_cht            
#            prevarea_FGBp = prevarea_cht
#            prevvol_FGBp = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv              
#        elif cohort == 23:
#            SGBp = cht
#            newStandSGBp = newStand
#            SGBppool = pooldict
#            endpoint_SGBp = endpoint_cht
#            clearfell_nextcycle_SGBp = clearfell_nextcycle_cht            
#            prevarea_SGBp = prevarea_cht
#            prevvol_SGBp = prevvol_cht
#            annual_sv = sum_sv + annual_sv
#            annual_hv = sum_hv + annual_hv  
        
        cht = 0
        thinTotal = 0
        remainvol = 0
        targetIndex = 0  
        sthin_out = 0
        sclear_out = 0   
        
    annualAgbiomass += fullpool['pool01'] + fullpool['pool02'] + fullpool['pool03'] + fullpool['pool07'] + fullpool['pool08'] + fullpool['pool09'] 

        
    for key in sorted(iter(fullpool.keys())):   
        output = (["Fullpool_%s: %.12f" % (key, fullpool[key])])
        a.writerow(output)         
        
    if prevarea_cht[z] == 0:
        prev_volha_cht[z] = 0
    else:
        prev_volha_cht[z] = prevvol_cht[z] / prevarea_cht[z]                


    output = (["Annual_above ground = "," %.2f" % annualAgbiomass])
    a.writerow(output) 
    output = (["Annual_below ground = "," %.2f" % annualBgbiomass])
    a.writerow(output) 
            
#    ANUUAL SUMMARIES
#    annual_sv += sum_sv
    output = (["Annual_summary_st_vol = "," %.2f" % annual_sv])
    a.writerow(output)    
    output = (["Annual_summary_hv_vol = ","%.2f" % annual_hv])
    a.writerow(output)    
    output = ([" "])  
    a.writerow(output) 
#    output = ([" "])
#    b.writerow(output)
    sum_sv = 0
    sum_hv = 0 
    annual_sv = 0
    annual_hv = 0 
#    pooldict['pool30'] = 0
#    standAge += 1
    year += 1
    step += 1
    sthin = 0
    sclear = 0
frequency = 500  # Set Frequency To 2500 Hertz
duration = 100  # Set Duration To 1000 ms == 1 second
#winsound.Beep(frequency, duration)
print('script duration = ',  datetime.now() - startTime)
commaout.close() 
