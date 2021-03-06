# A - Geometric Definitions
# A.1 - Set units
units_in()
# A.2 - Set our geometric interrogation.
# Read more here: https://help.paperlessparts.com/article/42-p3l-language-features
lathe = analyze_lathe()

# B - Part Variables
# B.1 - Set Turning Radius, Turning Length, Radial Buffer, Length Buffer, Part Volume, and Stock Volume
turning_radius = var('Turning Radius', 0, 'Outermost radius of part in inches', number, frozen=False)
turning_length = var('Turning Length', 0, 'Length of part along turning axis in inches', number, frozen=False)
radial_buffer = var('Radial Stock Buffer, in', 0.0625, 'Buffer applied to the outer radius of part in inches', number)
length_buffer = var('Length Stock Buffer, in', 0.125, 'Buffer to the length of the part along the turning axis in inches', number)
stock_volume = var('Stock Volume (in^3)', 0, '', number, frozen = False)
part_volume = var('Part Volume', 0, '', number, frozen = False)
volume_removed = var('Volume Removed (in^3)', 0, '', number, frozen = False)
percent_volume_removed = var('Percent Volume Removed (%)', 0, '', number, frozen = False)

# B.2 - Update variables based on interrogated values
turning_radius.update(lathe.stock_radius)
turning_radius.freeze()
turning_length.update(lathe.stock_length)
turning_length.freeze()

stock_radius = turning_radius + radial_buffer
stock_length = turning_length + length_buffer

part_volume.update(round(part.volume, 3))
part_volume.freeze()
stock_volume.update(round(stock_radius**2 * 3.1415926535 * turning_length, 3))
stock_volume.freeze()

# C - Project Variables
# C.1 Define Features
labor_rate = var('Labor Rate ($)', 0, '', currency)
features = var('Feature Count', 0, '', number, frozen=False)
setup_time_per_setup = var('Setup Time Per Setup', 0.5, 'Setup time per setup in hours', number)
setup_count = var('Setup Count', 0, '', number, frozen = False)
setup_time = var('setup_time', 0, 'Setup time, specified in hours', number, frozen = False)

setup_count.update(lathe.setup_count)
setup_count.freeze()
setup_time.update(setup_count * setup_time_per_setup)
setup_time.freeze()

# C.2 - Gather Features and Feedback Count
feature_count = len(get_features(lathe))
feedback_count = len(get_feedback(lathe))
features.update(feature_count + feedback_count)
features.freeze()

# C.3 - Define number of tools required based on Feature and Feedback count. The default number of features per tool is 4
num_tools = var('Number of Tools', 0, '', number, frozen=False)
num_tools.update(ceil(features / 4))
num_tools.freeze()

# D - Runtime Estimates
# D.1 - Set Removal Rate, Volume Cut Rate, Volume Removed, Runtime, Runtime per Setup and Runtime Multiplier variables
removal_rate = var('Material Removal Rate', 1, 'Material removal rate in cu.in./min', number, frozen = False)
vol_cut_rate = var('Volume Cut Rate (in^3 / hr)', 0, '', number, frozen = False)
runtime = var('runtime', 0, 'Runtime, specified in hours', number, frozen=False)
runtime_per_setup = var('Runtime per Setup (min)', 2, '', number)
runtime_mult = var('Runtime Multiplier', 1, '', number, frozen = False)

# D.2 - Update our Runtime Multiplier depending on which material family we use.
if part.material_family == 'Aluminum':
  runtime_mult.update(1)
elif 'Steel' in part.material_family:
  runtime_mult.update(1.5)
elif part.material_family == 'Titanium':
  runtime_mult.update(2)
else:
    runtime_mult.update(1)
runtime_mult.freeze()

# D.3 - Update Volume Removed based on interrogated values
volume_removed.update(round(stock_volume - part.volume, 3))
volume_removed.freeze()

percent_volume_removed.update(round((volume_removed / stock_volume) * 100, 2))
percent_volume_removed.freeze()

# D.4 - Update Removal Rate based on total volume removed
if volume_removed <= 1:
  removal_rate.update(0.50 / runtime_mult)
elif 1 < volume_removed <= 9:
  removal_rate.update(1 / runtime_mult)
elif 9 < volume_removed <= 16:
  removal_rate.update(1.5 / runtime_mult)
elif 16 < volume_removed:
  removal_rate.update(2 / runtime_mult)
removal_rate.freeze()

# D.5 - Update Volume Cut Rate based on removal rate - defined in cubic inches per hour
vol_cut_rate.update(70 * removal_rate)
vol_cut_rate.freeze()

# D.6 Set the 'Runtime Per Tool' - how long does it take for the typical tool change to occur?
tool_rate = var('Runtime Per Tool (seconds)', 15, '', number)
tool_runtime = var('Tool Runtime (minutes)', 0, '', number, frozen=False)
tool_runtime.update((tool_rate * num_tools) / 60)
tool_runtime.freeze()

# D.7 - Calculate estimated runtime based on defined variables. To set a minimum runtime, use (max(1/6, calculations...).
runtime.update((stock_volume / vol_cut_rate)								# A - Calculate our runtime estimate by dividing the total volume removed by our defined removal rate.
                + (get_workpiece_value('Tool Runtime', 0) / 60) 			# B - Add Tool Runtime, calculated in our Critical Information operation.
                + ((runtime_per_setup / 60) * setup_count))					# C - Add Setup Runtime.
runtime.freeze()

# E - Compile Calculations
# E.1 - Compile Cycle and Setup Costs
total_cycle_cost = part.qty * runtime * labor_rate
setup_cost = setup_time * labor_rate

# E.2 - Compile our total costs
PRICE = setup_cost + total_cycle_cost

# E.3 - Define how many days this operation will contribute to the project lead time.
DAYS = 0

# F - Workpiece Values
# F.1 - Set workpiece values to be used in subsequent operations.
set_workpiece_value('total_setup_time', get_workpiece_value('total_setup_time', 0) + setup_time)			# A - Cumulative project setup time
set_workpiece_value('total_runtime', get_workpiece_value('total_runtime', 0) + runtime)						# B - Cumulative project runtime
