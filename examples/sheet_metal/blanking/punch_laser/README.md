# Punch Laser
This formula costs blanking the flat part with a punch-laser machine.
Simple contours (circle, square, rectangle, slot, obround) below a size threshold specified in your custom interrogation (default 6 inches) will assume to be hit with a single hit.
Any non-simple contours or simple contours greater than that size threshold will assumed to be hit with the laser.

This operation determines setup time based on a fixed base setup time and the number of unique punch tools the part will need.
The total setup time is the base setup time plus an additional setup time per tool.
The number of punch tools is determined by the number of unique single hit contours found on the part.

The operation determines the punch runtime by applying a time-per-hit to the total number of single hit features with.
The operation determines laser runtime by applying a cut rate to the cut length of all features besides the single hit features and by applying a pierce time to all required pierces.
The number of pierces is determined by the total number of internal cutouts the laser must cut.

Collects cut rates and pierce times from a custom table with the name `laser_cut_rates`.
Formula performs lookups to table based on material family and material thickness.

`laser_cut_rates` custom table found in *../custom_tables*.


This operation should be linked to a custom interrogation that has punch-laser-style interrogation turned on.
The sample inputs you must have are provided in **custom_interrogation.json**.

**Operation Category**: Operation

**Is Outside Service**: false
