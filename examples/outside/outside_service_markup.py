# This applies a markup to outside service price by extracting it from the pricing dict.
# This applies a markup to outside service price by extracting it from the pricing dict.
# You can set your outside service markup with a default value, and modify it at quote time.

markup = var('Markup Percentage', 0, 'Percent markup on outside service cost', number)
outside_service_cost = get_price_value('--outside--')
set_operation_name('Outside Markup: {}%'.format(markup))

PRICE = outside_service_cost * markup / 100
DAYS = 0
