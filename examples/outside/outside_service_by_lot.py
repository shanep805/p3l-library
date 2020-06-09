# This outside service operation bases its pricing off of a lot charge and piece price model.
# If the quantity multiplied by the piece price is smaller than the lot charge, than the PRICE
# will be the lot charge. Otherwise it will be the extended piece price.
# You can apply additional lead time by using the added_lead_time variable

lot_charge = var('Lot Charge', 0, 'Lot charge for outside service', currency)
piece_price = var('Piece Price', 0, 'Price per unit for the outside service', currency)
added_lead_time = var('Added Lead Time', 0, 'Days of added lead time for outside service', number)

extended_price = part.qty * piece_price
if extended_price < lot_charge:
    PRICE = lot_charge
else:
    PRICE = extended_price

DAYS = added_lead_time
