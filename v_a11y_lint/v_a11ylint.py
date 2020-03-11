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


RECOMMENDATIONS = {
      "font size too small": "16px or higher",
      "chart needs title": "descriptive title (10+ chars)",
      "chart title lacks description": "descriptive title (10+ chars)",
      "palette": "colors not perceivably different (see CIEDE2000)",
      "colors too similar": "not enough contrast between colors - min. 4.5:1 needed"
    }


def fill_default(chart_specs, default_dict=ALTAIR_DEFAULTS):
    '''
    Inputs missing chart info w/ default Altair settings

    Inputs:
        chart_specs: dictionary representation of Altair chart obj.
        default_dict: dictionary of default config values for Altair charts

    Outputs: updated dictionary represention of Altair chart obj.
    '''
    for attribute, default in default_dict.items():
        if attribute not in chart_specs.keys():
            chart_specs['config'][attribute] = default
    return chart_specs


def pretty_print(issues_dict, verbose=False, d=0, prefix=None,
                 verb_dict=RECOMMENDATIONS):
    '''
    Prints an easily readable representation of accessbility issues for a chart

    Inputs:
        issue_dict: dictionary of issues in linted chart
        verbose(bool): if recommended fixes should also be printed
        d: int determining how far indented nested issues should print
        prefix: None or str representing overall issue name
        verb_dict: dictionary mapping recommended issue fixes to issue names

    Oututs: None (prints relevant strings)
    '''
    if not issues_dict or len(issues_dict) == 0:
        print("\t" * d, "-")
    else:
        for key, val in issues_dict.items():
            if isinstance(val, dict):
                tabs = "\t" * d
                print(f"{tabs}", key + ":")
                pretty_print(val, verbose, d+1, prefix=key)
            else:
                if verbose:
                    if key in verb_dict.keys():
                        descript = verb_dict[key]
                    elif prefix in verb_dict.keys():
                        descript = verb_dict[prefix]
                    else:
                        descript = verb_dict[val]
                    tabs = "\t" * d
                    print(f"{tabs}" f"{key}:", f"{val}\n {tabs} " + \
                         f"Recommendation: {descript}")
                else:
                    print("\t" * d, f"{key}:", f"{val}")


KEYWORD_DICT = {'font': (['font', 'Font', 'title'], []),
                'color': (['color', 'fill', 'range', 'background'], ['filled'])}

def run_lint(chart_obj, verbose=False, word_dict=KEYWORD_DICT):
    '''
    Takes an Altair chart object and flags accessibility issues

    Inputs:
        chart_obj: an Altair chart obj
        verbose(bool): if recommended fixes should also be printed
        word_dict: dictionary mapping keywords of issues to be linted to
                   relevant words in chart obj's dictionary representation

    Returns: dictionary of accessibility issues in chart obj
             also prints a prettified version of this dictionary
    '''
    all_issues = {}
    chart_specs = chart_obj.to_dict()
    chart_specs['config'] = fill_default(chart_obj.to_dict())
    font_dict = util_fns.call_recurse(chart_specs, word_dict['font'])
    #color_dict = util_fns.call_recurse(chart_specs, word_dict['color'])
    #color_issues = cr.check_all_color(color_dict)
    # if color_issues:
    #     all_issues['color'] = color_issues
    font_issues = fr.check_all_font(font_dict)
    if font_issues:
        all_issues['font'] = font_issues
    title_check = fr.check_title(chart_obj)
    if title_check:
        all_issues['title'] = title_check
    if not all_issues:
        return 'Visualization is Accessible!'
    # pretty_print(all_issues, verbose)
    return all_issues, font_dict
