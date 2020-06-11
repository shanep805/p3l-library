# Collects a time save per pass based on largest part dimension
# Defaults to two passes (one for each side)
# Lines out number of passes to update at quote time

units_in()
sheet_metal = analyze_sheet_metal()

setup_time = var('setup_time', 0.1, 'Setup time in hours', number)
runtime = var('runtime', 0, 'Runtime in hours', number, frozen=False)

time_save_inch = var('Time Save Inch', 3.0, 'inches/second', number)

ts_size = var('Time Save Size', 0, 'Max unfolded dimension', number, frozen=False)
ts_size.update(max(sheet_metal.size_x, sheet_metal.size_y))
ts_size.freeze()

passes = var('TS Passes', 2, 'Passes on time save', number)

time_save_run = var('Time Save Run', 0, 'Time save time in seconds', number, frozen=False)
time_save_run.update(ts_size / time_save_inch * passes)
time_save_run.freeze()

runtime.update(time_save_run / 3600)
runtime.freeze()

setup_rate = var('Setup Rate', 100, '$/hr', currency)
machine_rate = var('Machine Rate', 50, '$/hr', currency)

max_size = var('Part Max Dim', 0, '', number, frozen=False)
max_size.update(max(sheet_metal.size_x, sheet_metal.size_y))
max_size.freeze()
part_weight = var('Part Weight', 0, '', number, frozen=False)
part_weight.update(part.weight)
part_weight.freeze()

crew_size_thresh = var('Crew Size Thresh', 48, 'Size of part in inches requiring additional crew', number)
crew_weight_thresh = var('Crew Weight Thresh', 40, 'Weight of part in pounds requiring additional crew', number)
crew = var('Crew', 1, 'Number of crew required to setup and run based on part size', number, frozen=False)
if (max_size >= crew_size_thresh and max_size) or (part_weight >= crew_weight_thresh and part_weight):
  crew.update(2)
crew.freeze()

PRICE = setup_rate * setup_time * crew + machine_rate * runtime * part.qty
DAYS = 0