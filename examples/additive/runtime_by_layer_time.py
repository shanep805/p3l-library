units_mm()
additive = analyze_additive()

#shop rates
machine_rate = var('Machine Rate', 100, '$/ hr', currency)
labor_rate = var('Labor Rate', 85, '$/ hr', currency)

#declare default setup and runtime
setup_time = var('setup_time', 0.25, 'setup time, hr', number)
runtime = var('runtime', 0, 'runtime, hr', number, frozen=False)

#setup layer height and time per layer
layer_height = var('Layer Height, mm', 0.08, 'Height of each layer in mm', number)
layer_time = var('Layer Time, sec', 100, 'Layer time, seconds', number)

buffer = var('Buffer, mm', 6.35,'Buffer around part, mm', number)
volume_full_tray = var('Build Volume', 41295401, 'mm^3', number) # dimensions of full tray in inches

#identify number of layers on part
part_layers = var('# of Layers', 0, 'Total # of layers', number, frozen=False)
part_layers.update(ceil(part.size_z / layer_height))
part_layers.freeze()

#calculate % of build is part
volume_part_bbox = (part.size_x + buffer) * (part.size_y + buffer) * (part.size_z + buffer) #volume of part based on bounding box

use_packed_build = var('Use Packed Build', 1, '0 or 1 to assume packed build', number)

#runtime update
#Runtime is the based on total full tray runtime up to z-height of part * % of part bounding box volume
if use_packed_build:
  runtime.update((part_layers * layer_time) / 3600 * (volume_part_bbox / volume_full_tray))
else:
  runtime.update((part_layers * layer_time) / 3600)
runtime.freeze()

PRICE = setup_time * labor_rate + runtime * machine_rate * part.qty
DAYS = 0