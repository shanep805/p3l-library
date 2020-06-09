# Takes the total number of child purchased components and applies an insert time for each one

purchased_children = var('Hardware Count', 0, '', number, frozen=False)
purchased_children.update(part.purchased_children)
purchased_children.freeze()

set_operation_name('Assemble {} Inserts'.format(purchased_children))

time_per_insert = var('Timer per Insert', 30, 'Insert time in seconds', number)

runtime = var('runtime', 0, 'Runtime in hours', number, frozen=False)
runtime.update(purchased_children * time_per_insert / 3600)
runtime.freeze()

rate = var('Rate', 50, '$/hr', currency)

PRICE = rate * runtime * part.qty
DAYS = 0
