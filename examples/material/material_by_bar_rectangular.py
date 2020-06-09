# This prices material based on a parts per bar model, where you enter in the price per bar at quote time.
# Assumes a rectangular cross section bar.

units_in()

if part.material:
    set_operation_name(part.material)

price_per_bar = var('Price Per Bar', 0, 'Input Price for Below Bar Size', currency)
bar_length = var('Bar Length, in', 96, '', number)

part_length = var('Part Length, in', 0, '', number, frozen=False)
part_length.update(max(part.size_x, part.size_y, part.size_z))
part_length.freeze()

cutoff = var('Cutoff, in', 0.125, '', number)
facing = var('Facing, in', 0, '', number)

bar_end = var('Bar End, in', 0, 'Length of bar allocated for holding', number)

# required bars
parts_per_bar = var('Parts Per Bar', 0, '', number, frozen=False)
parts_per_bar.update(floor((bar_length - bar_end) / (part_length + cutoff + facing)))
parts_per_bar.freeze()
if parts_per_bar > 0:
    bars = ceil(part.qty / parts_per_bar)
else:
    bars = 1

PRICE = price_per_bar * bars
# part.mat_added_lead_time is specified in process material setup, defaults to 0
DAYS = part.mat_added_lead_time
