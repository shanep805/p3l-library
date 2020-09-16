# Punch
A sheet metal process that assumes blanking is performed with a punch machine.

Punch times are calculated based on the total number of hits and unique punch tools.
Total hits are the sum of total single hit features and an estimate for hits to accomplish all multi-hit features.

Material price is calculated by determining an estimate for parts per sheet and querying for a sheet cost from a table.

Forming times are calculated based on material type, thickness, and bend characteristics.

Material thickness and flat size is confirmed in the initial material operation and passed through the workpiece to downstream operations.

**Process Type**: Generic
