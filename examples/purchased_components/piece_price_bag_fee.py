# Prices purchased components based on piece price and whether or not you will have to
# break additional bags to fulfill the order, thus incurring more cost

piece_price = var('piece_price', 0, '', currency, frozen=False)
if part.purchased_component:
    piece_price.update(part.purchased_component.piece_price)
piece_price.freeze()

bag_fee = var('Bag Fee', 10, 'Cost to break each additional bag', currency)

number_per_bag = var('Number Per Bag', 0, 'number of pieces per bag', number, frozen=False)
if part.purchased_component:
    number_per_bag.update(part.purchased_component.number_per_bag)
number_per_bag.freeze()

if number_per_bag > 0:
    bags_to_break = floor(part.qty / number_per_bag)
    bag_break_cost = bags_to_break * bag_fee
else:
    bag_break_cost = 0

PRICE = piece_price * part.qty + bag_break_cost
DAYS = 0
