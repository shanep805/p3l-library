# Material Cost Per Sheet
Calculates material cost by looking up to a table of sheets that have thickness, length, width, and sheet price.
This custom table should be named `sheet_lookup`.
**NOTE: The sample data provided should not be considered accurate.**
The largest sheet for the material and thickness will be chosen by default from the custom table.
We will then perform an estimate for parts per sheet given a certain buffer.
Based on the number of parts per sheet and the requested quantity, we will determine the number of sheets required to satisfy the order.
The price for that quantity is then the number of required sheets multiplied by the sheet cost from the table row.

At quote time, any of the variables can be overridden to manual specifications.

We will set important values like thickness, flat width, flat length, and part weight in the workpiece for use in downstream operations.
This avoids redundant information input in the event of a non-geometric file or a file that cannot be properly unfolded.

**Operation Category**: Material

**Is Outside Service**: false
