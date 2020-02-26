'''
Functions to check for accessible fonts & font sizes
'''

DEFAULT_FONT_INFO = {'fontSize': 11,
                     'fontWeight': {"normal": 400,
                                    "bold": 700},
                     'font': 'Helvetica Neue'
                     }

def check_font_size(config_val, thres=16):
    '''
    Checks that all fonts are above a threshold value
    (Set at 16 b/c that's 1 em <- used by WCAG)
    '''
    for key, val in config_val.items():
        if 'fontSize' in key:
            if config_val[key] < 16:
                return 'font size too small: font should be at least 16px'



def check_title(chart_obj, min_len):
    '''
    Checks if chart has (useful) title
    '''
    if type(chart_obj.title) == alt.utils.schemapi.UndefinedType:
        return 'Missing chart title'
    elif len(chart_obj.title) < min_len:
        return 'Chart title lacks description'


def check_all_font(chart_configs):
    '''
    '''
    print('do something')
