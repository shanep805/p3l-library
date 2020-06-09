# Prices material on a per sheet basis. Based on a parts greatest two dimensions and an
# inputted sheet width and sheet length, this operation calculates how many sheets you need
# to fulfill a make quantity. This calculated value can be overridden at quote time if needed
# The price is then generated based on an inputted price per sheet.
# We call analyze_sheet_metal to get the unfolded dimensions of the part

units_in()
sm = analyze_sheet_metal()

if part.material:
    set_operation_name(part.material)

part_thickness = var('Part Thickness, in', 0, '', number, frozen=False)
part_thickness.update(sm.thickness)
part_thickness.freeze()

price_per_sheet = var('Price Per Sheet', 0, '', currency)
sheet_length = var('Sheet Length, in', 96, 'Longer dimension of sheet in inches', number)
sheet_width = var('Sheet Width, in', 48, 'Shorter dimension of sheet in inches', number)

part_length = var('Part Length, in', 0, 'Longest dimension of part', number, frozen=False)
part_length.update(max(sm.size_x, sm.size_y))
part_length.freeze()

part_width = var('Part Width, in', 0, 'Width of part', number, frozen=False)
part_width.update(min(sm.size_x, sm.size_y))
part_width.freeze()

material_buffer = var('Material Buffer, in', 0.125, 'Buffer in each dimension around part on sheet', number)

length = max(sheet_length, sheet_width)
width = min(sheet_length, sheet_width)

parts_per_sheet = var('Parts Per Sheet', 0, '', number, frozen=False)
if part_length > length or part_width > width:
    parts_per_sheet.update(0)
else:
    buffered_length = part_length + material_buffer
    buffered_width = part_width + material_buffer
    length_fit_count = floor(length / buffered_length)
    width_fit_count = floor(width / buffered_width)
    parts_per_sheet.update(width_fit_count * length_fit_count)
parts_per_sheet.freeze()

if parts_per_sheet > 0:
    sheets = ceil(part.qty / parts_per_sheet)
else:
    sheets = 1

PRICE = price_per_sheet * sheets
# part.mat_added_lead_time is specified in process material setup, defaults to 0
DAYS = part.mat_added_lead_time
