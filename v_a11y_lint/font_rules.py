'''
Functions to check for accessible fonts & font sizes
'''
import util_fns

DEFAULT_FONT_INFO = {'fontSize': 11,
                     'fontWeight': {"normal": 400,
                                    "bold": 700},
                     'font': 'Helvetica Neue'
                     }

def check_font_size(font_size_dict, thres=16):
    '''
    Checks that all fonts are above a threshold value
    (Set at 16 b/c that's 1.2 em <- used by WCAG)
    '''
    for key, val in font_size_dict.items():
        if 'Size' in key:
            if int(font_size_dict[key]) < 16:
                return 'font size too small: font should be at least 16px'



def check_title(chart_obj, min_len):
    '''
    Checks if chart has (useful) title
    '''
    if type(chart_obj.title) == alt.utils.schemapi.UndefinedType:
        return 'Missing chart title'
    elif len(chart_obj.title) < min_len:
        return 'Chart title lacks description'


def check_all_font(font_dict):
    '''
    '''
    issues = {}
    for key, val in font_dict.items():
        for k, v in val.items():
            if 'Size' in k:
                check = check_font_size(val)
                if check:
                    issues[key] = {k: check}
    return issues
