def convert_godot_tuple_to_python_list(tuple):
    tuple = [float(i) for i in tuple.strip("()").split(", ")]
    return tuple