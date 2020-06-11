# Tracks volume removal for called out features and applies a runtime per feature
# based on depth characteristics

units_in()
mill = analyze_mill3()

# create removal rate lookup tables based on material family, feature type, and depths
# units of cubic inches per minute
hole_removal_rates = {
    'Aluminum': {
        'shallow': 20,
        'deep': 7.5,
    },
    'Stainless Steel': {
        'shallow': 7,
        'deep': 2.5,
    },
    'Steel': {
        'shallow': 10,
        'deep': 3.75,
    },
}
countersink_removal_rates = {
    'Aluminum': {
        'shallow': 15,
        'deep': 5,
    },
    'Stainless Steel': {
        'shallow': 5,
        'deep': 2,
    },
    'Steel': {
        'shallow': 7,
        'deep': 3,
    },
}
circular_pocket_removal_rates = {
    'Aluminum': {
        'shallow': 15,
        'deep': 5,
    },
    'Stainless Steel': {
        'shallow': 5,
        'deep': 2,
    },
    'Steel': {
        'shallow': 10,
        'deep': 3,
    },
}
pocket_removal_rates = {
    'Aluminum': {
        'shallow': 13,
        'deep': 5,
    },
    'Stainless Steel': {
        'shallow': 4,
        'deep': 2,
    },
    'Steel': {
        'shallow': 8,
        'deep': 3,
    },
}

deep_hole_thresh = 8  # depth to diameter
deep_pocket_thresh = 3  # depth to tool diameter
# assume half inch tool diameter for roughing purposes
pocket_tool_diameter = 0.5
# if hole bottom type is obstructed or flat, we cannot use a drill bit, and will cut slower
# multiply runtime from these holes by a factor
obstructed_bottom_factor = 1.2
# if pocket has transition, apply a runtime muliplier
transition_multiplier = 1.4

if part.material_family in hole_removal_rates:
    hole_ref = hole_removal_rates[part.material_family]
    countersink_ref = countersink_removal_rates[part.material_family]
    circ_pocket_ref = circular_pocket_removal_rates[part.material_family]
    pocket_ref = pocket_removal_rates[part.material_family]
else:
    # if unknown material family, predict for worst case scenario
    hole_ref = hole_removal_rates['Stainless Steel']
    countersink_ref = countersink_removal_rates['Stainless Steel']
    circ_pocket_ref = circular_pocket_removal_rates['Stainless Steel']
    pocket_ref = pocket_removal_rates['Stainless Steel']

# establish tracking variables for hole and pocket runtime
hole_minutes = 0
pocket_minutes = 0
# tracking value for volume removed from features
tracked_volume = 0

for setup in get_setups(mill):
    # runtime logic for simple holes
    for simple_hole in get_features(setup, name='machined_simple_hole'):
        tracked_volume += simple_hole.properties.volume
        depth_ratio = simple_hole.properties.depth / simple_hole.properties.diameter
        is_deep_hole = depth_ratio > deep_hole_thresh or is_close(depth_ratio, deep_hole_thresh)
        if is_deep_hole:
            base_runtime = simple_hole.properties.volume / hole_ref['deep']
        else:
            base_runtime = simple_hole.properties.volume / hole_ref['shallow']

        # now based on bottom type, apply multiplier
        if simple_hole.properties.bottom_type == 'flat' or simple_hole.properties.bottom_type == 'obstructed':
            base_runtime *= obstructed_bottom_factor

        # now add to total runtime tracker
        hole_minutes += base_runtime

    # runtime logic for counterbores, which by definition, are simple holes with obstructed bottom types
    for counterbore in get_features(setup, name='machined_counter_bore'):
        tracked_volume += counterbore.properties.volume
        depth_ratio = counterbore.properties.depth / counterbore.properties.diameter
        is_deep_hole = depth_ratio > deep_hole_thresh or is_close(depth_ratio, deep_hole_thresh)
        if is_deep_hole:
            base_runtime = counterbore.properties.volume / hole_ref['deep']
        else:
            base_runtime = counterbore.properties.volume / hole_ref['shallow']

        # since we know by definition counterbores have obstructed bottoms, multiply by factor
        base_runtime *= obstructed_bottom_factor

        # now add to total runtime tracker
        hole_minutes += base_runtime

    # runtime logic for countersinks
    for countersink in get_features(setup, name='machined_counter_sink'):
        tracked_volume += countersink.properties.volume
        depth_ratio = countersink.properties.depth / countersink.properties.major_diameter
        is_deep_hole = depth_ratio > deep_hole_thresh or is_close(depth_ratio, deep_hole_thresh)
        if is_deep_hole:
            hole_minutes += countersink.properties.volume / countersink_ref['deep']
        else:
            hole_minutes += countersink.properties.volume / countersink_ref['shallow']

    # runtime logic for circular pockets
    for circ_pocket in get_features(setup, name='circular_pocket'):
        tracked_volume += circ_pocket.properties.volume
        depth_ratio = circ_pocket.properties.depth / pocket_tool_diameter
        is_deep_pocket = depth_ratio > deep_pocket_thresh or is_close(depth_ratio, deep_pocket_thresh)
        if is_deep_pocket:
            pocket_minutes += circ_pocket.properties.volume / circ_pocket_ref['deep']
        else:
            pocket_minutes += circ_pocket.properties.volume / circ_pocket_ref['shallow']

    # runtime logic for pockets
    for pocket in get_features(setup, name='pocket'):
        tracked_volume += pocket.properties.volume
        depth_ratio = pocket.properties.max_depth / pocket_tool_diameter
        is_deep_pocket = depth_ratio > deep_pocket_thresh or is_close(depth_ratio, deep_pocket_thresh)
        if is_deep_pocket:
            base_runtime = pocket.properties.volume / pocket_ref['deep']
        else:
            base_runtime = pocket.properties.volume / pocket_ref['shallow']

        # if pocket has transition, apply runtime multiplier
        if pocket.properties.has_transition:
            base_runtime *= transition_multiplier

        # now add to total runtime tracking
        pocket_minutes += base_runtime

# create dynamic variables and freeze them for operation overrides
hole_runtime = var('Hole Runtime', 0, 'Minutes of runtime for holes', number, frozen=False)
pocket_runtime = var('Pocket Runtime', 0, 'Minutes of runtime for pockets', number, frozen=False)
hole_runtime.update(round(hole_minutes, 3))
pocket_runtime.update(round(pocket_minutes, 3))
hole_runtime.freeze()
pocket_runtime.freeze()

# now resolve volume that has not been tracked with features
# bounding box volume minus part volume to get total required volume removal
# untracked volume difference between required and tracked
bbox_vol = part.size_x * part.size_y * part.size_z
required_total_volume_removal = bbox_vol - part.volume or 1
untracked_volume = required_total_volume_removal - tracked_volume
# make a dynamic variable for untracked volume percentage so
# you can have it as a reference at quote_time
untracked_vol_percentage = var('Untracked Vol %', 0, 'Percentage of volume not tracked with feature iteration', number, frozen=False)
untracked_vol_percentage.update(round(untracked_volume / required_total_volume_removal * 100, 2))
untracked_vol_percentage.freeze()

# now apply a leftover volume removal rate on untracked volume based on material family
# in inches/minute
leftover_volume_removal_rate = {
    'Aluminum': 5,
    'Stainless Steel': 2,
    'Steel': 3,
}
if part.material_family in leftover_volume_removal_rate:
    leftover_rate = leftover_volume_removal_rate[part.material_family]
else:
    leftover_rate = leftover_volume_removal_rate['Stainless Steel']

untracked_runtime = var('Untracked RT', 0, 'Runtime of untracked volume removal', number, frozen=False)
untracked_runtime.update(round(untracked_volume / leftover_rate, 3))
untracked_runtime.freeze()

# define total runtime and setup_time variables for operation overriding
runtime = var('runtime', 0, 'Runtime in hours', number, frozen=False)
runtime.update((pocket_runtime + hole_runtime + untracked_runtime) / 60)
runtime.freeze()

# just a basic 30 minute setup time, does not need to be dynamic because its just a constant
setup_time = var('setup_time', 0.5, 'Setup time in hours', number)

# define setup and machine rates to come up with a price
setup_rate = var('Setup rate', 80, '$/hr', currency)
machine_rate = var('Machine rate', 35, '$/hr', currency)

PRICE = setup_rate * setup_time + runtime * part.qty * machine_rate
DAYS = 0