'''
File with main accessible visualization linters

'''
import font_rules as fr
import color_rules as cr
import util_fns

### Helper Fns ###
def iterate_on_layers(chart_objs):
    '''
    Iterates through a layered chart & flags per usual
    '''


# NOTE NEED TO CHECK ALL CONFIGS (encoding, local & global)
# https://altair-viz.github.io/user_guide/configuration.html


KEYWORD_DICT = {'font': (['font', 'Font'], []),
                'color': (['color', 'fill', 'range', 'background'], ['filled'])}

def run_lint(chart_obj, word_dict=KEYWORD_DICT):
    '''
    Takes an Altair chart object and flags accessibility issues
    '''
    all_issues = {}
    chart_specs = chart_obj.to_dict()
    font_dict = util_fns.call_recurse(chart_specs, word_dict['font'])
    color_dict = util_fns.call_recurse(chart_specs, word_dict['color'])
    all_issues['color'] = cr.check_all_color(color_dict)
    all_issues['font'] = fr.check_all_font(font_dict)
    return all_issues
