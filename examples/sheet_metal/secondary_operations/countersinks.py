# For pricing countersinks

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

labor_rate = var('Labor Rate', 100, 'Cost per hour for setup', currency)
machine_rate = var('Machine Rate', 50, 'Cost per hour for run', currency)

# establish runtime and setup time based on variables above
setup_time = var('setup_time', 0, 'Setup Time in hours', number, frozen=False)
cs_setup_minutes = counter_sink_setups * counter_sink_time_per_setup
setup_time.update(cs_setup_minutes / 60.0)
setup_time.freeze()

runtime = var('runtime', 0, 'Runtime per part in hours', number, frozen=False)
cs_runtime = counter_sink_count * runtime_per_counter_sink
runtime.update(cs_runtime / 3600.0)
runtime.freeze()

total_cycle_time = part.qty * runtime

setup_cost = labor_rate * setup_time
machine_cost = machine_rate * total_cycle_time

PRICE = setup_cost + machine_cost
DAYS = 0