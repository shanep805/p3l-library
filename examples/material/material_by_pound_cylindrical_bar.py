# This operation prices material based on a per-pound price. Based on the material selected, we will extract
# the density of the material from our database, and then resolve a material cost per unit volume. You can set
# a buffer to expand the detected radius and length of the stock piece.
# We use dynamic variables here to provide you with important information like the cost per pound and
# pounds per part value at quote time.

units_in()
lathe = analyze_lathe()
if part.material:
    set_operation_name(part.material)

density = var('Density', 0, 'Density', number, frozen=False)
density.update(part.density)
density.freeze()

cost_per_pound = var('Cost Per Pound', 0, '', currency, frozen=False)
cost_per_pound.update(round(part.mat_cost_per_volume / density, 2))
cost_per_pound.freeze()

turning_radius = var('Turning Radius', 0, 'Outermost radius of part in inches', number, frozen=False)
turning_radius.update(lathe.stock_radius)
turning_radius.freeze()

turning_length = var('Turning Length', 0, 'Length of part along turning axis in inches', number, frozen=False)
turning_length.update(lathe.stock_length)
turning_length.freeze()

length_buffer = var('Length Buffer (in)', 0.125, 'Buffer in inches for length of raw material size', number)
radial_buffer = var('Radial Buffer (in)', 0.0625, 'Buffer in inches for radius of raw material size', number)

stock_radius = turning_radius + radial_buffer
stock_length = turning_length + length_buffer

mat_volume = stock_radius**2 * 3.1415926535 * turning_length
mat_weight = var('Pounds Per Part', 0, 'Per unit', number, frozen=False)
mat_weight.update(round(density * mat_volume, 2))
mat_weight.freeze()

mat_cost = var('Material Unit Cost', 0, '', currency, frozen=False)
mat_cost.update(round(mat_weight * cost_per_pound, 2))
mat_cost.freeze()

PRICE = mat_cost * part.qty
# part.mat_added_lead_time is specified in process material setup, defaults to 0
DAYS = part.mat_added_lead_time
