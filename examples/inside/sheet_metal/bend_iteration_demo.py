units_in()
sheet_metal = analyze_sheet_metal()

ninety_count = 0
non_ninety_count = 0
for bend in get_features(sheet_metal, name='bend'):
    if is_close(bend.properties.angle, 90):
      ninety_count += 1
    else:
      non_ninety_count += 1

# var out angle bend counts for ability to confirm and override at quote time
ninety_bend_count = var('90 Deg Bends', 0, '# of 90 deg bends', number, frozen=False)
ninety_bend_count.update(ninety_count)
ninety_bend_count.freeze()

non_ninety_bend_count = var('Non 90 Deg Bends', 0, '# of non 90 deg bends', number, frozen=False)
non_ninety_bend_count.update(non_ninety_count)
non_ninety_bend_count.freeze()

# setup time, 5 minutes per 90 degree, 10 minutes per non ninety degree
ninety_setup = 5
non_ninety_setup = 10
setup_time = var('setup_time', 0, 'Setup time in hours', number, frozen=False)
# setup_time must be updated in hours
setup_time.update((ninety_setup * ninety_bend_count + non_ninety_setup * non_ninety_bend_count) /60)
setup_time.freeze()

# runtime, 30 seconds per 90 degree, 60 seconds per non ninety degree
ninety_run = 30
non_ninety_run = 60
runtime = var('runtime', 0, 'Runtime in hours', number, frozen=False)
# runtime must be updated in hours
runtime.update((ninety_run * ninety_bend_count + non_ninety_run * non_ninety_bend_count) / 3600)
runtime.freeze()

rate = var('Rate', 50, '$/hr', currency)

# apply hourly rate for setup and run to get price
PRICE = setup_time * rate + runtime * part.qty * rate
DAYS = 0