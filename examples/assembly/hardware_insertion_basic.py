# Takes the total number of child purchased components in the entire assembly
# and applies a default insert time for each one

hardware_count = var('Hardware Count', 0, '', number, frozen=False)
hardware_count.update(part.purchased_child_count_recursive)
hardware_count.freeze()

set_operation_name('Assemble {} Inserts'.format(hardware_count))

time_per_insert = var('Time per Insert', 30, 'Insert time in seconds', number)

runtime = var('runtime', 0, 'Runtime in hours', number, frozen=False)
runtime.update(hardware_count * time_per_insert / 3600)
runtime.freeze()

rate = var('Rate', 60, '$/hr', currency)

PRICE = rate * runtime * part.qty
DAYS = 0
