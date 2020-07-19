

def flatten_to_string(l):
    """
    Recursive method.
    """

    new_list = []
    for x in l:
        if type(x)!=list:
            new_list.append(x)
        else:
            new_list.extend(flatten_to_string(x))
    # finally
    return new_list
