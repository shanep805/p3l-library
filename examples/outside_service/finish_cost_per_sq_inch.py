# This outside_service service operation calculates its pricing on a part surface area model.
# Surface area for most finishing operations is the driving factor for pricing.
# As long as part geometry is not overly complicated to hang on a rack and is not
# extremely large, with the correct price per square inch value, pricing is likely to
# be quite accurate.
# Price is calculated based on an inputted price per unit of surface area.
# Additional lead time can be controlled with the added_lead_time input

units_in()

price_per_sq_inch = var('Price Per Square Inch', 0.01, '', currency)
area = var('Part Area', 0, '', number, frozen = False)
area.update(round(part.area, 3))
area.freeze()

added_lead_time = var('Added Lead Time', 0, 'Days of added lead time for outside_service service', number)

PRICE = price_per_sq_inch * area * part.qty
DAYS = added_lead_time
