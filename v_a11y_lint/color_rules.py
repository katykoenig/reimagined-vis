'''
Functions to check for accessible colors & color maps
'''
from ast import literal_eval
from itertools import combinations
import json
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import XYZColor, sRGBColor, LabColor
from colormath.color_conversions import convert_color


COLOR_MAP_INFO = ['color-maps/vega-schema.json', 
                  'color-maps/colormap.json',
                  'color-maps/interpColorMaps.json',
                  'color-maps/basic_colors.json']

DEFAULT_COLORS = {'categorical': 'tableau10',
                  'ordinal': 'blues',
                  'quantitative': 'viridis',
                  'temporal': 'viridis',
                  'ramp': 'blues'
                   }


def grab_default(scale_type, defaults=DEFAULT_COLORS):
    '''
    Grabs the default color/color scheme for Altair if one not
    explicitly stated in chart's configurations

    Inputs:
        scale_type(str): type of color scale to be used
        defaults: a dictionary mapping type of color scale to default scale used

    Outputs: a list of hex strings representing the scale's color
    '''
    return translate_color(defaults[scale_type])


def get_rgb(hex_num):
    '''
    Takes a hex and converts it to RGB color values

    Input:
        hex_num(str): hex number of a color

    Output: tuple representing the rgb code of a color
    '''
    only_num = hex_num[1:]
    return tuple(int(only_num[i:i + 2], 16) for i in (0, 2, 4))


def get_luminence(rgb_tup):
    '''
    Calculates luminence number for RBG color value

    Input:
        rgb_tup: tuple representing the rgb code of a color

    Output: float of the luminence of a oclor
    '''
    return 0.2126 * rgb_tup[0] + 0.7152 * rgb_tup[1] + 0.0722 * rgb_tup[2]


def color_check(color):
    '''
    Checks to ensure color in rgb tuble and converts if not

    Input:
        color: string representing a color

    Output: an rgb tuple representation of the color
    '''
    if color[0] == '#':
        return get_rgb(color)
    elif color[0] == 'r':
        return literal_eval(color[3:])
    else:
        color = translate_color(color)
        return color_check(color)


def check_distance(color_tup, thres=2.3):
    '''
    Checks distance between two colors to ensure just-noticeable difference
    requirement met

    Inputs:

    Outputs:
    '''
    if calc_color_dist(color_tup) < thres:
        return 'colors too similar'


def calc_color_dist(color_tup):
    '''
    '''
    color1 = rgb2lab(color_tup[0])
    color2 = rgb2lab(color_tup[1])
    return delta_e_cie2000(color1, color2)


def rgb2lab(color):
    '''
    Converts from rgb color to Lab color
    '''
    color = color_check(color)
    rgb = sRGBColor(color[0], color[1], color[2])
    return convert_color(rgb, LabColor)


def calc_color_contrast(color_tup):
    '''
    Calculates the color constrast between two colors

    Inputs:
        color_tup: a tuple of two hex colors

    Outputs: a float representing the contrast between the two colors
    '''
    for i, color in enumerate(color_tup):
        rgb_color = color_check(color)
        lum = get_luminence(rgb_color)
        if i == 0:
            num = lum + 0.05
        else:
            denom = lum + 0.05
    return num / denom


def check_dist(color_tup, thres, pair_type):
    outcome = 0
    if pair_type == 'text':
        outcome = calc_color_contrast(color_tup)        
    elif pair_type == 'palette':
        outcome = calc_color_dist(color_tup)
    if outcome < thres:
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
            raw_json = json.load(f)
            for k, v in raw_json.items():
                all_info[k.lower()] = v
    return all_info[pal_str]


def check_palette(color_range, thres=4.6):
    '''
    Checks color palette to ensure that contrast of all
    colors above threshold value
    2.3 thres = JND (just noticeable difference for people w/o vision disability)
    I doubled it b/c IDK (really difficult to find info re. low vision users)
    
    Input:
        specs_dict['config']['range']

    Output: a dictionary mapping the palette type to issues (if any)
    '''
    issues = {}
    for pal_type, palette in color_range.items():
        if type(palette) == str:
            palette = translate_color(palette)
        issues_set = set([check_dist(x, thres, 'palette') for x in \
                           combinations(palette, 2)])
        issues_set.discard(None)
        issues[pal_type] = issues_set
    return issues
    

def check_all_color(color_dict):
    '''
    Checks all colors in a chart to ensure that color
    combinations are accessible

    Inputs:
        color_dict: a dictionary of the chart's color features to be checked

    Output: a dictionary representing the color issues of the chart
    '''
    # instead of feeding in specific keys instead it would be better to abstract
    # and maybe recursively iterate into chart to pull anything w/ color

    issues = {}
    for key, val in color_dict.items():
        if key == 'range':
            issues.update(check_palette(color_dict[key]))
        issues['text to background'] = {check_dist((color_dict['background'],
                      color_dict['text']['color']), 4.5, 'text')}
        issues['title color to background'] = {check_dist((color_dict['background'],
                      color_dict['title']['color']), 4.5, 'text')}
    return issues





# right now, it's linting a theme, not the actual chart itself
# i.e. it is linting all possibilities not what is actually being produced
# like all the color maps, even if none are used
# TODO: figure out what from config actually shown & only print errors w/r/t those aspects
# TODO: have it automatically add in defaults if not specified in theme