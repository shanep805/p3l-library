# To estimate a runtime, it uses a base material removal rate based on material family and applies
# it to a cylindrical stock piece extracted from the Paperless Parts lathe interrogation. You can set
# this material removal rate and adjust it at quote time.

units_in()
lathe = analyze_lathe()

# establish a dictionary (look-up table) for material removal rates based on material family or class
# units in cubic inches per minute
removal_rates = {
    'Aluminum': 1.0,
    'Steel': 0.5,
    'Stainless Steel': 0.25,
    'Polymer': 1.2,
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

turning_radius = var('Turning Radius', 0, 'Outermost radius of part in inches', number, frozen=False)
turning_radius.update(lathe.stock_radius)
turning_radius.freeze()

turning_length = var('Turning Length', 0, 'Length of part along turning axis in inches', number, frozen=False)
turning_length.update(lathe.stock_length)
turning_length.freeze()

radial_buffer = var('Radial Stock Buffer, in', 0.0625, 'Buffer applied to the outer radius of part in inches', number)
length_buffer = var('Length Stock Buffer, in', 0.125, 'Buffer to the length of the part along the turning axis in inches', number)

stock_radius = turning_radius + radial_buffer
stock_length = turning_length + length_buffer

stock_volume = stock_radius**2 * 3.1415926535 * turning_length
volume_removal = stock_volume - part.volume

# assume one hour setup time
setup_time = var('setup_time', 1, 'Setup time, specified in hours', number)

# minimum 30 seconds of runtime
runtime = var('runtime', 0, 'Runtime, specified in hours', number, frozen=False)
est_runtime = stock_volume / removal_rate
est_runtime = max(0.25 / 60, est_runtime)  # 15 second floor
est_runtime = min(10 / 60, est_runtime)  # 10 minute ceiling
runtime.update(est_runtime)
runtime.freeze()

labor_rate = var('Labor Rate', 0, 'Cost per hour for setup', currency)
machine_rate = var('Machine Rate', 0, 'Cost per hour for run', currency)

total_cycle_time = part.qty * runtime

setup_cost = labor_rate * setup_time
machine_cost = machine_rate * total_cycle_time

PRICE = setup_cost + machine_cost
DAYS = 0
