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


def make_basic_bar(title=False, source=make_small_df()):
    chart = alt.Chart(source).mark_bar().encode(
        x='a',
        y='b'
    )
    if title:
        chart.title = title
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


def bad_theme():
    return {
    "config": {
            "title": {
                "font": "Futura",
                "fontSize": 12,
                "anchor": "middle",
                "color": '#F5F5F5',
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
        "background": '#F5F5F5',
        "text": {
               "color": "#D3D3D3",
               "fontSize": 10,
               "fontWeight": 400,
            "baseline": "top",
            "filled": True,
            "lineBreak": "\n",
           },
            "bar": {
                "fill": "DarkGrey"
            },
            "line": {
               "strokeWidth": 3,
           },
        "range": {
                "category": "ylorrd",
                "diverging": "blueorange",
            "ramp": "ylorrd",
            "ordinal": "ylorrd",
            "heatmap": "viridis"
            },
        "legend": {
                "titleFontSize": 12
            }
    },
    }


def better_theme():
    return {
    "config": {
            "title": {
                "font": "Futura",
                "fontSize": 18,
                "anchor": "middle",
                "color": '#800000',
            },
         "axisX": {
                "grid": False,
                "tickSize": 6,
             "labelFontSize": 16,
             "titleFontSize": 16,
         },
        "axisY": {
                "labelFontSize": 16,
                "tickSize": 6,
            "titleFontSize": 16,
         },
        "background": 'white',
        "text": {
               "color": "#D3D3D3",
               "fontSize": 16,
               "fontWeight": 400,
            "baseline": "top",
            "filled": True,
            "lineBreak": "\n",
           },
            "bar": {
                "fill": "DarkGrey"
            },
            "line": {
               "strokeWidth": 3,
           },
        "range": {
                "category": "ylorrd",
                "diverging": "blueorange",
            "ramp": "ylorrd",
            "ordinal": "ylorrd",
            "heatmap": "viridis"
            },
        "legend": {
                "titleFontSize": 12
            }
    },
    }


def best_theme():
    return {
    "config": {
            "title": {
                "font": "Futura",
                "fontSize": 18,
                "anchor": "middle",
                "color": '#800000',
            },
         "axisX": {
                "grid": False,
                "tickSize": 6,
             "labelFontSize": 16,
             "titleFontSize": 16,
         },
        "axisY": {
                "labelFontSize": 16,
                "tickSize": 6,
            "titleFontSize": 16,
         },
        "background": 'white',
        "text": {
               "color": '#800000',
               "fontSize": 16,
               "fontWeight": 400,
            "baseline": "top",
            "filled": True,
            "lineBreak": "\n",
           },
            "bar": {
                "fill": "#003366"
            },
            "line": {
               "strokeWidth": 3,
           },
        "range": {
                "category": "ylorrd",
                "diverging": "blueorange",
            "ramp": "ylorrd",
            "ordinal": "ylorrd",
            "heatmap": "viridis"
            },
        "legend": {
                "titleFontSize": 16
            }
    },
    }

def set_theme(class_theme):
    alt.themes.register("my_custom_theme", class_theme)
    alt.themes.enable("my_custom_theme")

def reset_theme():
    alt.themes.enable('default')



# for non default theme: call set_theme()
# for default theme: reset_theme()
