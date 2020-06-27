## A - Geometric Definitions
## A.1 - Set units
units_in()
## A.2 - Set our geometric interrogation. We will the values associated with this interrogation in subsequent variables. Read more here: https://help.paperlessparts.com/article/42-p3l-language-features
mill = analyze_mill3()

## -------------------------------------------------------------------------------------------------------------------- ##

## B - Part Variables
## B.1 - Set our Min, Max, and Median part dimensions
min_size = min(part.size_x, part.size_y, part.size_z)
max_size = max(part.size_x, part.size_y, part.size_z)
med_size = median(part.size_x, part.size_y, part.size_z)

## B.2 Define the Surface Area to Bounding Box Area Ratio
surface_area = part.area
bbox_area = 2 * (med_size * min_size) + 2 * (med_size * max_size) + 2 * (min_size * max_size)
surface_area_ratio = part.area / bbox_area

## B.3 - Define Feature and Feedback Count, and certain manufacturability warning counts
feature_count = 0
feedback_count = 0

## B.4 - Update the various feature counts based on interrogation
for setup in get_setups(mill):
    feature_count += (len(get_features(setup)) - len(get_features(setup, name='hole')))
    feedback_count += (len(get_feedback(setup)))

## B.5 - Update the Total Feature Count based on defined Feature and Feedback interrogation
features = var('Feature Count', 0, '', number, frozen=False)
features.update(feature_count + feedback_count)
features.freeze()

## -------------------------------------------------------------------------------------------------------------------- ##

## C - Part Complexity
## C.1 - Define Part Complexity variable
part_complexity = var('Part Complexity', 0, '', number, frozen=False)

## C.2 - Update Part Complexity based on Feature Count - first text of complexity.
if features <= 25:
    part_complexity.update(1)
elif 25 < features <= 75:
    part_complexity.update(2)
elif 75 < features or 6 < mill.setup_count:
    part_complexity.update(3)

## C.3 - Update Part Complexity if certain manufacturability warnings present
if part_complexity == 1:
    if min_size < 0.25 and max_size < 0.25 and med_size < 0.25:
        part_complexity.update(2)
part_complexity.freeze()

## C.4 - Update operation name based on defined part complexity
if part_complexity == 1:
    set_operation_name('Part Level 1')
elif part_complexity == 2:
    set_operation_name('Part Level 2')
elif part_complexity == 3:
    set_operation_name('Part Level 3')

## C.4 - Store part level to be used in subsequent operations
set_workpiece_value('Part Complexity', part_complexity)

## -------------------------------------------------------------------------------------------------------------------- ##

PRICE = 0
DAYS = 0