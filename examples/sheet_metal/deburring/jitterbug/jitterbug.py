# Collects a deburring runtime by grabbing cut length and applying a length/time rate inches per second

units_in()
sheet_metal = analyze_sheet_metal()

setup_time = var('setup_time', 0.1, 'Setup time in hours', number)
runtime = var('runtime', 0, 'Runtime in hours', number, frozen=False)

deburr_rate = var('Deburr In/Sec', 1.0, 'inches/second', number)

cut_length = var('Cut Length', 0, 'Cut length', number, frozen=False)
cut_length.update(sheet_metal.total_cut_length)
cut_length.freeze()

runtime.update(edge_run / 3600)
runtime.freeze()

rate = var('Rate', 100, '$/hr', currency)

PRICE = rate * setup_time + rate * runtime * part.qty
DAYS = 0