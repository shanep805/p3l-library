# define variables
setup_time = var('setup_time', 0, '', number)
runtime = var('runtime', 0, '', number)
hourly_rate = var('Rate ($/hr)', 0, '', currency)

setup_cost = setup_time * hourly_rate
cycle_cost = runtime * part.qty * hourly_rate

PRICE = setup_cost + cycle_cost

# Define how many days this operation will contribute to the project lead time
# NOTE: this can be fractional
DAYS = 0

# set workpiece values to be used in subsequent operations.
set_workpiece_value('total_setup_time', get_workpiece_value('total_setup_time', 0) + setup_time)
set_workpiece_value('total_runtime', get_workpiece_value('total_runtime', 0) + runtime)
