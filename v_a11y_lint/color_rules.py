'''
Functions to check for accessible colors & color maps
'''
from itertools import combinations
import json

COLOR_MAP_INFO = ['color-maps/vega-schema.json', 
                  'color-maps/colormap.json',
                  'color-maps/interpColorMaps.json',
                  'color-maps/basic_colors.json']


def get_rgb(hex_num):
    '''
    Takes a hex and converts it to RGB color values
    '''
    only_num = hex_num[1:]
    return tuple(int(only_num[i:i+2], 16) for i in (0, 2, 4))


def get_luminence(rgb_tup):
    '''
    Calculates luminence number for RBG color value
    '''
    return 0.2126 * rgb_tup[0] + 0.7152 * rgb_tup[1] + 0.0722 * rgb_tup[2]


def color_check(color):
    '''
    '''
    if color[0] == '#':
        return get_rgb(color)
    else:
        return color


def calc_color_contrast(color_tup):
    '''
    Calculates the color constrast between two colors
    '''
    for i, color in enumerate(color_tup):
        rgb_color = color_check(color)
        lum = get_luminence(rgb_color)
        if i == 0:
            num = lum + 0.05
        else:
            denom = lum + 0.05
    return num / denom


def check_lumin(color_tup, thres=7):
    '''
    Checks luminence of two colors to ensure that their
    contrast above threshold value
    
    Inputs:
        specs_dict['config']['text']['color']
        specs_dict['config']['background']
    '''
    contrast = calc_color_contrast((color_tup[0], color_tup[1]))
    if contrast < thres:
        return 'colors too similar'


def translate_color(pal_str, color_jsons=COLOR_MAP_INFO):
    '''
    Converts named color palette to list of hex numbers

    Inputs:
        pal_str: name of palette to be converted
        color_jsons: list of jsons with color map info

    Outputs: list of hex numbers as strings
    '''
    all_info = {}
    for i_json in color_jsons:
        with open(i_json) as f:
            all_info.update(json.load(f))
    return all_info[pal_str]


def check_palette(color_range, thres=2):
    '''
    Checks color palette to ensure that contrast of all
    colors above threshold value
    
    Input:
        specs_dict['config']['range']
    '''
    issues = {}
    for pal_type, palette in color_range.items():
        if type(palette) == str:
            palette = translate_color(palette)
        # for palette may want to use a distance formula instead of lumin contrast
        # Read this: https://gramaz.io/pdf/gramazio-2016-ccd.pdf
        issues_set = set([check_lumin(x, thres) for x in \
                           combinations(palette, 2)])
        issues_set.discard(None)
        issues[pal_type] = issues_set
    return issues


def check_all_color(chart_configs):
    '''
    '''
    issues = {}
    for key, val in chart_configs.items():
        issues.update(check_palette(chart_configs['range']))
        issues['text to background'] = {check_lumin((chart_configs['background'],
                      chart_configs['text']['color']), 4.5)}
        # issues['title color to background'] = {check_lumin((chart_configs['background'],
        #               chart_configs['title']['color']), 4.5)}
    return issues



# want 7:1 for text

# right now, it's linting a theme, not the actual chart itself
# i.e. it is linting all possibilities not what is actually being produced
# like all the color maps, even if none are used

# TODO: figure out what from config actually shown & only print errors w/r/t those aspects
# TODO: have it automatically add in defaults if not specified in theme
# TODO: add other color maps, e.g. magma, viridis, and plain colors, e.g. 'darkblue'