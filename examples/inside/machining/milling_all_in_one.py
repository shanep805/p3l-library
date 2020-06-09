# For pricing milling operations. It additionally uses the Paperless Parts generated runtime values and setup
# count to estimate price. We also establish a conservative material removal rate to act as a governor
# on very high runtime estimates. The material removal rate is determined by the material family or class.
# This op is designed to be used as an all in one, and not applied per setup.
#
# When working with runtime or setup_time in your pricing formula, time will always be in hours.  The display units
# can be set on the operation level or when quoting.

units_in()
mill = analyze_mill3()

# establish a dictionary (look-up table) for material removal rates based on material family or class
# units in cubic inches per minute
removal_rates = {
    'Aluminum': 3.0,
    'Steel': 1.5,
    'Stainless Steel': 1.0,
    'Polymer': 3.5,
}

# collect removal rate based on material family or class
# if not found in the removal_rates lookup, go with worst case scenario (Stainless Steel)
if part.material_family in removal_rates:
    rate = removal_rates[part.material_family]
elif part.material_class in removal_rates:
    rate = removal_rates[part.material_class]
else:
    rate = removal_rates['Stainless Steel']

# putting upper limit to runtime based on minimum material removal rate
removal_rate = var('Minimum Material Removal Rate', 0, 'Material removal rate in cu.in./min', number, frozen=False)
removal_rate.update(rate)
removal_rate.freeze()

buffer = var('Stock Buffer, in', 0.25, 'Buffer to apply to part for when using material removal rate', number)
bbox = (part.size_x + buffer) * (part.size_y + buffer) * (part.size_z + buffer)
max_runtime = (bbox - part.volume) / removal_rate / 60

setup_time_per_setup = var('Setup Time Per Setup', 0.5, 'Setup time per setup in hours', number)
setup_time = var('setup_time', 0, 'Setup time, specified in hours', number, frozen=False)
setup_time.update(mill.setup_count * setup_time_per_setup)
setup_time.freeze()

paperless_runtime_estimate = mill.runtime

runtime = var('runtime', 0, 'Runtime per part, specified in hours', number, frozen=False)

has_been_interrogated = mill.runtime != 0
if has_been_interrogated:
    runtime.update(min(paperless_runtime_estimate, max_runtime))
else:
    runtime.update(max_runtime)
runtime.freeze()

labor_rate = var('Labor Rate', 0, 'Cost per hour for setup', currency)
machine_rate = var('Machine Rate', 0, 'Cost per hour for run', currency)

total_cycle_time = part.qty * runtime

setup_cost = labor_rate * setup_time
machine_cost = machine_rate * total_cycle_time

PRICE = setup_cost + machine_cost
DAYS = 0
