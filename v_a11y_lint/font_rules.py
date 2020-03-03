'''
Functions to check for accessible fonts & font sizes
'''
import altair as alt
import util_fns


def check_title(chart_obj):
    '''
    Checks to see if chart has title

    Inputs:
        chart_obj: Altair chart object

    Outputs: string with title issue (if relevant)
    '''
    if type(chart_obj.title) == alt.utils.schemapi.UndefinedType:
        return 'chart needs title'


def check_font_size(font_size_dict, thres=16):
    '''
    Checks that all fonts are above a threshold value
    Note:
        threshold value of 16 = 1.2 em, this is the guideline set by WCAG 2.0

    Inputs:
        font_size_dict: dictionary with all font aspects to be checked
        thres: int representing min. font size

    Outputs: string with size issue (if relevant)
    '''
    for key, val in font_size_dict.items():
        if 'Size' in key:
            if int(font_size_dict[key]) < 16:
                return 'font size too small'


def check_title_length(title, min_len=10):
    '''
    Checks if chart has descriptive title

    Inputs:
        title(str): chart's type
        min_len(int): min. desired length of titles

    Outputs: string with title issue (if relevant)
    '''
    if len(title) < min_len:
        return 'chart title lacks description'


def check_all_font(font_dict):
    '''
    Checks all fonts in a chart to ensure that font size and title
    combinations are accessible

    Inputs:
        font_dict: a dictionary of the chart's font features to be checked

    Output: a dictionary representing the font issues of the chart
    '''
    issues = {}
    for key, val in font_dict.items():
        if isinstance(val, dict):
            for k, v in val.items():
                if 'Size' in k:
                    check = check_font_size(val)
                    if check:
                        issues[key] = {k: check}
        else:
            title_issue = check_title_length(font_dict['title'])
            if title_issue:
                issues['title length'] = title_issue
    return issues
