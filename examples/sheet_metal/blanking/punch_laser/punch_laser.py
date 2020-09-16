# This operation assumes it will hit all single hits with the punch_cost_per_sheet
# and all larger more complicated contours with the laser.

units_in()
sheet_metal = analyze_sheet_metal()

thickness = var('thickness', 0, 'thickness', number, frozen=False)
thickness.update(sheet_metal.thickness)
thickness.freeze()

laser_cut_length = var('cut length', 0, 'inches', number, frozen=False)
laser_cut_length.update(sheet_metal.punch_multi_hit_cut_length)
laser_cut_length.freeze()

laser_pierce_count = var('pierce count', 0, 'number of times laser_cost_per_sheet needs to pierce', number, frozen=False)
laser_pierce_count.update(sheet_metal.pierce_count - sheet_metal.punch_single_hit_count)
laser_pierce_count.freeze()

mat_cut_rate = var('Mat Cut Rate', 10, 'material cut rate in/min', number, frozen=False)
mat_pierce_time = var('Mat Pierce Time', 2, 'material pierce time, seconds', number, frozen=False)

row = table_var(
  'Cut Rates',
  'Looking up to table for cut rates based on material family',
  'laser_cut_rates',
  create_filter(
    filter('material_family', '=', part.material_family),
    filter('thickness', '>', thickness),
  ),
  create_order_by('thickness', '-cut_rate'),
  'cut_rate'
)

if row:
  mat_cut_rate.update(row.cut_rate)
  mat_pierce_time.update(row.pierce_time)
mat_cut_rate.freeze()
mat_pierce_time.freeze()

# update laser_cost_per_sheet runtime
laser_runtime = var('Laser Time', 0, 'Minutes of laser_cost_per_sheet time', number, frozen=False)
laser_runtime.update(laser_cut_length / mat_cut_rate + laser_pierce_count * mat_pierce_time / 60)
laser_runtime.freeze()

# now calculate punch_cost_per_sheet setup time based on unique tools needed
single_hit_setups = var('Single Hit Setups', 0, 'Number of tools to make single-hit contours', number, frozen=False)
single_hit_setups.update(sheet_metal.punch_single_hit_setups)
single_hit_setups.freeze()

setup_time_per_tool = var('Setup time per tool', 10.0, 'Setup time per unique punch_cost_per_sheet tool in minutes', number)
punch_tool_setup_time = var('Punch Tooling Setup', 0, 'Setup time in minutes for unique punch_cost_per_sheet tools', number, frozen=False)
punch_tool_setup_time.update(setup_time_per_tool * single_hit_setups)
punch_tool_setup_time.freeze()

# now calculate punch_cost_per_sheet runtime based on single hits only and a time per hit
single_hit_count = var('Single Hit Count', 0, 'Total number of single hit strokes', number, frozen=False)
single_hit_count.update(sheet_metal.punch_single_hit_count)
single_hit_count.freeze()

runtime_per_hit = var('Time per hit', 1.5, 'Time per hit in seconds', number)

punch_runtime = var('Punch runtime', 0, 'Punch runtime in minutes', number, frozen=False)
punch_runtime.update(runtime_per_hit * single_hit_count / 60)
punch_runtime.freeze()

# now update total setup time as sum of punch_cost_per_sheet tool and base setup time
base_setup_time = var('Base Setup Time', 30.0, 'Base setup time in minutes', number)

setup_time = var('setup_time', 0, 'Setup Time in hours', number, frozen=False)
setup_time.update(base_setup_time / 60 + punch_tool_setup_time / 60)
setup_time.freeze()

# now update runtime as a sum of laser_cost_per_sheet and punch_cost_per_sheet runtimes
runtime = var('runtime', 0, 'Runtime per part in hours', number, frozen=False)
runtime.update(laser_runtime / 60 + punch_runtime / 60)
runtime.freeze()

# now establish and apply labor and machine rates
labor_rate = var('Labor Rate', 100, 'Cost per hour for setup', currency)
machine_rate = var('Machine Rate', 50, 'Cost per hour for run', currency)

total_cycle_time = part.qty * runtime

setup_cost = labor_rate * setup_time
machine_cost = machine_rate * total_cycle_time

PRICE = setup_cost + machine_cost
DAYS = 0
