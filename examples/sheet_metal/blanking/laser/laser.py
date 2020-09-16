units_in()
sheet_metal = analyze_sheet_metal()

setup_time = var('setup_time', 0.5, 'Setup time, specified in hours', number)
runtime = var('runtime', 0, 'Runtime, specified in hours', number, frozen=False)

# thickness stored from upstream material operation
thickness = var('thickness', 0, 'thickness', number, frozen=False)
thickness.update(get_workpiece_value('thickness', sheet_metal.thickness))
thickness.freeze()

cut_length = var('cut length', 0, 'inches', number, frozen=False)
cut_length.update(sheet_metal.total_cut_length)
cut_length.freeze()

pierce_count = var('pierce count', 0, 'number of times laser_cost_per_sheet needs to pierce', number, frozen=False)
pierce_count.update(sheet_metal.pierce_count)
pierce_count.freeze()

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

# update runtime to sheet metal cutting perimeter
runtime.update(cut_length / mat_cut_rate / 60 + pierce_count * mat_pierce_time / 3600)
runtime.freeze()

labor_rate = var('Labor Rate', 100, 'Cost per hour for setup', currency)
machine_rate = var('Machine Rate', 50, 'Cost per hour for run', currency)

total_cycle_time = part.qty * runtime

setup_cost = labor_rate * setup_time
machine_cost = machine_rate * total_cycle_time

PRICE = setup_cost + machine_cost
DAYS = 0
