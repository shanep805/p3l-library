# This is a generic template for a non recurring engineering add on that does not scale
# with part quantity. This should be set by default as required

setup_time = var('setup_time', 0, '', number)
labor_rate = var('Labor Rate ($)', 60, '', currency)

PRICE = setup_time * labor_rate
