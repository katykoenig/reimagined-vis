'''
File with main accessible visualization linters

'''
from ast import literal_eval
import font_rules as fr
import color_rules as cr
import util_fns

ALTAIR_DEFAULTS = {
    'background': 'white',
    'text': {'font': 'Helvetica Neue',
             'color': '#000000',
             'fontSize': 11},
    'title': {'color': '#000000',
              'fontSize': 11},
    'text': {'color': '#000000',
             'fontSize': 11,
             'fontWeight': 400,
             'baseline': 'top',
             'filled': True,
             'lineBreak': '\n'},
    'range': {'category': 'tableau10',
                  'ordinal': 'blues',
                  'quantitative': 'viridis',
                  'temporal': 'viridis',
                  'ramp': 'blues'},
    'legend': {'titleFontSize': 11},
    'bar': {'fill': '#4E79A7'},
    'line': {'strokeWidth': 3},
    'axisY': {'grid': True,
              'gridColor': 'lightgray',
              'gridWidth': 1,
              'gridOpacity': 1,
              'labelFontSize': 10,
              'tickSize': 6,
              'titleFontSize': 11},
    'axisX': {'grid': True,
              'gridColor': 'lightgray',
              'gridWidth': 1,
              'gridOpacity': 1,
              'tickSize': 6,
              'labelFontSize': 10,
              'titleFontSize': 11}
                   }


def fill_default(chart_specs, default_dict=ALTAIR_DEFAULTS):
    '''
    Inputs missing chart info w/ default Altair settings
    '''
    for attribute, default in default_dict.items():
        if not attribute in chart_specs.keys():
           chart_specs['config'][attribute] = default
    return chart_specs


    # {'title': {'font': 'Futura',
    #   'fontSize': 18,
    #   'anchor': 'middle',
    #   'color': 'darkblue'},
    #  'axisX': {'grid': False,
    #   'tickSize': 6,
    #   'labelFontSize': 10,
    #   'titleFontSize': 12},
    #  'axisY': {'labelFontSize': 10, 'tickSize': 6, 'titleFontSize': 12},


### Helper Fns ###
def iterate_on_layers(chart_objs):
    '''
    Iterates through a layered chart & flags per usual
    '''


# NOTE NEED TO CHECK ALL CONFIGS (encoding, local & global)
# https://altair-viz.github.io/user_guide/configuration.html


KEYWORD_DICT = {'font': (['font', 'Font', 'title'], []),
                'color': (['color', 'fill', 'range', 'background'], ['filled'])}

def run_lint(chart_obj, word_dict=KEYWORD_DICT):
    '''
    Takes an Altair chart object and flags accessibility issues
    '''
    all_issues = {}
    chart_dict = chart_obj.to_dict()
    chart_specs = fill_default(chart_dict)
    font_dict = util_fns.call_recurse(chart_specs, word_dict['font'])
    color_dict = util_fns.call_recurse(chart_specs, word_dict['color'])
    color_issues = cr.check_all_color(color_dict)
    if color_issues:
        all_issues['color'] = cr.check_all_color(color_dict)
    font_issues = fr.check_all_font(font_dict)
    if font_issues:
        all_issues['font'] = font_issues
    title_check = fr.check_title(chart_obj)
    if title_check:
        all_issues['title'] = title_check
    if not all_issues:
        return 'Visualization is Accessible!'
    return all_issues
