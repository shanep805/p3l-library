units_in()
cut_rate = var('Inches Per Min', 1, 'Inches per minute', number, frozen=False)
cut_rate.update(max(part.mat_cut_rate, 0.1))
cut_rate.freeze()

pierce_time = var('Pierce Seconds', 0, 'Time to pierce in seconds', number, frozen=False)
pierce_time.update(part.mat_pierce_time)
pierce_time.freeze()

obround_count = var('Count', 0, 'Count of obrounds of this type', number)
radius = var('Radius', 0, 'Radius of obround corners', number)
length = var('Length', 0, 'Total length of obround', number, frozen=False)
length.update(radius * 2)
length.freeze()
width = var('Width', 0, 'Total width of obround', number, frozen=False)
width.update(radius * 2)
width.freeze()

# cut length is 2w + 2l - 2pi*r
cut_length = 2 * width + 2 * length - 2 * 3.1415926536 * radius

runtime = var('runtime', 0, 'Runtime in hours', number, frozen=False)
runtime.update((pierce_time / 3600 + cut_length / cut_rate / 60) * obround_count)
runtime.freeze()

machine_rate = var('Machine Rate', 50, '$/hr', currency)

PRICE = machine_rate * runtime * part.qty
DAYS = 0