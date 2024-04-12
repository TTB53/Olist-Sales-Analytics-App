import json

import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import datetime as dt
import numpy as np
import plotly.io as pio
import page_utilities.page_utilities as pg_utils

pg_utils = pg_utils.PageUtilities()

dash.register_page(__name__,
                   path='/customer-analysis',
                   name='Customers',
                   title='Olist - Customer Analysis', )

"""
Layout for Customer Page
"""
layout = dbc.Container(
    children=[
        html.H1("Customer Insights", className='display-1'),
        html.Br(),
        html.P(
            children=[
                """
                As you go through the customer insights page, there a few things to keep in mind. 

            """,

            ],

        ),
        html.Br(),
        html.Ul(
            children=[
                html.Li(
                    """
                    Olist was founded in Feb 2015, the provided dataset starts in October 2016 however, it has missing
                    data from Nov and has very little data from Dec 2016. That aside, I decided to leave it as it 
                    shows that every dataset has flaws and characteristics that need to be cleansed.
                    """
                ),
                html.Li(
                    """
                    All of the Charts are meant to be interactive. You can hover and 
                    turn things on and off to get a better picture of the data.
                    get more detail by hovering, and when dealing with the top and bottom analysis 
                    you can drill down to into the data 
                    by selecting the category you wish to see.
                    """
                ),
                html.Li(
                    """
                    TODO
                    If trying to predict customers, mention something about that here.
                    """
                )
            ],
        ),
        # dcc.Dropdown(
        #     id='data-load-dropdown',
        #     value="load",
        #     className='hide',
        # ),
        # Customer Seller KPI Row -1
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                                pg_utils.create_kpi_card("cs-total-customers"),
                            ],
                            className='card-group',
                        ),
                    ],
                    width=12,
                    align='center'
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.Div(
                            # id='customer-seller-kpi-card-group-wrapper',
                            children=[
                                pg_utils.create_kpi_card("cs-tot-revenue"),

                                pg_utils.create_kpi_card("cs-avg-clv"),

                            ],
                            className='card-group',
                        )
                    ],
                    width=12,
                    align='center',
                ),
            ],
        ),

        # Customer Seller KPI Row -2
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.Div(
                            # id='customer-seller-kpi-card-group-wrapper',
                            children=[

                                pg_utils.create_kpi_card("cs-avg-review-score"),

                                pg_utils.create_kpi_card("cs-avg-days-to-receive"),

                            ],
                            className='card-group',
                        ),
                    ],
                    width=12,
                    align='center'
                ),

            ]
        ),

        html.Br(),
        html.H2('Where are our Customers Located.', className='display-2'),

        html.Br(),
        dbc.Row(
            children=[
                # html.H5("What states are we shipping the most too.", className='display-5'),
                html.P(
                    """
                    Here is how Olist Customer orders are distributed across Brazil. You can see that there 
                    are a few smaller orders from countries outside of Brazil, such as Portugal and 
                    Argentina. 
                    """
                ),
                html.Ul(
                    children=[
                        html.Li(["With more ", dcc.Link("Marketing", href='http://127.0.0.1:8050/marketing-analysis'),
                                 " data past 2018, I bet that we would see both growth in sellers on the platform,"
                                 " and how that somewhat played into their decisions to acquire a logistics company"
                                 " to help with deliveries, and an ERP company to help owners"
                                 " manage their inventories better."]),
                        html.Li(),
                        html.Li(),
                    ]
                ),
                html.Br(),
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Loading(
                                    dcc.Graph(
                                        id='customers-map',
                                        animate=True,
                                    ),
                                    type='dot', color="AQUAMARINE"
                                )
                            ),
                            className='kpi-card',
                        ),

                    ],
                    width=12
                )

            ],
            align='center'
        ),

        html.Br(),
        html.H2('Top and Bottom Analysis', className='display-2'),
        html.Br(),
        dbc.Row(
            children=[
                # html.H5("What are the top products that our customers ordered.",
                #         className='display-5'),
                html.Br(),
                html.P(
                    """
                    What are the top and bottom products that were ordered from the Olist platform.

                    """
                ),
                html.Br(),

                dbc.Card(
                    dbc.CardBody(
                        children=[
                            html.H6("Select A Value", className='display-6'),
                            html.P("Select a value to see the Top Customers by different categories."),
                            html.Br(),
                            dcc.Slider(
                                id='cs-n-slider',
                                min=0,
                                max=100,
                                step=10,
                                value=10,
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": True
                                }
                            ),
                            html.Br(),
                            html.H6("Select A Option", className='display-6'),
                            html.P("Select an option to view the data by."),
                            html.Br(),
                            dcc.RadioItems(
                                id='cs-n-radioitems',
                                options={
                                    'payment_value': 'Revenue',
                                    # 'seller_id': 'Merchant Count',
                                    # 'customer_unique_id': 'Customer Count',
                                    'freight_value': 'Shipping Cost',
                                    # 'review_score': 'Review Score',
                                    'profit': 'Profit'
                                },
                                value='payment_value',
                                inline=True,
                                persistence=True,

                            ),
                        ]
                    ),
                    className='kpi-card',
                ),

                html.Br(),
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dcc.Loading(
                                        dcc.Graph(
                                            id='cs-top-products',
                                        ),
                                        type='dot', color="AQUAMARINE"
                                    )
                                ]
                            ),
                            className='kpi-card'
                        ),

                    ],
                    width=6
                ),
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Loading(
                                    dcc.Graph(
                                        id='cs-top-customers',
                                    ),
                                    type='dot', color="AQUAMARINE"
                                )
                            ),
                            className='kpi-card'
                        ),

                    ],
                    width=6
                ),
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Loading(
                                    html.Div(
                                        id='cs-customers-pivot-table',
                                    ),
                                    type='dot',
                                    color="AQUAMARINE"
                                )
                            ),
                            className='kpi-card'
                        ),

                    ],
                    width=12
                )

            ],
            align='center'
        ),
        html.Br(),
        html.H2('Cohort Analysis and Segmentation', className='display-2'),
        # html.H5("Separating Customers into groups", className='display-5'),
        dbc.Row(
            children=[
                html.P(
                    """
                    Cohort analysis is an analytical technique that categorizes and divides
                    data into groups with common characteristics prior to analysis. Meaning that you can
                    segment customers into defined groupings based on prior knowledge.
                    \n
                    Cohort analysis helps track that the quality of the customer is improving over time and also
                    helps identify customer churn.
                    """
                ),
                # html.Br(),
                # html.P(
                #     """
                #
                #     """
                # ),
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dbc.Row(
                                        children=[
                                            dbc.Col(
                                                children=[
                                                    html.H3("Choose a Value from the dropdown menu"),
                                                    html.P(
                                                        """
                                                        This is a y value for the cohort analysis
                                                        """
                                                    ),
                                                    dcc.Dropdown(),
                                                ],
                                                width=6,
                                                align='center',
                                            ),
                                            dbc.Col(
                                                children=[
                                                    html.H3("Choose a Value from the dropdown menu"),
                                                    html.P(
                                                        """
                                                        This is a y value for the cohort analysis
                                                        """
                                                    ),
                                                    dcc.Dropdown(),
                                                ],
                                                width=6,
                                                align='center',
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            className='kpi-card',
                        ),
                    ]
                ),

                dbc.Col(
                    children=[
                        pg_utils.create_kpi_card('cohort-avg-price'),
                        pg_utils.create_kpi_card('cohort-retention'),
                        # dbc.Card(
                        #     dbc.CardBody(
                        #         [
                        #             dcc.Loading(
                        #                 dcc.Graph(id='cohort-avg-price', ),
                        #                 type='dot', color="AQUAMARINE"
                        #             )
                        #         ]
                        #     ),
                        #     className='kpi-card'
                        # ),

                    ],
                    width=12,
                ),
            ],
            align='center'
        ),
        html.Br(),
        html.H2('RFM Analysis', className='display-2'),
        # html.H5("How recent, how frequent, and how much.", className='display-5'),
        dbc.Row(
            children=[
                html.P(
                    """
                    Recency, frequency, monetary value (RFM) is a marketing analysis tool used to identify a firm's
                    best clients based on the nature of their spending habits. This helps you better allocate and
                    target the appropriate customer the right way.
                    """
                ),
                html.Br(),
                html.P(
                    """
                    For example, we might want to target our Champions(or top purchasers) with some kind of
                    discount incentive program.
                    """
                ),
                html.Br(),
                dbc.Col(
                    children=[
                        pg_utils.create_kpi_card('rfm-analysis'),
                        # dbc.Card(
                        #     dbc.CardBody(
                        #         dcc.Loading(
                        #             dcc.Graph(
                        #                 id='rfm-analysis',
                        #             ),
                        #             type='dot',
                        #             color="AQUAMARINE"
                        #         )
                        #     ),
                        #     className='kpi-card'
                        # ),

                    ],
                    width=12,
                    align='center'
                )

            ],
            align='center'
        ),
    ],
)


@callback(
    Output('cs-total-customers', 'figure'),
    Output('cs-avg-clv', 'figure'),
    # Output('cs-total-orders', 'figure'),
    Output('cs-tot-revenue', 'figure'),
    Output('cs-avg-review-score', 'figure'),
    Output('cs-avg-days-to-receive', 'figure'),
    # Output('cs-avg-order-value', 'figure'),
    # Output('cs-avg-order-items', 'figure'),
    # Output('cs-purchase-frequency', 'figure'),
    # Output('cs-profit-margin', 'figure'),
    # Output('cs-avg-customer-value', 'figure'),
    Input('data-store', 'data'),
    # prevent_initial_call=True
)
def update_customer_kpis(data):
    # dff = pd.DataFrame(data)
    datasets = json.loads(data)

    dff = pd.read_csv('./data/customers_df.csv')
    customers_by_month = pd.read_json(datasets['customer_by_month_df'])
    top_n_by_month = pd.read_json(datasets['top_n']['month'])
    top_n_by_customer = pd.read_json(datasets['top_n']['customer'])
    seller_cust_pivot_df = pd.read_json(datasets['seller_cust_pivot_df'])

    # TODO Double check that these numbers make senses
    tot_customers = customers_by_month.tot_unique_customers.sum()
    tot_orders = customers_by_month.order_id.sum()
    purchase_frequency = tot_orders / tot_customers
    tot_revenue = customers_by_month.customer_revenue.sum()
    # For Olist specifically this wouldn't really be the expenses but seeing this value could have, and probably was
    # a part of their decision to acquire Pax in 2020. This means that not only did they get the drivers and their
    # network they also pulled this carrier in-house which in theory should help reduce or control their freight
    # expenditures

    # I will use Freight Value to say we will be offering free shipping to all customers during this time.
    tot_expenses = customers_by_month.freight_value.sum()
    profit_margin = (tot_revenue - tot_expenses) / tot_revenue
    tot_items_ordered = customers_by_month.order_item_id.sum()
    avg_items_ordered = tot_items_ordered / tot_orders
    avg_order_value = tot_revenue / tot_orders

    # This isn't really used in this section of the analysis and needs a TODO to be moved to the proper section (marketing)
    repeat_rate = 0
    # repeat_rate_df = dff.groupby('customer_unique_id')['order_id'].count().reset_index()
    # repeat_rate = repeat_rate_df[repeat_rate_df['order_id'] >= 2].shape[0] / tot_customers
    churn_rate = 1 - repeat_rate

    customer_val = (avg_order_value / purchase_frequency) / churn_rate
    customer_lifetime_val = customer_val * profit_margin

    print("Customers by Month Dataframe\n", customers_by_month.head(10))

    # tot_customer_fig = go.Figure()

    # Function values = value, delta, title, rows=1, cols=1, x=[0, 1], y=[0, 1]

    tot_customer_fig = pg_utils.create_indicator_figure(
        value=tot_customers,
        delta=tot_customers,
        title="Total Customers",
        monetary=False
    )

    tot_customer_fig.add_bar(
        x=customers_by_month.order_month_date,
        y=customers_by_month.customer_count,
        opacity=.2,
        row=1,
        col=1,
        name='tot-custs',
        # marker={'line': {'color': '#E4F2EF', 'width': 0.5, }},
        hovertemplate="%{y:,}",
        xaxis='x1',
        yaxis='y1',
    )

    tot_customer_fig.add_bar(
        x=customers_by_month.order_month_date,
        y=customers_by_month.tot_unique_customers,
        opacity=.2,
        row=1,
        col=1,
        # secondary_y=True,
        name='tot_unique_custs',
        hovertemplate="%{y:,}",
        xaxis='x1',
        yaxis='y1',
        # visible='legendonly'
    )

    # tot_customer_fig.add_scatter(
    #     y=customers_by_month.customer_revenue,
    #     x=customers_by_month.order_month_date,
    #     opacity=.2,
    #     row=1,
    #     col=1,
    #     # secondary_y=True,
    #     name='revenue',
    #     hovertemplate="$%{y:,.2f}",
    #     xaxis='x1',
    #     yaxis='y2',
    #     # visible='legendonly',
    # )

    tot_customer_fig.update_layout(
        barmode='group',
    )

    tot_revenue_fig = pg_utils.create_indicator_figure(
        value=tot_revenue,
        delta=tot_revenue,
        title="Total Revenue",
        monetary=False
    )

    tot_revenue_fig.add_bar(
        y=customers_by_month.customer_revenue,
        x=customers_by_month.order_month_date,
        opacity=.2,
        row=1,
        col=1,
        name='revenue',
        hovertemplate="$%{y:,.2f}",
        xaxis='x1',
        yaxis='y1',
    )

    tot_revenue_fig.add_scatter(
        y=customers_by_month.revenue_per_customer,
        x=customers_by_month.order_month_date,
        opacity=.2,
        row=1,
        col=1,
        secondary_y=True,
        name='revenue/cust',
        hovertemplate="$%{y:,.2f}",
        visible='legendonly'
    )

    tot_revenue_fig.add_scatter(
        y=customers_by_month.profit_per_customer,
        x=customers_by_month.order_month_date,
        opacity=.2,
        row=1,
        col=1,
        secondary_y=True,
        name='profit/cust',
        hovertemplate="$%{y:,.2f}",
        # visible='legendonly'
    )

    customer_lifetime_val_fig = pg_utils.create_indicator_figure(
        value=customer_lifetime_val,
        delta=customer_lifetime_val,
        title="Customer Lifetime Value",
        monetary=False
    )

    customer_lifetime_val_fig.add_bar(
        y=customers_by_month.customer_value,
        x=customers_by_month.order_month_date,
        opacity=.2,
        row=1,
        col=1,
        name='cust-value',
        hovertemplate="$%{y:,.2f}",
        xaxis='x1',
        yaxis='y1',
    )

    customer_lifetime_val_fig.add_scatter(
        y=customers_by_month.avg_order_value,
        x=customers_by_month.order_month_date,
        opacity=.2,
        row=1,
        col=1,
        # secondary_y=True,
        name='AoV',
        # visible='legendonly'
    )

    customer_lifetime_val_fig.add_scatter(
        y=customers_by_month.profit_per_customer,
        x=customers_by_month.order_month_date,
        opacity=.2,
        row=1,
        col=1,
        # secondary_y=True,
        name='profit/cust',
        visible='legendonly'
    )

    customer_lifetime_val_fig.add_scatter(
        y=customers_by_month.revenue_per_customer,
        x=customers_by_month.order_month_date,
        opacity=.2,
        row=1,
        col=1,
        # secondary_y=True,
        name='revenue/cust',
        visible='legendonly',
        marker=dict(
            color='#4d675a'
        ),
    )

    avg_review_fig = pg_utils.create_indicator_figure(
        value=customers_by_month.review_score.mean(),
        delta=customers_by_month.review_score.mean(),
        title="Avg Review Score",
        monetary=False
    )

    avg_review_fig.add_bar(
        x=customers_by_month.order_month_date,
        y=customers_by_month.review_score,
        opacity=.2,
        row=1,
        col=1,
        name='review-score',
        hovertemplate="%{y:,.2f}",
        xaxis='x1',
        yaxis='y1',
    )

    avg_review_fig.add_scatter(
        x=customers_by_month.order_month_date,
        y=customers_by_month.review_count,
        opacity=.2,
        row=1,
        col=1,
        secondary_y=True,
        name='review-count',
        hovertemplate="%{y:,.2f}",
        # visible='legendonly'
    )

    customer_shipping_fig = pg_utils.create_indicator_figure(
        value=tot_expenses,
        delta=tot_expenses,
        title="Total Shipping Cost",
        monetary=False
    )

    customer_shipping_fig.add_bar(
        x=customers_by_month.order_month_date,
        y=customers_by_month.freight_value,
        opacity=.2,
        row=1,
        col=1,
        name='shipping cost',
        hovertemplate="$%{y:,.2f}",
        xaxis='x1',
        yaxis='y1',

    )

    customer_shipping_fig.add_scatter(
        x=customers_by_month.order_month_date,
        y=customers_by_month.order2cus_days,
        opacity=.2,
        row=1,
        col=1,
        secondary_y=True,
        name='days to receive',
        hovertemplate="%{y:,}",
        xaxis='x1',
        yaxis='y1',
        visible='legendonly',
    )

    customer_shipping_fig.add_scatter(
        x=customers_by_month.order_month_date,
        y=customers_by_month.on_time_days,
        opacity=.2,
        row=1,
        col=1,
        secondary_y=True,
        name='on time days',
        hovertemplate="%{y:,}",
        xaxis='x1',
        yaxis='y1',
        # visible='legendonly'
    )

    # customer_lifetime_val_fig.add_trace(
    #     go.Indicator(
    #         value=customer_lifetime_val,
    #         number={
    #             'font': {
    #                 'family': 'Bebas Neue',
    #                 'size': 24,
    #             }
    #         },
    #         title={
    #             'text': "Customer Lifetime\nValue\n(CLTV)",
    #             'align': 'center',
    #             'font': {
    #                 'family': 'Bebas Neue',
    #                 'size': 36,
    #             }
    #         },
    #         domain={'x': [0, 1], 'y': [0, 1]}
    #     ),
    # )

    # return tot_customer_fig, tot_revenue_fig, tot_orders_fig, avg_order_val_fig, avg_order_items_fig, purchase_frequency_fig, \
    #        profit_margin_fig, avg_customer_val_fig, customer_lifetime_val_fig

    # Adds Standardization to all the figs that
    figs = [tot_customer_fig, tot_revenue_fig, customer_lifetime_val_fig, avg_review_fig, customer_shipping_fig]
    pg_utils.create_standard_legend(figs)

    return tot_customer_fig, tot_revenue_fig, customer_lifetime_val_fig, avg_review_fig, customer_shipping_fig


@callback(
    Output('customers-map', 'figure'),
    Input('data-store', 'data'),
    # prevent_initial_call=True
)
def update_customer_map(data):
    # geolocation = './data/OListEcomData/olist_geolocation_dataset.csv'
    geolocation = './data/customers_geo_data.csv'
    geo_df = pd.read_csv(geolocation)
    # geo_df.rename(columns={"geolocation_zip_code_prefix": "zip_code"}, inplace=True)
    # dff = pd.DataFrame(data)

    datasets = json.loads(data)

    dff = pd.read_csv('./data/customers_df.csv')

    print(geo_df.head(), dff.head())
    dff = dff[['customer_unique_id', 'zip_code', 'payment_value']]
    dff = dff.groupby('customer_unique_id', as_index=False)['payment_value'].sum()
    dff = dff.merge(geo_df, on='customer_unique_id')
    dff['code'] = "BRA"

    # This keeps all the columns in the dataframe when doing a groupby 'first' is equivalent
    # to 'keep this, and keep it movin' whenever there are no duplicates

    # dff.groupby('zip_code', as_index=False).agg(
    #     {'geolocation_lat': 'first', 'geolocation_lng': 'first', 'geolocation_city': 'first',
    #      'geolocation_state': 'first', 'payment_value': 'sum'})
    # TODO Look into GeoPy package for getting the actual addresses of these places. is that ethical?

    color_series = dff['payment_value'].quantile(0.95)

    # customer_map_fig = go.Figure(
    #     go.Scattermapbox(
    #         lat=dff['geolocation_lat'],
    #         lon=dff['geolocation_lng'],
    #         mode='markers',
    #         text=["Customer has paid a total of ", dff.payment_value],
    #         marker=dict(
    #             color=dff['payment_value'],
    #             # cmin=color_series.min,
    #             # cmax=color_series.max,
    #             colorscale=pio.templates['atbAnalyticsGroupDefault'].layout.colorscale.diverging,
    #             # opacity=.5,
    #             size=10,
    #             sizemin=6,
    #             showscale=True,
    #         ),
    #         name="Amount Spent"
    #     )
    # )

    # customer_map_fig.update_layout(
    #     mapbox_style="stamen-terrain",
    #     autosize=True,
    # )
    # customer_map_fig.update_mapboxes(
    #
    #     bearing=0,
    #     pitch=25,
    #     center={
    #         'lat': dff.geolocation_lat.mode()[0],
    #         'lon': dff.geolocation_lng.mode()[0]
    #     },
    #     zoom=3,
    # )
    # customer_map_fig.update_layout(
    #     margin={"r": 20, "t": 50, "l": 20, "b": 20},
    #     hoverlabel=dict(
    #         bgcolor="#E4F2EF",
    #         bordercolor="#709784",
    #
    #     )

    # customer_map_fig = pg_utils.create_scattergeo_map(dff,
    #                                                   dff['geolocation_lat'],
    #                                                   dff['geolocation_lng'])

    customer_map_fig = pg_utils.create_px_mapbox(dff,
                                                 dff['payment_value'],
                                                 # 8,
                                                 dff['payment_value'] * 3,
                                                 "Customers",
                                                 dff['payment_value'].quantile(0.95),
                                                 mapbox_style='open-street-map'
                                                 )

    # customer_map_fig = go.Figure(go.Scattergeo())
    # customer_map_fig.add_scattergeo(
    #     locations=dff['code'],
    #     locationmode='country names',
    #     lat=dff['geolocation_lat'].astype(float),
    #     lon=dff['geolocation_lng'].astype(float),
    #     mode="markers",
    #     hoverinfo="text",
    #     # marker=dict(
    #     #     color=dff['payment_value'],
    #     #     # colorscale=DIVERGING,
    #     #     cmin=dff['payment_value'].min(),
    #     #     cmax=dff['payment_value'].max() * .95,
    #     #     size=5,
    #     #     colorbar=dict(
    #     #         thickness=10,
    #     #         titleside="right",
    #     #         outlinecolor="rgba(68, 68, 68, 0)",
    #     #         # tickvals=[-50, -30, -15, 0, 15, 30, 50],
    #     #         ticks="outside",
    #     #         ticklen=3,
    #     #         # ticksuffix=" C",
    #     #         showticksuffix="all"
    #     #     )
    #     # ),
    #     # text=["Customer:", dff['customer_unique_id'], " paid an amount of ", dff['payment_value']],
    # )

    # customer_map_fig.add_scattergeo(
    #     # locations=dff['code'],
    #     locationmode='country names',
    #     lat=dff['geolocation_lat'].astype(float),
    #     lon=dff['geolocation_lng'].astype(float),
    #     marker=dict(
    #         color=dff['payment_value']
    #     ),
    #     text=["Customer:", dff['customer_unique_id'], " paid an amount of ", dff['payment_value']],
    # )

    customer_map_fig.update_layout(
        height=800,
        margin={
            "r": 0,
            "t": 0,
            "l": 0,
            "b": 0
        },
        showlegend=True,
    )
    # For ScatterGeo
    # customer_map_fig.update_layout(
    #     geo=dict(
    #         # fitbounds='locations',
    #         resolution=110,
    #         # 'world', 'usa', 'europe', 'asia', 'africa', 'north america', 'south america'.
    #         scope='world',
    #         # 'equirectangular', 'mercator', 'orthographic', 'natural earth', 'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', 'azimuthal equidistant', 'conic equal area', 'conic conformal', 'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer', 'transverse mercator', 'albers usa', 'winkel tripel', 'aitoff' and 'sinusoidal'
    #         projection_type='orthographic',
    #         projection_rotation=dict(lat=dff.geolocation_lat.mode()[0].astype(float),
    #                                  lon=dff.geolocation_lng.mode()[0].astype(float),
    #                                  roll=5,
    #                                  ),
    #         showland=True,
    #         showocean=True,
    #         showlakes=True,
    #         showrivers=True,
    #         showcountries=True,
    #         showframe=True,
    #         showcoastlines=True,
    #         landcolor='#FEFFF1',
    #         countrycolor='#333333',
    #         oceancolor='#E4F2EF',
    #         lakecolor='#E4F2EF',
    #         rivercolor='#E4F2EF',
    #         showsubunits=True,
    #         subunitcolor="Blue",
    #         center=dict(
    #             lat=dff.geolocation_lat.mode()[0],
    #             lon=dff.geolocation_lng.mode()[0]
    #         ),
    #     ),
    # )

    # mapbox=dict(
    #     color=dff['payment_value'],
    #     zoom=5,
    #     pitch=1,
    #     # width=1200,
    #     # height=800,
    #     size=dff['payment_value'],
    #     size_max=20,
    #     hover_name=dff['customer_unique_id'],
    #     title='Customer Orders',
    #     range_color=[0, dff['payment_value'].quantile(0.95)],  # To negate ouliers
    #     color_continuous_scale=pio.templates[
    #         'atbAnalyticsGroupDefault'].layout.colorscale.diverging,
    #     center={
    #         'lat': dff.geolocation_lat.mode()[0],
    #         'lon': dff.geolocation_lng.mode()[0]
    #     },
    # )
    # )

    return customer_map_fig


@callback(
    Output('cs-top-products', 'figure'),
    Output('cs-top-customers', 'figure'),
    # Output('cs-customers-pivot-table', 'children'),
    Input('data-store', 'data'),
    Input('cs-n-slider', 'value'),
    Input('cs-n-radioitems', 'value'),
    # prevent_initial_call=True,
)
def update_cs_n_products_graphs(data, slider_value, radio_value):
    # dff = pd.DataFrame(data)
    datasets = json.loads(data)

    dff = pd.read_csv('./data/customers_df.csv')
    # customers_by_month = pd.read_json(datasets['customer_by_month_df'])
    # top_n_df_by_month = pd.read_json(datasets['top_n']['month'])
    top_n_df_by_product = pd.read_json(datasets['top_n']['product'])
    seller_cust_pivot_df = pd.read_json(datasets['seller_cust_pivot_df'])
    bottom_n_df_by_product = pd.read_json(datasets['top_n']['product'])

    # top_n_df_by_month.sort_values(by=f'{radio_value}', ascending=True),
    top_n_df_by_product.sort_values(by=f'{radio_value}', ascending=False, inplace=True)
    # top_n_df_by_product.reset_index()
    bottom_n_df_by_product.sort_values(by=f'{radio_value}', ascending=True, inplace=True)
    # bottom_n_df_by_product.reset_index()

    print("top products by month\n", top_n_df_by_product.head(slider_value))
    print("bottom products by month\n", bottom_n_df_by_product.head(slider_value))

    top_n_df_by_product = top_n_df_by_product[:slider_value]
    # top_n_df_by_product.sort_values(by=f'{radio_value}', ascending=False, inplace=True)
    bottom_n_df_by_product = bottom_n_df_by_product[:slider_value]

    cs_top_prod_fig = make_subplots(rows=1, cols=1,
                                    specs=[[{"secondary_y": True}]])
    cs_top_prod_fig.add_trace(
        go.Bar(
            y=top_n_df_by_product.product_category_name_english,
            x=top_n_df_by_product[radio_value],
            orientation='h',
            name=f'{radio_value}',
        )
    )

    # Creating the Top Product Bar Graph
    cs_top_prod_fig.add_bar(
        x=top_n_df_by_product.profit,
        y=top_n_df_by_product.product_category_name_english,
        # opacity=.2,
        row=1,
        col=1,
        # secondary_y=True,
        name='profit',
        orientation='h',
        # visible='legendonly'
        # marker={'line': {'color': '#E4F2EF', 'width': 0.5, }},
    )

    cs_top_prod_fig.add_bar(
        x=top_n_df_by_product.freight_value,
        y=top_n_df_by_product.product_category_name_english,
        # opacity=.2,
        row=1,
        col=1,
        # secondary_y=True,
        name='shipping_cost',
        orientation='h',
        # visible='legendonly'
    )
    cs_top_prod_fig.update_layout(
        title=f'Top {slider_value} Products',
        barmode='stack',  # 'stack', 'group', 'overlay', 'relative',
        # clickmode='event+select',
    )
    cs_top_prod_fig.layout.yaxis.title = "Product Category"
    cs_top_prod_fig.layout.hovermode = 'closest'

    # Bottom Product Fields
    cs_bottom_prod_fig = make_subplots(rows=1, cols=1,
                                       specs=[[{"secondary_y": True}]])
    cs_bottom_prod_fig.add_trace(
        go.Bar(
            y=bottom_n_df_by_product.product_category_name_english,
            x=bottom_n_df_by_product[radio_value],
            orientation='h',
            name=f'{radio_value}',
        )
    )

    # adding customers by month bar chart to figure.
    cs_bottom_prod_fig.add_bar(
        x=bottom_n_df_by_product.profit,
        y=bottom_n_df_by_product.product_category_name_english,
        # opacity=.2,
        row=1,
        col=1,
        # secondary_y=True,
        name='profit',
        orientation='h'
        # marker={'line': {'color': '#E4F2EF', 'width': 0.5, }},
    )

    cs_bottom_prod_fig.add_bar(
        x=bottom_n_df_by_product.freight_value,
        y=bottom_n_df_by_product.product_category_name_english,
        # opacity=.2,
        row=1,
        col=1,
        # secondary_y=True,
        name='shipping_cost',
        orientation='h'
    )

    cs_bottom_prod_fig.update_layout(
        title=f'Bottom {slider_value} products',
        barmode='stack',  # 'stack', 'group', 'overlay', 'relative'
    )
    cs_bottom_prod_fig.layout.yaxis.title = "Product Category"

    # Customers Pivot Table Creation

    return cs_top_prod_fig, cs_bottom_prod_fig


@callback(
    Output('cs-customers-pivot-table', 'children'),
    Input('cs-n-radioitems', 'value'),
    Input('data-store', 'data'),
    Input('cs-top-customers', 'clickData'),
    Input('cs-top-products', 'clickData'),
)
def drilldown_customers(radio_value, data, cus_clickData, prod_clickData):
    datasets = json.loads(data)

    seller_cust_pivot_df = pd.read_json(datasets['seller_cust_pivot_df'])
    cs_customers_pivot_table = dash_table.DataTable()

    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == 'cs-top-products' or trigger_id == 'cs-top-customers':
        if trigger_id == 'cs-top-customers':
            clickData = cus_clickData
            seller_cust_pivot_df.sort_values(by='payment_value', ascending=False, inplace=True)
        else:
            clickData = prod_clickData
            seller_cust_pivot_df.sort_values(by='payment_value', ascending=True, inplace=True)

        if clickData is not None:
            product = clickData['points'][0]['label']

            sc_pivot_filtered = seller_cust_pivot_df[seller_cust_pivot_df['product_category_name_english'] == product]

            customers_gby = sc_pivot_filtered.groupby("customer_unique_id").agg({
                # 'order_month_date': 'first',
                # 'seller_id': 'nunique',
                'payment_value': 'sum',
                'freight_value': 'sum',
                'order_item_id': 'sum',
                'review_score': 'mean'

            }).reset_index()

            if trigger_id == 'cs-top-customers':
                customers_gby.sort_values(by=f'{radio_value}', ascending=True, inplace=True)
            else:
                customers_gby.sort_values(by=f'{radio_value}', ascending=False, inplace=True)
            # customers_gby['id'] = customers_gby['customer_unique_id']
            #
            # customers_gby['id'] = customers_gby['customer_unique_id']
            tooltip_header = {
                'payment_value': 'Total Amount of Revenue from this customer',
                # 'Origin supplier': 'Suppliers since 1994',
            }
            tooltip_data = [
                {
                    'payment_value': {
                        'value': f"{row['customer_unique_id']} has purchased a total of ${row['payment_value']} "
                                 f"from OList",
                        'type': 'Markdown'
                    }
                } for row in customers_gby.to_dict('records')
            ]
            # customers_gby = customers_gby.sort_values(by=f"{radio_value}", ascending=False, inplace=True)
            cs_customers_pivot_table = pg_utils.generate_generic_dash_datatable(
                customers_gby,
                'cs-customers-pivot-table',
                tooltip_data,
                # tooltip_header,
            )

            # cs_customers_pivot_table.add_heatmap(
            #     y=customers_gby.order_item_id,
            #     x=customers_gby.order_month_date,
            #     z=customers_gby.payment_value
            # )
            #
            # cs_customers_pivot_table.update_layout(
            #     title=f'{product}'
            # )

            # cs_customers_pivot_table['data'] = customers_gby
        else:
            pass
    else:

        customers_gby = seller_cust_pivot_df.groupby("customer_unique_id").agg({
            # 'order_month_date': 'first',
            # 'seller_id': 'nunique',
            'payment_value': 'sum',
            'freight_value': 'sum',
            'order_item_id': 'sum',
            'review_score': 'mean'

        }).reset_index()
        # customers_gby['id'] = customers_gby['customer_unique_id']
        tooltip_header = {
            'payment_value': 'Total Amount of Revenue from this customer',
            # 'Origin supplier': 'Suppliers since 1994',
        }
        tooltip_data = [
            {
                'payment_value': {
                    'value': f"{row['customer_unique_id']} has purchased a total of ${row['payment_value']} from OList",
                    'type': 'markdown'
                }
            } for row in customers_gby.to_dict('records')
        ]

        customers_gby.sort_values(by=f"{radio_value}", ascending=False, inplace=True)
        cs_customers_pivot_table = pg_utils.generate_generic_dash_datatable(
            customers_gby,
            'cs-customers-pivot-table',
            tooltip_data,
            # tooltip_header
        )
    return cs_customers_pivot_table


# TODO add Axes Title and main header Title to graph. ADD TO CUSTOMERS PAGE
@callback(
    Output('cohort-retention', 'figure'),
    Output('cohort-avg-price', 'figure'),
    Input('data-store', 'data'),
    # prevent_initial_call=True
)
def update_cohort_analysis_graphs(data):
    datasets = json.loads(data)

    # Customers Data for creating a customers cohort
    dff = pd.read_csv('./data/combined_olist_data.csv')

    # Marketing Data for creating a seller's cohort
    mql_df = pd.read_json(datasets['marketing_mql'])
    closed_df = pd.read_json(datasets['marketing_closed_deals'])

    marketing_df = mql_df.merge(closed_df, on='mql_id', how='left')

    # Finding the number of customers that belong to each cohort
    cohortGrouping = dff.groupby(['cohort_month', 'cohort_index'])
    cohortGrouping_df = cohortGrouping['seller_id'].apply(pd.Series.nunique).reset_index()
    cohortGrouping_counts = cohortGrouping_df.pivot(index='cohort_month', columns='cohort_index',
                                                    values='seller_id')
    print(cohortGrouping_counts)

    # Calculating Cohort Retention Rates amoung the cusotmers.
    total_cohort = cohortGrouping_counts.iloc[:, 0]
    retention_cohort = cohortGrouping_counts.divide(total_cohort, axis=0)
    print("Retention Cohort has a type of", type(retention_cohort))
    retention_cohort = retention_cohort.iloc[:, 1:].round(3) * 100
    print(retention_cohort)

    # Calculating Cohort Average Payment Value
    # #TODO turn this into a function that takes 3 col name parameters
    avg_price_cohortGrouping = dff.groupby(['cohort_month', 'cohort_index'])
    avg_price_cohortGrouing_df = avg_price_cohortGrouping['payment_value'].mean().reset_index()
    avg_price_cohort = avg_price_cohortGrouing_df.pivot(
        index='cohort_month',
        columns='cohort_index',
        values='payment_value'
    ).round(1)
    print(avg_price_cohort)

    retention_cohort = retention_cohort.dropna(axis=0, how='all').fillna(0)
    print(retention_cohort.head())
    print("Retention Cohort has a type of", type(retention_cohort))

    retention_cohort_fig = go.Figure()
    retention_cohort_fig.add_trace(
        go.Heatmap(z=retention_cohort.values,
                   x=retention_cohort.index,
                   y=retention_cohort.columns,
                   # text=retention_cohort.values,
                   # texttemplate="%{text}",
                   colorscale=pio.templates['atbAnalyticsGroupDefault'].layout.colorscale.diverging
                   ),
    )

    avg_price_cohort = avg_price_cohort.dropna(axis=0, how='all').fillna(0)
    avg_price_cohort_fig = go.Figure()
    avg_price_cohort_fig.add_trace(
        go.Heatmap(z=avg_price_cohort.values,
                   x=avg_price_cohort.index,
                   y=avg_price_cohort.columns,
                   # text=retention_cohort.values,
                   # texttemplate="%{text}",
                   colorscale=pio.templates['atbAnalyticsGroupDefault'].layout.colorscale.diverging
                   ),
    )

    return retention_cohort_fig, avg_price_cohort_fig


# TODO add Axes Title and main header Title to graph.
# TODO add interactivity to the rfm analysis - instead of monetary change to frequency, or recency
@callback(
    Output('rfm-analysis', 'figure'),
    Input('data-store', 'data'),
    # prevent_initial_call=True
)
def update_rfm_analysis_graph(data):
    datasets = json.loads(data)

    # Customers Data for creating a customers cohort
    dff = pd.read_csv('./data/combined_olist_data.csv')

    # Marketing Data for creating a seller's cohort
    mql_df = pd.read_json(datasets['marketing_mql'])
    closed_df = pd.read_json(datasets['marketing_closed_deals'])

    marketing_df = mql_df.merge(closed_df, on='mql_id', how='left')

    # Calculating the Recency, Frequency and Monetary Value for
    # each customer
    dff['order_purchase_timestamp'] = pd.to_datetime(dff['order_purchase_timestamp'], errors='coerce',
                                                     infer_datetime_format=True)
    today = dff['order_purchase_timestamp'].max()
    print("Today has a datatype of", type(today))

    c_today = dt.datetime.timestamp(today)
    print("Today has a datatype of ", type(today))
    print("Converted Today has a datatype of ", type(c_today))
    print("most_recent_order has a datatype of ", type(dff['most_recent_order'].loc[0]))
    dff['most_recent_order'] = pd.to_datetime(dff['most_recent_order'], errors='coerce',
                                              infer_datetime_format=True).apply(lambda x: pd.to_datetime(x))
    print(type(dff['most_recent_order'].loc[0]))

    # Checking the number of repeat customers. This is good to know so we can tell the sales reps what type of small
    # Businesses we're looking to Target to bring onto the platform.
    repeat_rate_df = dff.groupby('customer_unique_id')['order_id'].count().reset_index()

    # TODO Should this be the basis for the RFM analysis?
    rrdf = repeat_rate_df[repeat_rate_df['order_id'] > 1]  # Only the Orders that are greater than 1.
    repeat_percent = rrdf['order_id'].sum() / repeat_rate_df['order_id'].sum()
    print("Percent of repeat customers ", repeat_percent * 100)

    # repeat_rate = sum of cust order 2+ times/ sum of cust order 1+ times (tot customers)
    repeat_rate = rrdf['order_id'].count() / repeat_rate_df['order_id'].count()
    churn_rate = 1 - repeat_rate

    rfm_s = dff[['customer_unique_id', 'most_recent_order', 'order_id', 'payment_value']]
    rfm = rfm_s.groupby('customer_unique_id').agg(
        {
            'most_recent_order': lambda day: (today - day.max()).days,
            'order_id': lambda num: num.count(),
            'payment_value': lambda pv: pv.sum()
        })

    rfm_cols = ['recency', 'frequency', 'monetary']
    rfm.columns = rfm_cols
    print(rfm)

    # Calculating the RFM Scores
    # for R - 1 is the best
    # for M & F - 5 is the best
    # https://medium.com/@bitaazari71/crm-analytics-customer-segmentation-with-rfm-customer-lifetime-value-part-1-d1773c7c5cd9

    rfm['recency_score'] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])  # Creates quartiling
    # rfm['frequency_score'] = pd.qcut(rfm["frequency"], 5,
    #                                  duplicates='drop')  # Creates quartiling labels=[1, 2, 3, 4, 5],
    # frequecy_lbl_list = rfm['frequency_score'].unique().tolist()
    # label_mapping = {
    #     label: i for i, label in enumerate(frequecy_lbl_list)
    # }
    rfm['frequency_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm['monetary_score'] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])  # Creates quartiling
    rfm["rfm_Score"] = rfm["recency"].astype(str) + rfm["frequency"].astype(str) + rfm["monetary"].astype(str)

    # calculating  rfm_score
    # https://www.geeksforgeeks.org/rfm-analysis-analysis-using-python/
    # rfm['rfm_score_calc'] = 0.15 * rfm['recency_score'] + 0.28 * rfm['frequency_score'] + 0.57 * rfm['monetary_score']
    print(rfm.head(10))

    # RFM Segmenting
    seg_map = {
        r'[1-2][1-2]': 'Hibernating',  # Long time between purchases, low order count. Maybe lost
        r'[1-2][3-4]': 'At Risk',  # Used to purchase often, but haven't for a long time. Need them back.
        r'[1-2]5': 'Can\'t Loose',  # Used to purchase frequently, but haven't returned for a long time.
        r'3[1-2]': 'About to Sleep',  # Below Average Recency and Frequency will lose if not reactivated.
        r'33': 'Need Attention',
        # Above Average Recency, Frequency, and monetary values. May not have bought super recently though.
        r'[3-4][4-5]': 'Loyal Customers',  # Buy on a Regular basis, responsive to promotions.
        r'41': 'Promising',  # Recent Shoppers, but haven't spent much.
        r'51': 'New Customers',  # Recent shoppers but not often shoppers.
        r'[4-5][2-3]': 'Potential Loyalists',  # Recent customers with average frequency.
        r'5[4-5]': 'Champions'  # Bought Recently, buy often, and spend the most. Platinum customers.
    }

    rfm['segment'] = rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str)
    rfm['segment'] = rfm['segment'].replace(seg_map, regex=True)

    rfm.groupby('segment', as_index=False).mean().sort_values('monetary')
    print(rfm)
    # rfm = rfm.fillna(1, inplace=True)
    # print(rfm)

    rfm_fig = go.Figure()
    rfm_fig.add_heatmap(
        y=rfm.segment,
        x=np.sort(rfm.monetary_score),
        z=rfm.monetary,
        colorscale=pio.templates['atbAnalyticsGroupDefault'].layout.colorscale.diverging,

    )
    rfm_fig.update_xaxes(autorange='reversed')

    rfm_fig.layout.yaxis.type = 'category'
    rfm_fig.layout.xaxis.type = 'category'

    return rfm_fig
