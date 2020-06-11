# Assumes one cut for every part in make quantity.
units_in()

setup_time = var('setup_time', 0.25, 'Setup Time in hours', number)
runtime = var('runtime', 0.0028, 'Runtime per material prep cut in hours (10 seconds)', number)

labor_rate = var('Labor Rate', 50, '$/hr', currency)
machine_rate = var('Machine Rate', 50, '$/hr', currency)

setup_cost = setup_time * labor_rate
machine_cost = machine_rate * runtime * part.qty

PRICE = setup_cost + machine_cost
DAYS = 0
