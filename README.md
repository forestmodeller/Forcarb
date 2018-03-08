# Forcarb

The forest estate is represented by matrix detailing cohort (spruce, pine, etc), yield class, age (age class), area, biomass, volume per hectare and the current annual increment of that cohort.

The matrix is fed into the program and divided up into cohorts. A cohort is a species at a productivity class.

These are processed by the main program code on an annual basis.

The area comprising a cohort ages one year at a time. In that year, the volume of the cohort is grown incrementally according to the Forestry Commission yield tables. During a ‘run’, thinnings and final harvests are undertaken according to rules (see below). To complete a run, the area that is clearfelled becomes the new area in the next run.

The code outputs the modified cohort matrix together with summary totals: standing volume, harvested volume. These are collated and will be used to estimate biomass pools using the biomass functions.

The run follows these steps consistently:
1 Vol modification 
2 Thinning / Harvest
3 Area modification
4 Vol increment

The script gets complex when conditions arise in which the estsate is not clearfelled as the criteria are not met. In situations these situations, the forest estate gains an additional age. This has implications for the what is termed the “endpoint” which determines the estate age. Endpoint is determined at the beginning of each annual run. Prior to this step, the matrix data is checked for rows of trailing zeros: if a line of zeros is present at the bottom (only) of the matrix, it is removed. Various calculations are based around this endpoint. 
Another situation can arise due to input data having zero ages represented while older ages do exist. 

volume mod
standingvol[z] = prevvol[z]
prevvol[z] = matrix[z-1]

area mod
area[z] = prevarea[z], 
prevarea[z] = matrix[z-1]

volume increment
Increment = Area * CAI
Increment + standing vol = New Vol

thinning
In a single year, steps 3 and 4 above are followed for each age until the thinning age is reached. Then the available thinning volume is calculated and compared to the target. Volume is removed accordingly. 

final harvest
Similarly, steps 3 and 4 are followed until the clearfell age is reached (clearfell age follows upper thinning age). Then the available standing volume for clearfell is calculated and compared with the target.

For harvest there are two main categories:
1) If the target harvest is greater than the available volume
2) If the target harvest is less than the available volume

more to follow ...


