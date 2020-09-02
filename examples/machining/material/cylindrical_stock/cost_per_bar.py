# A - Geometric Definitions
# A.1 - Set units
units_in()
# A.2 - Set our geometric interrogation.
# Read more here: https://help.paperlessparts.com/article/42-p3l-language-features
lathe = analyze_lathe()

# B - Bar Variables
# B.1 - Define Bar Variables
price_per_bar = var('Price Per Bar', 0, '', currency)
bar_length = var('Bar Length, in', 96, '', number)
length_buffer = var('Length Buffer (in)', 0.125, 'Buffer in inches for length of raw material size', number)
cutoff = var('Cutoff, in', 0.125, '', number)
facing = var('Facing, in', 0, '', number)
bar_end = var('Bar End, in', 0, 'Length of bar allocated for holding', number)
parts_per_bar = var('Parts Per Bar', 0, '', number, frozen=False)

# C - Geometric Calculations
# C.1 - Define Part Length Variable
part_length = var('Part Length, in', 0, '', number, frozen=False)

# C.2 - Update Part Length based on interrogation
part_length.update(lathe.stock_length)
part_length.freeze()

stock_length = part_length + length_buffer

# C.3 - Update Parts Per Bar based on Bar Length and Part Length
parts_per_bar.update(floor((bar_length - bar_end) / (stock_length + cutoff + facing)))
parts_per_bar.freeze()
if parts_per_bar > 0:
    bars = ceil(part.qty / parts_per_bar)
else:
    bars = 1

# D - Final Calculations
# D.1 - Compile our costs. This pricing scales and updates the requiered bars for each respective quantity break.
PRICE = price_per_bar * bars

# D.2 - Define how many days this operation will contribute to the project lead time. Uses the added lead time from the Materials Page in Processes. Defaults to 0 if no value found.
DAYS = part.mat_added_lead_time