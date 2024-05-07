def get_for_list(array, index):
    try:
        return array[index]
    except IndexError:
        return None
