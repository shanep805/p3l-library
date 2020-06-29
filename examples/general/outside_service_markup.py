# This applies a markup to outside_service service price by extracting it from the pricing dict.
# You can set your outside_service service markup with a default value, and modify it at quote time.

markup = var('Markup Percentage', 0, 'Percent markup on outside_service service cost', number)
outside_service_cost = get_price_value('--outside--')

PRICE = outside_service_cost * markup / 100
DAYS = 0
