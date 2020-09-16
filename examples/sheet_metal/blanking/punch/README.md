# Punch
This formula costs blanking the flat part with a punch machine.
Simple contours (circle, square, rectangle, slot, obround) below a size threshold specified in your custom interrogation (default 6 inches) will assume to be hit with a single hit.
Any non-simple contours or simple contours greater than that size threshold will be considered multi-hit features.

This operation determines setup time based on a fixed base setup time and the number of unique punch tools the part will need.
The total setup time is the base setup time plus an additional setup time per tool.
The number of punch tools is determined by the number of unique single hit contours found on the part.
This formula assumes no additional tools will be needed to hit multi-hit features.

The operation determines runtime by adding the total number of single hit features with an estimate for the number of hits required to accomplish all multi-hit features.
The estimate for number of hits for multi-hit features is determined using a factor for how much cut length each hit can accomplish.
We then divide the total multi-hit cut length by this factor to get an estimate for hit count.
The runtime is then calculated by multiplying the number of hits by a time per hit.

This operation should be linked to a custom interrogation that has punch-style interrogation turned on.
The sample inputs you must have are provided in **custom_interrogation.json**.

**Operation Category**: Operation

**Is Outside Service**: false
