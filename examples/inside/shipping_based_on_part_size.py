units_in()

setup_time = var('setup_time', 0, 'Setup time in hours', number, frozen=False)
runtime = var('runtime', 0, 'Run time in hours', number, frozen=False)

max_size = var('Max Size', 0, 'Max size in inches', number, frozen=False)
max_size.update(max(part.size_x, part.size_y, part.size_z))
max_size.freeze()

small_thresh = 6.0
med_thresh = 12.0
large_thresh = 36.0

# setup and runtimes for different size thresholds in minutes
small_setup = 10
small_run = 1
med_setup = 15
med_run = 2
large_setup = 20
large_run = 5
pallet_setup = 30
pallet_run = 30

# determining size thresholding based on the longest
is_small = max_size < small_thresh or is_close(max_size, small_thresh)
is_med = not is_small and (max_size < med_thresh or is_close(max_size, med_thresh))
is_large = not is_small and not is_med and (max_size < large_thresh or is_close(max_size, large_thresh))

if is_small:
    setup_time.update(small_setup / 60)
    runtime.update(small_run / 60)
elif is_med:
    setup_time.update(med_setup / 60)
    runtime.update(med_run / 60)
elif is_large:
    setup_time.update(large_setup / 60)
    runtime.update(large_run / 60)
else:
    setup_time.update(pallet_setup / 60)
    runtime.update(pallet_run / 60)

setup_time.freeze()
runtime.freeze()

rate = var('Rate', 50, '$/hr', currency)

PRICE = rate * setup_time + rate * runtime * part.qty
DAYS = 0
