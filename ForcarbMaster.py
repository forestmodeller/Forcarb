from IPython import get_ipython
get_ipython().magic('reset -sf')
#     %reset
import numpy as np
import csv
import os
import pandas as pd
from pandas import DataFrame
#from __future__ import division

### things to modify for cohort addition
#  _m
#  [m
#  "m"
#  increment
#  cohort ratios
#  move thintensity
     
#### FUNCTIONS #### 
    
def availthvol(area, thin_intensity):
    availablevolume = (thin_intensity*area*thinfreq)
    return availablevolume

   
def thincheck2(availablevolume):
    if ageClass[z] < age_th: # or ageClass >= age_th_upper:
        actualthinvol = 0
    elif age_th <= ageClass[z] < age_th_upper:
        actualthinvol = (availablevolume * targetvolume / thinvolume)
    else:
        actualthinvol = 0
    return actualthinvol
            
def volinc(cai, area, standingvol):
    vol_inc = (cai * area )
    newvol = (standingvol + vol_inc)
    if newvol == 0 or area==0:
        volha = 0
    else:
        volha = newvol / (area )
    return volha

def thinintensity(YC):
    thin_intensity = YC*1*0.7
    return thin_intensity
     
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

def previous(endpoint, prevarea, prevvol):
    arealist = [1,1,18,175,380,540,640,660,680,720,760,800,900,1000,1200,1400,1600,1800,2000,2100,2200,2400,2440,2480,2520,2560,2600,2640,2680,2720,2760,2800,3000,3200,3300,3400,3600,3800,4000,4100,4200,4400,4000,3600,3400,3000,2760,2400,2200,2000,1400]  #80,80,80,75,65,55,65,60]
    volumelist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,4746.112,9848.23193,15952.31984,22010.26775,28569.19966,43190.01544,45047.2898,46941.85731,48873.71796,50842.87174,54061.34573,56123.73237,58223.41215,60360.38507,62534.65113,66051.47024,76517.01124,87748.89609,96813.38581,106261.0475,126305.8865,140603.1468,155666.7508,167413.444,179543.3091,204952.5551,198274.9593,189206.4726,188856.2884,175603.7426,178052.5907,162001.0126,155075.8783,146955.2985,107052.7681,92336.70911,0,0,0,0,0,0]
    for x in range(endpoint):
        prevarea[x] = arealist[x]
        prevvol[x] = volumelist[x]
    return prevarea, prevvol  
    

    
os.chdir("D:\Data\DropDS\Notes & work\IrishLandUSes\Matrix")
#os.chdir("C:\Users\UCD\Documents\Cloudstation\Notes & work\IrishLandUSes\Matrix")


##### file managment
#m = np.genfromtxt('dataframe24.csv', delimiter=',')
#mdf = DataFrame(m)
#endpoint = len(mdf.index)
#endpoint_1 = endpoint
#MatrixAllTest
m_df = pd.read_csv("AgeMatrixNFI2012_NEW_Redux_12.csv",names = ['FT', 'YC','Age', 'Area', 'Litter', 'Stump', 'DW', 'Volha','CAI'])
#  MatrixAllTest
#    https://docs.python.org/2/library/csv.html#examples

##### cohort managment
#PA = m_df[m_df.FT == 'PA']
PA = DataFrame(m_df, columns = ['FT', 'YC','Age', 'Area', 'Litter', 'Stump', 'DW', 'Volha','CAI'])
PA12 = PA[PA.YC == 12]
endpointPA12 = len(PA12.index)
endpointPA12_1 = endpointPA12
#endpoint = max(PA12.index)
PA12 = PA12.values
#PA16 = PA[PA.YC == 16]
#PA16 = PA16.values
#PA20 = PA[PA.YC == 20]
#PA20 = PA20.values
#PA24 = PA[PA.YC == 24]
#PA24 = PA24.values
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



#newendpointPA12 = endpointPA12 + 6
prevarea12 = [None]*endpointPA12
prevvol12 = [None]*endpointPA12
prevarea12, prevvol12 = previous(endpointPA12, prevarea12, prevvol12)


##### thinning parameters
YC_PA12 = PA12[0,1]
age_th = 13 #9  
age_th_upper = 39 #19
thinfreq = 0.2
cohortratio = 1  # 0.5   #0.14
targetthin = 35000 #250000    # total forest target   # int(raw_input("enter target thin m3: "))
targetvolume = targetthin*cohortratio  # total volume from cohort
thinvolume = 0
runTotalThin_PA12 = 0
runTotalThin_PS = 0
thin_intensity_PA12 = thinintensity(YC_PA12)
defor = 1000
deforYear = 35
affor = 500
afforYear = 25

increment = 1
cohort = PA12[0,0]

##### clearfell parameters
targetvol = 2250000  #4500000
  #25000000 # 9500 # 950000 
targetvolcf = 22500000
volha_cf = 50 # m3/ha
age_cf = 40 # 20
cohortratio_cf = 0.5
clearfell_nextcycle_PA12 = 2000 
clearfell_nextcycle_PS = 0 
remainvol = 0
newcohortvol = 0
newcohortarea_old = 0
newcohortarea = 0
new_area = 0
newrow = [None]*9
chk_newvol = 0

commaout = open('matrix_output_list.csv',mode='wb')
a = csv.writer(commaout, dialect='excel', delimiter=',')  
headers = 'Cohort', ' Year', ' Age', ' Area', ' VolPerHa', ' StandingVol', ' Thin/CF volume (if any)'  #' Standing Vol',
a.writerow(headers)
output = (["____________________________________________________________________"])        
a.writerow(output)
output = ([" "])        
a.writerow(output)

prevthinvol = 0

year = 1
while year < 40:  
    PA12 = PA12[np.logical_not(np.logical_and(PA12[:,3] == 0, PA12[:,2] >= age_cf))]  #  , PA12[:,7] == 0
    newarea = 0
    newendpointPA12 = len(PA12)
    if newendpointPA12 > endpointPA12:
        endpointPA12 = newendpointPA12
        diff = newendpointPA12 - endpointPA12
    else:
        endpointPA12 = newendpointPA12
    if clearfell_nextcycle_PA12 == "NoCF":
        clearfell_nextcycle_PA12 = 0
        newcohortarea_old = newcohortarea
    else:
        clearfell_nextcycle_PA12 = clearfell_nextcycle_PA12
    area = [None]*endpointPA12     
    ageClass = [None]*endpointPA12 
    volha = [None]*endpointPA12     
    availablevolume = [None]*endpointPA12      
    sumvolcheck1 = 0  
    remainvol = 0
    cfVolCheck = 0
    run_check_inc = 0
    run_check_inc_early = 0
    run_check_inc_one = 0
    run_check_inc_two = 0
    run_check_inc_three = 0
    thinvolumecheck = [None]*endpointPA12
    check_inc = [0]*endpointPA12
#    if year == afforYear:
#        PA12[0,3] = PA12[0,3] + affor    
    for z in range(endpointPA12):       
        ageClass[z] = PA12[z,2]
        area[z] = PA12[z,3]
        availablevolume[z] = availthvol(area[z], thin_intensity_PA12)
        if ageClass[z] < age_th:
            thinvolume = 0
        if age_th <= ageClass[z] < age_th_upper:
            thinvolume = (prevthinvol + availablevolume[z])
        prevthinvol = thinvolume   
        sumvolcheck1 += PA12[z,7] * PA12[z,3]
    originalvoltotal = sumvolcheck1 
    chk_newvol = 0
    area = [None]*endpointPA12     
    ageClass = [None]*endpointPA12    
    for z in range(endpointPA12):
        volha = [None]*endpointPA12
        cai = [None]*endpointPA12       
        availablevolume = [None]*endpointPA12
        harvested = [None]*endpointPA12
        actualthinvol = [None]*endpointPA12
        standingvol = [None]*endpointPA12
        teststanding = [None]*endpointPA12
        newstandingvol = [None]*endpointPA12       
        adjvol = [None]*endpointPA12
        cfVolCheck = [None]*endpointPA12  
        ageClass[z] = PA12[z,2]               
        area[z] = PA12[z,3]      
        volha[z] = PA12[z,7]  
        cai[z] = PA12[z,8]
        standingvol[z] = PA12[z,7] * PA12[z,3]  
    #####  thinning         
        availablevolume[z] = availthvol(area[z], thin_intensity_PA12)
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
            for y in range(age_cf, endpointPA12):
                availablevolume_cf += (PA12[y,7] * PA12[y,3])
                availablearea_cf += PA12[y,3]
            if targetvol < availablevolume_cf:
                print " target < available"
                that_check_inc = 0
                standingvollist = [None]*endpointPA12                    
                for y in range(endpointPA12):        
                    standingvollist[y] = PA12[y,7] * PA12[y,3] 
                    sss = standingvollist[::-1]
                rollingSumSSS = np.cumsum(sss)                
                target_age = targetage(sss, targetvol)
                remainvol = target_age[1]
                targetIndex = target_age[0]
                cohortFelled = target_age[2]
                remainarea = remainvol / PA12[endpointPA12-targetIndex-1,7]                     
                volclearfelled = targetvol   
                cfVolCheck = volclearfelled 
                clearedArea = 0 
                for z in range(z, endpointPA12-targetIndex-1):  
                    cai[z] = PA12[z,8]
                    area[z] = PA12[z,3]
                    new_area = PA12[z,3] 
                    ageClass[z] = PA12[z,2] 
                    area[z] = prevarea12[z] 
                    prevarea12[z] = PA12[z-1,3] 
                    standingvol[z] = PA12[z,7] * area[z]
                    adjvol[z] = prevvol12[z]
                    volha[z] = volinc(cai[z], area[z], adjvol[z])
                    newstandingvol[z] = volha[z]*area[z] 
                    check_inc[z] = newstandingvol[z] - PA12[z,7] * PA12[z,3]
                    prevvol12[z] = PA12[z-1,3]*PA12[z-1,7]  
                    output = (["PA12", " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " Not clearfelled"])
                    a.writerow(output)
                    PA12[z,3] = area[z]
                    PA12[z,7] = volha[z]
                    run_check_inc_one += check_inc[z]                                 
                for z in range(endpointPA12 - targetIndex -1, endpointPA12 - targetIndex):
                    cai[z] = PA12[z,8]
                    felledCohort = PA12[z,3] 
                    area[z] = PA12[z,3]
                    OtherClearedArea = area[z] - remainarea
                    ageClass[z] = PA12[z,2]
                    standingvol[z] = PA12[z,7] * PA12[z,3]
                    partHarvested = standingvol[z] - remainvol
                    OtherClAreaCheck = partHarvested / PA12[endpointPA12 -targetIndex - 1,7]                    
                    area[z] = prevarea12[z]  
                    adjvol[z] = prevvol12[z] + remainvol
                    volha[z] = volinc(cai[z], area[z], adjvol[z])
                    newstandingvol[z] = volha[z]*area[z] 
                    prevvol12[z] =  PA12[z-1,3]*PA12[z-1,7]  
                    if targetIndex ==  0 and felledCohort > 0:
                        area[z] = new_area 
                        newstandingvol[z] = volha[z]*area[z] 
                        output = (["PA12", " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " NotFelled"])   # , " %.2F" % check_inc[z]])
                        a.writerow(output)
                        if targetIndex >0:
                            pass
                        else:
                            newarea = remainarea  # + prevarea12[z]
                            prevarea12.append(newarea)
                            newarea_hold_2 = newarea
                            newadjvol = remainvol 
                            chk_newvol = newadjvol
                            prevvol12.append(newadjvol)  
                            newvolha = newadjvol/newarea       
                            newrow = np.array((cohort, YC_PA12, (ageClass[z]+increment), newarea, 0, 0, 0, newvolha, (cai[z]-1)), dtype = object)
                            PA12 = np.vstack([PA12, newrow])   
                            output = (["PA12", " %.d" % year, " %.d" % PA12[z+1,2], " %.2F" % PA12[z+1,3], " %.2F" % PA12[z+1,7],  " %.2F" % newadjvol, " %.2F " % partHarvested])
                            a.writerow(output)
#                            prevarea12[z] =  area[z-1]
                    else:
                        output = (["PA12", " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z], " %.2F " % partHarvested])   # , " %.2F" % check_inc[z]])
                        a.writerow(output)
                        
                    check_inc[z] = newstandingvol[z] - PA12[z,7] * PA12[z,3]  # + chk_newvol        

                    PA12[z,3] = area[z]
                    PA12[z,7] = volha[z]         
                    prevarea12[z] = PA12[z-1,3]  #area[z-1]
                    run_check_inc_two += check_inc[z] 
                for z in range(endpointPA12-targetIndex, endpointPA12):
            #  THIS loop only qualifies when targetIndex > 0
                    cai[z] = PA12[z,8] 
                    area[z] = PA12[z,3] 
                    clearedArea += PA12[z,3] 
                    ageClass[z] = PA12[z,2] 
                    standingvol[z] = PA12[z,7] * PA12[z,3]                        
                    harvested[z] = standingvol[z]
                    if z == (endpointPA12-targetIndex):
                        area[z] = remainarea  # prevarea12[z]
                        prevarea12[z] = PA12[z-1,3]  
                        standingvol[z] = prevvol12[z]   
                        volha[z] = volinc(cai[z], area[z], standingvol[z])
                        newstandingvol[z] = volha[z]*area[z]                        
                        prevvol12[z] = PA12[z-1,3]*PA12[z-1,7]                        
                    else:
                        area[z] = 0
                        prevarea12[z] = 0
                        standingvol[z] = 0
                        volha[z] = volinc(cai[z], area[z], standingvol[z])
                        newstandingvol[z] = volha[z]*area[z]
                        prevvol12[z] = 0  
                    check_inc[z] = newstandingvol[z] - PA12[z,7] * PA12[z,3]
                    output = (["PA12", " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z], " %.2F" % harvested[z] ])
                    a.writerow(output)
                    PA12[z,3] = area[z]
                    PA12[z,7] = volha[z]
                    run_check_inc_three += check_inc[z]      
                if 'run_check_inc_two' in locals():
                    run_check_inc = run_check_inc_one + run_check_inc_two # + run_check_inc_early
                if 'run_check_inc_three' in locals():
                    run_check_inc = run_check_inc + run_check_inc_three
                TotalClearedArea = clearedArea +  OtherClAreaCheck    # + OtherClearedArea #
                clearfell_area_PA12 = clearedArea +  OtherClAreaCheck                  
                ClearfellCheck = clearfell_area_PA12
                clearfell_nextcycle_PA12 =   clearfell_area_PA12  # TotalClearedArea
                clearfell_area_PA12 = 0       
                break
            elif targetvol >= availablevolume_cf:
                areafelled = 0 
                that_check_inc = 0
                print "target > availab"  
                volclearfelled  = availablevolume_cf  
                cfVolCheck[z] = volclearfelled
                runVolCheck += cfVolCheck[z]
                for z in range(z, endpointPA12):                       
                    cai[z] = PA12[z,8]
                    ageClass[z] = PA12[z,2] 
                    areafelled += PA12[z,3]                      
                    standingvol[z] = PA12[z,7] * PA12[z,3]                                   
                    harvested[z] = standingvol[z]
                    if endpointPA12 - endpointPA12_1 > 0:
                        area[z] = prevarea12[z]  #areamod(0, prevarea12[z-1])
                        prevarea12[z] = PA12[z-1,3] 
                        standingvol[z] = prevvol12[z]
                        volha[z] = volinc(cai[z], area[z], standingvol[z])
                        newstandingvol[z] = volha[z]*area[z]                        
                        prevvol12[z] = PA12[z-1,3]*PA12[z-1,7]   
                    elif ageClass[z] == age_cf:
                        area[z] = prevarea12[z]  #areamod(0, prevarea12[z-1])
                        prevarea12[z] = PA12[z-1,3] 
                        standingvol[z] = prevvol12[z]
                        volha[z] = volinc(cai[z], area[z], standingvol[z])
                        newstandingvol[z] = volha[z]*area[z]                        
                        prevvol12[z] = PA12[z-1,3]*PA12[z-1,7]  
                    else:
                        area[z] = 0 
                        prevarea12[z] =  0 
                        standingvol[z] = 0  
                        prevvol12[z] = 0                        
                        volha[z] = volinc(cai[z], area[z], standingvol[z])
                        newstandingvol[z] = volha[z]*area[z] 
                    check_inc[z] = newstandingvol[z] - PA12[z,7] * PA12[z,3]
                    output = (["PA12", " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " %.2F" % harvested[z]])
                    a.writerow(output)
                    PA12[z,3] = area[z]
                    PA12[z,7] = volha[z]                    
                    run_check_inc += check_inc[z]                 
                clearfell_area_PA12 = (areafelled)
                clearfell_nextcycle_PA12 = clearfell_area_PA12
                clearfell_area_PA12 = 0  
                break    
        else:
        #####  area modification   
            ageClass[z] = PA12[z,2]               
            area[z] = PA12[z,3]      
            volha[z] = PA12[z,7]  
            cai[z] = PA12[z,8]        
            if z == 0:
                if year == afforYear: 
                    area[z] = clearfell_nextcycle_PA12 + affor
                elif year == deforYear:
                    area[z] = clearfell_nextcycle_PA12 + defor
                else:
                    area[z] = clearfell_nextcycle_PA12                     
                area[z-1] = prevarea12[-1]                 
                clearfell_nextcycle_PA12 = 0
            elif z == (endpointPA12-1):         
                area[z] = prevarea12[z] 
        ##### create new cohort   
                if ageClass > age_cf:          
                    newarea =new_area    
                    prevarea12.append(new_cohort_prev)   # newarea)
                    newarea_hold_2 = newarea
            else:            
                new_cohort_prev = prevarea12[z+1]                
                new_area = PA12[z+1,3] 
                area[z] = prevarea12[z]                 
        #####  volume modification and increment   
            if z == 0:
                adjvol[z] = volha[z]*area[z]
                volha[z] = volinc(cai[z], area[z], adjvol[z])
                newstandingvol[z] = area[z]*volha[z]
                prevvol12[z] = PA12[z-1,3]*PA12[z-1,7]              
            elif z == (endpointPA12-1):
                adjvol[z] = volha[z]*area[z]
                newadjvol = adjvol[z]                
                adjvol[z] = prevvol12[z]
                volha[z] = volinc(cai[z], area[z], adjvol[z])                
        ##### create new cohort when there has been NO CLEARFELL                 
                if ageClass > age_cf:
                    newvolha = newadjvol/newarea 
                    chk_newvol = newadjvol
                    prevvol12.append(newadjvol)
                    newrow = np.array((cohort, YC_PA12, (ageClass[z]+increment), newarea, 0, 0, 0, newvolha, (cai[z]-1)), dtype = object)
                    PA12 = np.vstack([PA12, newrow])   
                    PA12[z+1,3] = newarea
                newstandingvol[z] = area[z]*volha[z]
                prevvol12[z] = PA12[z-1,3]*PA12[z-1,7]
            else:     
                adjvol[z] = volha[z]*area[z]
                adjvol[z] = prevvol12[z]
                volha[z] = volinc(cai[z], area[z], adjvol[z])                                         
                newstandingvol[z] = area[z]*volha[z]
                prevvol12[z] = PA12[z-1,3]*PA12[z-1,7] 
            check_inc[z] = newstandingvol[z] - PA12[z,7] * PA12[z,3]
            PA12[z,3] = area[z]
            PA12[z,7] = volha[z] 
            prevarea12[z] = area[z-1]  #PA12[z-1,3]  #
            output = (["PA12", " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.2F" % newstandingvol[z],   " %.2F" % actualthinvol[z]])
            a.writerow(output)    

            run_check_inc_early += check_inc[z] 
            
            runTotalThin_PA12 += actualthinvol[z] 
            thinvolumecheck[z] = actualthinvol[z]
            actualthinvol[z] = 0
            
            if z == (endpointPA12 - 1):         
                output = (["PA12", " %.d" % year, " %.d" % PA12[z+1,2], " %.2F" % PA12[z+1,3], " %.2F" % PA12[z+1,7],  " %.2F" % newadjvol,   " 0.000", " %.2F" % PA12[z,3]])
                a.writerow(output)                   
    run_check_inc = run_check_inc + run_check_inc_early 
    sumvolcheck2 = 0
    finalthincheck = 0 
    finalvoltotal = 0
    that_check_inc = 0  
    cftotal = 0
    sumarea = 0
    presum = 0
    newcohortarea_old = newcohortarea
    newcohortarea = 0
    finalvol = [None]*endpointPA12
    newcohortvol_final = [None]*(endpointPA12+1) 
    
    sumvolcheck333 = 0
    EndRunVol = 0
    for z in range(endpointPA12):       
        sumvolcheck333 += PA12[z,7] * PA12[z,3] 
    if 'chk_newvol' in locals():
        EndRunVol = sumvolcheck333  + chk_newvol  
        run_check_inc = run_check_inc + chk_newvol
        chk_newvol = 0
    else:
        EndRunVol = sumvolcheck333 
        
    if 'thinvolumecheck' in locals():     
        for z in range((age_th+1)/increment, (age_th_upper+1)/increment):
            finalthincheck += thinvolumecheck[z]
        del thinvolumecheck
    else:
        finalthincheck = 0        
    if 'newarea_hold_2' in locals():
        for z in range(endpointPA12):  
            finalvol[z] = PA12[z,7] * PA12[z,3] 
            finalvoltotal += finalvol[z]
            presum += PA12[z,3]
            sumarea = (presum + PA12[z+1,3] )
            that_check_inc += check_inc[z]    
        areaTotal = sumarea + clearfell_nextcycle_PA12 
        for z in range(endpointPA12_1, endpointPA12+1):
            newcohortarea += (PA12[z,3])
            newcohortvol_final[z] = PA12[z,7]*PA12[z,3]
            newcohortvol += newcohortvol_final[z]            
        del newarea_hold_2            
    else:
        for x in range(endpointPA12):        
            finalvol[x] = PA12[x,7] * PA12[x,3] 
            finalvoltotal += finalvol[x] 
            sumarea += PA12[x,3]
            that_check_inc += check_inc[x]
        areaTotal = sumarea + clearfell_nextcycle_PA12
        newcohortarea_old = 0
#    volincrement = finalvoltotal - originalvoltotal        
#    if newcohortvol != 0 and 'volclearfelled' in locals():
#        newvolumecheck = finalvoltotal - that_check_inc + newcohortvol 
#        newcohortvol = 0
#    else:
#        newvolumecheck = finalvoltotal - that_check_inc    
#    if 'volclearfelled' in locals(): 
#        del volclearfelled
#    else:
#        output = (["  No Clearfell Occurred"])
#        a.writerow(output) 
    LatestFinalVolume = originalvoltotal + run_check_inc 
    output = (["VolCheck1 = %.d" % LatestFinalVolume])
    a.writerow(output)    
    output = (["VolCheck2 = %.d" % EndRunVol] )   
    a.writerow(output)    
    output = (["Area check = %.2F" % areaTotal ])
    a.writerow(output)
    output = (["Volume TargetTh = %.d" % targetthin ])    
#    a.writerow(output)      
    output = (["Volume Thinned = %.d" % runTotalThin_PA12 ])    
    a.writerow(output)   
    if 'volclearfelled' in locals():
        output = (["Volume Clearfelled = %.2f" % volclearfelled ])    
        a.writerow(output)      
#    output = (["Remainvol = %.2F" % remainvol ])    
#    a.writerow(output)    
#    output = (["run_check_inc = %.2F" % run_check_inc])
#    a.writerow(output)
#    if type(clearfell_nextcycle_PA12) == str:
#        output = (["cf_area_nextcycle = NoCf"])  
#        a.writerow(output)
#    else:        
#        output = (["cf_area_nextcycle = %.2F" % clearfell_nextcycle_PA12])
#        a.writerow(output)
    if 'volclearfelled' in locals(): 
        del volclearfelled
    else:
        output = (["  No Clearfell Occurred"])
        a.writerow(output)     
    output = ([" "])  
    a.writerow(output)  





###################################### cohort
#    area = [None]*endpointPS     
#    ageClass = [None]*endpointPS 
#    volha = [None]*endpointPS     
#    availablevolume = [None]*endpointPS    
#    for z in range(endpointPS):       
#        ageClass[z] = PS[z,2]
#        area[z] = PS[z,3]
#        availablevolume[z] = availthvol(area[z])
#        if ageClass[z] < age_th:
#            thinvolume = 0
#        if age_th <= ageClass[z] < age_th_upper:
##        if ageClass[z] >= age_th and ageClass[z] < age_th_upper:
#            thinvolume = float(prevthinvol + availablevolume[z])
##        if ageClass[z] >= age_th_upper:
##            thinvolume = thinvolume
#        prevthinvol = thinvolume       
#    for z in range(endpointPS):
#        area = [None]*endpointPS     
#        ageClass = [None]*endpointPS
#        volha = [None]*endpointPS
#        cai = [None]*endpointPS       
#        availablevolume = [None]*endpointPS
#        actualthinvol = [None]*endpointPS
#        standingvol = [None]*endpointPS
#        teststanding = [None]*endpointPS
#        newstandingvol = [None]*endpointPS
#        adjvol = [None]*endpointPS
#        ageClass[z] = PS[z,2]               
#        area[z] = PS[z,3]      
#        volha[z] = PS[z,7]  
#        cai[z] = PS[z,8]
#        standingvol[z] = PS[z,7] * PS[z,3]
#    #####  treatment         
#        availablevolume[z] = availthvol(area[z])
#        actualthinvol[z] = thincheck2(availablevolume[z])
#        adjvol[z] = standingvol[z] - actualthinvol[z]
#    #####  area modification    
#        if PS[z,3] == PS[0,3]:
#            area[z] = areamod(area[z], clearfell_nextcycle_PS)
#        elif PS[z,3] == PS[-1,3]:
#            clearfell_area_PS = PS[-1,3]            
#            area[z] = areamod(0, NPS[z-1]) 
#        else:            
#            area[z] = areamod(area[z], NPS[z-1])  
#        NPS[z-1] = PS[z-1,3]*0.1
#    #####  volume modification and increment     
#        if PS[z,7] == PS[0,7]:
#            adjvol[z] = volmod(adjvol[z], 0)
#        elif PS[z,7] == PS[-1,7]:
#            volharvestd = PS[-1,7]*0.1            
#            adjvol[z] = volmod(0, prevvolPS[z-1]) 
#        else:            
#            adjvol[z] = volmod(adjvol[z], prevvolPS[z-1])                  
#        volha[z] = volinc(cai[z], area[z], adjvol[z])
#        newstandingvol[z] = volha[z]*area[z] 
#        prevvolPS[z-1] = PS[z-1,3]*PS[z-1,7]*0.1         
#        
#        output = (["PS", " %.d" % year, " %.d" % ageClass[z], " %.2F" % area[z], " %.2F" % volha[z],  " %.d" % newstandingvol[z],   " %.2F" % actualthinvol[z]])
#        a.writerow(output)
#        runTotalThin_PS = actualthinvol[z] + runTotalThin_PS
#        PS[z,3] = area[z]
#        PS[z,7] = volha[z]
#        actualthinvol[z] = 0
#        
#    output = (["clearfell = %.d" % clearfell_area_PS])
#    a.writerow(output)
##    sumvols = PS[0,7] + PS[1,7] + PS[2,7] + PS[3,7] +  PS[4,7] + PS[5,7] + PS[6,7] + PS[7,7] + PS[8,7] + clearfell_area
##    output = (["vol check = %.d" % sumvols])
##    a.writerow(output)
#    sumarea = PS[0,3] + PS[1,3] + PS[2,3] + PS[3,3] +  PS[4,3] + PS[5,3] + PS[6,3] + PS[7,3] + PS[8,3] + clearfell_area_PS
#    output = (["Area check = %.d" % sumarea ])
#    a.writerow(output)
#    output = (["Target ThinningVolume = %.d" % targetthin ])    
#    a.writerow(output)      
#    output = (["Volume Thinned = %.d" % runTotalThin_PS ])    
#    a.writerow(output)     
#    output = ([" "])        
#    a.writerow(output) 
###################################### cohort    
      
  
    remainvol = 0
    targetIndex = 0
    runTotalThin_PA12 = 0    
#    runTotalThin_PS = 0
#    dogs = finalvoltotal
    year = year + 1
        
commaout.close()  
