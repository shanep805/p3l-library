# for pricing manually drilled simple holes

units_in()
sheet_metal = analyze_sheet_metal()

# collect simple drilled hole setups and count, and establish runtime/setup time for them
# simple drilled hole setups are determined by hole diameter
# NOTE: holes will only be called out as drilled holes if their diameter is less than (default) 1x the thickness
simple_hole_setups = var('Simple Hole Setups', 0, 'Count of simple hole setups', number, frozen=False)
simple_hole_setups.update(sheet_metal.simple_drilled_hole_setups)
simple_hole_setups.freeze()
simple_hole_count = var('Simple Hole Count', 0, 'Count of simple holes', number, frozen=False)
simple_hole_count.update(sheet_metal.simple_drilled_hole_count)
simple_hole_count.freeze()
simple_hole_time_per_setup = var('Time per SH setup', 5.0, 'Time per SH setup in minutes', number)
runtime_per_simple_hole = var('Runtime per SH', 5.0, 'Runtime per SH in seconds', number)

# establish runtime and setup time based on variables above
setup_time = var('setup_time', 0, 'Setup Time in hours', number, frozen=False)
sh_setup_minutes = simple_hole_setups * simple_hole_time_per_setup
setup_time.update(sh_setup_minutes / 60.0)
setup_time.freeze()

runtime = var('runtime', 0, 'Runtime per part in hours', number, frozen=False)
sh_runtime = simple_hole_count * runtime_per_simple_hole
runtime.update(sh_runtime / 3600.0)
runtime.freeze()

labor_rate = var('Labor Rate', 100, 'Cost per hour for setup', currency)
machine_rate = var('Machine Rate', 50, 'Cost per hour for run', currency)

total_cycle_time = part.qty * runtime

setup_cost = labor_rate * setup_time
machine_cost = machine_rate * total_cycle_time

PRICE = setup_cost + machine_cost
DAYS = 0