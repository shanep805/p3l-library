# This operation describes how to price mold construction for a urethane casting process by figuring out the number of
# molds required to make based off of an established mold life.
# This operation takes in to account mold preparation, construction, and material cost.

units_in()
casting = analyze_casting()

mold_life = var('Mold Life', 20, 'Number of shots per mold', number)
pattern_prep = var('Pattern Prep (hrs)', 0.5, 'Hours to prepare mold', number)
mold_making = var('Mold Making (hrs)', 0.5, 'Hours to create mold', number)
extra_cost = var('Extra cost per mold', 0, 'Adjustment for extra part shot', currency)

molds_to_make = ceil(part.qty / mold_life)

mold_buffer = var('Mold Buffer (in)', 1, 'Buffer to apply to part bounding box when making mold', number)
mold_mat_cost_per_volume = var('Mold Material Cost ($/cu. in)', 0.67, 'Mold material cost per volume', currency)

mold_bbox = (part.size_x + mold_buffer) * (part.size_y + mold_buffer) * (part.size_z + mold_buffer)
per_mold_mat_cost = mold_bbox * mold_mat_cost_per_volume

setup_labor_rate = var('Setup Labor Rate', 0, 'Labor cost per hour to setup mold', currency)
run_labor_rate = var('Run Labor Rate', 0, 'Labor cost per hour to make mold', currency)

per_mold_labor_cost = setup_labor_rate * pattern_prep + run_labor_rate * mold_making

total_labor_cost = per_mold_labor_cost * molds_to_make
total_mold_mat_cost = per_mold_mat_cost * molds_to_make
total_extra_cost = extra_cost * molds_to_make

PRICE = total_labor_cost + total_mold_mat_cost + total_extra_cost
DAYS = 0
