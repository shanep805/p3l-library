# Standard setup time, runtime, labor rate, machine rate template for the simplest pricing structure

setup_time = var('setup_time', 0, 'Setup time, specified in hours', number)
runtime = var('runtime', 0, 'Runtime, specified in hours', number)

labor_rate = var('Labor Rate', 0, 'Cost per hour for setup', currency)
machine_rate = var('Machine Rate', 0, 'Cost per hour for run', currency)

total_cycle_time = part.qty * runtime

setup_cost = labor_rate * setup_time
machine_cost = machine_rate * total_cycle_time

PRICE = setup_cost + machine_cost
DAYS = 0
