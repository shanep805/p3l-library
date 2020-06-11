# This operation describes how to price a 3D printer for a part that requires a dedicated build. This means that you
# will price the part as if each part will require its own build in the printer.
#
# Be sure to associate your 3D printer machine with this operation to have access to additive pricing features such as
# build area checks and orientation in the partviewer. Also be sure to populate important information about your printer
# like layer height and layer time.
#
# The part.size_z field corresponds to the height, and will update as you change orientation.
#
# When working with runtime or setup_time in your pricing formula, time will always be in hours.  The display units
# can be set on the operation level or when quoting.

units_in()
additive = analyze_additive()

machine_rate = var('Machine Rate', 0, '$/ hr', currency)
labor_rate = var('Labor Rate', 0, '$/ hr', currency)

setup_time = var('setup_time', 0, 'Setup time, specified in hours', number)
runtime = var('runtime', 0, 'Runtime, specified in hours', number, frozen=False)

# setup layer height and time per layer
layer_height = var('Layer Height (in)', 0, 'Height of each layer in inches', number)
layer_time = var('Layer Time (sec)', 0, 'Estimated average layer time in seconds', number)

# identify number of layers on part
part_layers = var('# of Layers', 0, 'Total # of layers', number, frozen=False)
if layer_height:
    part_layers.update(ceil(part.size_z / layer_height))
else:
    part_layers.update(0)
part_layers.freeze()

# runtime update
runtime.update((part_layers * layer_time) / 3600)
runtime.freeze()

setup_cost = setup_time * labor_rate
machine_usage_cost = runtime * machine_rate * part.qty
PRICE = setup_cost + machine_usage_cost

DAYS = 0
