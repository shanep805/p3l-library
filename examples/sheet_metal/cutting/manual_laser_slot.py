# When working with prints and you see many instances of slot features, you can quickly input total length, diameter
# and count to calculate cut times for these features.
# You can extend this by performing a look up using a table_var to a custom table of cut rates based on thickness and material

units_in()
cut_rate = var('Inches Per Min', 50, 'Inches per minute', number)

pierce_time = var('Pierce Seconds', 2, 'Time to pierce in seconds', number)

slot_count = var('Count', 0, 'Count of slots of this type', number)
diameter = var('Diameter', 0, 'Diameter of slot ends', number)
length = var('Length', 0, 'Total length of slot', number, frozen=False)
length.update(diameter)
length.freeze()

# cut length is circumference, pi * d, plus sides
cut_length = 3.1415926536 * diameter + 2 * (length - diameter)

runtime = var('runtime', 0, 'Runtime in hours', number, frozen=False)
runtime.update((pierce_time / 3600 + cut_length / cut_rate / 60) * slot_count)
runtime.freeze()

machine_rate = var('Machine Rate', 50, '$/hr', currency)

PRICE = machine_rate * runtime * part.qty
DAYS = 0