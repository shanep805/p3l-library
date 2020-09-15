# This flat hole is used for fabricating holes for flat parts (simple drilled holes, countersinks, and counterbores).
# The cost is driven by number of unique setups of each type and the count of each in the part.

units_in()
sheet_metal = analyze_sheet_metal()

# collect countersink setups and count, and establish runtime/setup time for them
# countersink setups are determined by a major diameter, a depth, and a semi-angle
counter_sink_setups = var('Countersink Setups', 0, 'Count of countersink setups', number, frozen=False)
counter_sink_setups.update(sheet_metal.counter_sink_setups)
counter_sink_setups.freeze()
counter_sink_count = var('Countersink Count', 0, 'Count of countersinks', number, frozen=False)
counter_sink_count.update(sheet_metal.counter_sink_count)
counter_sink_count.freeze()
counter_sink_time_per_setup = var('Time per CS setup', 10.0, 'Time per CS setup in minutes', number)
runtime_per_counter_sink = var('Runtime per CS', 10.0, 'Runtime per CS in seconds', number)

# collect counterbore setups and count, and establish runtime/setup time for them
# counterbore setups are determined by a major diameter and a depth
counter_bore_setups = var('Counterbore Setups', 0, 'Count of counterbore setups', number, frozen=False)
counter_bore_setups.update(sheet_metal.counter_bore_setups)
counter_bore_setups.freeze()
counter_bore_count = var('Counterbore Count', 0, 'Count of counterbores', number, frozen=False)
counter_bore_count.update(sheet_metal.counter_bore_count)
counter_bore_count.freeze()
counter_bore_time_per_setup = var('Time per CB setup', 15.0, 'Time per CB setup in minutes', number)
runtime_per_counter_bore = var('Runtime per CB', 20.0, 'Runtime per CB in seconds', number)

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
cs_setup_minutes = counter_sink_setups * counter_sink_time_per_setup
cb_setup_minutes = counter_bore_setups * counter_bore_time_per_setup
sh_setup_minutes = simple_hole_setups * simple_hole_time_per_setup
setup_time.update((cs_setup_minutes + cb_setup_minutes + sh_setup_minutes) / 60.0)
setup_time.freeze()

runtime = var('runtime', 0, 'Runtime per part in hours', number, frozen=False)
cs_runtime = counter_sink_count * runtime_per_counter_sink
cb_runtime = counter_bore_count * runtime_per_counter_bore
sh_runtime = simple_hole_count * runtime_per_simple_hole
runtime.update((cs_runtime + cb_runtime + sh_runtime) / 3600.0)
runtime.freeze()

max_size = var('Part Max Dim', 0, '', number, frozen=False)
max_size.update(get_workpiece_value('flat_length', max(sheet_metal.size_x, sheet_metal.size_y)))
max_size.freeze()
part_weight = var('Part Weight', 0, '', number, frozen=False)
part_weight.update(get_workpiece_value('weight', part.weight))
part_weight.freeze()

crew_size_thresh = var('Crew Size Thresh', 48, 'Size of part in inches requiring additional crew', number)
crew_weight_thresh = var('Crew Weight Thresh', 40, 'Weight of part in pounds requiring additional crew', number)
crew = var('Crew', 1, 'Number of people assigned to attend work center', number, frozen=False)
if (max_size >= crew_size_thresh and max_size) or (part_weight >= crew_weight_thresh and part_weight):
    crew.update(2)
crew.freeze()

labor_rate = var('Labor Rate', 100, 'Cost per hour for setup', currency)
machine_rate = var('Machine Rate', 50, 'Cost per hour for run', currency)

total_cycle_time = part.qty * runtime

setup_cost = labor_rate * setup_time * crew
machine_cost = machine_rate * total_cycle_time

PRICE = setup_cost + machine_cost
DAYS = 0