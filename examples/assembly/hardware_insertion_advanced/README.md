# Hardware Insertion
Costs the insertion of hardware by collecting the information on the component's direct child components.
By only referencing the component's direct children, you can split up hardware insertion costs into individual subassemblies.

Insertion times are collected by looping through child info and summing the individual insertion times for each child purchased component.
If the purchased component does not have an insertion time specified, it will apply a default insertion time specified with a variable in the operation.

The lead time for this operation will be collected as the maximum lead time listed across all purchased components in the tree.
We will only add to lead time if the component is the root component.

The operation will be dynamically renamed based on how many total pieces of hardware must be inserted.

**Operation Category**: Operation

**Is Outside Service**: false
