# This wire edm operation is an extension of the work center operation template, but contextualizes it
# for wire edm processes.
# Establishes a ceiling for wire edm cut rates extracted from cutting steel parts at varying cut depths.
#
# When working with runtime or setup_time in your pricing formula, time will always be in hours.  The display units
# can be set on the operation level or when quoting.

units_in()
wire = analyze_wire_edm()

min_cut_rate = 0.007
cut_rate_slope = 0 - 0.009
cut_rate_intercept = 0.05

cut_rate_calculated = cut_rate_slope * wire.average_cut_depth + cut_rate_intercept
if cut_rate_calculated < min_cut_rate:
    cut_rate_use = min_cut_rate
else:
    cut_rate_use = cut_rate_calculated

cut_rate = var('Cut Rate', 0, 'in/min', number, frozen=False)
cut_rate.update(cut_rate_use)
cut_rate.freeze()
cut_length = var('Cut Length, in', 0, 'in', number, frozen=False)

setup_time_per_setup = var('Base Setup Time per setup', 60.0, 'minutes', number)
setup_time = var('setup_time', 0, 'Total setup time, specified in hours', number, frozen=False)
setup_time.update(wire.setup_count * setup_time_per_setup / 60.0)
setup_time.freeze()

runtime_per_drilled_hole = var('Runtime Per Drilled Hole', 2.5, 'minutes', number)
total_drilled_runtime = wire.pierce_count * runtime_per_drilled_hole / 60.0

cut_length.update(wire.cut_length)
cut_length.freeze()

runtime = var('runtime', 0, 'Runtime per part, specified in hours', number, frozen=False)
runtime.update(total_drilled_runtime + cut_length / cut_rate / 60.0)
runtime.freeze()

labor_rate = var('Labor Rate', 0, 'Cost per hour for setup', currency)
machine_rate = var('Machine Rate', 0, 'Cost per hour for run', currency)

total_cycle_time = part.qty * runtime

setup_cost = labor_rate * setup_time
machine_cost = machine_rate * total_cycle_time

PRICE = setup_cost + machine_cost
DAYS = 0