'''
Functions to check for accessible colors & color maps
'''
from ast import literal_eval
from itertools import combinations
import json
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import XYZColor, sRGBColor, LabColor
from colormath.color_conversions import convert_color
import util_fns


COLOR_MAP_INFO = ['../v_a11y_lint/color-maps/vega-schema.json', 
                  '../v_a11y_lint/color-maps/colormap.json',
                  '../v_a11y_lint/color-maps/interpColorMaps.json',
                  '../v_a11y_lint/color-maps/basic_colors.json']


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

    Output: float of the luminence of a color
    '''
    return 0.2126 * rgb_tup[0] + 0.7152 * rgb_tup[1] + 0.0722 * rgb_tup[2]


def color_check(color):
    '''
    Checks to ensure color in rgb tuble and converts if not

    Input:
        color: string representing a color

    Output: an rgb tuple representation of the color
    '''
    if len(color) == 1:
        color = color[0]
    if color[0] == '#':
        return get_rgb(color)
    elif color[0] == 'r':
        return literal_eval(color[3:])
    else:
        color = translate_color(color)
        return color_check(color)


def calc_color_dist(color_tup):
    '''
    Converts colors from rgb color space to L*a*b* color space
    and gets the distance between two colors using CIEDE2000 formula

    Inputs:
        color_tup: a tuple of two colors in their rgb color format

    Outputs: a float representing the distance between two colors
    '''
    color1 = rgb2lab(color_tup[0])
    color2 = rgb2lab(color_tup[1])
    return delta_e_cie2000(color1, color2)


def rgb2lab(color):
    '''
    Converts from hex to rgb color (if necessary) and then to Lab color

    Input:
        color: a tuple or list of the rgb number for a color

    Output: a Lab color space representation of a color
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
    '''
    If a text color, checks the contrast between two colors
    If a color a palette, checks that colors are perceptibly different
    in CieLab color space

    Inputs:
        color_tup: tuple representing two colors
        thres: float or int representing the min. required distance
               between two colors
        pair_type(str): either 'text' or 'palette'

    Output: string representing issue (if any)
    '''
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
    Note:
        2.3 is definited as just noticeable difference (JND)
            for people w/o vision disability
        There no is a JND for low vision viewers, so we somewhat
            arbitrarily chose 4.6 as it is double

    Input:
        color_range: a dictionary of the color palettes for each type of chart
            e.g. {'heatmap': 'viridis'}

    Output: a dictionary mapping the palette type to issues (if any)
    '''
    issues = {}
    for pal_type, palette in color_range.items():
        if type(palette) == str:
            palette = translate_color(palette)
        issues_set = set([check_dist(x, thres, 'palette') for x in \
                           combinations(palette, 2)])
        if None not in issues_set:
            issues[pal_type] = issues_set
        if None in issues_set:
            issues_set.discard(None)
            if len(issues_set) == 1:
                issues[pal_type] = list(issues_set)[0]
            elif len(issues_set) > 1:
                issues[pal_type] = issues_set
    return issues


def check_and_fill(color_tup, issues, key, check_type):
    '''
    Checks issues for a color pair and inputs them into
    the issues dictionary if necessary
    
    Inputs:
        color_tup: tuples of two colors
        issues: dictionary of issues
        key: string representing issue name to be inputted
                    into dictionary if needed
        check_type: string representing if checking a palette or text colors

    Outputs: None, modifies issues dictionary in place
    '''
    if check_type == 'palette':
        # double JND
        thres = 4.6
    if check_type == 'text':
        # from WCAG
        thres = 4.5
    back_text_check = check_dist(color_tup, thres, check_type)
    issues = util_fns.fill_dict(issues, key, back_text_check)


def check_all_color(color_dict):
    '''
    Checks all colors in a chart to ensure that color
    combinations are accessible

    Inputs:
        color_dict: a dictionary of the chart's color features to be checked

    Output: a dictionary representing the color issues of the chart
    '''
    issues = {}
    if 'background' in color_dict.keys():
        background = color_dict['background']
    else: 
        background = '#FFFFFF'
    spec_filled = None
    check_col = None
    for key in color_dict.keys():
        if key in ['axisX', 'axisY']:
            check_and_fill((background, color_dict[key]['color']),
                                     issues, f'{key} to background', 'text')
        if key == 'encoding':
            for key, val in color_dict[key]['color'].items():
                if key == 'value':
                    spec_filled = val
                    check_and_fill((background, spec_filled),
                                     issues, f'{key} to background', 'palette')
                if key == 'condition':
                    check_col = val['value']
                    check_and_fill((background, check_col),
                                     issues, 'encoding to background, ' + \
                                     f'color {check_col}', 'palette')
                if check_col and spec_filled:
                    check_and_fill((spec_filled, check_col), issues,
                                  'specified encoding colors too similar',
                                  'palette')
        if key == 'title':
            title_color = color_dict[key]['color']
            check_and_fill((background, title_color), issues,
                          'title to background', 'text')
        if key == 'text':
            txt_color = color_dict[key]['color']
            check_and_fill((background, txt_color), issues,
                            'text to background', 'text')
        if key == 'config':
            palette_iss = check_palette(color_dict[key]['range'])
            if palette_iss:
                issues['palette'] = palette_iss
        if key == 'bar':
            bar_fill = color_dict[key]['fill'][0].lower()
            check_and_fill((background, bar_fill), issues,
                            'bar fill to background', 'palette')
    return issues
