## A - Define Markup
markup = var('Markup (%)', 0, '', number)

## B - Define and calculate Markup Cost
markup_cost = get_price_value('--material--') * (markup / 100)

## C - Compile our costs
PRICE = markup_cost

## D - Define how many days this operation will contribute to the project lead time.
DAYS = 0