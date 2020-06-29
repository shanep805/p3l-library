## A - Geometric Definitions
## A.1 - Set units
units_in()
## A.2 - Set our geometric interrogation. We will the values associated with this interrogation in subsequent variables. Read more here: https://help.paperlessparts.com/article/42-p3l-language-features
lathe = analyze_lathe()

## -------------------------------------------------------------------------------------------------------------------- ##

## B - Material Variables
## B.1 - Define Density and Cost Per Pound variables
density = var('Density', 0, 'Density', number, frozen=False)
cost_per_pound = var('Cost Per Pound', 0, '', currency, frozen=False)

## B.2 - Update variables based on project details
density.update(part.density)
density.freeze()

cost_per_pound.update(round(part.mat_cost_per_volume / density, 2))
cost_per_pound.freeze()

## -------------------------------------------------------------------------------------------------------------------- ##

## C - Part Variables
## C.1 - Define Buffer, Material Volume, Material Weight, and Material Cost.
buffer = var('Material Buffer (in)', 0.25, 'Buffer in inches for raw material size', number)
mat_volume = (part.size_x + buffer) * (part.size_y + buffer) * (part.size_z + buffer)
mat_weight = var('Pounds Per Part', 0, 'Per unit', number, frozen=False)
mat_cost = var('Material Unit Cost', 0, '', currency, frozen=False)

## C.2 - Update variables based on geometric interrogation
mat_weight.update(round(density * mat_volume, 2))
mat_weight.freeze()

mat_cost.update(round(mat_weight * cost_per_pound, 2))
mat_cost.freeze()

## -------------------------------------------------------------------------------------------------------------------- ##

## D - Final Calculations
## D.1 - Compile our costs. We multiply the cost per unit by the part quantity.
PRICE = mat_cost * part.qty

## D.2 - Define how many days this operation will contribute to the project lead time. Uses the added lead time from the Materials Page in Processes. Defaults to 0 if no value found.
DAYS = part.mat_added_lead_time