import math



############## growth functions
def availthvol(area, intensity, thinfreq):
    availablevolume = (intensity*area*thinfreq)
    return availablevolume

   
def thincheck2(availablevolume, ageClass, age_th, age_th_upper, targetThVolume, thinvolume):
    if thinvolume == 0:
        actualthinvol = 0
    else:
        if ageClass < age_th:
            actualthinvol = 0
        elif age_th <= ageClass < age_th_upper:
            actualthinvol = (availablevolume * targetThVolume / thinvolume)
        else:
            actualthinvol = 0
    return actualthinvol
            
def volinc(cai, area, standingvol):
    vol_inc = cai * area
    newvol = standingvol + vol_inc
    if newvol <= 0 or area <= 0:       
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

############## biomass functions
# Eq 1
def sbiom(a, b, vol):
    return float(a*vol**b)
    
    
# Eq2
def nmbiom(a,b,k,bm, bnlim):
    bmnf = k + a*bm**b 
#    print bmnf
    if bmnf < bnlim:
        return bm*bmnf - bm
        
    else:
        return bm*bnlim - bm
        
        
# Eq3
def sapfactor(a,b,y,bnm,bslim ):
    sbf = y + a*bnm**b
#    print sbf
    if  sbf < bslim:
        return bnm*sbf - bnm
        
    else:
        return bnm*bslim - bnm
        
def pStemwood(a1,a2,a3,b1,b2,b3,c1,c2,c3,vol):
#    pstem = 1 / ((1 + math.exp(inParm5.at[cht,'a1'] + a2*vol + a3*math.log(vol + 5)))
#            + math.exp(b1 + b2*vol + b3*math.log(vol + 5)) 
#            + math.exp(c1 + inParm5.at[cht,'c2']*vol + inParm5.at[cht,'c3']*math.log(vol + 5)))
    pstem = 1 / ((1 + math.exp(a1 + a2*vol + a3*math.log(vol + 5)))
            + math.exp(b1 + b2*vol + b3*math.log(vol + 5)) 
            + math.exp(c1 + c2*vol + c3*math.log(vol + 5)))
    return pstem



def pBark(a1,a2,a3,b1,b2,b3,c1,c2,c3,vol):
    pbark = (math.exp(a1 + a2*vol + a3*math.log(vol+5))) /  (
        (1+math.exp(a1 + a2*vol + a3*math.log(vol+5))) + 
        (math.exp(b1 + b2*vol + b3*math.log(vol+5))) + 
        (math.exp(c1 + c2*vol + c3*math.log(vol+5))))
    return pbark
    
#biomassbk = biomassag * pbark

# Eq6
def pBranch(a1,a2,a3,b1,b2,b3,c1,c2,c3,vol):
    pbranch = (math.exp(b1 + b2*vol + b3*math.log(vol+5))) / (
        (1+math.exp(a1 + a2*vol + a3*math.log(vol+5))) + 
        (math.exp(b1 + b2*vol + b3*math.log(vol+5))) + 
        (math.exp(c1 + c2*vol + c3*math.log(vol+5))))
    return pbranch
    
#biomassbr = biomassag * pbranch

# Eq7
def pFoliage(a1,a2,a3,b1,b2,b3,c1,c2,c3,vol):
    pfoliage = (math.exp(c1 + c2*vol + c3*math.log(vol+5))) / (
        (1+math.exp(a1 + a2*vol + a3*math.log(vol+5))) + 
        (math.exp(b1 + b2*vol + b3*math.log(vol+5))) + 
        (math.exp(c1 + c2*vol + c3*math.log(vol+5))))
    return pfoliage


def sbiomroot(a, b, biomassag):
    return a*biomassag**b        

