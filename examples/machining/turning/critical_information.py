## A - Geometric Definitions
## A.1 - Set units
units_in()
## A.2 - Set our geometric interrogation. We will the values associated with this interrogation in subsequent variables. Read more here: https://help.paperlessparts.com/article/42-p3l-language-features
lathe = analyze_lathe()

## -------------------------------------------------------------------------------------------------------------------- ##

## B - Part Variables
## B.1 - Set our Min, Max, and Median part dimensions
min_size = min(part.size_x, part.size_y, part.size_z)
max_size = max(part.size_x, part.size_y, part.size_z)
med_size = median(part.size_x, part.size_y, part.size_z)

## Define Part Features and Feedback
feature_count = 0
feedback_count = 0
for feature in get_features(lathe):
    feature_count = (len(get_features(lathe)))

for feedback in get_feedback(lathe):
    feedback_count = (len(get_feedback(lathe)))

features = var('Feature Count', 0, '', number, frozen=False)
features.update(feature_count + feedback_count)
features.freeze()

## -------------------------------------------------------------------------------------------------------------------- ##

## C - Part Complexity
## C.1 - Define Part Complexity variable
part_complexity = var('Part Complexity', 0, '', number, frozen=False)

## C.2 - Update Part Complexity based on Feature Count
if features <= 25:
    part_complexity.update(1)
elif 25 < features <= 75:
    part_complexity.update(2)
elif 75 < features or 6 < lathe.setup_count:
    part_complexity.update(3)
part_complexity.freeze()

## C.3 - Update operation name based on defined part complexity
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