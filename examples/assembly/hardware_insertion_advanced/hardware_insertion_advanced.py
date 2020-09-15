# Loops through the child information of the component (just direct children) and collects the insertion time
# specified on each individual purchased component

hardware_count = var('Hardware Count', 0, '', number, frozen=False)
hardware_count.update(part.purchased_child_count_recursive)
hardware_count.freeze()

set_operation_name('Assemble {} Inserts'.format(hardware_count))

default_insertion_time = var('Default Insertion Time', 30, 'Insert time in seconds', number)

rts = 0
for child in get_child_info(type=PURCHASED, recursive=False):
    if child.purchased_component.insertion_time:
        rts += child.purchased_component.insertion_time
    else:
        rts += default_insertion_time

runtime = var('runtime', 0, 'Runtime in hours', number, frozen=False)
runtime.update(rts / 3600)
runtime.freeze()

rate = var('Rate', 50, '$/hr', currency)

# if root component, add lead time based on the maximum specified lead time from all purchased components in the tree
days_added = var('Days Added', 0, 'Business days added in lead time', number, frozen=False)
if part.is_root_component:
    max_lead_time = 0
    for child in get_child_info(type=PURCHASED, recursive=True):
        if child.purchased_component.lead_time > max_lead_time:
            max_lead_time = child.purchased_component.lead_time
    days_added.update(max_lead_time)
days_added.freeze()

PRICE = rate * runtime * part.qty
DAYS = days_added
