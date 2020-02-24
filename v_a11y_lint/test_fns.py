'''
Makes test charts for checking linter
'''

import altair as alt
import pandas as pd
from vega_datasets import data


def make_small_df():
    source = pd.DataFrame({
    'a': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
    'b': [28, 55, 43, 91, 81, 53, 19, 87, 52]})
    return source


def make_basic_bar(source=make_small_df()):
    chart = alt.Chart(source).mark_bar().encode(
        x='a',
        y='b'
    )
    return chart


def make_annotated_bar(source=data.barley()):
    bars = alt.Chart(source).mark_bar().encode(
        x=alt.X('sum(yield):Q', stack='zero'),
        y=alt.Y('variety:N'),
        color=alt.Color('site')
    )

    text = alt.Chart(source).mark_text(dx=-15, dy=3, color='white').encode(
        x=alt.X('sum(yield):Q', stack='zero'),
        y=alt.Y('variety:N'),
        detail='site:N',
        text=alt.Text('sum(yield):Q', format='.1f')
    )
    return bars + text


def class_theme():
    main_palette = ["#385ed4","#55b748","#db2b27","#b589da",
                    "#b75f31","#1696d2","#fdbf11","#ff1ae4"]
    sequential_palette = ["#cfe8f3","#aaecff","#a2d4ec","#73bfe2", 
                          "#46abdb","#1696d2","#12719e","#0a4c6a","#062635"]
    return {
    "config": {
            "title": {
                "font": "Futura",
                "fontSize": 18,
                "anchor": "middle",
                "color": "darkblue",
            },
         "axisX": {
                "grid": False,
                "tickSize": 6,
             "labelFontSize": 10,
             "titleFontSize": 12,
         },
        "axisY": {
                "labelFontSize": 10,
                "tickSize": 6,
            "titleFontSize": 12,
         },
        "background": "#FFFFFF",
        "text": {
               "color": "#686863",
               "fontSize": 10,
               "fontWeight": 400,
            "baseline": "top",
            "filled": True,
            "lineBreak": "\n",
           },
            "bar": {
                "fill": "#1696d2"
            },
            "line": {
               "strokeWidth": 3,
           },
        "range": {
                "category": main_palette,
                "diverging": "blueorange",
            "ramp": sequential_palette,
            "ordinal": sequential_palette,
            "heatmap": sequential_palette
            },
        "legend": {
                "titleFontSize": 12
            }
    },
    }

def set_theme():
    alt.themes.register("my_custom_theme", class_theme)
    alt.themes.enable("my_custom_theme")

def reset_theme():
    alt.themes.enable('default')
