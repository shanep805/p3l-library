units_in()
sm = analyze_sheet_metal()

if part.material:
    set_operation_name(part.material)

part_thickness = var('Part Thickness, in', 0, '', number, frozen=False)
part_thickness.update(sm.thickness)
part_thickness.freeze()

set_workpiece_value('thickness', part_thickness)

part_length = var('Part Length, in', 0, 'Longest dimension of part', number, frozen=False)
part_length.update(max(sm.size_x, sm.size_y))
part_length.freeze()

set_workpiece_value('flat_length', part_length)

part_width = var('Part Width, in', 0, 'Width of part', number, frozen=False)
part_width.update(min(sm.size_x, sm.size_y))
part_width.freeze()

set_workpiece_value('flat_width', part_width)

# collect part weight, for workpiece purposes
# estimate weight for print case
est_weight = part_thickness * part_length * part_width * part.density

part_weight = var('Part Weight', 0, '', number, frozen=False)
part_weight.update(part.weight or est_weight)
part_weight.freeze()

set_workpiece_value('weight', part_weight)

material_buffer = var('Material Buffer, in', 0.125, 'Buffer in each dimension around part on sheet', number)

row = table_var(
  'Sheet Selection',
  'Lookup for dynamic sheet stock selection',
  'sheet_lookup',
  create_filter(
    filter('material', '=', part.global_material),
    filter('thickness', 'range', create_range(part_thickness - 0.01, part_thickness + 0.01)),
    filter('length', '>=', part_length + material_buffer),
    filter('width', '>=', part_width + material_buffer),
  ),
  create_order_by('thickness', '-length', '-width', 'sheet_cost'),
  'display',
)

sheet_length = var('Sheet Length, in', 96, 'Longer dimension of sheet in inches', number, frozen=False)
sheet_width = var('Sheet Width, in', 48, 'Shorter dimension of sheet in inches', number, frozen=False)
price_per_sheet = var('Price Per Sheet', 0, '', currency, frozen=False)

if row:
  sheet_length.update(row.length)
  sheet_width.update(row.width)
  price_per_sheet.update(row.sheet_cost)
sheet_length.freeze()
sheet_width.freeze()
price_per_sheet.freeze()

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
DAYS = 0
