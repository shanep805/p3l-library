# A - Geometric Definitions
# A.1 - Set units
units_in()
# A.2 - Set our geometric interrogation.
# Read more here: https://help.paperlessparts.com/article/42-p3l-language-features
lathe = analyze_lathe()

# B - Material Variables
# B.1 - Define Density and Cost Per Pound variables
density = var('Density', 0, 'Density', number, frozen=False)
cost_per_pound = var('Cost Per Pound', 0, '', currency, frozen=False)

# B.2 - Update variables based on project details
density.update(part.density)
density.freeze()

cost_per_pound.update(round(part.mat_cost_per_volume / density, 2))
cost_per_pound.freeze()

# C - Bar and Part Variables
# C.1 - Define Bar Variables
bar_length = var('Bar Length, in', 96, '', number)
bar_radius = var('Bar Radius, in', 0, '', number, frozen = False)
cutoff = var('Cutoff, in', 0.125, '', number)
facing = var('Facing, in', 0, '', number)
bar_end = var('Bar End, in', 0, 'Length of bar allocated for holding', number)
parts_per_bar = var('Parts Per Bar', 0, '', number, frozen=False)

# C.2 - Define Part Variables
turning_length = var('Turning Length', 0, 'Length of part along turning axis in inches', number, frozen=False)
turning_radius = var('Turning Radius', 0, 'Outermost radius of part in inches', number, frozen=False)
length_buffer = var('Length Buffer (in)', 0.125, 'Buffer in inches for length of raw material size', number)
radial_buffer = var('Radial Buffer (in)', 0.0625, 'Buffer in inches for radius of raw material size', number)

# C.3 - Update variables based on geometric interrogation
turning_length.update(lathe.stock_length)
turning_length.freeze()

turning_radius.update(lathe.stock_radius)
turning_radius.freeze()

stock_length = turning_length + length_buffer
bar_radius.update(ceil((turning_radius + radial_buffer) * 4) / 4)
bar_radius.freeze()

# C.4 - Update Parts Per Bar based on Bar Length and Part Length
parts_per_bar.update(floor((bar_length - bar_end) / (stock_length + cutoff + facing)))
parts_per_bar.freeze()
if parts_per_bar > 0:
    bars = ceil(part.qty / parts_per_bar)
else:
    bars = 1

# D - Material Calculations
# D.1 - Define Material Volume, Material Weight, and Material Cost
mat_weight = var('Material Weight (lbs)', 0, '', number, frozen = False)
mat_cost = var('Material Cost ($)', 0, '', currency, frozen = False)
cost_per_unit = var('Cost Per Unit ($)', 0, '', currency, frozen = False)

# D.2 - Update variables based on calculations
mat_volume = bar_radius**2 * 3.1415926535 * bar_length

mat_weight.update(round(density * mat_volume, 2))
mat_weight.freeze()

mat_cost.update(round(mat_weight * cost_per_pound, 2))
mat_cost.freeze()

cost_per_unit.update(round(mat_cost / parts_per_bar, 3))
cost_per_unit.freeze()

# E - Final Calculations
# E.1 - Compile our costs. We multiply the cost per unit by the part quantity.
PRICE = cost_per_unit * part.qty

# E.2 - Define how many days this operation will contribute to the project lead time. Uses the added lead time from the Materials Page in Processes. Defaults to 0 if no value found.
DAYS = part.mat_added_lead_time