# Manual operation to cost welds. Prices by number of unique welds and total weld length

units_in()

segments = var('Segments', 0, 'Number of segments', number)
total_length = var('Total length', 0, 'Total length of welds in inches', number)

setup_time_per_segment = var('Setup Time Per Segment', 5, 'minutes', number)

setup_time = var('setup_time', 0, '', number, frozen = False)
setup_time.update(setup_time_per_segment * segments / 60)
setup_time.freeze()

weld_speed = var('Weld Speed', 3, 'inches/min', number)
runtime = var('runtime', 0, '', number, frozen = False)
runtime.update(total_length / weld_speed / 60)
runtime.freeze()

rate = var('Rate', 100, '$/hr', currency)

PRICE = setup_time * rate + runtime * rate * part.qty
DAYS = 0