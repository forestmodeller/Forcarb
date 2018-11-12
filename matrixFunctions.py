import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
 
def previous(cht, endpoint, prevarea, prevvol, prev_volha):
    arealist = cht[:,3]
    volumelist = cht[:,7]    
    for x in range(endpoint):
        prevarea[x] = arealist[x]
        prevvol[x] = volumelist[x]*arealist[x]
        if prevarea[x] == 0:
            prev_volha[x] = 0
        else:
            prev_volha[x] = prevvol[x] / prevarea[x]
    return prevarea, prevvol, prev_volha 
    
def speciesLookup(species):
    if species == "CBmix":
        species = "IE_Cbmix"
    elif species == "Cmix":
        species = "IE_Cmix"
    elif species == "PS12":
        species = "IE_Pine4-12"
    elif species == "PS20":
        species = "IE_Pine12-20"
    elif species == "OC":
        species = "IE_OC"
    elif species == "PA12":
        species = "IE_Spruce4-12"
    elif species == "PA16":
        species = "IE_Spruce13-16"        
    elif species == "PA20":
        species = "IE_Spruce17-20"
    elif species == "PA24":
        species = "IE_Spruce20-24"
    elif species == "PA30":
        species = "IE_Spruce24-30"
    elif species == "SGB":
        species = "IE_SGB"
    elif species == "FGB":
        species = "IE_FGB"  
    elif species == "CBmixp":
        species = "IE_Cbmix"
    elif species == "Cmixp":
        species = "IE_Cmix"
    elif species == "PS12p":
        species = "IE_Pine4-12"
    elif species == "PS20p":
        species = "IE_Pine12-20"
    elif species == "OCp":
        species = "IE_OC"
    elif species == "PA12p":
        species = "IE_Spruce4-12"
    elif species == "PA16p":
        species = "IE_Spruce13-16"        
    elif species == "PA20p":
        species = "IE_Spruce17-20"
    elif species == "PA24p":
        species = "IE_Spruce20-24"
    elif species == "PA30p":
        species = "IE_Spruce24-30"
    elif species == "SGBp":
        species = "IE_SGB"
    elif species == "FGBp":
        species = "IE_FGB"         
    return species
    
def targets(TARG, species, step):  #, age_cf):
#    if step > 20 and step < age_cf:
#        target = 0 # vol*0.25
#    else:
#    if step > age_cf + 1:
#        target = 0
#    else:
    sp = species
    step = step
    line = TARG[(TARG['Species'] == sp) & (TARG['Step'] == step)]
    target = line.iloc[[0],[1]]
    target = target.iloc[-1]['Amount']
    return target    

############## biomass functions
# Eq 1
def sbiom(a, b, vol):
    return float(a*vol**b)
#
#def nmbiom(a,b,k,bm, bnlim, minlim):
#    bmnf = k + a*bm**b 
##    print bmnf
#    if bmnf < minlim:
#        return bm*minlim - bm
#    elif bmnf < bnlim:
#        return bm*bmnf - bm        
#    else:
#        return bm*bnlim - bm

      
def nmbiom(a,b,k,bm, bnlim, minlim):
    bmnf = k + a*bm**b 
#    print bmnf
    if bmnf < minlim:
        return bm*minlim - bm
    elif bmnf < bnlim:
        return bm*bmnf - bm        
    else:
        return bm*bnlim - bm
        
        
# Eq3
#def sapfactor(a,b,y,bnm,bslim ):
#    sbf = y + a*bnm**b
##    print sbf
#    if  sbf < bslim:
#        return bnm*sbf - bnm
#        
#    else:
#        return bnm*bslim - bnm

def sapfactor(a,b,y,bnm,bslim, minlim ):
    if bnm == 0:
        y = 0
        sbf = y + a*bnm**b
    else:
        sbf = y + a*bnm**b
#    print sbf
    if sbf < minlim:
        return bnm*minlim - bnm
    elif  sbf < bslim:
        return bnm*sbf - bnm        
    else:
        return bnm*bslim - bnm
        
def pStemwood(a1,a2,a3,b1,b2,b3,c1,c2,c3,vol):
#    pstem = 1 / ((1 + math.exp(inParm5.at[cht,'a1'] + a2*vol + a3*math.log(vol + 5)))
#            + math.exp(b1 + b2*vol + b3*math.log(vol + 5)) 
#            + math.exp(c1 + inParm5.at[cht,'c2']*vol + inParm5.at[cht,'c3']*math.log(vol + 5)))
    pstem = 1 / (1 + math.exp(a1 + a2*vol + a3*math.log(vol + 5))
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


def sbiombg(biomassag, hardwood):
    if hardwood == 0:
        bg = biomassag*0.222*2
#        a*biomassag**b        
    else:
        bg = 1.576*abs(biomassag*2)**0.615
    return bg

#def decayFunction(pool, bdr, tempmod, standmod, patm, pt):
#    decay = bdr * tempmod * standmod
#    atm = decay * patm
#    xfer = decay * pt
#    pool = pool - decay
#    return pool, atm, xfer


#def decayFunction(pool, pooldict, bdr, patm, pt):
#    decay = pool * bdr * 1 * 1   # tempmod * standmod
#    atm = decay * patm
#    if pool == pooldict['pool20'] or pooldict['pool21'] or pooldict['pool22'] or pooldict['pool23']:
#        agslow = decay * pt
#        bgslow = 0            
#    elif pool == pooldict['pool14'] or pooldict['pool16']:  
#        bgslow = decay * pt
#        agslow = 0        
#    else: 
#        agslow = 0
#        bgslow = 0
#    pool = pool - decay
#    return pool, atm, agslow, bgslow
    
#def decayFunction(pooldict, bdr, patm, pt, physical):
#    decay = float(pool * bdr * 1 * 1)   # tempmod * standmod
#    atm = decay * patm
#    agslow = decay * pt 
#    bgslow = 0
#    pool -= decay
#    return pool, atm, agslow, bgslow
    
def decayFunction(pool, bdr, patm, pt, physical):
    decay = float(pool * bdr * 1 * 1)   # tempmod * standmod
    atm = decay * patm      
    agslow = decay * pt        
    other = (pool - decay) * physical
    bgslow = 0
#    pool = pool - decay
    return pool, atm, agslow, bgslow, decay, other    

def decayFunction2(pool, bdr, patm, pt, physical):          
    decay = float(pool * bdr * 1 * 1)   # tempmod * standmod
    atm = decay * patm      
    bgslow = decay * pt        
    other = (pool-decay) * physical
    agslow = 0
#    pool = pool - decay
    return pool, atm, agslow, bgslow, decay, other
 

        
#def disturbanceMatrix(distmatrix, pooldict):                       
#    for line in distmatrix:
#        dist = line.split(',')
#        fromPool = dist[1]
#        Pool_to = dist[2]
#        proPortion = float(dist[3])
#        pooldict[Pool_to] += float(pooldict[fromPool]*proPortion)  
#        if fromPool == Pool_to:
#            pooldict[fromPool] = float(pooldict[fromPool]*proPortion)  
#        else:
#            pooldict[fromPool] = 0   
def disturbanceMatrix(distmatrix, pooldict):  
    proPortionRunTotal = 0   
    newOriginalPool = 0                 
    for line in distmatrix: 
        dist = line.split(',')
        fromPool = dist[1]
        Pool_to = dist[2]
        proPortion = float(dist[3])
        proPortionRunTotal += proPortion 
        if proPortionRunTotal == 1:   # 0.9999:
            proPortionRunTotal = 0
            if fromPool != Pool_to:
                pooldict[Pool_to] += float(pooldict[fromPool]*proPortion)
                pooldict[fromPool] = newOriginalPool
            else:
                pooldict[Pool_to] = float(pooldict[fromPool]*proPortion)
        else:
            if fromPool != Pool_to:
                pooldict[Pool_to] += float(pooldict[fromPool]*proPortion) 
            else:newOriginalPool = float(pooldict[fromPool]*proPortion)
    return pooldict
    
def harvWoodProd(inflow, pool, hl):
    k = math.log(2)/hl
    c_new = math.exp(-k) * pool + (1 - math.exp(-k))*inflow/k
    return c_new
    
def svol(a, b, biom):
    vol = (biom/a)**(b**-1)
    return vol        


def agbmpool(pool1, pool2, pool3, pool4, standAge ):
    x = list(range(standAge))
    plt.plot(x,pool1, color = 'r', linewidth = 3)
    plt.plot(x,pool2, color = 'b', linewidth = 3)
    plt.plot(x,pool3, color = 'g', linewidth = 3)
    plt.plot(x,pool4, color = 'y', linewidth = 3) 
#    plt.legend(loc='upper left', shadow=True, fontsize='large')
    plt.show()
    
def agbmpool2(pool1, pool2, pool3, pool4, standAge ):
    x = list(range(standAge))
    fig, ax = plt.subplots()
    ax.set(xlabel = 'Year', ylabel = 'Tonnes of C', title = 'Aboveground Biomass Stocks')
    formatter = ticker.FormatStrFormatter('%1.0f')
    ax.yaxis.set_major_formatter(formatter)
    ax.plot(x,pool1, color = 'r', linewidth = 3, label= 'MerchBk')
    ax.plot(x,pool2, color = 'b', linewidth = 3, label= 'Foliage')
    ax.plot(x,pool3, color = 'g', linewidth = 3, label= 'Other')
    ax.plot(x,pool4, color = 'y', linewidth = 3, label= 'Above') 
    ax.legend(loc='upper left', shadow=True, fontsize='large')
    plt.savefig('abg5.png', dpi = 250)
    plt.show()    
