# Collects a time save per pass based on largest part dimension
# Defaults to two passes (one for each side)
# Lines out number of passes to update at quote time

units_in()
sheet_metal = analyze_sheet_metal()

setup_time = var('setup_time', 0.1, 'Setup time in hours', number)
runtime = var('runtime', 0, 'Runtime in hours', number, frozen=False)

time_save_inch = var('Time Save In/Sec', 0.5, 'inches/second', number)

flat_length = var('Flat Length', 0, 'Max unfolded dimension', number, frozen=False)
flat_length.update(get_workpiece_value('flat_length', max(sheet_metal.size_x, sheet_metal.size_y)))
flat_length.freeze()

passes = var('Num Passes', 2, 'Passes on time save', number)

runtime.update(flat_length / time_save_inch * passes / 3600)
runtime.freeze()

setup_rate = var('Setup Rate', 100, '$/hr', currency)
machine_rate = var('Machine Rate', 50, '$/hr', currency)

part_weight = var('Part Weight', 0, '', number, frozen=False)
part_weight.update(get_workpiece_value('weight', part.weight))
part_weight.freeze()

crew_size_thresh = var('Crew Size Thresh', 48, 'Size of part in inches requiring additional crew', number)
crew_weight_thresh = var('Crew Weight Thresh', 40, 'Weight of part in pounds requiring additional crew', number)
crew = var('Crew', 1, 'Number of crew required to setup and run based on part size', number, frozen=False)
if (flat_length >= crew_size_thresh and flat_length) or (part_weight >= crew_weight_thresh and part_weight):
    crew.update(2)
crew.freeze()

setup_cost = setup_rate * setup_time * crew
run_cost = machine_rate * runtime * part.qty

PRICE = setup_cost + run_cost
DAYS = 0
