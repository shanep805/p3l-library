# This operation describes how to price a HP Multi Jet Fusion printer for a part
# that will have a dedicated build, containing maximal quantity of only one part.
# Pricing will be calculated based off of an established cost per full build
# input. This operation generates pricing by extracting the number of builds
# calculated in the HP Multi Jet Fusion Build Setups operation from the workpiece.
#
# Be sure to associate your 3D printer machine with this operation to have access
# to additive pricing features such as build area checks and orientation in the
# partviewer.

units_in()
additive = analyze_additive()

# shop rates
cost_per_full_build = var('Cost Per Full Build', 713, 'Full Build - 2 year payback (6%)', currency)
number_of_builds = get_workpiece_value('hp_build_count', 1)

PRICE = cost_per_full_build * number_of_builds
DAYS = 0
