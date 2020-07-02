# This shows you how to enforce a minimum order item value regardless of what quantity
# the user selects. This add on by default should be required

min_order_val = var('Min Order Value', 1500, '', currency)
total_price = get_price_value('--total--') + get_price_value('--required_add_on--')
PRICE = max(min_order_val - total_price, 0)