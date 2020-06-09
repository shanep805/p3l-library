# This applies a markup to material price by extracting it from the pricing dictionary.
# You can set your material markup with a default value, and modify it at quote time.

markup = var('Markup Percentage', 0, 'Percent markup on material cost', number)
material_cost = get_price_value('--material--')
if part.material:
    set_operation_name('{} Markup: {}%'.format(part.material, markup))

PRICE = material_cost * markup / 100
DAYS = 0
