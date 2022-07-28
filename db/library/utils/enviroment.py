def parse_str_list_to_list(str_list):
    if not str_list or not isinstance(str_list, str):
        return []
    return [string.strip() for string in str_list.split(',') if string]
