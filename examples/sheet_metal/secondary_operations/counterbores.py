units_in()
sheet_metal = analyze_sheet_metal()

counter_bore_setups = var('Counterbore Setups', 0, 'Count of counterbore setups', number, frozen=False)
counter_bore_setups.update(sheet_metal.counter_bore_setups)
counter_bore_setups.freeze()
counter_bore_count = var('Counterbore Count', 0, 'Count of counterbores', number, frozen=False)
counter_bore_count.update(sheet_metal.counter_bore_count)
counter_bore_count.freeze()
counter_bore_time_per_setup = var('Time per CB setup', 15.0, 'Time per CB setup in minutes', number)
runtime_per_counter_bore = var('Runtime per CB', 20.0, 'Runtime per CB in seconds', number)

labor_rate = var('Labor Rate', 100, 'Cost per hour for setup', currency)
machine_rate = var('Machine Rate', 50, 'Cost per hour for run', currency)

# establish runtime and setup time based on variables above
setup_time = var('setup_time', 0, 'Setup Time in hours', number, frozen=False)
cb_setup_minutes = counter_bore_setups * counter_bore_time_per_setup
setup_time.update(cb_setup_minutes / 60.0)
setup_time.freeze()

runtime = var('runtime', 0, 'Runtime per part in hours', number, frozen=False)
cb_runtime = counter_bore_count * runtime_per_counter_bore
runtime.update(cb_runtime / 3600.0)
runtime.freeze()

total_cycle_time = part.qty * runtime

setup_cost = labor_rate * setup_time
machine_cost = machine_rate * total_cycle_time

PRICE = setup_cost + machine_cost
DAYS = 0