import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly import graph_objects as go
import pandas as pd
import plotly.io as pio
import page_utilities.page_utilities as pg_utils
import json

pg_utils = pg_utils.PageUtilities()

dash.register_page(__name__, path='/contact', name='Contact')

layout = dbc.Container(
    children=[
        html.H1("Ready to Do More with your Data?", className='display-1'),
        html.Br(),
        html.H3("Contact ATB Analytics Group"),
        html.Br(),
        html.P(
            children=[
                """
                Let us know what it is that you are looking to achieve. Do you need help with your data strategy and analytics? 

                Does your Dashboard need an updated design and branding refresh to truly show your boss what is needed to grow? 

                Do you need both, or are you unsure? 

                Let's connect, and see how we can help.
 
            """,

            ],

        ),

        dcc.Link("ATB Analytics Group", href='https://atb-analytics-group.webflow.io/#call-to-action'),
        html.Br(),
    ]
)

