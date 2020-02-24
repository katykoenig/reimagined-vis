'''
File with main accessible visualization linters

'''
import altair as alt
import pandas as pd
import font_rules as fr


### Helper Fns ###
def iterate_on_layers(chart_objs):
    '''
    Iterates through a layered chart & flags per usual
    '''


# NOTE NEED TO CHECK ALL CONFIGS (encoding, local & global)
# https://altair-viz.github.io/user_guide/configuration.html


def run_lint(chart_obj):
    '''
    Takes an Altair chart object and flags accessibility issues
    '''
    print('anything')
    chart_specs = chart.to_dict()['config']
    for key, val in chart_specs.items():
        print(key)
        if 'fontSize' in val:
            test = fr.check_font_size(val)
    return test
