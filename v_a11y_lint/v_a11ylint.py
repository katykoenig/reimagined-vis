'''
File with main accessible visualization linters

'''
import altair as alt
import pandas as pd
import font_rules as fr
import color_rules as cr


### Helper Fns ###
def iterate_on_layers(chart_objs):
    '''
    Iterates through a layered chart & flags per usual
    '''


# NOTE NEED TO CHECK ALL CONFIGS (encoding, local & global)
# https://altair-viz.github.io/user_guide/configuration.html

def call_recurse(configs, keys):
    '''
    '''
    check_dict = {}
    recusive_find(configs, keys, check_dict)
    return check_dict


def recusive_find(configs, keywords, check_dict, prefix=None):
    '''
    '''
    for k, v in configs.items():
        if any(word in k for word in keywords[0]) and k not in keywords[1]:
            if prefix:
                if prefix in check_dict.keys():
                    check_dict[prefix][k] = v
                else:
                    check_dict[prefix] = {k: v}
            else:
                check_dict[k] = v
        elif isinstance(v, dict):
            recusive_find(v, keywords, check_dict, k)


KEYWORD_DICT = {'font': (['font', 'Font'], []),
                'color': (['color', 'fill', 'range', 'background'], ['filled'])}

def run_lint(chart_obj, word_dict=KEYWORD_DICT):
    '''
    Takes an Altair chart object and flags accessibility issues
    '''
    all_issues = {}
    chart_specs = chart_obj.to_dict()['config']
    font_dict = call_recurse(chart_specs, word_dict['font'])
    color_dict = call_recurse(chart_specs, word_dict['color'])
    all_issues['color'] = cr.check_all_color(color_dict)
    #all_issues['font'] = fr.check_all_font(font_lst)
    return all_issues
