# Uses Paperless Parts sheet metal interrogation to pull out bends from a geometry
# and applies a runtime for each bending operation found.

units_in()
sheet_metal = analyze_sheet_metal()

# setup: 15 min / bend
setup_time_per_bend = var('Setup Time Per Bend (hr)', 0.25, 'hr', number)
# runtime: 15 seconds / bend
run_time_per_bend = var('Run Time Per Bend (seconds)', 15, 'seconds per bend', number)

bend_count = var('Bend Count', 0, 'total bends', number, frozen=False)
bend_count.update(sheet_metal.bend_count)
bend_count.freeze()

setup_time = var('setup_time', 0, 'Setup time, specified in hours', number, frozen=False)
setup_time.update(bend_count * setup_time_per_bend)
setup_time.freeze()

runtime = var('runtime', 0, 'Runtime, specified in hours', number, frozen=False)
runtime.update(bend_count * run_time_per_bend / 3600)
runtime.freeze()

labor_rate = var('Labor Rate', 100, 'Cost per hour for setup', currency)
machine_rate = var('Machine Rate', 50, 'Cost per hour for run', currency)

total_cycle_time = part.qty * runtime

setup_cost = labor_rate * setup_time
machine_cost = machine_rate * total_cycle_time

PRICE = setup_cost + machine_cost
DAYS = 0
