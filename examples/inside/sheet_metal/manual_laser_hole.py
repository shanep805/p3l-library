units_in()
cut_rate = var('Inches Per Min', 0.1, 'Inches per minute', number, frozen=False)
cut_rate.update(max(part.mat_cut_rate, 0.1))
cut_rate.freeze()

pierce_time = var('Pierce Seconds', 0, 'Time to pierce in seconds', number, frozen=False)
pierce_time.update(part.mat_pierce_time)
pierce_time.freeze()

hole_count = var('Count', 0, 'Count of holes of this type', number)
diameter = var('Diameter', 0, 'Diameter of hole', number)

# cut length is circumference, pi * d
cut_length = 3.1415926536 * diameter

runtime = var('runtime', 0, 'Runtime in hours', number, frozen=False)
runtime.update((pierce_time / 3600 + cut_length / cut_rate / 60) * hole_count)
runtime.freeze()

machine_rate = var('Machine Rate', 50, '$/hr', currency)

PRICE = machine_rate * runtime * part.qty
DAYS = 0