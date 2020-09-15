# Hole Secondaries
Costs the manufacturing of any secondary drilling/machining operations associated with countersinks, counterbores, and manual drilled holes.

Will apply a setup cost per unique setup of each type and a runtime for every instance of each type found.
Manual drilled holes are detected based on a ratio of diameter to material thickness. The default value is 1.0.
If you want to specify a different value for automatically detecting manual drilled holes, create a custom interrogation and link it to this operation.

All setup counts and total counts for each type can be overridden at quote time.

**Operation Category**: Operation
**Is Outside Service**: false
