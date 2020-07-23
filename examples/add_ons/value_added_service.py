# This is a template to use for a value added service add on that does not scale with quantity
# As this is not a requirement of the job, this should be set to not required
# as the buyer has the discretion to include this into the order item or not

setup_time = var('setup_time', 0, '', number)
labor_rate = var('Labor Rate ($)', 0, '', currency)

PRICE = setup_time * labor_rate
