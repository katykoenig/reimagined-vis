'''
Helper Functions for v_a11ylint
'''

def fill_dict(dict_obj, key, issues):
    '''
    Updates input dictionary only if issues
    To avoid adding empty values and clutter dictionary

    Inputs:
        dict_obj: dictionary of issues
        key: dictionary key to be added if issues
        issues: list or string of issues if any (else: None)

    Outputs: an updated version of input dictionary
    '''
    if issues != None:
        dict_obj[key] = issues
    return dict_obj


def call_recurse(configs, keys):
    '''
    Calls recursive function to find keywords in dictionary and returns a
    pared down dictionary

    Inputs:
        configs: dictionary representing the theme configuration of a chart obj
        keys: list of keywords we want to find in dictionary

    Output:
        check_dict: dictionary with only relevant key, value pairs
                    for given keywords
    '''
    check_dict = {}
    recusive_find(configs, keys, check_dict)
    return check_dict


def recusive_find(configs, keywords, check_dict, prefix=None):
    '''
    Recursively iterates through a dictionary to check if keys anywhere
    in configs dictionary

    Inputs:
        configs: dictionary representing the theme configuration of a chart obj
        keywords: list of keywords we want to find in dictionary
        check_dict: dictionary with only relevant key, value pairs
                    for given keywords

    Outputs: None, modifies dictionary in place
    '''
    for k, v in configs.items():
        if any(word in k for word in keywords[0]) and k not in keywords[1]:
            if prefix and prefix != 'config':
                if prefix in check_dict.keys():
                    if k in check_dict[prefix].keys():
                        check_dict[prefix][k].append(v)
                    else:
                        check_dict[prefix][k] = [v]
                else:
                    check_dict[prefix] = {k: [v]}
            else:
                if k in check_dict.keys():
                    check_dict[k].append(v)
                else:
                    check_dict[k] = [v]
        elif isinstance(v, dict):
            recusive_find(v, keywords, check_dict, k)
