# CNC Milling (Level 1)

# A - Define Setup Time, Runtime, and Labor Rate variables
setup_time = var('setup_time', 0, '', number)
runtime = var('runtime', 0, '', number)
labor_rate = var('Labor Rate ($)', 0, '', currency)

# B - Compile Setup Cost and Cycle Cost
setup_cost = setup_time * labor_rate
cycle_cost = runtime * part.qty * labor_rate

# C - Final Calculations
PRICE = setup_cost + cycle_cost

# D - Define how many days this operation will contribute to the project lead time
DAYS = 0

# E - Set workpiece values to be used in subsequent operations.
set_workpiece_value('Total Setup Time', get_workpiece_value('Total Setup Time', 0) + setup_time)			# A - Cumulative project setup time
set_workpiece_value('Total Runtime', get_workpiece_value('Total Runtime', 0) + runtime)						# B - Cumulative project runtime
set_workpiece_value('Operation Count', get_workpiece_value('Operation Count', 0) + 1)						# C - Cumulative operation count