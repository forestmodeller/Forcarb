### Forcarb

The forest estate is represented by matrix detailing cohort (spruce, pine, etc) yield class, age (age class), area, biomass, volume per hectare and the current annual increment of that cohort. The cohorts above are further classified by soil (peat and non-peat).

There are two main scripts (so far).

### 1st script

The 1st script prepares the input data.

Using equations from Boudewyn et al 2007 and Li et al 2003 the volume per ha by species cohort is converted into biomass pool growth curves: merchBark, foliage and otherWood.

The biomass of the stem that is merchantable is evluated, next the non-merchantable stem biomass is found. The sum of these enables calculation of the sap biomass.... proportions... 

These curves are then smoothed using the approach specified by S. Kull (CBM). Note, results for broadleaf species much more accurate when smoothing is disabled.

Increments are evaluated by subtracting the biomass at t1 from t2.

The increments are appended to the original input file.

### 2nd script

The 2nd script conducts the simulation.

Note: This will be run separately for afforestation scenarios (AR) and existing forests (FM). Increments from above are assumed identical for peat and non-peat cohorts. The only difference is the starting condition of Pool19, this is equal to 92 if non-peat and 0 if peat.

The matrix is fed into the program and divided up into cohorts. A cohort is a species at a productivity class.

These cohorts are processed by the main program code on an annual step basis and aggregated into a common pool at the end of each annual step.

The area comprising a cohort ages one year at a time. In that year, the volume of the cohort is grown incrementally according to the Chapmann-Richards growth function, previously calibrated by the Irish NFI. During a ‘run’, thinnings and final harvests are undertaken according to rules (see below). To complete a run, the area that is clearfelled becomes the new area in the next run.

The code outputs the modified cohort matrix together with summary totals: standing volume, harvested volume. These are collated and will be used to estimate biomass pools using the biomass functions.

The run follows these steps consistently:
1 Vol modification 
2 Thinning / Harvest
3 Area modification
4 Vol increment

The script gets complex when conditions arise in which the estsate is not clearfelled as the criteria are not met. In situations these situations, the forest estate gains an additional age. This has implications for the what is termed the “endpoint” which determines the estate age. Endpoint is determined at the beginning of each annual run. Prior to this step, the matrix data is checked for rows of trailing zeros: if a line of zeros is present at the bottom (only) of the matrix, it is removed. Various calculations are based around this endpoint. 
Another situation can arise due to input data having zero ages represented while older ages do exist. 

volume mod:
standingvol[z] = prevvol[z]
prevvol[z] = matrix[z-1]

area mod:
area[z] = prevarea[z], 
prevarea[z] = matrix[z-1]

volume increment:
Increment = Area * CAI
Increment + standing vol = New Vol

thinning:
In a single year, steps 3 and 4 above are followed for each age until the thinning age is reached. Then the available thinning volume is calculated and compared to the target. Volume is removed accordingly. 

final harvest:
Similarly, steps 3 and 4 are followed until the clearfell age is reached (clearfell age follows upper thinning age). Then the available standing volume for clearfell is calculated and compared with the target.

For harvest there are two main categories:
1) If the target harvest is greater than the available volume
2) If the target harvest is less than the available volume

more to follow ...

### Biomass steps

In AR, as the estate increases in age, the biomass increments (merchBark, foliage, otherWood) are appended to the output file dependent on the afforestation area amount (if any).

above ground biomass = sum(area*(merchBark + foliage + otherWood))
below ground biomass = sbiombg(agbiomass)
[Li et all equations]  fineRoot, coarseRoot turnover (caluculated in units of biomass, not C)

Stem, branch, foliate and coarse root turnover amounts are calculated and moved to the receiving DOM pools.

Decay transfer dynamics undertaken.

Harvest wood product transfers undertaken.

### Checks

A series of checks are is undertaken to ensure conservation of mass balance, etc.

cohorts updated

output file produced



