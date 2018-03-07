# Forcarb

The forest estate is represented by matrix detailing cohort (spruce, pine, etc), yield class, age (age class), area, biomass, volume per hectare and the current annual increment of that cohort.

The matrix is fed into the program and divided up into cohorts. A cohort is a species at a productivity class.

These are processed by the main program code on an annual basis.

The area comprising a cohort ages one year at a time. In that year, the volume of the cohort is grown incrementally according to the Forestry Commission yield tables. During a ‘run’, thinnings and final harvests are undertaken according to rules (see below). To complete a run, the area that is clearfelled becomes the new area in the next run.

The code outputs the modified cohort matrix together with summary totals: standing volume, harvested volume. These are collated and will be used to estimate biomass pools using the biomass functions.

