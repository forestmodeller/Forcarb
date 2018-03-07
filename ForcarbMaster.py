from IPython import get_ipython
get_ipython().magic('reset -sf')
#     %reset
import numpy as np
import csv
import os
import pandas as pd
from pandas import DataFrame
#from __future__ import division

     
#### Functions #### 
    
def availthvol(area, intensity):
    availablevolume = (intensity*area*thinfreq)
    return availablevolume

   
def thincheck2(availablevolume):
    if ageClass[z] < age_th: # or ageClass >= age_th_upper:
        actualthinvol = 0
    elif age_th <= ageClass[z] < age_th_upper:
        actualthinvol = (availablevolume * targetThVolume / thinvolume)
    else:
        actualthinvol = 0
    return actualthinvol
            
def volinc(cai, area, standingvol):
    vol_inc = cai * area
    newvol = standingvol + vol_inc
    if newvol <= 0 or area <= 0:
#    if newvol <= 0.0001 or area <= 0.0001        
        volha = 0
    else:
        volha = newvol / area 
    return volha

def thin_intensity(YC):
    intensity = YC*1*0.7
    return intensity
     
def targetage(lst, target):
    i = 0
    newtotal = lst[i]
    if newtotal > target:
        remainvol = newtotal - target
        pass
    else:
        while newtotal <= target:        
            i += 1
            newtotal += lst[i] 
        remainvol = newtotal - target
    return i, remainvol, lst[i-1]  
 
def previous(cht, endpoint, prevarea, prevvol):
    arealist = cht[:,3]
    volumelist = cht[:,7]    
    for x in range(endpoint):
        prevarea[x] = arealist[x]
        prevvol[x] = volumelist[x]*arealist[x]
    return prevarea, prevvol 
    
#os.chdir("D:\Data\DropDS\Notes & work\IrishLandUSes\Matrix\Files")
os.chdir("C:\Users\UCD\Documents\Cloudstation\Notes & work\IrishLandUSes\Matrix\Files")


#with open('AgeMatrixNFI2017.csv', mode='r') as infile:
#    reader = csv.reader(infile)
#    FM_TH = dict((rows[0],rows[1]) for rows in reader)


### Harvest rules by year
with open('HarvestTargets.csv', mode='r') as infile:
    reader = csv.reader(infile)
    FM_TH = dict((rows[0],rows[1]) for rows in reader)   #p2
with open('HarvestTargets.csv', mode='r') as infile:
    reader = csv.reader(infile)    
    FM_CF = dict((rows[0],rows[2]) for rows in reader) 
#with open('HarvestTargets.csv', mode='r') as infile:
#    reader = csv.reader(infile)     
#    AR_TH = dict((rows[0],rows[3]) for rows in reader) 
#with open('HarvestTargets.csv', mode='r') as infile:
#    reader = csv.reader(infile)     
#    AR_CF = dict((rows[0],rows[4]) for rows in reader)  
##        mydict = {rows[0]:rows[1] for rows in reader}   #p3    


with open('ClearfellRules.csv', mode='r') as infile:
    reader = csv.reader(infile)
    CF_AGE_MIN = dict((rows[0],rows[1]) for rows in reader)
with open('ClearfellRules.csv', mode='r') as infile:
    reader = csv.reader(infile)
    CF_VOLHA = dict((rows[0],rows[3]) for rows in reader)
    
with open('ThinningHarvestRules.csv', mode='r') as infile:
    reader = csv.reader(infile)
    TH_AGE_MIN = dict((rows[0],rows[1]) for rows in reader)
with open('ThinningHarvestRules.csv', mode='r') as infile:
    reader = csv.reader(infile)
    TH_VOLHA = dict((rows[0],rows[3]) for rows in reader)
  
    
##### file managment
#m_df = pd.read_csv("AgeMatrixNFI2012_Redux_cohorts.csv",names = ['FT', 'YC','Age', 'Area', 'Litter', 'Stump', 'DW', 'Volha','CAI'])
m_df = pd.read_csv("AgeMatrixNFI2017_portion.csv",names = ['FT', 'YC','Age', 'Area', 'Litter', 'Stump', 'DW', 'Volha','CAI'])

##### cohort managment
#PA = m_df[m_df.FT == 'PA']
PA = DataFrame(m_df, columns = ['FT', 'YC','Age', 'Area', 'Litter', 'Stump', 'DW', 'Volha','CAI'])
#PA["newcht"] = PA["FT"].map(str) + PA["YC"]
PA12 = PA[PA.YC == 12]
endpoint_PA12 = len(PA12.index)
#endpoint_PA12_1 = endpoint_PA12
#endpoint = max(PA12.index)
PA12 = PA12.values
PA16 = PA[PA.YC == 16]
endpoint_PA16 = len(PA16.index)
#endpoint_PA16_1 = endpoint_PA16
PA16 = PA16.values
PA20 = PA[PA.YC == 20]
endpoint_PA20 = len(PA20.index)
PA20 = PA20.values
PA24 = PA[PA.YC == 24]
endpoint_PA24 = len(PA24.index)
PA24 = PA24.values
#PS = m_df[m_df.FT == 'PS']
#PS = DataFrame(PS, columns = ['FT', 'YC','Age', 'Area', 'Litter', 'Stump', 'DW', 'Volha','CAI'])
#PScopy = PS
#endpointPS = len(PS.index)
#PS = PS.values
#OC = m_df[m_df.FT == 'OC']
#OC = DataFrame(OC, columns = ['FT', 'YC','Age', 'Area', 'Litter', 'Stump', 'DW', 'Volha','CAI'])
#OC = OC.values
#AC = m_df[m_df.FT == 'AC']
#AC = DataFrame(AC, columns = ['FT', 'YC','Age', 'Area', 'Litter', 'Stump', 'DW', 'Volha','CAI'])
#AC = AC.values
#FS = m_df[m_df.FT == 'FS']
#FS = DataFrame(FS, columns = ['FT', 'YC','Age', 'Area', 'Litter', 'Stump', 'DW', 'Volha','CAI'])
#FS = FS.values
#OB = m_df[m_df.FT == 'OB']
#OB = DataFrame(OB, columns = ['FT', 'YC','Age', 'Area', 'Litter', 'Stump', 'DW', 'Volha','CAI'])
#OB = OB.values



cohortlist = 4 #(1,2)   # PA12, PA16, etc.

for cohort in range(cohortlist):
    if cohort == 0: 
        prevarea_PA12 = [None]*endpoint_PA12
        prevvol_PA12 = [None]*endpoint_PA12
        prevarea_PA12, prevvol_PA12 = previous(PA12, endpoint_PA12, prevarea_PA12, prevvol_PA12)
    if cohort == 1: 
        prevarea_PA16 = [None]*endpoint_PA16
        prevvol_PA16 = [None]*endpoint_PA16
        prevarea_PA16, prevvol_PA16 = previous(PA16, endpoint_PA16, prevarea_PA16, prevvol_PA16)        
    if cohort == 2:  
        prevarea_PA20 = [None]*endpoint_PA20
        prevvol_PA20 = [None]*endpoint_PA20
        prevarea_PA20, prevvol_PA20 = previous(PA20, endpoint_PA20, prevarea_PA20, prevvol_PA20)  
    if cohort == 3: 
        prevarea_PA24 = [None]*endpoint_PA24
        prevvol_PA24 = [None]*endpoint_PA24
        prevarea_PA24, prevvol_PA24 = previous(PA24, endpoint_PA24, prevarea_PA24, prevvol_PA24)  
        

### initialise variables
thinfreq = 0.2
thinvolume = 0
prevthinvol = 0
defor = 0 # 1000
deforYear = 35
affor = 0 # 500
afforYear = 25
remainvol = 0
newcohortvol = 0
#newcohortarea_old = 0
#newcohortarea = 0
new_area = 0
#newrow = [None]*9
chk_newvol = 0
runTotalThin_cht = 0
runTotalThin_PS = 0
sum_sv = 0
sum_hv = 0
annual_sv = 0
areaFelled = 0
#appendarea = 0
#appendvol = 0
clearfell_nextcycle_PA12 = 2000 
clearfell_nextcycle_PA16 = 1800 
clearfell_nextcycle_PA20 = 1800 
clearfell_nextcycle_PA24 = 1800 
cohortratio = 0.13 
cohortratio_cf = 0.13
increment = 1

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


      
year = 1906
# cohort 1, cohort 2, etc
# stores each cohort's respective variables
while year <= 2030:      
    for cohort in range(cohortlist):
        if cohort == 0:  # PA12:
            cht = PA12
#            endpoint_cht = endpoint_PA12
#            endpoint_cht_1 = endpoint_PA12_1
            clearfell_nextcycle_cht = clearfell_nextcycle_PA12
            prevarea_cht = prevarea_PA12
            prevvol_cht = prevvol_PA12
        elif cohort == 1:  # PA16:
            cht = PA16
#            endpoint_cht = endpoint_PA16
#            endpoint_cht_1 = endpoint_PA16_1        
            clearfell_nextcycle_cht = clearfell_nextcycle_PA16   
            prevarea_cht = prevarea_PA16
            prevvol_cht = prevvol_PA16   
        elif cohort == 2:  # PA16:
            cht = PA20
#            endpoint_cht = endpoint_PA16       
            clearfell_nextcycle_cht = clearfell_nextcycle_PA20 
            prevarea_cht = prevarea_PA20
            prevvol_cht = prevvol_PA20
        elif cohort == 3:  # PA16:
            cht = PA24
#            endpoint_cht = endpoint_PA16        
            clearfell_nextcycle_cht = clearfell_nextcycle_PA24
            prevarea_cht = prevarea_PA24
            prevvol_cht = prevvol_PA24               
        age_cf = int(CF_AGE_MIN[cht[0,0]])
        age_th = int(TH_AGE_MIN[cht[0,0]])
        volha_cf = int(CF_VOLHA[cht[0,0]])
        age_th_upper = age_cf        
        YC_cht = cht[0,1]
        thin_intensity_cht = thin_intensity(YC_cht)
        
#        n = np.sum((np.where(cht[:,3] >0),np.where(cht[:,5]>0)),axis = 1)[0][-1]
#        cht = cht[:(n+1)]
        newarea = 0
        endpoint_cht = len(cht)
        if clearfell_nextcycle_cht == "NoCF":
            clearfell_nextcycle_cht = 0
#            newcohortarea_old = newcohortarea
        else:
            clearfell_nextcycle_cht = clearfell_nextcycle_cht
        area = [None]*endpoint_cht     
        ageClass = [None]*endpoint_cht 
        volha = [None]*endpoint_cht     
        availablevolume = [None]*endpoint_cht      
        sumvolcheck1 = 0  
        remainvol = 0
        cfVolCheck = 0
        run_check_inc = 0
        run_check_inc_early = 0
        run_check_inc_one = 0
        run_check_inc_two = 0
        run_check_inc_three = 0
        thinvolumecheck = [None]*endpoint_cht
        check_inc = [0]*endpoint_cht
        targetthin = 940846
        targetvolcf = 272601200        
        if year < 2006:
            targetthin = 940846
            targetvolcf = 272601200
        else:
            stryear = str(year)
            targetthin = int(FM_TH[stryear])
            targetvolcf =  int(FM_CF[stryear])
        targetvol = targetvolcf*cohortratio_cf     
        targetThVolume = targetthin*cohortratio          
        for z in range(endpoint_cht):       
            ageClass[z] = cht[z,2]
            area[z] = cht[z,3]
            availablevolume[z] = availthvol(area[z], thin_intensity_cht)
            if ageClass[z] < age_th:
                thinvolume = 0
            if age_th <= ageClass[z] < age_th_upper:
                thinvolume = (prevthinvol + availablevolume[z])
            prevthinvol = thinvolume   
            sumvolcheck1 += cht[z,7] * cht[z,3]
        originalvoltotal = sumvolcheck1 
        chk_newvol = 0
        area = [None]*endpoint_cht     
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
            cfVolCheck = [None]*endpoint_cht  
            ageClass[z] = cht[z,2]               
            area[z] = cht[z,3]      
            volha[z] = cht[z,7]  
            cai[z] = cht[z,8]
            standingvol[z] = prevvol_cht[z] # cht[z,7] * cht[z,3]  
        #####  thinning         
            availablevolume[z] = availthvol(area[z], thin_intensity_cht)
            actualthinvol[z] = thincheck2(availablevolume[z])
            if standingvol[z] == 0:
                adjvol[z] = 0
            else:
                adjvol[z] = standingvol[z] - actualthinvol[z]
        #####   clearfell
            if ageClass[z] >= age_cf and volha[z] >= volha_cf:
                runVolCheck = 0
                availablevolume_cf = 0
                availablearea_cf = 0   
#                adjvol[z] = prevvol_cht[z]
                ageClassCount = 0
                for y in range(z, endpoint_cht):
                    availablevolume_cf += (cht[y,7] * cht[y,3])   #prevvol_cht[y] #
                    availablearea_cf += cht[y,3]
                    ageClassCount += 1
                if targetvol < availablevolume_cf:
#                    print "%.d -  target < available" % remainarea
                    that_check_inc = 0
                    standingvollist = [None]*endpoint_cht  
                    standingarealist = [None]*endpoint_cht
                    for y in range(endpoint_cht):        
                        standingvollist[y] =  cht[y,7] * cht[y,3]  #prevvol_cht[y] #
                        sss = standingvollist[::-1]
#                        standingarealist[y] = cht[y,3]
#                        ttt = standingarealist[::-1]
                    rollingSumSSS = np.cumsum(sss)                
                    target_age = targetage(sss, targetvol)
                    remainvol = target_age[1]
                    targetIndex = target_age[0]
#                    print targetIndex                    
                    cohortFelled = target_age[2]
                    remainarea = remainvol / cht[endpoint_cht-targetIndex-1,7]  
#                    print "- %.d -  target < available" % year # ageClassCount                   
                    volclearfelled = targetvol   
                    cfVolCheck = volclearfelled 
                    clearedArea = 0 
                    newAreaFelled = 0
                    for z in range(z, endpoint_cht-targetIndex-1):  
                        cai[z] = cht[z,8]
                        area[z] = cht[z,3]
                        new_area = cht[z,3] 
                        ageClass[z] = cht[z,2] 
                        area[z] = prevarea_cht[z]                           
                        prevarea_cht[z] = cht[z-1,3] 
                        adjvol[z] = prevvol_cht[z]
                        volha[z] = volinc(cai[z], area[z], adjvol[z])
                        newstandingvol[z] = volha[z]*area[z] 
                        check_inc[z] = newstandingvol[z] - cht[z,7] * cht[z,3]
                        prevvol_cht[z] = cht[z-1,3]*cht[z-1,7]  
                        output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " Not clearfelled"])
                        a.writerow(output)
                        output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
                        b.writerow(output)
                        cht[z,3] = area[z]
                        cht[z,7] = volha[z]
                        run_check_inc_one += check_inc[z]                                 
                    for z in range(endpoint_cht - targetIndex -1, endpoint_cht - targetIndex):
                        cai[z] = cht[z,8]
#                        felledCohort = cht[z,3] 
#                        newAreaFelled += cht[z,3]
                        newarea = cht[z,3]
                        area[z] = prevarea_cht[z] 
                        OtherClearedArea = newarea - remainarea
                        del newarea
                        ageClass[z] = cht[z,2]
                        adjvol[z] = prevvol_cht[z] # + remainvol                        
                        partHarvested = cht[z,3]*cht[z,7] - remainvol
                        OtherClAreaCheck = partHarvested / cht[endpoint_cht -targetIndex - 1,7]                          
#                        area[z] = prevarea_cht[z]  
                        volha[z] = volinc(cai[z], area[z], adjvol[z])  #adjvol[z])
                        newvolha = volinc(cai[z], remainarea, remainvol) 
                        newstandingvol[z] =  volha[z]*area[z]
                        # new cohort added
                        if targetIndex == 0:
                            nextarea = remainarea
                            prevarea_cht.insert(z,remainarea)  #cht[z,3])
                            prevarea_cht[z] = cht[z-1,3]
#                            newvolha = volha[z]
    #                        prevvol_cht[z] = cht[z-1,3]*cht[z-1,7]
#                            prevvol_cht.insert(z, newstandingvol[z]) 
#                            print partHarvested
                            prevvol_cht.insert(z+1,remainvol)                            
                            prevvol_cht[z] = cht[z-1,3]*cht[z-1,7]
#                            prevvol_cht.insert(z+1,remainvol)  # remainvol)
                            newrow = np.array((cht[0,0], YC_cht, (ageClass[z]+increment), nextarea, 0, 0, 0, newvolha, (cai[z]-1)), dtype = object)
                            cats = 7777                                                   
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
#                            OtherClearedArea =   cht[z+1,3]
                            partHarvested = cht[z,3]*cht[z,7] - remainvol
                            newvolha = volinc(cai[z], remainarea, remainvol) 
                            prevarea_cht.insert(z,remainarea)  #cht[z,3])
                            prevarea_cht[z] = cht[z-1,3]
#                            newvolha = volha[z]
    #                        prevvol_cht[z] = cht[z-1,3]*cht[z-1,7]
#                            prevvol_cht.insert(z, newstandingvol[z]) 
#                            print partHarvested
                            prevvol_cht.insert(z+1,remainvol)                            
                            prevvol_cht[z] = cht[z-1,3]*cht[z-1,7]
#                            prevvol_cht.insert(z+1,remainvol)  # remainvol)
                            nextrow = np.array((cht[0,0], YC_cht, (ageClass[z]+increment), nextarea, 0, 0, 0, newvolha, (cai[z]-1)), dtype = object)
                            eagle = 7777                                                   
                            output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z], " no cf" ])  # " %.2F" % harvested[z]  ])
                            a.writerow(output)
                            output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
                            b.writerow(output)
                            output = (['nextrow', " %.d" % year, " %.d" % (ageClass[z]+1), " %.2F" % nextarea, " %.2F" % newvolha,  " %.2F" % remainvol, " partial fell"])   # , " %.2F" % check_inc[z]])
                            a.writerow(output)
                            output = ([cht[0,0], " %.d" % year, " %.d" % (ageClass[z]+1), " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
                            b.writerow(output)                             
                            
                        check_inc[z] = newstandingvol[z] - cht[z,7] * cht[z,3]  # + chk_newvol        
    
                        cht[z,3] = area[z]
                        cht[z,7] = volha[z]         
                        run_check_inc_two += check_inc[z] 
                    for z in range(endpoint_cht-targetIndex, endpoint_cht):
#                #  THIS loop only qualifies when targetIndex > 0
                        cai[z] = cht[z,8] 
                        area[z] = cht[z,3] 
                        clearedArea += cht[z,3] 
                        newAreaFelled += cht[z,3]
                        ageClass[z] = cht[z,2] 
#                        standingvol[z] = cht[z,7] * cht[z,3]                        
                        adjvol[z] = prevvol_cht[z]                       
                        harvested[z] = adjvol[z]
                        area[z] = 0
#                        prevarea_cht[z] = 0
                        adjvol[z] = 0  # standingvol
                        volha[z] = volinc(cai[z], area[z], adjvol[z])                     
                        newstandingvol[z] = volha[z]*area[z]
#                        prevvol_cht[z] = 0  
                        check_inc[z] = newstandingvol[z] - cht[z,7] * cht[z,3]                       
                        cht[z,3] = area[z]
                        cht[z,7] = volha[z]
                        run_check_inc_three += check_inc[z]  
#                    if 'cats' in locals():        
#                        cht = np.vstack([cht, newrow]) 
##                        output = (["newrow", " %.d" % year, " %.d" % cht[(z+1),2], " %.2F" % cht[z+1,3], " %.2F" % cht[z+1,7],  " %.2F" % (cht[z+1,3]*cht[z+1,7]),  " %.2F" % partHarvested  ])
##                        a.writerow(output)
##                        output = ([cht[0,0], " %.d" % year, " %.d" % cht[z+1,2], " %.d" % prevarea_cht[z+1], " %.2f" % prevvol_cht[z+1]])
##                        b.writerow(output)
#                        del cats   
#                        del newrow        
#                    if 'eagle' in locals():
#                        cht = np.vstack([cht, nextrow]) 
##                        output = (["nextrow", " %.d" % year, " %.d" % cht[(z+1),2], " %.2F" % cht[z+1,3], " %.2F" % cht[z+1,7],  " %.2F" % (cht[z+1,3]*cht[z+1,7]),  " %.2F" % partHarvested  ])
##                        a.writerow(output)
##                        output = ([cht[0,0], " %.d" % year, " %.d" % cht[z+1,2], " %.d" % prevarea_cht[z+1], " %.2f" % prevvol_cht[z+1]])
##                        b.writerow(output)
#                        del eagle   
#                        del nextrow                         
                    if 'run_check_inc_two' in locals():
                        run_check_inc = run_check_inc_one + run_check_inc_two # + run_check_inc_early
                    if 'run_check_inc_three' in locals():
                        run_check_inc = run_check_inc + run_check_inc_three
#                    TotalClearedArea = clearedArea +  OtherClAreaCheck    # + OtherClearedArea #
                    clearfell_area_cht = clearedArea +  OtherClearedArea   #partAreaHarvest  #OtherClAreaCheck    
#                    clearfell_area_cht = newAreaFelled - remainarea
                    remainarea = 0
                    clearedArea = 0
                    print "- %.d -  target < available" % year # newAreaFelled # clearfell_area_cht 
#                    print targetIndex
#                    print cht[0,0]
                    ClearfellCheck = clearfell_area_cht
                    clearfell_nextcycle_cht =   clearfell_area_cht  # TotalClearedArea
                    clearfell_area_cht = 0       
                    break
                elif targetvol >= availablevolume_cf:
                    areafelled = availablearea_cf #0 
                    that_check_inc = 0
                    print "%.d - target > availab" % year
                    volclearfelled  = availablevolume_cf  
                    cfVolCheck[z] = volclearfelled
                    runVolCheck += cfVolCheck[z]
                    for z in range(z, endpoint_cht):    
#                        print "   woot"
                        cai[z] = cht[z,8]
                        ageClass[z] = cht[z,2] 
#                        areafelled += cht[z,3] 
                        adjvol[z] = prevvol_cht[z]                                 
                        harvested[z] = cht[z,3]*cht[z,7] 
                        if ageClass[z] == endpoint_cht - ageClassCount:
#                        cht[z,3]*cht[z,7] == availablevolume_cf:
                            area[z] = prevarea_cht[z]  #areamod(0, prevarea_cht[z-1])
                            prevarea_cht[z] = cht[z-1,3] 
                            volha[z] = volinc(cai[z], area[z], adjvol[z])
                            newstandingvol[z] = volha[z]*area[z]                        
                            prevvol_cht[z] =  cht[z-1,3]*cht[z-1,7]                             
                        else:
                            area[z] = 0 
                            prevarea_cht[z] = 0# cht[z-1,3]
                            adjvol[z] = 0    #standingvol
                            prevvol_cht[z] = 0# cht[z-1,3]*cht[z-1,7]                      
                            volha[z] = volinc(cai[z], area[z], adjvol[z])
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
                        run_check_inc += check_inc[z]                 
                    clearfell_area_cht = areafelled
                    clearfell_nextcycle_cht = clearfell_area_cht
                    clearfell_area_cht = 0  
                    break    
            else:
            #####  area & volume modification = pre-thin & pre-cf and no clearfells              
                ageClass[z] = cht[z,2]      
#                newarea = cht[z,3]                
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
                    volha[z] = volinc(cai[z], area[z], adjvol[z])
                    newstandingvol[z] = area[z]*volha[z]
                    prevvol_cht[z] = 0  # cht[z-1,7]  #cht[z-1,3]*cht[z-1,7] 
                elif z == endpoint_cht-1:
                    newarea = cht[z,3]                    
                    area[z] = prevarea_cht[z]
                    prevarea_cht.insert(z+1,area[z])
                    volha[z] = volinc(cai[z], area[z], adjvol[z])
                    newvolha = volinc(cht[z,8], cht[z,3], cht[z,3]*cht[z,7])
                    newstandingvol[z] = area[z]*volha[z]
                    prevvol_cht[z] = cht[z-1,3]*cht[z-1,7]                     
                    newadjvol = newstandingvol[z] # adjvol[z]
                    chk_newvol = newadjvol
                    prevvol_cht.insert(z+1,area[z]*volha[z]) # newarea*newvolha)# area[z]*cht[z,7])                        
                    newrow = [None]*9                    
                    newrow = np.array((cht[0,0], YC_cht, (ageClass[z]+increment), newarea, 0, 0, 0, newvolha, (cai[z]-1)), dtype = object)
                    dinosaur = 7777     
#                    clearfell_nextcycle_cht = newarea
                else:            
                    area[z] = prevarea_cht[z]                  
                    volha[z] = volinc(cai[z], area[z], adjvol[z])                                         
                    newstandingvol[z] = area[z]*volha[z]
                    prevvol_cht[z] = cht[z-1,3]*cht[z-1,7] 
                check_inc[z] = newstandingvol[z] - cht[z,7] * cht[z,3]   
                prevarea_cht[z] = cht[z-1,3]  
                if ageClass[z] >= age_th_upper:
                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " 0.0"])
                    a.writerow(output)  
                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
                    b.writerow(output)
                elif age_th <= ageClass[z] < age_th_upper:
                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " %.2F" % actualthinvol[z]])
                    a.writerow(output) 
                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
                    b.writerow(output)
                else:
                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " 0.0000"])
                    a.writerow(output)
                    output = ([cht[0,0], " %.d" % year, " %.d" % ageClass[z], " %.d" % prevarea_cht[z], " %.2f" % prevvol_cht[z]])
                    b.writerow(output)                        
                cht[z,3] = area[z]
                cht[z,7] = volha[z] 
                run_check_inc_early += check_inc[z] 
                
                runTotalThin_cht += actualthinvol[z] 
                actualthinvol[z] = 0                 
   
                if 'dinosaur' in locals():        
                    cht = np.vstack([cht, newrow]) 
                    output = (["newrow", " %.d" % year, " %.d" % cht[(z+1),2], " %.2F" % cht[z+1,3], " %.2F" % cht[z+1,7],  " %.2F" % (cht[z+1,3]*cht[z+1,7]),   " 0.000"])
                    a.writerow(output)
                    output = ([cht[0,0], " %.d" % year, " %.d" % cht[z+1,2], " %.d" % prevarea_cht[z+1], " %.2f" % prevvol_cht[z+1]])
                    b.writerow(output)
                    del dinosaur  
                    del newrow
#        n = np.sum((np.where(cht[:,3] >0),np.where(cht[:,5]>0)),axis = 1)[0][-1]
#        cht = cht[:(n+1)]                    
#        if 'cats' in locals():        
#            cht = np.vstack([cht, newrow]) 
##                        output = (["newrow", " %.d" % year, " %.d" % cht[(z+1),2], " %.2F" % cht[z+1,3], " %.2F" % cht[z+1,7],  " %.2F" % (cht[z+1,3]*cht[z+1,7]),  " %.2F" % partHarvested  ])
##                        a.writerow(output)
##                        output = ([cht[0,0], " %.d" % year, " %.d" % cht[z+1,2], " %.d" % prevarea_cht[z+1], " %.2f" % prevvol_cht[z+1]])
##                        b.writerow(output)
#            del cats   
#            del newrow        
#        if 'eagle' in locals():
#            cht = np.vstack([cht, nextrow]) 
##                        output = (["nextrow", " %.d" % year, " %.d" % cht[(z+1),2], " %.2F" % cht[z+1,3], " %.2F" % cht[z+1,7],  " %.2F" % (cht[z+1,3]*cht[z+1,7]),  " %.2F" % partHarvested  ])
##                        a.writerow(output)
##                        output = ([cht[0,0], " %.d" % year, " %.d" % cht[z+1,2], " %.d" % prevarea_cht[z+1], " %.2f" % prevvol_cht[z+1]])
##                        b.writerow(output)
#            del eagle   
#            del nextrow              
        run_check_inc = run_check_inc + run_check_inc_early  
        finalvoltotal = 0
        sumarea = 0
        presum = 0
        finalvol = [None]*endpoint_cht        
        sumvolcheck333 = 0
        EndRunVol = 0
        for z in range(endpoint_cht):       
            sumvolcheck333 += cht[z,7] * cht[z,3] 
            presum += cht[z,3]
        if 'newarea' in locals():
            sumarea = presum  + newarea
            del newarea
        elif 'nextarea' in locals():
            sumarea = presum + nextarea
            del nextarea
        else:
            sumarea = presum
            
        if 'chk_newvol' in locals():
            EndRunVol = sumvolcheck333  + chk_newvol  
            run_check_inc = run_check_inc + chk_newvol
            chk_newvol = 0
        else:
            EndRunVol = sumvolcheck333                      
        areaTotal = sumarea  + clearfell_nextcycle_cht  
                  
        LatestFinalVolume = originalvoltotal + run_check_inc 
        output = (["VolCheck1 = %.d" % LatestFinalVolume])
        a.writerow(output)    
        output = (["VolCheck2 = %.d" % EndRunVol] )   
        a.writerow(output)      
        output = (["Area check = %.2F" % areaTotal ])
        a.writerow(output)  
        output = (["CF Volume Target = %.d" % targetvol ])    
        a.writerow(output)         
        output = (["Volume TargetTh = %.d" % targetThVolume ])    
        a.writerow(output)      
        output = (["Volume Thinned = %.d" % runTotalThin_cht ])    
        a.writerow(output)  
        if type(clearfell_nextcycle_cht) == str:
            output = (["cf_area_nextcycle = NoCf"])  #  % clearfell_nextcycle_PA12])
            a.writerow(output)
        else:        
            output = (["cf_area_nextcycle = %.2F" % clearfell_nextcycle_cht])
            a.writerow(output) 
        if year > 2000:
            sum_sv = LatestFinalVolume
#            sum_hv += runTotalThin_cht + volclearfelled
            output = (["summary_st_vol = %.2f" % sum_sv])
            a.writerow(output)
#            output = (["summary_hv_vol = %.2f" % sum_hv])
#            a.writerow(output)
#        n = np.sum((np.where(cht[:,3] >0),np.where(cht[:,5]>0)),axis = 1)[0][-1]
#        cht = cht[:(n+1)]
        n = np.sum((np.where(cht[:,3] >0),np.where(cht[:,5]>0)),axis = 1)[0][-1]
        cht = cht[:(n+1)]                    
        if 'cats' in locals():        
            cht = np.vstack([cht, newrow]) 
#                        output = (["newrow", " %.d" % year, " %.d" % cht[(z+1),2], " %.2F" % cht[z+1,3], " %.2F" % cht[z+1,7],  " %.2F" % (cht[z+1,3]*cht[z+1,7]),  " %.2F" % partHarvested  ])
#                        a.writerow(output)
#                        output = ([cht[0,0], " %.d" % year, " %.d" % cht[z+1,2], " %.d" % prevarea_cht[z+1], " %.2f" % prevvol_cht[z+1]])
#                        b.writerow(output)
            del cats   
            del newrow        
        if 'eagle' in locals():
            cht = np.vstack([cht, nextrow]) 
#                        output = (["nextrow", " %.d" % year, " %.d" % cht[(z+1),2], " %.2F" % cht[z+1,3], " %.2F" % cht[z+1,7],  " %.2F" % (cht[z+1,3]*cht[z+1,7]),  " %.2F" % partHarvested  ])
#                        a.writerow(output)
#                        output = ([cht[0,0], " %.d" % year, " %.d" % cht[z+1,2], " %.d" % prevarea_cht[z+1], " %.2f" % prevvol_cht[z+1]])
#                        b.writerow(output)
            del eagle   
            del nextrow              
        if 'volclearfelled' in locals():
            sum_hv = runTotalThin_cht + volclearfelled            
            output = (["Volume Clearfelled = %.2f" % volclearfelled ])    
            a.writerow(output)  
            output = (["summary_hv_vol = %.2f" % sum_hv])
            a.writerow(output)            
            while len(prevarea_cht) > len(cht)  :
                prevarea_cht.pop()         
            while len(prevvol_cht) > len(cht) :
                prevvol_cht.pop()     
            del volclearfelled
        else:
            output = (["  No Clearfell Occurred"])
            a.writerow(output)
            print "%.d -  nope to cf" % year         
        output = ([" "])  
        a.writerow(output)  
        endpoint_cht = len(cht)
        
    # end renaming:
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
        cht = 0
        runTotalThin_cht = 0
        remainvol = 0
        targetIndex = 0         
#    ANUUAL SUMMARIES
#    annual_sv += sum_sv
    output = (["Annual_summary_st_vol = %.2f" % annual_sv])
    a.writerow(output)    
    output = (["Annual_summary_hv_vol = %.2f" % annual_hv])
    a.writerow(output)    
    output = ([" "])  
    a.writerow(output) 
    output = ([" "])
    b.writerow(output)
    sum_sv = 0
    sum_hv = 0 
    annual_sv = 0
    annual_hv = 0   
    year = year + 1
        
commaout.close() 
