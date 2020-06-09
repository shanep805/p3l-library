# NOTE: to be used with material_by_sheet_section_template

if part.material:
    set_operation_name('{} Markup'.format(part.material))

blank_size = get_workpiece_value('blank_size', 64)
if is_close(blank_size, 1):
    markup = 1.0
elif is_close(blank_size, 2):
    markup = 0.8
elif is_close(blank_size, 4):
    markup = 0.6
elif is_close(blank_size, 8):
    markup = 0.5
elif is_close(blank_size, 16):
    markup = 0.3
elif is_close(blank_size, 32):
    markup = 0.25
elif is_close(blank_size, 64):
    markup = 0.2
else:
    markup = 0.0

PRICE = get_price_value('--material--') * markup
DAYS = 0
