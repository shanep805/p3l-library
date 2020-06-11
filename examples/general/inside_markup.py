# This applies a markup to all operations above this one that are not outside_service or material extracting it from the pricing dictionary.
# You can set your markup with a default value, and modify it at quote time.

markup = var('Markup Percentage', 15, 'Percent markup on inside ops', number)
inside_cost = get_price_value('--inside--')
set_operation_name('Inside Markup: {}%'.format(markup))

PRICE = inside_cost * markup / 100
DAYS = 0
