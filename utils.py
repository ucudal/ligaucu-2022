def sum_by_common_key(input_list, index_key='ID'):
    output_dict = {}
    for d in input_list:
        index = d[index_key]
        if index not in output_dict:
            output_dict[index] = {}
        for k, v in d.items():
            if k not in output_dict[index]:
                output_dict[index][k] = v
            elif k != index_key:
                output_dict[index][k] += v
    return output_dict.values()