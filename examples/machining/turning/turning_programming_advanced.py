# A - Geometric Definitions
# A.1 - Set units
units_in()
# A.2 - Set our geometric interrogation.
# Read more here: https://help.paperlessparts.com/article/42-p3l-language-features
lathe = analyze_lathe()

# B - Feature and Feedback Count
# B.1 - Define Feature Count and Feedback Count
feature_count = len(get_features(lathe))
feedback_count = len(get_feedback(lathe))
features = var('Feature Count', 0, '', number, frozen=False)
features.update(feature_count + feedback_count)
features.freeze()

# C - Set and Update Variables
# C.1 - Define Features, Time Per Feature, Setup Time, and Labor Rate variables
features = var('Feature Count', 0, '', number, frozen=False)
time_per_feature = var('Time Per Feature (Minutes)', 5, '', number)
setup_time = var('setup_time', 0, '', number, frozen=False)
labor_rate = var('Labor Rate ($)', 65, '', currency)

# C.2 - Update Features and Setup Time based on calculated values
features.update(feature_count + feedback_count)
features.freeze()
setup_time.update(max(0.5, (features * time_per_feature) / 60))  # We set the Setup Time to a minimum of 0.5 hours (30 minutes). If the calculated programming time is greater than 30 minutes, we use that time).
setup_time.freeze()

# D - Final Calculations
# D.1 - Compile our costs
PRICE = setup_time * labor_rate

# D.2 - Define how many days this operation will contribute to the project lead time.
DAYS = 0

# D.3 - Set workpiece values to be used in subsequent operations.
set_workpiece_value('total_setup_time', get_workpiece_value('total_setup_time', 0) + setup_time)  # A - Cumulative project setup time