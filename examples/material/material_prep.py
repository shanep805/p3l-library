# Assumes one cut for every part in make quantity. Builds on the standard
# work center costing logic.

units_in()

setup_time = var('setup_time', 0, 'Setup Time in hours', number)
runtime = var('runtime', 0.0028, 'Runtime per material prep cut in hours (10 seconds)', number)

setup_labor_rate = var('Setup Labor Rate', 0, 'Labor cost per hour to setup workcenter', currency)
run_labor_rate = var('Run Labor Rate', 0, 'Labor cost per hour to attend workcenter machine', currency)
machine_rate = var('Machine Rate', 0, 'Cost per hour to keep workcenter machine occupied', currency)
efficiency = var('Efficiency', 100, 'Percentage of real time the workcenter is running with regards to runtime', number)
percent_attended = var('Percent Attended', 100, 'Percentage of time workcenter must be attended', number)
crew = var('Crew', 1, 'Number of people assigned to attend workcenter', number)

total_cycle_time = part.qty * runtime
total_machine_occupied_time = total_cycle_time / efficiency * 100
total_attended_time = total_machine_occupied_time * percent_attended / 100

setup_cost = setup_time * setup_labor_rate
workcenter_usage_cost = total_machine_occupied_time * machine_rate
run_labor_cost = total_attended_time * run_labor_rate * crew

PRICE = setup_cost + workcenter_usage_cost + run_labor_cost
DAYS = 0