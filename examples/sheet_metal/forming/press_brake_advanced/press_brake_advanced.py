# collects bend runtime and bend setup time based on the characteristics of bends in the part
# there is a base bend runtime and setup time, and based on things like angle, length, radius
# the times will increment. Difficulty points will multiply runtime increments

units_in()
sheet_metal = analyze_sheet_metal()

setup_time = var('setup_time', 0, 'Setup time in hours', number, frozen=False)
runtime = var('runtime', 0, 'Runtime in hours', number, frozen=False)

thickness = var('Thickness', 0, 'thickness of sheet metal part', number, frozen=False)
thickness.update(get_workpiece_value('thickness', sheet_metal.thickness))
thickness.freeze()

# perform lookup to bend table to get threshold and time values
row = table_var(
  'Bend Table Lookup',
  'Extracting setup and runtime values for thickness and material family',
  'bend_table',
  create_filter(
    filter('material_family', '=', part.material_family),
    filter('thickness', '<=', thickness),
  ),
  create_order_by('-thickness'),
  'base_runtime',
)

# establish base setup time and time increments in minutes
base_bend_setup_time = var('Base Bend Setup Time', 5, 'Base setup time in minutes for each bend', number, frozen=False)
st_increment = var('Setup Time Increment', 2.5, 'Setup time increment in minutes for each difficulty point', number, frozen=False)

# establish base runtime and time increments in seconds
base_bend_runtime = var('Base Bend Runtime', 30, 'Base runtime in seconds for each bend', number, frozen=False)
rt_increment = var('Runtime Increment', 2.5, 'Runtime increment in seconds for each difficulty point', number, frozen=False)

# establish geometric thresholds for incrementing times
# in inches
medium_radius_thresh = var('Medium Radius Thresh', 2.0, 'Threshold in inches for bend radius being +1 difficulty point', number, frozen=False)
large_radius_thresh = var('Large Radius Thresh', 4.0, 'Threshold in inches for bend radius being +2 difficulty points', number, frozen=False)
medium_length_thresh = var('Medium Length Thresh', 20.0, 'Threshold in inches for bend length being +1 difficulty point', number, frozen=False)
large_length_thresh = var('Medium Length Thresh', 40.0, 'Threshold in inches for bend length being +2 difficulty points', number, frozen=False)

if row:
  base_bend_setup_time.update(row.base_setup_time)
  st_increment.update(row.setup_time_increment)
  base_bend_runtime.update(row.base_runtime)
  rt_increment.update(row.runtime_increment)
  medium_radius_thresh.update(row.large_radii_thresh1)
  large_radius_thresh.update(row.large_radii_thresh2)
  medium_length_thresh.update(row.long_bend_thresh1)
  large_length_thresh.update(row.long_bend_thresh2)
base_bend_setup_time.freeze()
st_increment.freeze()
base_bend_runtime.freeze()
rt_increment.freeze()
medium_radius_thresh.freeze()
large_radius_thresh.freeze()
medium_length_thresh.freeze()
large_length_thresh.freeze()

# establish our variables that we will use as pricing levers in the operation
# also establish their local tracking variables
base_bend_count = var('Total Bends', 0, 'Number of bends detected', number, frozen=False)
bbc = 0
non_ninety_bends = var('Non-90 Bends', 0, 'Number of non-90 degree bends', number, frozen=False)
nnb = 0
med_rads = var('Med Rad Bends', 0, 'Number of bends with medium rads', number, frozen=False)
mr = 0
large_rads = var('Large Rad Bends', 0, 'Number of bends with large rads', number, frozen=False)
lr = 0
med_lengths = var('Med Length Bends', 0, 'Number of bends with medium length', number, frozen=False)
ml = 0
large_lengths = var('Large Length Bends', 0, 'Number of bends with large length', number, frozen=False)
ll = 0

# first track standard bends
for bend in get_features(sheet_metal, name='bend'):
    # increment bend count variable
    bbc += 1

    # increment for angle if necessary
    if not is_close(bend.properties.angle, 90):
        nnb += 1

    # if radius is medium or large, increment
    r = bend.properties.radius
    is_rad_medium = medium_radius_thresh <= r < large_radius_thresh or is_close(r, medium_radius_thresh)
    is_rad_large = r >= large_radius_thresh or is_close(r, large_radius_thresh)
    if is_rad_medium:
        mr += 1
    elif is_rad_large:
        lr += 1

    l = bend.properties.length
    is_length_medium = medium_length_thresh <= l < large_length_thresh or is_close(l, medium_length_thresh)
    is_length_large = l >= large_length_thresh or is_close(l, large_length_thresh)
    if is_length_medium:
        ml += 1
    elif is_length_large:
        ll += 1

# track open_hems as standard bends
for bend in get_features(sheet_metal, name='open_hem'):
    # increment bend count variable
    bbc += 1

    # increment for angle if necessary
    if not is_close(bend.properties.angle, 90):
        nnb += 1

    # if radius is medium or large, increment
    r = bend.properties.radius
    is_rad_medium = medium_radius_thresh <= r < large_radius_thresh or is_close(r, medium_radius_thresh)
    is_rad_large = r >= large_radius_thresh or is_close(r, large_radius_thresh)
    if is_rad_medium:
        mr += 1
    elif is_rad_large:
        lr += 1

    l = bend.properties.length
    is_length_medium = medium_length_thresh <= l < large_length_thresh or is_close(l, medium_length_thresh)
    is_length_large = l >= large_length_thresh or is_close(l, large_length_thresh)
    if is_length_medium:
        ml += 1
    elif is_length_large:
        ll += 1

# track tear drops as standard bends
for bend in get_features(sheet_metal, name='tear_drop'):
    # increment bend count variable
    bbc += 1

    # increment for angle if necessary
    if not is_close(bend.properties.angle, 90):
        nnb += 1

    # if radius is medium or large, increment
    r = bend.properties.radius
    is_rad_medium = medium_radius_thresh <= r < large_radius_thresh or is_close(r, medium_radius_thresh)
    is_rad_large = r >= large_radius_thresh or is_close(r, large_radius_thresh)
    if is_rad_medium:
        mr += 1
    elif is_rad_large:
        lr += 1

    l = bend.properties.length
    is_length_medium = medium_length_thresh <= l < large_length_thresh or is_close(l, medium_length_thresh)
    is_length_large = l >= large_length_thresh or is_close(l, large_length_thresh)
    if is_length_medium:
        ml += 1
    elif is_length_large:
        ll += 1

# track curls as standard bends
for bend in get_features(sheet_metal, name='curl'):
    # increment bend count variable
    bbc += 1

    # increment for angle if necessary
    if not is_close(bend.properties.angle, 90):
        nnb += 1

    # if radius is medium or large, increment
    r = bend.properties.radius
    is_rad_medium = medium_radius_thresh <= r < large_radius_thresh or is_close(r, medium_radius_thresh)
    is_rad_large = r >= large_radius_thresh or is_close(r, large_radius_thresh)
    if is_rad_medium:
        mr += 1
    elif is_rad_large:
        lr += 1

    l = bend.properties.length
    is_length_medium = medium_length_thresh <= l < large_length_thresh or is_close(l, medium_length_thresh)
    is_length_large = l >= large_length_thresh or is_close(l, large_length_thresh)
    if is_length_medium:
        ml += 1
    elif is_length_large:
        ll += 1

# track offsets as 2x bends
for bend in get_features(sheet_metal, name='offset'):
    # increment bend count variable
    bbc += 2

    # increment for angle if necessary
    if not is_close(bend.properties.angle, 90):
        nnb += 2

    # if radius is medium or large, increment
    r = bend.properties.radius
    is_rad_medium = medium_radius_thresh <= r < large_radius_thresh or is_close(r, medium_radius_thresh)
    is_rad_large = r >= large_radius_thresh or is_close(r, large_radius_thresh)
    if is_rad_medium:
        mr += 2
    elif is_rad_large:
        lr += 2

    l = bend.properties.length
    is_length_medium = medium_length_thresh <= l < large_length_thresh or is_close(l, medium_length_thresh)
    is_length_large = l >= large_length_thresh or is_close(l, large_length_thresh)
    if is_length_medium:
        ml += 2
    elif is_length_large:
        ll += 2

# now update and freeze our op variables and then calculate times so overrides at
# quote time can take effect as runtime and setup time increments
# apply a base time for each bend, and if bend angle is not 90, up tick,
# and if bend length and radius fall within gaps, increment times
base_bend_count.update(bbc)
base_bend_count.freeze()
total_bend_setup = base_bend_setup_time * base_bend_setup_time
total_bend_run = base_bend_count * base_bend_runtime

non_ninety_bends.update(nnb)
non_ninety_bends.freeze()
total_bend_setup += non_ninety_bends * st_increment
total_bend_run += non_ninety_bends * rt_increment

med_rads.update(mr)
med_rads.freeze()
total_bend_setup += med_rads * st_increment
total_bend_run += med_rads * rt_increment

large_rads.update(lr)
large_rads.freeze()
total_bend_setup += large_rads * 2 * st_increment
total_bend_run += large_rads * 2 * rt_increment

med_lengths.update(ml)
med_lengths.freeze()
total_bend_setup += med_lengths * st_increment
total_bend_run += med_lengths * rt_increment

large_lengths.update(ll)
large_lengths.freeze()
total_bend_setup += large_lengths * 2 * st_increment
total_bend_run += large_lengths * 2 * rt_increment

# establish final times as a sum of all above
# convert times to hours
setup_time.update(total_bend_setup / 60)
setup_time.freeze()
runtime.update(total_bend_run / 3600)
runtime.freeze()

setup_labor_rate = var('Setup Labor Rate', 50, 'Labor cost per hour to set up work center', currency)
run_labor_rate = var('Run Labor Rate', 25, 'Labor cost per hour to attend work center machine', currency)
machine_rate = var('Machine Rate', 25, 'Cost per hour to keep work center machine occupied', currency)
efficiency = var('Efficiency', 100, 'Percentage of real time the work center is processing parts', number)
percent_attended = var('Percent Attended', 80, 'Percentage of time work center must be attended', number)

max_size = var('Part Max Dim', 0, '', number, frozen=False)
max_size.update(get_workpiece_value('flat_length', max(sheet_metal.size_x, sheet_metal.size_y)))
max_size.freeze()
part_weight = var('Part Weight', 0, '', number, frozen=False)
part_weight.update(get_workpiece_value('weight', part.weight))
part_weight.freeze()

crew_size_thresh = var('Crew Size Thresh', 48, 'Size of part in inches requiring additional crew', number)
crew_weight_thresh = var('Crew Weight Thresh', 40, 'Weight of part in pounds requiring additional crew', number)
crew = var('Crew', 1, 'Number of people assigned to attend work center', number, frozen=False)
if (max_size >= crew_size_thresh and max_size) or (part_weight >= crew_weight_thresh and part_weight):
    crew.update(2)
crew.freeze()

total_cycle_time = part.qty * runtime
total_machine_occupied_time = total_cycle_time / efficiency * 100
total_attended_time = total_machine_occupied_time * percent_attended / 100

setup_cost = setup_time * setup_labor_rate
work_center_usage_cost = total_machine_occupied_time * machine_rate
run_labor_cost = total_attended_time * run_labor_rate * crew
PRICE = setup_cost + work_center_usage_cost + run_labor_cost
DAYS = 0
