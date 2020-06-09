units_in()
sheet_metal = analyze_sheet_metal()

if part.material:
    set_operation_name(part.material)

size_buffer = var('X-Y Buffer', 0.125, 'Buffer in inches for each part', number)
size_x = var('Size X', 0, 'Size of part in x direction', number, frozen=False)
size_x.update(sheet_metal.size_x + size_buffer)
size_x.freeze()
size_y = var('Size Y', 0, 'Size of part in y direction', number, frozen=False)
size_y.update(sheet_metal.size_y + size_buffer)
size_y.freeze()

max_dim = max(size_x, size_y)
min_dim = min(size_x, size_y)

# find x and y min blank size quadrants
if min_dim < 12:
    min_x = 12
elif 12 <= min_dim < 24:
    min_x = 24
elif 24 <= min_dim < 48:
    min_x = 48
else:
    min_x = min_dim
    # part size is too big, so we no quote it
    no_quote()

minimum_x = var('Minimum Short Dim', 0, 'Minimum shorter dimension for sheet quadrant', number, frozen=False)
minimum_x.update(min_x)
minimum_x.freeze()

# find x and y min blank size quadrants
if max_dim < 12:
    min_y = 12
elif 12 <= max_dim < 24:
    min_y = 24
elif 24 <= max_dim < 48:
    min_y = 48
elif 48 <= max_dim < 96:
    min_y = 96
else:
    min_y = max_dim
    # part size is too big, so we no quote it
    no_quote()

minimum_y = var('Minimum Long Dim', 0, 'Minimum longer dimension for sheet quadrant', number, frozen=False)
minimum_y.update(min_y)
minimum_y.freeze()

mat_cost = var('Mat Cost Per Sq In', 0, 'Material cost per square inch', currency, frozen=False)
mat_cost.update(part.mat_cost_per_area)
mat_cost.freeze()

# track up the width and length breaks until we satisfy quantity
if minimum_x < 12 and minimum_y < 12 and floor(12 / min_dim) * floor(12 / max_dim) >= part.qty:
    blank_size = 12 * 12
    blank_count = 1
elif minimum_x < 12 and minimum_y < 24 and floor(12 / min_dim) * floor(24 / max_dim) >= part.qty:
    blank_size = 12 * 24
    blank_count = 1
elif minimum_x < 24 and minimum_y < 24 and floor(24 / min_dim) * floor(24 / max_dim) >= part.qty:
    blank_size = 24 * 24
    blank_count = 1
elif minimum_x < 24 and minimum_y < 48 and floor(24 / min_dim) * floor(48 / max_dim) >= part.qty:
    blank_size = 24 * 48
    blank_count = 1
elif minimum_x < 48 and minimum_y < 48 and floor(48 / min_dim) * floor(48 / max_dim) >= part.qty:
    blank_size = 48 * 48
    blank_count = 1
elif minimum_x < 48 and minimum_y < 96 and floor(48 / min_dim) * floor(96 / max_dim) >= part.qty:
    blank_size = 48 * 96
    blank_count = 1
else:
    blank_size = 48 * 96
    blank_count = ceil(floor(48 / min_dim) * floor(96 / max_dim) / part.qty)

PRICE = blank_size * blank_count * mat_cost
DAYS = 0

set_workpiece_value('mat_sq_ft', blank_size / 144.0 * blank_count)
set_workpiece_value('blank_size', blank_size / 144.0)

