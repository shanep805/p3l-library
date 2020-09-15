# Press Brake Advanced
This operation costs press brake forming using a bend-difficulty based approach.
There is base runtime and setup time per bend on the part.
If any of these bends are more challenging to form, we will increment the setup time and runtime contribution for each difficult bend.
The incrementing of runtime and setup time works with a "difficulty point" approach.
If a bend is long, has a large radius, or is not 90 degrees, we will add difficulty points to the bend.
For every difficulty point the bend accrues, we will add one unit of time increment to its contribution to total setup time or runtime.
The base bend runtimes, setup times, and difficulty point time increments are collected from a custom table.
These values vary based on material type and material thickness. This custom table is called `bend_table`.

Special bends like open hems, tear drops, and curls will be costed and tracked in the same manner as standard bends.
Offsets will be costed as if they were two bends.

Finally, when collecting costs by applying rates to our runtime and setup time, we will enforce percent attendance.
Setup cost is the setup time multiplied by the setup labor rate.
Run cost will be a combination of total runtime times machine rate and the required labor to monitor and operate the machine.
Since press brake operators must be at the machine for a high percentage of the time, we must charge a labor rate for the operator as well as a machine rate for machine.
Additionally, larger/heavier parts are harder to handle, and often require two operators.
Based on certain size and weight thresholds, the number of operators will be increased to 2.

**Operation Category**: Operation

**Is Outside Service**: false
