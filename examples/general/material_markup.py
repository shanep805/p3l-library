## A - Define Markup
markup = var('Markup (%)', 0, '', number)

## B - Define and calculate Markup Cost
markup_cost = get_price_value('--material--') * (markup / 100)

## C - Set the name of the operation for visibility on markup
if part.material:
    set_operation_name('{} Markup: {}%'.format(part.material, markup))

## D - Compile our costs
PRICE = markup_cost

## E - Define how many days this operation will contribute to the project lead time.
DAYS = 0