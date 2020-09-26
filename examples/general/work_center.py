# Represents an internal operation performed at a work center. Priced based on
# setup labor, run labor, and machine time. These variables are available:
#
# setup_labor_rate: hourly labor rate ($/hr) applied to setup time (the time it
# takes to prepare the work center for this operation)
# run_labor_rate: hourly labor rate ($/hr) applied to runtime
# crew: number of people assigned to attend work center
# machine_rate: hourly rate ($/hr) applied to the time this work center will be
# occupied
# efficiency: percentage of real time that work center will be processing parts
#     e.g. If part runtime is 60 minutes and efficiency is 50%, then each part
#     will occupy work center for 120 minutes
# percent_attended: percentage of total work center occupation time that requires
# crew to attend to the machine. Run labor rate is only applied to the attended
# time.
#
# When working with runtime or setup_time in your pricing formula, time will always be in hours.  The display units
# can be set on the operation level or when quoting.

units_in()
setup_time = var('setup_time', 0, 'Setup time, specified in hours', number)
runtime = var('runtime', 0, 'Runtime per part, specified in hours', number)

setup_labor_rate = var('Setup Labor Rate', 65, 'Labor cost per hour to set up work center', currency)
run_labor_rate = var('Run Labor Rate', 65, 'Labor cost per hour to attend work center machine', currency)
crew = var('Crew', 1, 'Number of people assigned to attend work center', number)
machine_rate = var('Machine Rate', 220, 'Cost per hour to keep work center machine occupied', currency)
efficiency = var('Efficiency', 100, 'Percentage of real time the work center is processing parts', number)
percent_attended = var('Percent Attended', 0, 'Percentage of time work center must be attended', number)

total_cycle_time = part.qty * runtime
total_machine_occupied_time = total_cycle_time / efficiency * 100
total_attended_time = total_machine_occupied_time * percent_attended / 100

setup_cost = setup_time * setup_labor_rate
work_center_usage_cost = total_machine_occupied_time * machine_rate
run_labor_cost = total_attended_time * run_labor_rate * crew

PRICE = setup_cost + work_center_usage_cost + run_labor_cost
DAYS = 0
