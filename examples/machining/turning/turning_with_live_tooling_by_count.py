units_in()
lathe = analyze_lathe()

stock_diameter = var('Stock Diameter', 0, 'Minimum stock diameter', number, frozen=False)
stock_diameter.update(lathe.stock_radius * 2)
stock_diameter.freeze()

stock_length = var('Stock Length', 0, 'Minimum stock length', number, frozen=False)
stock_length.update(lathe.stock_length)
stock_length.freeze()

pi = 3.1415926535
cross_area = pi * (stock_diameter / 2) ** 2
stock_volume = cross_area * stock_length

# removal rates based on material in inches cubed per min
rates = {
    'Aluminum': 3.0,
    'Stainless Steel': 1.0,
    'Steel': 1.5,
    'Polymer': 4.0,
}

if part.material_family in rates:
    removal_rate = rates[part.material_family]
else:
    # assume worst case scenario
    removal_rate = 1.0

base_runtime = (stock_volume - part.volume) / removal_rate / 60

# adjust runtime based on presence of live tooling
count_live_holes = var('Live Tooling Holes', 0, 'Number of holes requiring live tooling', number, frozen=False)
count_live_holes.update(len(get_features(lathe, name='live_tooling_hole')))
count_live_holes.freeze()

count_live_cavities = var('Live Tooling Cavities', 0, 'Number of cavities requiring live tooling', number, frozen=False)
count_live_cavities.update(len(get_features(lathe, name='live_tooling_cavity')))
count_live_cavities.freeze()

count_live_protrusions = var('Live Tooling Protrusions', 0, 'Number of protrusions requiring live tooling', number, frozen=False)
count_live_protrusions.update(len(get_features(lathe, name='live_tooling_protrusion')))
count_live_protrusions.freeze()

runtime_per_live_feature = var('Live Feature Time', 60, 'number of seconds of runtime per live feature detected', number)

live_features = count_live_holes + count_live_cavities + count_live_protrusions
live_runtime = live_features * runtime_per_live_feature / 3600

runtime = var('runtime', 0, 'runtime in hours', number, frozen=False)
runtime.update(base_runtime + live_runtime)
runtime.freeze()

# setup time is just a base 30 minutes, but 1 hour if live tooling
setup_time = var('setup_time', 0, 'Setup time in hours', number, frozen=False)
if live_features > 0:
    setup_time.update(1.0)
else:
    setup_time.update(0.5)
setup_time.freeze()

hour_rate = var('Rate', 50, '$/hr for machine and setup time', currency)

PRICE = setup_time * hour_rate + runtime * part.qty * hour_rate
DAYS = 0