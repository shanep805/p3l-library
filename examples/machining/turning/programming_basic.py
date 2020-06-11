## Setup Time and Labor Rate Operation

## A - Define Setup Time and Labor Rate variables
setup_time = var('setup_time', 0, '', number)
labor_rate = var('Labor Rate ($)', 0, '', currency, frozen = False)

## B - Update Labor Rate based on global labor rate. To not use the global labor rate, simply do not use a dynamic variable.
labor_rate.update(get_custom_attribute('labor_rate', 0))
labor_rate.freeze()

## C - Compile costs
PRICE = setup_time * labor_rate

## D - Define how many days this operation will contribute to the project lead time.
DAYS = 0

## E - Set workpiece values to be used in subsequent operations.
set_workpiece_value('Total Setup Time', get_workpiece_value('Total Setup Time', 0) + setup_time)			## A - Cumulative project setup time
set_workpiece_value('Operation Count', get_workpiece_value('Operation Count', 0) + 1)						## B - Cumulative operation count