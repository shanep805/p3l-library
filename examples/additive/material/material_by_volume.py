# Pricing based on cost per cubic inch. This is ideal for additive.

units_in()
additive = analyze_additive()


if part.material:
    set_operation_name(part.material)

price_per_vol = var('Price Per Cubic Inch', 1, '', currency, frozen=False)
price_per_vol.update(part.mat_cost_per_volume)
price_per_vol.freeze()

part_vol = var('Part Volume', 0, '', number, frozen=False)
part_vol.update(part.volume)
part_vol.freeze()

supp_vol = var('Support Volume', 0, '', number, frozen=False)
supp_vol.update(additive.support_volume)
supp_vol.freeze()

PRICE = price_per_vol * (part_vol + supp_vol) * part.qty
DAYS = 0
