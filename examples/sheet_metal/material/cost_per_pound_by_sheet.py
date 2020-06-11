# This operation prices material based on a per-pound price for sheet metal parts. Based on the material selected, we
# will extract the density of the material from our database, and then resolve a material cost per unit volume. You can
# set a buffer to expand the unfolded x and y of the part geometry using the buffer variable.
# We use dynamic variables here to provide you with important information like the cost per pound and
# pounds per part value at quote time.

units_in()
sheet_metal = analyze_sheet_metal()
if part.material:
    set_operation_name(part.material)

density = var('Density', 0, 'Density', number, frozen=False)
density.update(part.density)
density.freeze()

cost_per_pound = var('Cost Per Pound', 0, '', currency, frozen=False)
cost_per_pound.update(round(part.mat_cost_per_volume / density, 2))
cost_per_pound.freeze()

unfolded_x = var('Unfolded X', 0, 'Size of unbent part in x dimension', number, frozen=False)
unfolded_x.update(sheet_metal.size_x)
unfolded_x.freeze()

unfolded_y = var('Unfolded Y', 0, 'Size of unbent part in y dimension', number, frozen=False)
unfolded_y.update(sheet_metal.size_y)
unfolded_y.freeze()

thickness = var('Thickness', 0, '', number, frozen=False)
thickness.update(sheet_metal.thickness)
thickness.freeze()

buffer = var('Material Buffer (in)', 0, 'Buffer in inches for raw material size', number)
mat_volume = (unfolded_x + buffer) * (unfolded_y + buffer) * thickness
mat_weight = var('Material Weight', 0, 'Per unit', number, frozen=False)
mat_weight.update(round(density * mat_volume, 2))
mat_weight.freeze()

mat_cost = var('Material Unit Cost', 0, '', currency, frozen=False)
mat_cost.update(round(mat_weight * cost_per_pound, 2))
mat_cost.freeze()

PRICE = mat_cost * part.qty
# part.mat_added_lead_time is specified in process material setup, defaults to 0
DAYS = part.mat_added_lead_time
