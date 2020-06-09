# This flat punching operation is for flat punching operations.
# Simple contours (circles, squares, rectangles, slots, obrounds) below your custom
# max size threshold will be assumed to cut with a single hit from a punch tool. All other contours are assumed
# to be multi-hit features. We provide you the multi-hit cut length to estimate pricing of these operations.

units_in()
sheet_metal = analyze_sheet_metal()

single_hit_setups = var('Single Hit Setups', 0, 'Number of tools to make single-hit contours', number, frozen=False)
single_hit_count = var('Single Hit Count', 0, 'Total number of single hit strokes', number, frozen=False)
multi_hit_cut_length = var('Multi Hit Length', 0, 'Cut length accomplished by multi hits', number, frozen=False)

single_hit_setups.update(sheet_metal.punch_single_hit_setups)
single_hit_setups.freeze()
single_hit_count.update(sheet_metal.punch_single_hit_count)
single_hit_count.freeze()
multi_hit_cut_length.update(sheet_metal.punch_multi_hit_cut_length)
multi_hit_cut_length.freeze()

setup_time = var('setup_time', 0, 'Setup Time in hours', number, frozen=False)
runtime = var('runtime', 0, 'Runtime per part in hours', number, frozen=False)

base_setup_time = var('Base Setup Time', 30.0, 'Base setup time in minutes', number)
setup_time_per_tool = var('Setup time per tool', 10.0, 'Setup time per unique punch tool in minutes', number)
setup_time.update(base_setup_time / 60.0 + setup_time_per_tool * single_hit_setups / 60.0)
setup_time.freeze()

# apply a runtime per punch and estimate number of punches to accomplish multi hit features using a factor to runtime
runtime_per_punch = var('Time per punch', 1.5, 'Time per punch in seconds', number)
multi_hit_per_punch_length = var(
    'Multi hit per punch length', 2, 'Amount of cut length removed per stroke for multi-hit contours', number
)
multi_hit_count = var('Multi hit count', 0, 'Total number of hits to punch multi-hit contours', number, frozen=False)
multi_hit_count.update(ceil(multi_hit_cut_length / multi_hit_per_punch_length))
multi_hit_count.freeze()

# update runtime to sheet metal cutting perimeter
runtime.update((single_hit_count + multi_hit_count) * runtime_per_punch / 3600.0)
runtime.freeze()

labor_rate = var('Labor Rate', 100, 'Cost per hour for setup', currency)
machine_rate = var('Machine Rate', 50, 'Cost per hour for run', currency)

total_cycle_time = part.qty * runtime

setup_cost = labor_rate * setup_time
machine_cost = machine_rate * total_cycle_time

PRICE = setup_cost + machine_cost
DAYS = 0
