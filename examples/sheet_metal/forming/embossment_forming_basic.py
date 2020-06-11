# Applies a runtime per embossments

units_in()
sheet_metal = analyze_sheet_metal()

embossment_count = var('Embossment Count', 0, 'Number of embossments', number, frozen=False)
embossment_count.update(len(get_features(sheet_metal, name='embossment')))
embossment_count.freeze()

setup_time = var('setup_time', 1, 'Setup time in hours', number, frozen=False)
if embossment_count < 1:
    setup_time.update(0)
setup_time.freeze()

time_per_embossment = var('Seconds/Embossment', 15, 'Seconds per embossment', number)

runtime = var('runtime', 0, 'Runtime in hours', number, frozen=False)
runtime.update(time_per_embossment * embossment_count / 3600)
runtime.freeze()

rate = var('Rate', 50, '$/hr', currency)

PRICE = setup_time * rate + runtime * part.qty * rate
DAYS = 0
