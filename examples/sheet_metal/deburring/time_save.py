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

rate = var('Rate', 100, '$/hr', currency)

PRICE = rate * setup_time + rate * runtime * part.qty
DAYS = 0