# This prices material based on a cost per square inch price. It calls the sheet metal analysis
# to unfold the part to get the true x and y extents of the unfolded part. It then calculates price
# from an inputted value of price per square inch.
# It references a custom table with the name cost_per_area with column names material_family, thickness, cost_per_area
# You will have to setup a custom table with matching column names to get this formula to compile

units_in()
sm = analyze_sheet_metal()

if part.material:
    set_operation_name(part.material)

thickness = var('Part Thickness, in', 0, '', number, frozen=False)
thickness.update(sm.thickness)
thickness.freeze()

row = table_var(
  'Sq In Pricing',
  'Looking up to table for square inch pricing based on material family',
  'cost_per_area',
  create_filter(
    filter('material_family', '=', part.material_family),
    filter('thickness', '>', thickness),
  ),
  create_order_by('thickness', 'cost_per_area'),
  'cost_per_area'
)

price_per_sq_inch = var('Price Per Square Inch', 0, '', currency, frozen=False)
if row:
    price_per_sq_inch.update(row.cost_per_area)
price_per_sq_inch.freeze()

material_buffer = var('Material Buffer, in', 0.125, 'Buffer in each dimension around part on sheet', number)

part_length = var('Part Length, in', 0, 'Longest dimension of part', number, frozen=False)
part_length.update(max(sm.size_x, sm.size_y))
part_length.freeze()

part_width = var('Part Width, in', 0, 'Width of part', number, frozen=False)
part_width.update(min(sm.size_x, sm.size_y))
part_width.freeze()

PRICE = price_per_sq_inch * (part_width + material_buffer) * (part_length + material_buffer) * part.qty
# part.mat_added_lead_time is specified in process material setup, defaults to 0
DAYS = part.mat_added_lead_time
