# Time Save with Crew
Determines runtime per pass for a time saver operation by applying a time-per-inch rate against the longest dimension of the flat part.
Operation defaults to 2 passes (one for each side of the flat).
This can be overridden if there are certain features that prevent both sides from running through the machine.

Setup times are a set value. Setup costs are determined by applying a labor rate to this setup time multiplied by the number of operators required (or "crew").
If the size or weight of the flat is greater than a certain threshold, the operation will assign a crew of 2 to handle the part, doubling setup cost.

**Operation Category**: Operation

**Is Outside Service**: false
