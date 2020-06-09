for op_name in get_allowed_operations():
    if part.component_type == MANUFACTURED:
        generate_operation(op_name)