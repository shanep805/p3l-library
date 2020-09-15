# lookup based on part number, grab latest revision
row = table_var(
    'Historical Ref',
    'Look up by part number to historical quotes',
    'historical_pricing',
    create_filter(
        filter('part_no', '=', part.part_number),
    ),
    create_order_by('part_no', '-part_rev'),
    'part_no',
)

if row:
    set_operation_name('REPEAT - Unit Price: ${}'.format(row.unit_price))
else:
    set_operation_name('NEW - No Historical Pricing')
