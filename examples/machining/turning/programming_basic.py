# Setup Time and Labor Rate Operation

# A - Define Setup Time and Labor Rate variables
setup_time = var('setup_time', 0, '', number)
labor_rate = var('Labor Rate ($)', 0, '', currency)

# B - Compile costs
PRICE = setup_time * labor_rate

# C - Define how many days this operation will contribute to the project lead time.
DAYS = 0

# D - Set workpiece values to be used in subsequent operations.
set_workpiece_value('total_setup_time', get_workpiece_value('total_setup_time', 0) + setup_time)			# A - Cumulative project setup time
