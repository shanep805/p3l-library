# Waterjet Cost Per Sheet
A sheet metal process that assumes blanking is performed with a waterjet.

Waterjet times are calculated based on number of pierces, cut length, and a look-up table for pierce times and cut rates based on material and thickness.

Material price is calculated by determining an estimate for parts per sheet and querying for a sheet cost from a table.

Forming times are calculated based on material type, thickness, and bend characteristics.

Material thickness and flat size is confirmed in the initial material operation and passed through the workpiece to downstream operations.

**Process Type**: Generic
