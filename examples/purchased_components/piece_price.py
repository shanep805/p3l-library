# This example references the piece price of the purchased component associated with the part
# to yield a price for the operation

piece_price = var('piece_price', 0, '', currency, frozen=False)
if part.purchased_component:
    piece_price.update(part.purchased_component.piece_price)
piece_price.freeze()
PRICE = piece_price * part.qty
DAYS = 0
