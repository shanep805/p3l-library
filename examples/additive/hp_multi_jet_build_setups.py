# This operation describes how to price the build setups for an HP Multi Jet printer for a part that will
# be part of a shared build. This means that you will price the part as if it is already part of a full build in your
# machine. The number of builds required to fulfill a quantity will be calculated based on the percentage of build
# volume the part geometry occupies. You can set and adjust things like nesting and packing factors at quote time to
# tweak the number of parts to fit in a build.
# This calculated number of builds will then be used to calculate total setup and cooldown costs, and it will also be
# stored in the workpiece for usage in the operation where we apply pricing.
#
# Be sure to associate your 3D printer machine with this operation to have access to additive pricing features such as
# build area checks and orientation.

units_in()
additive = analyze_additive()

labor_rate = var('Labor Rate', 50, '$/ hr', currency)
setup_time_per_build = var('Setup Time Per Build (min)', 30, 'setup time per build in minutes', number)

buffer = var('Buffer (in)', 0.25,'Buffer around part (in)', number)
volume_full_tray = var('Build Volume (cu. in)', 2520, 'Build volume (cu. in)', number)

# calculate % of build is part
packing_factor = var('Packing Factor', 80, 'Percentage of total build volume that can be occupied per build', number)
available_build_volume = volume_full_tray * packing_factor / 100

nesting_factor = var('Nesting Factor', 100, 'Percentage of part bounding box volume to apply to build usage', number)
volume_part_bbox = (part.size_x + buffer) * (part.size_y + buffer) * (part.size_z + buffer)
occupational_volume = volume_part_bbox * nesting_factor / 100

volume_usage = occupational_volume / available_build_volume

# calculate number of parts in a build, no impact on pricing
number_of_parts_per_build = var('Number of parts per build', 1, '# of parts', number, frozen=False)
if available_build_volume > 0:
    number_of_parts_per_build.update(floor(available_build_volume / occupational_volume))
number_of_parts_per_build.freeze()

number_of_builds = ceil(part.qty / number_of_parts_per_build)
# add to the workpiece the number of builds
set_workpiece_value('hp_build_count', number_of_builds)

PRICE = setup_time_per_build / 60 * number_of_builds * labor_rate

DAYS = 0
