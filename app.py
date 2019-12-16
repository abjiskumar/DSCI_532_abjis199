import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import vega_datasets
from altair import datum
import altair as alt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, assets_folder='assets',
                external_stylesheets=[dbc.themes.CERULEAN])
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Dash App For DSCI - 532'

# Tab 1


def chart1_1():
    """
    To make a box plot that shows the range of bikes rented in London over different seasons across a range of years
    ----------------
    Returns:
    Returns a box plot that shows the required data

    """
    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 14,
                    "font": font,
                    "anchor": "start",  # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300,
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    # "domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 10,
                    "labelAngle": 0,
                    "tickColor": axisColor,
                    "tickSize": 5,  # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 12,
                    "titlePadding": 10,  # guessing, not specified in styleguide
                    "title": "X Axis Title (units)",
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 10,
                    "labelAngle": 0,
                    # "ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 12,
                    "titlePadding": 10,  # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)",
                    # titles are by default vertical left of axis so we need to hack this
                    # "titleAngle": 0, # horizontal
                    # "titleY": -10, # move it up
                    # "titleX": 18, # move it to the right so it aligns with the labels
                },
            }
        }

    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)

    # enable the newly registered theme
    alt.themes.enable('mds_special')
    from vega_datasets import data

    london_data = pd.read_csv('data/london_merged_cleaned.csv')

    p1 = alt.Chart(london_data).mark_boxplot().encode(
        x='weather_code:O',
        y='cnt',
        color='season:N',
        column='Year'
    ).properties(
        width=400,
        height=700
    )

    return p1


# Tab 2
def chart2_1():
    """
    To show the variation in the usage of bikes according to changes in season and hour of the day
    ----------------
    Returns:
    Returns a multi-line graph

    """

    london_data = pd.read_csv('data/london_merged_cleaned.csv')

    highlight = alt.selection(type='single', on='mouseover',
                              fields=['season'], nearest=True)

    base = alt.Chart(london_data).encode(
        x='Time:Q',
        y='cnt:Q',
        color=alt.condition(highlight, 'season:N', alt.value("lightgray"))
    )

    points = base.mark_circle().encode(
        opacity=alt.value(0)
    ).add_selection(
        highlight
    ).properties(

        width=800,
        height=800

    )

    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(1), alt.value(3))
    )

    return points + lines


tabs_styles = {
    'height': '30px',
    'width': '1500px',
    'marginLeft': 20
}

tab_selected_style = {
    'borderTop': '1px solid #d1abab',
    'padding-left': '5px',
    'padding-bottom': '100px',
}

footer = dcc.Markdown('''\* Note  - **The first graph gives information about the bikes shared over different weathers across years**, 
                        \n **The second graph gives information on the trend of bike sharing over different hours of the day across seasons** ''', style={'font-size': '12px'})

app.layout = html.Div([


    html.Div([dbc.Jumbotron([
        dbc.Container([
                      html.H2(
                          "London Bike Sharing Trends Across Seasons and Weathers"),
                      dcc.Markdown('''
                    This dashobard gives an overview of the trends on how bikes are shared in London over different weathers and seasons.
    '''), ],  # fluid=True,
                      )],
        fluid=True,

    ),
    ]),

    html.Div([
        # Add Tabs to the top of the page
        dcc.Tabs(id='tabs', value='tab-1', children=[
            dcc.Tab(label='Weather and Seasons', value='tab-1'),
            dcc.Tab(label='Hour of the Day and Seasons', value='tab-2'),
        ], style=tabs_styles),

        html.Div(id='tabs-content-example')
    ])
])


# Function to update tabs on clicking
@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs', 'value')])
def render_content(tab='tab-1'):
    """
    """
    if tab == 'tab-1':
        return html.Div([
            html.H2('Trends of bike share through weathers ',
                    style={'font-family': 'arial', 'font-size': '20px', 'padding-left': '400px', 'padding-top': '50px'}),

            html.P('The weather in London can get very unpredictable and it can impact many systems in place. \
            The bike sharing facility in London also varies with this weather. \
            The graphs in this section will help get an understanding of the same.',
                   style={'font-family': 'arial', 'font-size': '16px', 'padding-left': '100px', 'padding-bottom': '40px',
                          'color': 'black'}),

            html.Div([
                html.Iframe(
                    sandbox='allow-scripts',
                    id='plot1',
                    height='400',
                    width='800',
                    style={'border-width': '0'},
                    # The magic happens here
                    srcDoc=open('chart.html').read()
                    # The magic happens here
                )],
                style={'display': 'inline-block',
                       'width': '58%', 'border-width': '0'}
            )
        ], style=tab_selected_style)
    elif tab == 'tab-2':
        return html.Div([
            html.H2('Season and Hour of the Day',
                    style={'font-family': 'arial', 'font-size': '20px', 'padding-left': '400px', 'padding-top': '50px'}),
            html.P('',
                   style={'font-family': 'arial', 'font-size': '16px', 'padding-left': '100px', 'padding-bottom': '40px',
                          'color': 'black'}),
            html.Iframe(
                sandbox='allow-scripts',
                id='plot',
                height='700',
                width='1300',
                style={'border-width': '0'},
                # The magic happens here
                srcDoc=open('chart_2.html').read()
                # The magic happens here
            ),
            footer
        ], style={'borderTop': '1px solid #d6d6d6', 'padding-left': '5px'})

if __name__ == '__main__':
    app.run_server(debug=True)
