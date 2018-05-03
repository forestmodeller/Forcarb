from IPython import get_ipython
get_ipython().magic('reset -sf')

import matrixFunctions
import numpy as np
import csv
import os
import pandas as pd
#import math
from pandas import DataFrame
#from __future__ import division




######## file management

#os.chdir("D:\Data\Cloudstation\Notes & work\IrishLandUSes\Matrix\Files")
os.chdir("D:\Documents\Cloudstation\Notes & work\IrishLandUSes\Matrix\Files")

######## main input file
df = pd.read_csv("FinalAR_Actual_newCai.csv", names = ['FT', 'YC','Age', 'Area', 'Litter', 'Stump', 'DW', 'Volha','CAI'])
#df = pd.read_csv("FinalAR_Actual.csv", names = ['FT', 'YC','Age', 'Area', 'Litter', 'Stump', 'DW', 'Volha','CAI'])

######## Harvest targets, Clearfell & Thinning rules by year
with open('HarvestTargets.csv', mode='r') as infile:
    reader = csv.reader(infile)
    HarvTHparm = dict((rows[0],rows[1]) for rows in reader)   #p2
with open('HarvestTargets.csv', mode='r') as infile:
    reader = csv.reader(infile)
    HarvCFparm = dict((rows[0],rows[2]) for rows in reader)
#with open('HarvestTargets.csv', mode='r') as infile:
#    reader = csv.reader(infile)
#    HarvTHparm = dict((rows[0],rows[3]) for rows in reader)
#with open('HarvestTargets.csv', mode='r') as infile:
#    reader = csv.reader(infile)
#    HarvCFparm = dict((rows[0],rows[4]) for rows in reader)
##        mydict = {rows[0]:rows[1] for rows in reader}   #p3

with open('newClearfellRules.csv', mode='r') as infile:
    reader = csv.reader(infile)
    CF_AGE_MIN = dict((rows[0],rows[1]) for rows in reader)
with open('newClearfellRules.csv', mode='r') as infile:
    reader = csv.reader(infile)
    CF_VOLHA = dict((rows[0],rows[3]) for rows in reader)

with open('newThinningHarvestRules.csv', mode='r') as infile:
    reader = csv.reader(infile)
    TH_AGE_MIN = dict((rows[0],rows[1]) for rows in reader)
with open('newThinningHarvestRules.csv', mode='r') as infile:
    reader = csv.reader(infile)
    TH_FREQ = dict((rows[0],rows[3]) for rows in reader)
#    TH_VOLHA = dict((rows[0],rows[3]) for rows in reader)


######## Biomass parameters
inParm1 = pd.read_csv("BmEq1.csv", names = ['cohort','1a','1b','vlim'])
inParm2 = pd.read_csv("BmEq2.csv", names = ['cohort','2k','2a','2b','fbnlim'])
inParm3 = pd.read_csv("BmEq3.csv", names = ['cohort','3k','3a','3b','fbslim'])
inParm4 = pd.read_csv("BmEq4.csv", names = ['cohort','4a','4b'])  #,'fbslim'])
inParm5 = pd.read_csv("BmEq5.csv", names = ['cohort','a1','a2','a3','b1','b2','b3','c1','c2','c3','volLimit'])
inParm6 = pd.read_csv("BmEq6.csv", names = ['cohort','6a','6b', 'biomassab'])

######## DOM parameters
DOM = pd.read_csv("DOMparams.csv", names = ['DOM_FoliageHW','DOM_FoliageSW','DOM_CoarseRoot','DOM_FRTO','DOM_OWTO','DOM_STO'])


########  output file(s)
commaout = open('matrix_output_list.csv',mode='wb')
a = csv.writer(commaout, dialect='excel', delimiter=',')
prevout = open('prevarea_out.csv',mode='wb')
b = csv.writer(prevout, dialect='excel', delimiter=',')
headers = 'Cohort', ' Year', ' Age', ' Area', ' VolPerHa', ' StandingVol', ' Thin/CF volume (if any)'  #' Standing Vol',
a.writerow(headers)
output = (["____________________________________________________________________"])
a.writerow(output)
output = ([" "])
a.writerow(output)


######## cohort managment
PA = DataFrame(df, columns = ['FT', 'YC','Age', 'Area', 'Litter', 'Stump', 'DW', 'Volha','CAI'])
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



######## more cohort management
######## begin cohort re-naming:
cohortlist = 11 #(1,2)   # PA12, PA16, etc.
for cohort in range(cohortlist):
    if cohort == 0:
        prevarea_PA12 = [None]*endpoint_PA12
        prevvol_PA12 = [None]*endpoint_PA12
        prevarea_PA12, prevvol_PA12 = matrixFunctions.previous(PA12, endpoint_PA12, prevarea_PA12, prevvol_PA12)
        bm_cohort = 0
    if cohort == 1:
        prevarea_PA16 = [None]*endpoint_PA16
        prevvol_PA16 = [None]*endpoint_PA16
        prevarea_PA16, prevvol_PA16 = matrixFunctions.previous(PA16, endpoint_PA16, prevarea_PA16, prevvol_PA16)
        bm_cohort = 0
    if cohort == 2:
        prevarea_PA20 = [None]*endpoint_PA20
        prevvol_PA20 = [None]*endpoint_PA20
        prevarea_PA20, prevvol_PA20 = matrixFunctions.previous(PA20, endpoint_PA20, prevarea_PA20, prevvol_PA20)
        bm_cohort = 0
    if cohort == 3:
        prevarea_PA24 = [None]*endpoint_PA24
        prevvol_PA24 = [None]*endpoint_PA24
        prevarea_PA24, prevvol_PA24 = matrixFunctions.previous(PA24, endpoint_PA24, prevarea_PA24, prevvol_PA24)
        bm_cohort = 0
    if cohort == 4:
        prevarea_PA30 = [None]*endpoint_PA30
        prevvol_PA30 = [None]*endpoint_PA30
        prevarea_PA30, prevvol_PA30 = matrixFunctions.previous(PA30, endpoint_PA30, prevarea_PA30, prevvol_PA30)
        bm_cohort = 0
    if cohort == 5:
        prevarea_PS12 = [None]*endpoint_PS12
        prevvol_PS12 = [None]*endpoint_PS12
        prevarea_PS12, prevvol_PS12 = matrixFunctions.previous(PS12, endpoint_PS12, prevarea_PS12, prevvol_PS12)
        bm_cohort = 1
    if cohort == 6:
        prevarea_PS20 = [None]*endpoint_PS20
        prevvol_PS20 = [None]*endpoint_PS20
        prevarea_PS20, prevvol_PS20 = matrixFunctions.previous(PS20, endpoint_PS20, prevarea_PS20, prevvol_PS20)
        bm_cohort = 1
    if cohort == 7:
        prevarea_OC = [None]*endpoint_OC
        prevvol_OC = [None]*endpoint_OC
        prevarea_OC, prevvol_OC = matrixFunctions.previous(OC, endpoint_OC, prevarea_OC, prevvol_OC)
        bm_cohort = 2
    if cohort == 8:
        prevarea_Cmix = [None]*endpoint_Cmix
        prevvol_Cmix = [None]*endpoint_Cmix
        prevarea_Cmix, prevvol_Cmix = matrixFunctions.previous(Cmix, endpoint_Cmix, prevarea_Cmix, prevvol_Cmix)
        bm_cohort = 2
    if cohort == 9:
        prevarea_CBmix = [None]*endpoint_CBmix
        prevvol_CBmix = [None]*endpoint_CBmix
        prevarea_CBmix, prevvol_CBmix = matrixFunctions.previous(CBmix, endpoint_CBmix, prevarea_CBmix, prevvol_CBmix)
        bm_cohort = 3
    if cohort == 10:
        prevarea_FGB = [None]*endpoint_FGB
        prevvol_FGB = [None]*endpoint_FGB
        prevarea_FGB, prevvol_FGB = matrixFunctions.previous(FGB, endpoint_FGB, prevarea_FGB, prevvol_FGB)
        bm_cohort = 3
    if cohort == 11:
        prevarea_SGB = [None]*endpoint_SGB
        prevvol_SGB = [None]*endpoint_SGB
        prevarea_SGB, prevvol_SGB = matrixFunctions.previous(SGB, endpoint_SGB, prevarea_SGB, prevvol_SGB)
        bm_cohort = 4



######## initialise variables
thinvolume = 0
prevthinvol = 0
defor = 0 # 1000
deforYear = 35
affor = 0 # 500
afforYear = 25
remainvol = 0
newcohortvol = 0
new_area = 0
thinTotal = 0
sum_sv = 0
sum_hv = 0
annual_sv = 0
areaFelled = 0
clearfell_nextcycle_PA12 = 2000
clearfell_nextcycle_PA16 = 1800
clearfell_nextcycle_PA20 = 1800
clearfell_nextcycle_PA24 = 1800
clearfell_nextcycle_PA30 = 1800
clearfell_nextcycle_PS12 = 1800
clearfell_nextcycle_PS20 = 1800
clearfell_nextcycle_OC = 1800
clearfell_nextcycle_Cmix = 1800
clearfell_nextcycle_CBmix = 1800
clearfell_nextcycle_FGB = 1800
clearfell_nextcycle_SGB = 1800
cohortratio = 0.0833 # 1.0/(cohortlist+1)
cohortratio_cf = 0.0833
increment = 1


year = 1986   #1906
######## stores each cohort's respective variables
while year <=  2030:
#    if year == 2021:
#        cats = raw_input()
#        doh = cats
    for cohort in range(cohortlist):
        if cohort == 0:
            cht = PA12
            clearfell_nextcycle_cht = clearfell_nextcycle_PA12
            prevarea_cht = prevarea_PA12
            prevvol_cht = prevvol_PA12
        elif cohort == 1:
            cht = PA16
            clearfell_nextcycle_cht = clearfell_nextcycle_PA16
            prevarea_cht = prevarea_PA16
            prevvol_cht = prevvol_PA16
        elif cohort == 2:
            cht = PA20
            clearfell_nextcycle_cht = clearfell_nextcycle_PA20
            prevarea_cht = prevarea_PA20
            prevvol_cht = prevvol_PA20
        elif cohort == 3:
            cht = PA24
            clearfell_nextcycle_cht = clearfell_nextcycle_PA24
            prevarea_cht = prevarea_PA24
            prevvol_cht = prevvol_PA24
        elif cohort == 4:
            cht = PA30
            clearfell_nextcycle_cht = clearfell_nextcycle_PA30
            prevarea_cht = prevarea_PA30
            prevvol_cht = prevvol_PA30
        elif cohort == 5:
            cht = PS12
            clearfell_nextcycle_cht = clearfell_nextcycle_PS12
            prevarea_cht = prevarea_PS12
            prevvol_cht = prevvol_PS12
        elif cohort == 6:
            cht = PS20
            clearfell_nextcycle_cht = clearfell_nextcycle_PS20
            prevarea_cht = prevarea_PS20
            prevvol_cht = prevvol_PS20
        elif cohort == 7:
            cht = OC
            clearfell_nextcycle_cht = clearfell_nextcycle_OC
            prevarea_cht = prevarea_OC
            prevvol_cht = prevvol_OC
        elif cohort == 8:
            cht = Cmix
            clearfell_nextcycle_cht = clearfell_nextcycle_Cmix
            prevarea_cht = prevarea_Cmix
            prevvol_cht = prevvol_Cmix
        elif cohort == 9:
            cht = CBmix
            clearfell_nextcycle_cht = clearfell_nextcycle_CBmix
            prevarea_cht = prevarea_CBmix
            prevvol_cht = prevvol_CBmix
        elif cohort == 10:
            cht = FGB
            clearfell_nextcycle_cht = clearfell_nextcycle_FGB
            prevarea_cht = prevarea_FGB
            prevvol_cht = prevvol_FGB
        elif cohort == 11:
            cht = SGB
            clearfell_nextcycle_cht = clearfell_nextcycle_SGB
            prevarea_cht = prevarea_SGB
            prevvol_cht = prevvol_SGB

        age_cf = int(CF_AGE_MIN[cht[0,0]])
        age_th = int(TH_AGE_MIN[cht[0,0]])
        thinfreq = 1  #int(TH_FREQ[cht[0,0]])
        volha_cf = int(CF_VOLHA[cht[0,0]])
        age_th_upper = age_cf
        YC_cht = cht[0,1]
        thin_intensity_cht = matrixFunctions.thin_intensity(YC_cht)

        newarea = 0
        endpoint_cht = len(cht)
        if clearfell_nextcycle_cht == "NoCF":
            clearfell_nextcycle_cht = 0
        else:
            clearfell_nextcycle_cht = clearfell_nextcycle_cht
        area = [None]*endpoint_cht
        ageClass = [None]*endpoint_cht
        volha = [None]*endpoint_cht
        availablevolume = [None]*endpoint_cht
        sumvolcheck1 = 0
        remainvol = 0
#        cfVolCheck = 0
        volIncPostHarvest = 0
        volIncPreHarvest = 0
        volIncNotFelled = 0
        volIncFelled = 0
        volIncFelled2 = 0
        thinvolumecheck = [None]*endpoint_cht
        check_inc = [0]*endpoint_cht
        targetthin = 940846
        targetvolcf = 272601200
        if year < 2006:
            targetthin = 940846
            targetvolcf = 272601200
        else:
            stryear = str(year)
            targetthin = int(HarvTHparm[stryear])
            targetvolcf =  int(HarvCFparm[stryear])
        targetvol = targetvolcf*cohortratio_cf
        targetThVolume = targetthin*cohortratio
        area = [None]*endpoint_cht
########  thinning preparation
        for z in range(endpoint_cht):
            ageClass[z] = cht[z,2]
#            area[z] = cht[z,3]
            area[z] = prevarea_cht[z]
            availablevolume[z] = matrixFunctions.availthvol(area[z], thin_intensity_cht, thinfreq)
            if ageClass[z] < age_th:
                thinvolume = 0
            if age_th <= ageClass[z] < age_th_upper:
                thinvolume = (prevthinvol + availablevolume[z])
            prevthinvol = thinvolume
            sumvolcheck1 += cht[z,7] * cht[z,3]
        originalvoltotal = sumvolcheck1
#        chk_newvol = 0
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
#            cfVolCheck = [None]*endpoint_cht
            ageClass[z] = cht[z,2]
#            area[z] = cht[z,3]
            volha[z] = cht[z,7]
            cai[z] = cht[z,8]
            standingvol[z] = prevvol_cht[z]
########  more thinning preparation
            availablevolume[z] = matrixFunctions.availthvol(area[z], thin_intensity_cht, thinfreq)
            actualthinvol[z] = matrixFunctions.thincheck2(availablevolume[z], ageClass[z], age_th, age_th_upper, targetThVolume, thinvolume)
            if standingvol[z] == 0:
                adjvol[z] = 0
                actualthinvol[z] = 0
                printvol = 0
            else:
                adjvol[z] = standingvol[z] - actualthinvol[z]
                if adjvol[z] < 0:
                    adjvol[z] = 0
                    actualthinvol[z] = standingvol[z]
                printvol = actualthinvol[z]
########   clearfell
            if ageClass[z] >= age_cf and volha[z] >= volha_cf:
                runVolCheck = 0
                availablevolume_cf = 0
                availablearea_cf = 0
                ageClassCount = 0
#                if cht[-1, 2] > endpoint_cht - 1: # OR cht[-1, 2] == endpoint_cht:
#                    for y in range(endpoint_cht):
#                        availablevolume_cf += (cht[y,7] * cht[y,3])
#                        availablearea_cf += cht[y,3]
#                        ageClassCount += 1
#                else:
                for y in range(z, endpoint_cht):
                    availablevolume_cf += (cht[y,7] * cht[y,3])
                    availablearea_cf += cht[y,3]
                    ageClassCount += 1
                if targetvol < availablevolume_cf:
                    print "%.d -  target < available" % year
                    that_check_inc = 0
                    standingvollist = [None]*endpoint_cht
                    standingarealist = [None]*endpoint_cht
                    for y in range(endpoint_cht):
                        standingvollist[y] =  cht[y,7] * cht[y,3]
                        sss = standingvollist[::-1]
                    rollingSumSSS = np.cumsum(sss)
                    target_age = matrixFunctions.targetage(sss, targetvol)
                    remainvol = target_age[1]
                    targetIndex = target_age[0]
                    cohortFelled = target_age[2]
                    remainarea = remainvol / cht[endpoint_cht-targetIndex-1,7]
                    volclearfelled = targetvol
                    cfVolCheck = volclearfelled
                    clearedArea2 = 0
                    newAreaFelled = 0
                    for z in range(z, endpoint_cht-targetIndex-1):
                        cai[z] = cht[z,8]
#                        area[z] = cht[z,3]
                        new_area = cht[z,3]
                        ageClass[z] = cht[z,2]
                        area[z] = prevarea_cht[z]
                        prevarea_cht[z] = cht[z-1,3]
#                        adjvol[z] = prevvol_cht[z]
                        volha[z] = matrixFunctions.volinc(cai[z], area[z], adjvol[z])
                        newstandingvol[z] = volha[z]*area[z]
                        check_inc[z] = newstandingvol[z] - cht[z,7] * cht[z,3]
                        prevvol_cht[z] = cht[z-1,3]*cht[z-1,7]
                        output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " Not clearfelled"])
                        a.writerow(output)
                        output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
                        b.writerow(output)
                        cht[z,3] = area[z]
                        cht[z,7] = volha[z]
                        volIncNotFelled += check_inc[z]
                    for z in range(endpoint_cht - targetIndex -1, endpoint_cht - targetIndex):
                        cai[z] = cht[z,8]
                        newarea = cht[z,3]
                        area[z] = prevarea_cht[z]
                        clearedArea1 = newarea - remainarea
                        del newarea
                        ageClass[z] = cht[z,2]
#                        adjvol[z] = prevvol_cht[z] # + remainvol
                        partHarvested = cht[z,3]*cht[z,7] - remainvol
                        OtherClAreaCheck = partHarvested / cht[endpoint_cht -targetIndex - 1,7]
#                        area[z] = prevarea_cht[z]
                        volha[z] = matrixFunctions.volinc(cai[z], area[z], adjvol[z])  #adjvol[z])
                        newvolha = matrixFunctions.volinc(cai[z], remainarea, remainvol)
                        newstandingvol[z] =  volha[z]*area[z]
######### new cohort added
                        if targetIndex == 0:
                            nextarea = remainarea
                            prevarea_cht.insert(z,remainarea)  #cht[z,3])
                            prevarea_cht[z] = cht[z-1,3]
                            prevvol_cht.insert(z+1,remainvol)
                            prevvol_cht[z] = cht[z-1,3]*cht[z-1,7]
#                            prevvol_cht.insert(z+1,remainvol)  # remainvol)
                            newrow = np.array((cht[0,0], YC_cht, (ageClass[z]+increment), nextarea, 0, 0, 0, newvolha, (cai[z]-1)), dtype = object)
                            holder1 = 7777
                            output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z], " doh1 - not cf"])   # , " %.2F" % check_inc[z]])
                            a.writerow(output)
                            output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
                            b.writerow(output)
                            output = (['nextrow', " %.d" % year, " %.d" % (ageClass[z]+1), " %.2F" % nextarea, " %.2F" % newvolha,  " %.2F" % remainvol, " part felling"])   # , " %.2F" % check_inc[z]])
                            a.writerow(output)
                            output = ([cht[0,0], " %.d" % year, " %.d" % (ageClass[z]+1), " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
                            b.writerow(output)
                            partAreaHarvest = 0
                        elif targetIndex != 0:
                            nextarea = remainarea # prevarea_cht[z] #cht[z+1,3]
                            partAreaHarvest = prevarea_cht[z] - nextarea
                            partHarvested = cht[z,3]*cht[z,7] - remainvol
                            newvolha = matrixFunctions.volinc(cai[z], remainarea, remainvol)
                            prevarea_cht.insert(z,remainarea)  #cht[z,3])
                            prevarea_cht[z] = cht[z-1,3]
                            prevvol_cht.insert(z+1,remainvol)
                            prevvol_cht[z] = cht[z-1,3]*cht[z-1,7]
#                            prevvol_cht.insert(z+1,remainvol)  # remainvol)
                            nextrow = np.array((cht[0,0], YC_cht, (ageClass[z]+increment), nextarea, 0, 0, 0, newvolha, (cai[z]-1)), dtype = object)
                            holder2 = 7777
                            output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z], " no cf" ])  # " %.2F" % harvested[z]  ])
                            a.writerow(output)
                            output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
                            b.writerow(output)
                            output = (['nextrow', " %.d" % year, " %.d" % (ageClass[z]+1), " %.2F" % nextarea, " %.2F" % newvolha,  " %.2F" % remainvol, " partial fell"])   # , " %.2F" % check_inc[z]])
                            a.writerow(output)
                            output = ([cht[0,0], " %.d" % year, " %.d" % (ageClass[z]+1), " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
                            b.writerow(output)

                        check_inc[z] = newstandingvol[z] - cht[z,7] * cht[z,3]

                        cht[z,3] = area[z]
                        cht[z,7] = volha[z]
                        volIncFelled += check_inc[z]
                    for z in range(endpoint_cht-targetIndex, endpoint_cht):
########  THIS loop only qualifies when targetIndex > 0
                        cai[z] = cht[z,8]
#                        area[z] = cht[z,3]
                        clearedArea2 += cht[z,3]
                        newAreaFelled += cht[z,3]
                        ageClass[z] = cht[z,2]
#                        adjvol[z] = prevvol_cht[z]
                        harvested[z] = adjvol[z]
                        area[z] = 0
                        adjvol[z] = 0
                        volha[z] = matrixFunctions.volinc(cai[z], area[z], adjvol[z])
                        newstandingvol[z] = volha[z]*area[z]
                        check_inc[z] = newstandingvol[z] - cht[z,7] * cht[z,3]
                        cht[z,3] = area[z]
                        cht[z,7] = volha[z]
                        volIncFelled2 += check_inc[z]
########  volume checks throughout re: "volIncFelled"
                    if 'volIncFelled' in locals():
                        volIncPostHarvest = volIncNotFelled + volIncFelled # + volIncPreHarvest
                    if 'volIncFelled2' in locals():
                        volIncPostHarvest = volIncPostHarvest + volIncFelled2
                    clearfell_nextcycle_cht = clearedArea2 +  clearedArea1
                    remainarea = 0
                    clearedArea1 = 0
                    clearedArea2 = 0
                    break
                elif targetvol >= availablevolume_cf:
                    areafelled = availablearea_cf #0
                    that_check_inc = 0
                    print "%.d - target > availab" % year
                    volclearfelled  = availablevolume_cf
                    for z in range(z, endpoint_cht):
                        cai[z] = cht[z,8]
                        ageClass[z] = cht[z,2]
#                        adjvol[z] = prevvol_cht[z]
                        harvested[z] = cht[z,3]*cht[z,7]
                        if ageClass[z] == endpoint_cht - ageClassCount:
                            area[z] = prevarea_cht[z]
                            prevarea_cht[z] = cht[z-1,3]
                            volha[z] = matrixFunctions.volinc(cai[z], area[z], adjvol[z])
                            newstandingvol[z] = volha[z]*area[z]
                            prevvol_cht[z] =  cht[z-1,3]*cht[z-1,7]
                        else:
                            area[z] = 0
                            prevarea_cht[z] = 0
                            adjvol[z] = 0
                            prevvol_cht[z] = 0
                            volha[z] = matrixFunctions.volinc(cai[z], area[z], adjvol[z])
                            newstandingvol[z] = volha[z]*area[z]
                        if area[z] > 0:
                            check_inc[z] = newstandingvol[z] - cht[z,7] * cht[z,3]
                            output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],  " %.2F" % harvested[z]])  # " 0.000000000" ])  #
                            a.writerow(output)
                            output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
                            b.writerow(output)
                        check_inc[z] = newstandingvol[z] - cht[z,7] * cht[z,3]
                        cht[z,3] = area[z]
                        cht[z,7] = volha[z]
                        volIncPostHarvest += check_inc[z]
                    clearfell_nextcycle_cht = areafelled
                    break
            else:
######## area & volume modification = pre-thin & pre-cf and no clearfells
                ageClass[z] = cht[z,2]
                volha[z] = cht[z,7]
                cai[z] = cht[z,8]
                if z == 0:
                    if year == afforYear:
                        area[z] = clearfell_nextcycle_cht + affor
                    elif year == deforYear:
                        area[z] = clearfell_nextcycle_cht - defor
                    else:
                        area[z] = clearfell_nextcycle_cht
                    clearfell_nextcycle_cht = 0
                    volha[z] = matrixFunctions.volinc(cai[z], area[z], adjvol[z])
                    newstandingvol[z] = area[z]*volha[z]
                    prevvol_cht[z] = 0  # cht[z-1,7]  #cht[z-1,3]*cht[z-1,7]
                elif ageClass[z] == endpoint_cht-1:
######### new cohort added
                    newarea = cht[z,3]
                    area[z] = prevarea_cht[z]
                    prevarea_cht.insert(z+1,area[z])
                    volha[z] = matrixFunctions.volinc(cai[z], area[z], adjvol[z])
                    newvolha = matrixFunctions.volinc(cht[z,8], cht[z,3], cht[z,3]*cht[z,7])
                    newstandingvol[z] = area[z]*volha[z]
                    prevvol_cht[z] = cht[z-1,3]*cht[z-1,7]
                    newadjvol = newstandingvol[z] # adjvol[z]
                    prevvol_cht.insert(z+1,area[z]*volha[z]) # newarea*newvolha)# area[z]*cht[z,7])
                    newrow = [None]*9
                    newrow = np.array((cht[0,0], YC_cht, (ageClass[z]+increment), newarea, 0, 0, 0, newvolha, (cai[z]-1)), dtype = object)
                    holder3 = 7777
                else:
                    area[z] = prevarea_cht[z]
                    volha[z] = matrixFunctions.volinc(cai[z], area[z], adjvol[z])
                    newstandingvol[z] = area[z]*volha[z]
                    prevvol_cht[z] = cht[z-1,3]*cht[z-1,7]
#                check_inc[z] = newstandingvol[z] - cht[z,7] * cht[z,3]
                prevarea_cht[z] = cht[z-1,3]
#                if cht[0,0] == 'OC':
#                if ageClass[z] >= age_th_upper:
#                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " 0.0"])
#                    a.writerow(output)
#                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
#                    b.writerow(output)
#                elif age_th <= ageClass[z] < age_th_upper:
#                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " %.2F" % actualthinvol[z]])
#                    a.writerow(output)
#                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
#                    b.writerow(output)
#                else:
#                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " 0.0000"])
#                    a.writerow(output)
#                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
#                    b.writerow(output)
                if ageClass[z] >= age_th_upper:
                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " 0.0", " %.3F" % cai[z]])
                    a.writerow(output)
                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
                    b.writerow(output)
                elif age_th <= ageClass[z] < age_th_upper:
                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],  " %.2F" % printvol, " %.3F" % cai[z]]) #actualthinvol[z]])
                    a.writerow(output)
                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
                    b.writerow(output)
                else:
                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " 0.0000", " %.3F" % cai[z]])
                    a.writerow(output)
                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
                    b.writerow(output)

                if 'holder3' in locals():
                    cht = np.vstack([cht, newrow])
#                    if cht[0,0] == 'PA12':
                    output = (["newrow", " %.d" % year, " %.d" % cht[(z+1),2], " %.2F" % cht[z+1,3], " %.2F" % cht[z+1,7],  " %.2F" % (cht[z+1,3]*cht[z+1,7]),   " 0.000"])
                    a.writerow(output)
                    output = ([cht[0,0], " %.d" % year, " %.d" % cht[z+1,2], " %.d" % prevarea_cht[z+1], " %.2f" % prevvol_cht[z+1]])
                    b.writerow(output)
                    del holder3
                    del newrow
                check_inc[z] = newstandingvol[z] - cht[z,7] * cht[z,3]
                cht[z,3] = area[z]
                cht[z,7] = volha[z]
                volIncPreHarvest += check_inc[z]

                thinTotal += printvol #actualthinvol[z]
                printvol = 0 #actualthinvol[z] = 0
################   Biomass calculations   ################
####  Note: at-based indexing on an integer index can only have integer indexers
####        use "cohort" instead of 'cht'

#bm_cohort = 0
#                if year > 2000:
#                    cht_volha = volha[z]  # 5.4128246  #112.82  #sum_sv / sumarea
#                    bm = matrixFunctions.sbiom(inParm1.loc[bm_cohort,'1a'], inParm1.loc[bm_cohort,'1b'], cht_volha)
#                    nonmerch = matrixFunctions.nmbiom(inParm2.loc[bm_cohort,'2a'], inParm2.loc[bm_cohort,'2b'], inParm2.loc[bm_cohort,'2k'], bm, inParm2.loc[bm_cohort,'fbnlim'])
#                    bnm = bm + nonmerch
#                    bs = matrixFunctions.sapfactor(inParm3.loc[bm_cohort,'3a'], inParm3.loc[bm_cohort,'3b'],inParm3.loc[bm_cohort,'3k'], nonmerch, inParm3.loc[bm_cohort,'fbslim'] )
#                    bsnm = bs + bnm
#                    #                    othersbf = bsnm / bnm
#                    if bs == 0.5:
#                        biomassswt = bs
#                    else:
#                        biomassswt = bm  + nonmerch + bs
#                    pstem = matrixFunctions.pStemwood(inParm5.loc[bm_cohort,'a1'],inParm5.loc[bm_cohort,'a2'],inParm5.loc[bm_cohort,'a3'],
#                              inParm5.loc[bm_cohort,'b1'],inParm5.loc[bm_cohort,'b2'],inParm5.loc[bm_cohort,'b3'],
#                              inParm5.loc[bm_cohort,'c1'],inParm5.loc[bm_cohort,'c2'],inParm5.loc[bm_cohort,'c3'], cht_volha)
#                    biomassag = biomassswt / pstem
#
#                    pbark = matrixFunctions.pBark(inParm5.loc[bm_cohort,'a1'],inParm5.loc[bm_cohort,'a2'],inParm5.loc[bm_cohort,'a3'],
#                              inParm5.loc[bm_cohort,'b1'],inParm5.loc[bm_cohort,'b2'],inParm5.loc[bm_cohort,'b3'],
#                              inParm5.loc[bm_cohort,'c1'],inParm5.loc[bm_cohort,'c2'],inParm5.loc[bm_cohort,'c3'], cht_volha)
#                    biomassbk = biomassag * pbark
#
#                    pbranch = matrixFunctions.pBranch(inParm5.loc[bm_cohort,'a1'],inParm5.loc[bm_cohort,'a2'],inParm5.loc[bm_cohort,'a3'],
#                      inParm5.loc[bm_cohort,'b1'],inParm5.loc[bm_cohort,'b2'],inParm5.loc[bm_cohort,'b3'],
#                      inParm5.loc[bm_cohort,'c1'],inParm5.loc[bm_cohort,'c2'],inParm5.loc[bm_cohort,'c3'], cht_volha)
#                    biomassbr = biomassag * pbranch
#
#                    pfoliage = matrixFunctions.pFoliage(inParm5.loc[bm_cohort,'a1'],inParm5.loc[bm_cohort,'a2'],inParm5.loc[bm_cohort,'a3'],
#                      inParm5.loc[bm_cohort,'b1'],inParm5.loc[bm_cohort,'b2'],inParm5.loc[bm_cohort,'b3'],
#                      inParm5.loc[bm_cohort,'c1'],inParm5.loc[bm_cohort,'c2'],inParm5.loc[bm_cohort,'c3'], cht_volha)
#                    biomassfl = biomassag * pfoliage
#
#                    biomasstem = biomassag - biomassbk - biomassbr - biomassfl
#                    biomassbg = matrixFunctions.sbiomroot(inParm4.loc[bm_cohort,'4a'], inParm4.loc[bm_cohort, '4b'], biomassag )
#
#                    pf = 0.072+0.354*math.exp(-0.06*biomassbg)
#                    frb = pf*biomassbg
#                    # Eq10
#                    frto = frb * DOM['DOM_FRTO']
#                    litterIn = biomassfl*DOM['DOM_FoliageHW']
#                    crto = biomassbg*DOM['DOM_CoarseRoot']
#                    owto = (biomassbr+bs)*DOM['DOM_OWTO']
#                    sto = biomasstem*DOM['DOM_STO']
#                    output = (["Frto = %.2f" % frto, "Littinin = %.2f" % litterIn, "Crto = %.2f" % crto, "Owto = %.2f" % owto, "Sto = %.2f" % sto])
#                    a.writerow(output)


########  more volume checks
        volIncPostHarvest = volIncPostHarvest + volIncPreHarvest
        finalvoltotal = 0
        sumarea = 0
        presum = 0
        finalvol = [None]*endpoint_cht
        volumeCheck2 = 0

########  area check
        for z in range(endpoint_cht):
            volumeCheck2 += cht[z,7] * cht[z,3]
            presum += cht[z,3]
        if 'newarea' in locals():
            sumarea = presum  + newarea
            del newarea
        elif 'nextarea' in locals():
            sumarea = presum + nextarea
            del nextarea
        else:
            sumarea = presum
        areaTotal = sumarea  + clearfell_nextcycle_cht

#        if cht[0,0] == 'OC':
        output = (["Year = "," %.d" % year])
        a.writerow(output)
        output = (["Species cohort = %s" % cht[0,0]])
        a.writerow(output)
        volumeCheck1 = originalvoltotal + volIncPostHarvest
        output = (["VolCheck1 = %.2F" % volumeCheck1])
        a.writerow(output)
        output = (["VolCheck2 = %.2F" % volumeCheck2] )
        a.writerow(output)
        output = (["Area check = "," %.2F" % areaTotal ])
        a.writerow(output)
        output = (["VolHa check = %.2F" % (volumeCheck1 / areaTotal ) ])
        a.writerow(output)
        output = (["CF Volume Target = %.d" % targetvol ])
        a.writerow(output)
#        output = (["Volume TargetTh = %.d" % targetThVolume ])
#        a.writerow(output)
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
        if year > 2000:
            sum_sv = volumeCheck1
#            sum_hv += thinTotal + volclearfelled
#            output = (["summary_st_vol = %.2f" % sum_sv])
#            a.writerow(output)

########  These two lines removing lines of trailing zeros
        n = np.sum((np.where(cht[:,3] >0),np.where(cht[:,5]>0)),axis = 1)[0][-1]
        cht = cht[:(n+1)]

        if 'holder1' in locals():
            n = np.sum((np.where(cht[:,3] >0),np.where(cht[:,5]>0)),axis = 1)[0][-1]
            cht = cht[:(n+1)]
            cht = np.vstack([cht, newrow])
            del holder1
            del newrow
        if 'holder2' in locals():
            n = np.sum((np.where(cht[:,3] >0),np.where(cht[:,5]>0)),axis = 1)[0][-1]
            cht = cht[:(n+1)]
            cht = np.vstack([cht, nextrow])
            del holder2
            del nextrow


        if 'volclearfelled' in locals():
            sum_hv = thinTotal + volclearfelled
#            output = (["Volume Clearfelled = %.2f" % volclearfelled ])
#            a.writerow(output)
#            output = (["summary_hv_vol = %.2f" % sum_hv])
#            a.writerow(output)
########  These lines keep the prev* lists in line with the cht matrix
            while len(prevarea_cht) > len(cht)  :
                prevarea_cht.pop()
            while len(prevvol_cht) > len(cht) :
                prevvol_cht.pop()
            del volclearfelled
        else:
            print "%.d -  nope to cf" % year

########  This step deals with issue when a row of zeros is removed but the
########      ages aren't monotonic, which causes probs down the line
        endpoint_cht = len(cht)
        if cht[endpoint_cht-1,2] - cht[endpoint_cht-2,2]>1:
            cht[endpoint_cht-1,2] = cht[endpoint_cht-2,2] + 1
        endpoint_cht = len(cht)

######## end cohort re-naming:
        if cohort == 0:
            PA12 = cht
            endpoint_PA12 = endpoint_cht
            clearfell_nextcycle_PA12 = clearfell_nextcycle_cht
            prevarea_PA12 = prevarea_cht
            prevvol_PA12 = prevvol_cht
            annual_sv = sum_sv
            annual_hv = sum_hv
        elif cohort == 1:
            PA16 = cht
            endpoint_PA16 = endpoint_cht
            clearfell_nextcycle_PA16 = clearfell_nextcycle_cht
            prevarea_PA16 = prevarea_cht
            prevvol_PA16 = prevvol_cht
            annual_sv = sum_sv + annual_sv
            annual_hv = sum_hv + annual_hv
        elif cohort == 2:
            PA20 = cht
            endpoint_PA20 = endpoint_cht
            clearfell_nextcycle_PA20 = clearfell_nextcycle_cht
            prevarea_PA20 = prevarea_cht
            prevvol_PA20 = prevvol_cht
            annual_sv = sum_sv + annual_sv
            annual_hv = sum_hv + annual_hv
        elif cohort == 3:
            PA24 = cht
            endpoint_PA24 = endpoint_cht
            clearfell_nextcycle_PA24 = clearfell_nextcycle_cht
            prevarea_PA24 = prevarea_cht
            prevvol_PA24 = prevvol_cht
            annual_sv = sum_sv + annual_sv
            annual_hv = sum_hv + annual_hv
        elif cohort == 4:
            PA30 = cht
            endpoint_PA30 = endpoint_cht
            clearfell_nextcycle_PA30 = clearfell_nextcycle_cht
            prevarea_PA30 = prevarea_cht
            prevvol_PA30 = prevvol_cht
            annual_sv = sum_sv + annual_sv
            annual_hv = sum_hv + annual_hv
        elif cohort == 5:
            PS12 = cht
            endpoint_PS12 = endpoint_cht
            clearfell_nextcycle_PS12 = clearfell_nextcycle_cht
            prevarea_PS12 = prevarea_cht
            prevvol_PS12 = prevvol_cht
            annual_sv = sum_sv + annual_sv
            annual_hv = sum_hv + annual_hv
        elif cohort == 6:
            PS20 = cht
            endpoint_PS20 = endpoint_cht
            clearfell_nextcycle_PS20 = clearfell_nextcycle_cht
            prevarea_PS20 = prevarea_cht
            prevvol_PS20 = prevvol_cht
            annual_sv = sum_sv + annual_sv
            annual_hv = sum_hv + annual_hv
        elif cohort == 7:
            OC = cht
            endpoint_OC = endpoint_cht
            clearfell_nextcycle_OC = clearfell_nextcycle_cht
            prevarea_OC = prevarea_cht
            prevvol_OC = prevvol_cht
            annual_sv = sum_sv + annual_sv
            annual_hv = sum_hv + annual_hv
        elif cohort == 8:
            Cmix = cht
            endpoint_Cmix = endpoint_cht
            clearfell_nextcycle_Cmix = clearfell_nextcycle_cht
            prevarea_Cmix = prevarea_cht
            prevvol_Cmix = prevvol_cht
            annual_sv = sum_sv + annual_sv
            annual_hv = sum_hv + annual_hv
        elif cohort == 9:
            CBmix = cht
            endpoint_CBmix = endpoint_cht
            clearfell_nextcycle_CBmix = clearfell_nextcycle_cht
            prevarea_CBmix = prevarea_cht
            prevvol_CBmix = prevvol_cht
            annual_sv = sum_sv + annual_sv
            annual_hv = sum_hv + annual_hv
        elif cohort == 10:
            FGB = cht
            endpoint_FGB = endpoint_cht
            clearfell_nextcycle_FGB = clearfell_nextcycle_cht
            prevarea_FGB = prevarea_cht
            prevvol_FGB = prevvol_cht
            annual_sv = sum_sv + annual_sv
            annual_hv = sum_hv + annual_hv
        elif cohort == 11:
            SGB = cht
            endpoint_SGB = endpoint_cht
            clearfell_nextcycle_SGB = clearfell_nextcycle_cht
            prevarea_SGB = prevarea_cht
            prevvol_SGB = prevvol_cht
            annual_sv = sum_sv + annual_sv
            annual_hv = sum_hv + annual_hv
        cht = 0
        thinTotal = 0
        remainvol = 0
        targetIndex = 0

#    ANUUAL SUMMARIES
    annual_sv += sum_sv
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
    year = year + 1

commaout.close()
