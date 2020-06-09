# collects bend runtime and bend setup time based on the characteristics of bends in the part
# there is a base bend runtime and setup time, and based on things like angle, length, radius
# the times will increment

units_in()
sheet_metal = analyze_sheet_metal()

setup_time = var('setup_time', 0, 'Setup time in hours', number, frozen=False)
runtime = var('runtime', 0, 'Runtime in hours', number, frozen=False)

# establish base setup time and time increments in minutes
base_bend_setup_time = 6
st_increment = 3

# establish base runtime and time increments in seconds
base_bend_runtime = 30
rt_increment = 15

# establish geometric thresholds for incrementing times
# in inches
medium_radius_thresh = 2.0
large_radius_thresh = 4.0
medium_length_thresh = 20
large_length_thresh = 40

# establish our variables that we will use as pricing levers in the operation
# also establish their local tracking variables
base_bend_count = var('Bend Count', 0, 'Number of bends detected', number, frozen=False)
bbc = 0
non_ninety_bends = var('Non-90 Bend Count', 0, 'Number of non-90 degree bends', number, frozen=False)
nnb = 0
med_rads = var('Medium Rads', 0, 'Number of bends with medium rads', number, frozen=False)
mr = 0
large_rads = var('Large Rads', 0, 'Number of bends with large rads', number, frozen=False)
lr = 0
med_lengths = var('Medium Lengths', 0, 'Number of bends with medium length', number, frozen=False)
ml = 0
large_lengths = var('Large Lengths', 0, 'Number of bends with large length', number, frozen=False)
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

# now track hems, curls, and teardrops into hem category
ohc = len(get_features(sheet_metal, name='open_hem'))
tdc = len(get_features(sheet_metal, name='tear_drop'))
cc = len(get_features(sheet_metal, name='curl'))
hem_count = var('Hem Count', 0, 'Number of hems and curls', number, frozen=False)
hem_count.update(ohc + tdc + cc)
hem_count.freeze()

# increment runtimes and setup times 2x base value for every hem, curl, and teardrop found in the geometry
total_hem_setup = 2 * base_bend_setup_time * hem_count
total_hem_run = 2 * base_bend_runtime * hem_count

# now track offsets
offset_count = var('Offset Count', 0, 'Number of offsets', number, frozen=False)
offset_count.update(len(get_features(sheet_metal, name='offset')))
offset_count.freeze()

# increment 2x standard times for each presence of offset
offset_setup = 2 * base_bend_setup_time * offset_count
offset_run = 2 * base_bend_runtime * offset_count

# establish final times as a sum of all above
# convert times to hours
setup_time.update((total_bend_setup + total_hem_setup + offset_setup) / 60)
setup_time.freeze()
runtime.update((total_bend_run + total_hem_run + offset_run) / 3600)
runtime.freeze()

rate = var('Rate', 100, '$/hr', currency)

PRICE = setup_time * rate + runtime * part.qty * rate
DAYS = 0
