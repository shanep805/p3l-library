# A - Set Lot Charge, Piece Price, Added Lead Time variables
lot_charge = var('Lot Charge', 0, 'Lot charge for outside_service service', currency)
piece_price = var('Piece Price', 0, 'Price per unit for the outside_service service', currency)
added_lead_time = var('Added Lead Time', 0, 'Days of added lead time for outside_service service', number)

# B - Define Extended Price
extended_price = part.qty * piece_price

# C - Compile costs
if extended_price < lot_charge:					# If the part quantity * piece price is less than the lot charge, then use the lot charge.
    PRICE = lot_charge
else:											# Otherwise, use the quantity * piece price.
    PRICE = extended_price

# D - Define how many days this operation will contribute to the project lead time.
DAYS = added_lead_time