markup = var('Markup (%)', 0, '', number)

if part.material:
    set_operation_name('{} Markup {}%'.format(part.material, markup))

markup_cost = get_price_value('--material--') * (markup / 100)

PRICE = markup_cost
DAYS = 0
