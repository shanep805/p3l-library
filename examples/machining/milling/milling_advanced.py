## A - Geometric Definitions
## A.1 - Set units
units_in()
## A.2 - Set our geometric interrogation. We will the values associated with this interrogation in subsequent variables. Read more here: https://help.paperlessparts.com/article/42-p3l-language-features
mill = analyze_mill3()

## -------------------------------------------------------------------------------------------------------------------- ##

## B - Part Dimensions
## B.1 - Get part dimensions
min_size = min(part.size_x, part.size_y, part.size_z)
max_size = max(part.size_x, part.size_y, part.size_z)
med_size = median(part.size_x, part.size_y, part.size_z)

## B.2 - Set the buffer to apply to the part bounding box
buffer = var('Stock Buffer, in', 0.25, 'Buffer to apply to part for when using material removal rate', number)

## B.3 - Update the dimensions to accommodate the buffer
size_x = max_size + buffer
size_y = med_size + buffer
size_z = min_size + buffer

## -------------------------------------------------------------------------------------------------------------------- ##

## C. Geometrically Driven Definitions
## C.1 Define the part's Feature Count, Bounding Box, Volume, Volume Removed, and Percent Volume Removed
features = var('Feature Count', 0, '', number, frozen=False)
bbox = var('Bounding Box Volume (in^3)', 1, '', number, frozen=False)
volume = var('Part Volume (in^3)', 0, '', number, frozen=False)
volume_removed = var('Volume Removed (in^3)', 0, '', number, frozen=False)
percent_volume_removed = var('Percent Volume Removed (%)', 0, '', number, frozen = False)

## C.2 - Gather Features and Feedback Count
feature_count = 0
feedback_count = 0

for setup in get_setups(mill):
    feature_count += (len(get_features(setup)) - len(get_features(setup, name='hole')))
    feedback_count += (len(get_feedback(setup)))

## C.3 - Update variables based on part values
bbox.update(round((part.size_x + buffer) * (part.size_y + buffer) * (part.size_z + buffer), 3))
bbox.freeze()
volume.update(round(part.volume, 3))
volume.freeze()
volume_removed.update(round(bbox - part.volume, 3))
volume_removed.freeze()
percent_volume_removed.update(round((volume_removed / bbox) * 100, 2))
percent_volume_removed.freeze()
features.update(feature_count + feedback_count)
features.freeze()

## C.4 - Define number of tools required based on Feature and Feedback count. The default number of features per tool is 4
num_tools = var('Number of Tools', 0, '', number, frozen=False)
num_tools.update(ceil(features / 4))
num_tools.freeze()

## C.5 Set the 'Runtime Per Tool' - how long does it take for the typical tool change to occur?
tool_rate = var('Runtime Per Tool (seconds)', 15, '', number)
tool_runtime = var('Tool Runtime (minutes)', 0, '', number, frozen=False)
tool_runtime.update((tool_rate * num_tools) / 60)
tool_runtime.freeze()

## -------------------------------------------------------------------------------------------------------------------- ##

## D. Removal Rates
## D.1 - Define Removal Rate and Runtime Multiplier Variables
removal_rate = var('Material Removal Rate (in^3)', 0, 'Material removal rate in cu.in./min', number, frozen=False)
runtime_mult = var('Runtime Multiplier', 1, '', number, frozen = False)

## D.2 - Update our Runtime Multiplier depending on which material family we use. The higher the runtime multiplier, the more difficult the material is to remove. Note that by using part.material, we are simply looking to see if the respective word (e.g. 'Aluminum' or 'Stainless Steel') appears in the material name. This is a different qualifying tactic than using part.material_family.
if part.material_family == 'Aluminum':
  runtime_mult.update(1)
elif 'Steel' in part.material_family:
  runtime_mult.update(1.5)
elif part.material_family == 'Titanium':
  runtime_mult.update(2)
else:
    runtime_mult.update(1)
runtime_mult.freeze()

## D.3 - Update our removal rate based on the amount of material (volume) that is being removed.
if volume_removed <= 1:
    removal_rate.update(round(0.25 / runtime_mult, 2))
elif 1 < volume_removed <= 9:
    removal_rate.update(round(0.5 / runtime_mult, 2))
elif 9 < volume_removed <= 16:
    removal_rate.update(round(0.75 / runtime_mult, 2))
elif 16 < volume_removed:
    removal_rate.update(round(1 / runtime_mult, 2))
removal_rate.freeze()

## -------------------------------------------------------------------------------------------------------------------- ##

## E - Setup Time Calculations
## E.1 - Define Setup Time Per Setup, Setup Count, and Setup Time
setup_time_per_setup = var('Setup Time Per Setup', 0.5, 'Setup time per setup in hours', number)
setup_count = var('Setup Count', 0, '', number, frozen=False)
setup_time = var('setup_time', 0, 'Setup time, specified in hours', number, frozen=False)

## E.2 - Update Setup Count based on geometric interrogation.
setup_count.update(mill.setup_count)
setup_count.freeze()

## E.3 - Update the Setup Time based on Setup Count
setup_time.update(setup_count * setup_time_per_setup)
setup_time.freeze()

## E.4 - Define Runtime Per Setup. This is the time it takes to adjust the setup while machining. Will contribute to our runtime estimate.
runtime_per_setup = var('Runtime Per Setup (min)', 2, '', number)

## -------------------------------------------------------------------------------------------------------------------- ##

## F - Runtime Calculations
## F.1 - Define Runtime
runtime = var('runtime', 0, 'Runtime per part, specified in hours', number, frozen=False)

## F.2 - Update Runtime based on defined calculations. To set a minimum runtime, use (max(1/6, calculations...).
runtime.update(((bbox - part.volume) / removal_rate / 60) 				## A - Calculate our runtime estimate by dividing the total volume removed by our defined removal rate. Divide by 60 to get our units into minutes.
               + (tool_runtime / 60) 									## B - Add Tool Runtime, calculated in our Critical Information operation.
               + (setup_count * (runtime_per_setup / 60)))				## C - Add Setup Runtime.
runtime.freeze()

## -------------------------------------------------------------------------------------------------------------------- ##

## G. - Costs
## G.1 - Define Labor Rate
labor_rate = var('Labor Rate ($)', 65, '', currency, frozen = False)

## B - Update Labor Rate based on global labor rate. To not use the global labor rate, simply do not use a dynamic variable.
labor_rate.update(get_custom_attribute('labor_rate', 0))
labor_rate.freeze()

## G.3 - Calculate Total Cycle Cost and Setup Cost
total_cycle_cost = part.qty * runtime * labor_rate
setup_cost = setup_time * labor_rate

## -------------------------------------------------------------------------------------------------------------------- ##

## H - Final Calculations
## H.1 Compile our costs
PRICE = setup_cost + total_cycle_cost

## H.2 - Define how many days this operation will contribute to the project lead time.
DAYS = 0

## -------------------------------------------------------------------------------------------------------------------- ##

## I - Workpiece Values
## I.1 - Set workpiece values to be used in subsequent operations.
set_workpiece_value('Total Setup Time', get_workpiece_value('Total Setup Time', 0) + setup_time)			## A - Cumulative project setup time
set_workpiece_value('Total Runtime', get_workpiece_value('Total Runtime', 0) + runtime)						## B - Cumulative project runtime
set_workpiece_value('Operation Count', get_workpiece_value('Operation Count', 0) + 1)						## C - Cumulative operation count