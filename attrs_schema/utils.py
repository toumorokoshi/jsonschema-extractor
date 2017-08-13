import copy


def merge_attributes(core, additional):
    return_value = copy.deepcopy(core)
    return_value.update(additional)
    return return_value
