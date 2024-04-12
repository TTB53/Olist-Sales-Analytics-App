import json
from os.path import exists

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
from joblib import load

pg_utils = pg_utils.PageUtilities()

dash.register_page(__name__,
                   path='/customer-analysis',
                   name='Customers',
                   title='Olist - Customer Analysis - ATB Analytics Group', )

customers_df = pd.read_csv('./data/customers_df.csv')
geo_df = pd.read_csv('./data/customers_geo_data.csv')

# Loading in the tot_unique_customer prediction model.
if not exists('ml/models/unique_customers_lr.joblib') or not exists('ml/models/total_customers_lr.joblib'):
    from ml.sales_models import ForecastingModel as fcastModel

    ml_df = customers_df[['order_month_date', 'tot_unique_customers']]
    ml_df2 = customers_df[['order_month_date', 'customer_unique_id']]

    ml_df = ml_df.groupby('order_month_date').agg(
        {'tot_unique_customers': 'nunique'}
    ).reset_index()
    ml_df2 = ml_df2.groupby('order_month_date').agg(
        {'customer_unique_id': 'count'}
    ).reset_index()
    pg_utils.convert_to_datetime(ml_df, 'order_month_date')
    pg_utils.convert_to_datetime(ml_df2, 'order_month_date')

    lr_model = fcastModel.linear_regression(fcastModel, ml_df, 'order_month_date', 'tot_unique_customers', '2019-02-01',
                                            ['2018-11-01', '2018-12-01', '2019-01-01', '2019-02-01'],
                                            '2022-06-01', scale=False, filename='unique_customers_lr')

    lr_model_2 = fcastModel.linear_regression(fcastModel, ml_df2, 'order_month_date', 'customer_unique_id',
                                              '2019-02-01',
                                              ['2018-11-01', '2018-12-01', '2019-01-01', '2019-02-01'],
                                              '2022-06-01', scale=False, filename='total_customers_lr')

    pred = np.array(pd.to_numeric(pd.to_datetime(['2020-02-01']))).reshape(-1, 1)

    print(lr_model.predict(pred))
    print(lr_model_2.predict(pred))
else:
    lr_model = load('ml/models/unique_customers_lr.joblib')
    lr_model_2 = load('ml/models/total_customers_lr.joblib')

    pred = np.array(pd.to_numeric(pd.to_datetime(['2020-02-01']))).reshape(-1, 1)

    print(lr_model.predict(pred))
    print(lr_model_2.predict(pred))

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
                    [
                        html.P(
                            ["""
        Olist provided us data on their platform from October 2016 to November of 2018.
        Since there is very little data for the 2016 year, we will compare the 2017 and 2018 data.
        """]
                        )
                    ]
                ),
                html.Li(
                    [
                        html.P(
                            id='cs-insight-1',
                            children="""
                                Generating Automated Insights...
                                """,
                        )
                    ]
                ),
                html.Li(
                    [
                        html.P(
                            id='cs-insight-2',
                            children="""
Generating Automated Insights...
""",
                        )
                    ]
                ),
                html.Li(
                    [
                        html.P(
                            id='cs-insight-3',
                            children="""
                            Generating Automated Insights...
                            """,
                        )
                    ]
                ),
                # html.Li(["With more ", dcc.Link("Marketing", href='http://127.0.0.1:8050/marketing-analysis'),
                #          " campaign data past 2018, I bet that we would see both growth in sellers on the platform,"
                #          " and how that somewhat played into their decisions to acquire a logistics company"
                #          " to help with deliveries, and an ERP company to help owners"
                #          " manage their inventories better. As well as an increase in customers as they add more and more merchants."]),
                html.Li([
                    "There were a number of merchants that signed up due to ",
                    dcc.Link("Marketing", href='http://127.0.0.1:8050/marketing-analysis'),
                    " efforts. Combining marketing data and customer data, with the existing ",
                    dcc.Link("Merchants", href='http://127.0.0.1:8050/merchants-analysis'),
                    " data, Olist can begin to build better forecast models for predicting customer growth and "
                    "acquisition, which can help them predict and target better merchants to add to the platform, while "
                    "driving the overall goal of exapansion and providing smaller merchants a spolight on the global "
                    "stage."
                ]),
                # html.Li(
                #     [
                #         dcc.Link("Sales", href='http://127.0.0.1:8050/sales-analysis'),
                #         " generated through the platform helped the company"
                #         " to continue to raise money, and expand into different markets as well."
                #     ]
                # ),
                # html.Li(
                #     """
                #     All of the Charts are meant to be interactive. You can hover and
                #     turn things on and off to get a better picture of the data.
                #     get more detail by hovering, and when dealing with the top and bottom analysis
                #     you can drill down to into the data
                #     by selecting the category you wish to see.
                #     """
                # ),
                # html.Li(
                #     """
                #
                #     If trying to predict customers, mention something about that here.
                #     """
                # )
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
                    align='center',
                    className='col-md-12',
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

                            ],
                            className='card-group',
                        )
                    ],
                    # width=6,
                    align='center',
                    className='col-md-6 col-sm-12',
                ),

                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                                pg_utils.create_kpi_card("cs-avg-clv"),
                            ],
                            className='card-group'
                        ),

                    ],
                    # width=6,
                    align='center',
                    className='col-md-6 col-sm-12',
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

                            ],
                            className='card-group',
                        ),
                    ],
                    # width=12,
                    align='center',
                    className='col-md-6 col-sm-12'
                ),

                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                                pg_utils.create_kpi_card("cs-avg-days-to-receive"),
                            ],
                            className='card-group'
                        )
                    ],
                    align='center',
                    className='col-md-6 col-sm-12'
                ),

            ]
        ),

        html.Br(),
        html.H2('Where are our Customers Located.', className='display-2'),

        html.Br(),
        dbc.Row(
            children=[
                # html.H5("What states are we shipping the most too.", className='display-5'),
                html.Div(
                    ["""
                    Here is how Olist Customer orders are distributed throughout Brazil.
                    """,
                     html.Br(),
                     """
                     You can see that there 
                     are a few smaller orders from countries outside of Brazil, such as Portugal and 
                     Argentina as well. 
                     """,
                     html.Br(),
                     """ 
                      which are inline with Olist's overall business goal of expanding its footprint 
                     to all Latin American countries. 
                     """,
                     html.Br(),
                     ]
                ),
                # html.Ul(
                #     children=[
                #         html.Li(),
                #     ]
                # ),
                html.Br(),
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            html.H3("Map View"),
                                            html.P("Choose how you would like to view the map."),

                                            dbc.RadioItems(
                                                id='cs-map-selection-value',
                                                options=[{'label': 'Tot Customers', 'value': 'customer_unique_id'},
                                                         {'label': 'Payment value', 'value': 'payment_value'},
                                                         {'label': 'Payment value(Scaled)',
                                                          'value': 'payment_value_scaled'}
                                                         ],

                                                inline=True,
                                                value='customer_unique_id'
                                            )
                                        ]
                                    ),
                                    className='user-selection-card'
                                )
                            ]
                        ),
                        pg_utils.create_kpi_card('customers-map'),
                        html.Br(),
                        html.P(
                            id='cs-map-insight-1',
                            children=[
                                'Click on a Location Dot Above to learn more about it.'
                            ]
                        )
                    ],
                    width=12,
                    align='center',
                ),
                # dbc.Col(
                #     children=[
                #         dbc.Card(
                #             dbc.CardBody(
                #                 children=[
                #                     dcc.Loading(
                #                         dcc.Graph(
                #                             id='customers-map',
                #                             animate=True,
                #                             # responsive=True,
                #                         ),
                #                         type='dot',
                #                         color="AQUAMARINE"
                #                     ),
                #                     html.Br(),
                #                     dcc.Slider(
                #                         id='customers-map-slider',
                #                         min=0,
                #                         max=5,
                #                         # step=5,
                #                         value=3,
                #                         tooltip={
                #                             "placement": "bottom",
                #                             "always_visible": True
                #                         },
                #                         className='ui-selection-slider',
                #                     ),
                #
                #                 ]
                #
                #             ),
                #             className='kpi-card',
                #         ),
                #
                #     ],
                #     width=12
                # )

            ],
            align='center'
        ),

        html.Br(),
        html.H2('Top Customer Analysis', className='display-2'),
        html.Br(),
        dbc.Row(
            children=[
                # html.H5("What are the top products that our customers ordered.",
                #         className='display-5'),
                html.Br(),
                html.P(
                    """
                    What are the top product categories, who are the top customers that make up the majority of
                    the ordering.
                
                    """
                ),
                html.Br(),
                dbc.Col(
                    html.Div(
                        children=[
                            dbc.Card(
                                dbc.CardBody(
                                    children=[
                                        html.H3("Top n Value Selector", className='text-center'),
                                        html.Br(),
                                        html.P(
                                            "Select a value to see the our customers Top/Bottom "
                                            "ordered product categories are."),
                                        html.Br(),
                                        dcc.Slider(
                                            id='cs-n-slider',
                                            min=0,
                                            max=25,
                                            step=5,
                                            value=10,
                                            tooltip={
                                                "placement": "bottom",
                                                "always_visible": True
                                            },
                                            className='ui-selection-slider',
                                        ),
                                        # html.Br(),
                                    ]
                                ),
                                className='user-selection-card',
                            ),

                            dbc.Card(
                                dbc.CardBody(
                                    children=[
                                        html.H3("Select A Filter Option", className='text-center'),
                                        html.Br(),
                                        html.P(
                                            "Select the option to use as the filter for the Top/Bottom Product Category."),
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
                                            # inline=True,
                                            persistence=True,
                                            className='ui-selection-radio-items',
                                        ),
                                    ]
                                ),
                                className='user-selection-card',
                            )
                        ],
                        className='card-group'
                    ),
                    align='center',
                    width='12',
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
                    className='col-md-6 col-sm-12',
                    align='center',
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
                    className='col-md-6 col-sm-12',
                    align='center',
                ),
                # dbc.Col(
                #     children=[
                #         dbc.Card(
                #             dbc.CardBody(
                #                 dcc.Loading(
                #                     html.Div(
                #                         id='cs-customers-pivot-table',
                #                     ),
                #                     type='dot',
                #                     color="AQUAMARINE"
                #                 )
                #             ),
                #             className='kpi-card'
                #         ),
                #         html.Button("Download Data", id="btn_csv", className='btn btn-outline-dark'),
                #         dcc.Download(id="download-dataframe-csv")
                #
                #     ],
                #     width=12
                # )

            ],
            align='center'
        ),
        html.Br(),
        html.H2('Cohort Analysis and Segmentation', className='display-2'),
        # html.H5("Separating Customers into groups", className='display-5'),
        dbc.Row(
            children=[
                html.P(
                    [
                        """
                        Cohort analysis is an analytical technique that categorizes and divides data into groups with 
                        common characteristics prior to analysis. This is useful in helping you to find and identify 
                        groups of customers you might not have originally segmented together. 
                   """,
                        html.Br(),
                        """
                        Cohort analysis helps track that the quality of the customer is improving over time 
                        and also helps identify when customer's churn allowing for proper targeting for 
                        marketing purposes.
                        """
                    ]
                ),
                # html.Br(),
                # html.P(
                #     """
                #
                #     """
                # ),
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                                dbc.Card(
                                    children=[
                                        dbc.CardBody(
                                            children=[
                                                html.H3("Choose a Value",
                                                        className='text-center'),
                                                html.P(
                                                    """
                                                    Select a value to compare the average price Cohort Analysis with.
                                                    Can be either Average Order Items or the Average Shipping Cost.
                                                    """
                                                ),
                                                dcc.Dropdown(
                                                    id='cohort_selection_dd',
                                                    # options=[{"label": x, "value": x} for x in
                                                    #          dff.product_category_name_english.unique()],
                                                    optionHeight=40,
                                                    # value=options[0],
                                                    clearable=False,
                                                    style={"width": "100%"},
                                                    persistence=True,
                                                    persistence_type="session"
                                                ),
                                            ]
                                        )
                                    ],
                                    className='user-selection-card',
                                ),
                                # dbc.Card(
                                #     children=[
                                #         dbc.CardBody(
                                #             children=[
                                #                 html.H3("Choose a Value from the dropdown menu",
                                #                         className='text-center'),
                                #                 html.P(
                                #                     """
                                #                     This is a y value for the cohort analysis
                                #                     """
                                #                 ),
                                #                 dcc.Dropdown(),
                                #             ]
                                #         )
                                #     ],
                                #     className='user-selection-card',
                                # )
                            ],
                            className='card-group'
                        ),
                    ],
                    width=12,
                    align='center',
                    # className='kpi-card'
                ),

                dbc.Col(
                    children=[
                        pg_utils.create_kpi_card('cohort-avg-price'),
                    ],
                    # width=6,
                    className='col-md-6 col-sm-12',
                    align='center'
                ),

                dbc.Col(
                    children=[
                        pg_utils.create_kpi_card('cohort-retention'),
                    ],
                    # width=6,
                    className='col-md-6 col-sm-12',
                    align='center'
                )
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
                    children=[
                        """
                        For example, we might want to target our Champions(or top purchasers) with some kind of
                        discount incentive program.
                        """,
                        html.Br(),
                        """
                        We might want to also entice promising customers by 
                        sending them exclusive deals related to items they have ordered. 
                        """,
                        html.Br(),
                        """
                        Or follow up with 
                        New customers on how their purchase was and if they have seen the latest offerings. 
                        """
                    ]

                ),
                html.Br(),
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                                dbc.Card(
                                    children=[
                                        dbc.CardBody(
                                            children=[
                                                html.H3("Choose a Value from the dropdown menu",
                                                        className='text-center'),
                                                html.P(
                                                    """
                                                    Choose to view the customer segmentation by Recency, Frequecny, or 
                                                    Monetary levels. To read this 5 is better than 1 except in the case
                                                    of Monetary. 
                                                    """
                                                ),
                                                dcc.Dropdown(
                                                    id='rfm_selection_dd',
                                                    # options=[{"label": x, "value": x} for x in
                                                    #          dff.product_category_name_english.unique()],
                                                    optionHeight=40,
                                                    # value=options[0],
                                                    clearable=False,
                                                    style={"width": "100%"},
                                                    persistence=True,
                                                    persistence_type="session"
                                                ),
                                            ]
                                        )
                                    ],
                                    className='user-selection-card',
                                ),

                                # dbc.Card(
                                #     children=[
                                #         dbc.CardBody(
                                #             children=[
                                #                 html.H3("Choose a Value from the dropdown menu",
                                #                         className='text-center'),
                                #                 html.P(
                                #                     """
                                #                     This is a y value for the cohort analysis
                                #                     """
                                #                 ),
                                #                 dcc.Dropdown(),
                                #             ]
                                #         )
                                #     ],
                                #     className='user-selection-card',
                                # )
                            ],
                            className='card-group'
                        ),
                    ],
                    width=12,
                    align='center',
                    # className='kpi-card'
                ),
                html.Br(),
                dbc.Col(
                    children=[
                        html.P(id='rfm-date'),
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
    Output('cs-insight-1', 'children'),
    Output('cs-insight-2', 'children'),
    Output('cs-insight-3', 'children'),
    Output('cohort_selection_dd', 'options'),
    Output('rfm_selection_dd', 'options'),
    Input('data-store', 'data'),
)
def custmomer_insights(data):
    datasets = json.loads(data)

    customers_by_month = pd.read_json(datasets['customer_by_month_df'])
    pg_utils.convert_to_datetime(customers_by_month, "order_month_date")
    map_slider_max = np.log10(customers_by_month.customer_revenue).max()

    customers_by_month['year'] = customers_by_month['order_month_date'].dt.year
    year_df = customers_by_month.groupby('year').agg(
        {
            'customer_count': 'sum',
            'tot_unique_customers': 'sum',
            'customer_revenue': 'sum',
            'order_item_id': 'sum',
        }
    ).reset_index()
    yoy_insight_df = year_df[['year', 'customer_count', 'tot_unique_customers', 'customer_revenue', 'order_item_id']]
    yoy_insight_cc = yoy_insight_df['customer_count'].pct_change()[2]  # Can use on the whole dataframe as well
    yoy_insight_tuc = yoy_insight_df['tot_unique_customers'].pct_change()[2]  # Can use on the whole dataframe as well
    yoy_insight_cr = yoy_insight_df['customer_revenue'].pct_change()[2]  # Can use on the whole dataframe as well
    yoy_insight_oii = yoy_insight_df['order_item_id'].pct_change()[2]  # Can use on the whole dataframe as well

    print(yoy_insight_df)

    yoy_insight, yoy_insight_2, yoy_insight_3 = "", "", ""

    if yoy_insight_cc > 0:
        yoy_insight += "During that time, the number of customers that used the platform grew from {:,.0f} in 2017 to " \
                       "{:,.0f} in 2018, or an increase in customers using the platform by {:.2%}." \
                       "".format(yoy_insight_df['customer_count'][1],
                                 yoy_insight_df['customer_count'][2],
                                 yoy_insight_cc)

        if yoy_insight_tuc > 0:
            if yoy_insight_cr > 0:
                yoy_insight += " The unique customers grew as well. Increasing,from {:,.0f} to {:,.0f} in 2018, or a {:.2%} increase.".format(
                    yoy_insight_df['tot_unique_customers'][1],
                    yoy_insight_df['tot_unique_customers'][2],
                    yoy_insight_tuc)
            else:
                yoy_insight += " Although the unique customers grew, {:.2%}, however customer revenues did not. " \
                               "Revenue fell by {:.2%} yoy.".format(yoy_insight_tuc, yoy_insight_cr)
        else:
            if yoy_insight_cr > 0:
                yoy_insight += " The unique customers did not increase and actually fell by, {:.2%}. Going" \
                               "from {:,.0f} in 2017 to {:,.0f} in 2018.But customer revenues " \
                               "remained strong and increased by {:.2%} yoy.".format(
                    yoy_insight_df['tot_unique_customers'][2],
                    yoy_insight_df['tot_unique_customers'][1],
                    yoy_insight_tuc, yoy_insight_cr)
            else:
                yoy_insight += " he unique customers did not increase and actually fell by, {:.2%}, " \
                               "customer revenues followed suit and fell by {:.2%} yoy.".format(yoy_insight_tuc,
                                                                                                yoy_insight_cr)
    else:
        yoy_insight += " fell by {:.2%}.".format(yoy_insight_cc)

        if yoy_insight_tuc > 0:
            if yoy_insight_cr > 0:
                yoy_insight += " despite the drop in total customers, the unique customers grew by, {:.2%}. The" \
                               " customer revenues also increased by {:.2%}.".format(yoy_insight_tuc, yoy_insight_cr)
            else:
                yoy_insight += " despite the drop in total customers, the unique customers grew, {:.2%}." \
                               " However customer revenues did not, and fell in line with total customers. Leading to " \
                               "revenue falling by {:.2%} yoy.".format(yoy_insight_tuc, yoy_insight_cr)
        else:
            if yoy_insight_cr > 0:
                yoy_insight += " The unique customers did not increase and actually fell by, {:.2%}. But customer revenues " \
                               "remained strong and increased by {:.2%} yoy.".format(yoy_insight_tuc, yoy_insight_cr)
            else:
                yoy_insight += " he unique customers did not increase and actually fell by, {:.2%}, " \
                               "customer revenues followed suit and fell by {:.2%} yoy.".format(yoy_insight_tuc,
                                                                                                yoy_insight_cr)

    if yoy_insight_cr > 0:
        yoy_insight_2 += "From 2017 to 2018, customer revenues went from ${:,.2f}, to ${:,.2f}, or an increase of " \
                         "{:,.2%}. This revenue increase was driven by {:,.0f} unique customers.".format(
            yoy_insight_df['customer_revenue'][1],
            yoy_insight_df['customer_revenue'][2],
            yoy_insight_cr,
            yoy_insight_df['tot_unique_customers'][2]
        )

    else:
        yoy_insight_2 += "From 2017 to 2018, customer revenues went from ${:,.2f}, to ${:,.2f}, or an decrease of " \
                         "{:,.2%}.".format(
            yoy_insight_df['customer_revenue'][1],
            yoy_insight_df['customer_revenue'][2],
            yoy_insight_cr
        )

    if yoy_insight_oii > 0 and yoy_insight_cr > 0:
        yoy_insight_3 += " Just like the revenue, the number of items ordered increased from 2017 to 2018." \
                         " Going from {:,} items ordered to {:,} items order from Olist Merchants. This increase represents" \
                         "a {:,.2%} change".format(
            yoy_insight_df['order_item_id'][1],
            yoy_insight_df['order_item_id'][2],
            yoy_insight_oii,

        )
    elif yoy_insight_oii > 0 and yoy_insight_cr < 0:
        yoy_insight_3 += " Just like the revenue, the number of items ordered increased from 2017 to 2018." \
                         " Going from {} items ordered to {} items order from Olist Merchants. This increase represents" \
                         "a {:,.2%} change".format(
            yoy_insight_df['order_item_id'][1],
            yoy_insight_df['order_item_id'][2],
            yoy_insight_oii,

        )
    elif yoy_insight_oii < 0 and yoy_insight_cr > 0:
        yoy_insight_3 += " Just like the revenue, the number of items ordered increased from 2017 to 2018." \
                         " Going from {} items ordered to {} items order from Olist Merchants. This increase represents" \
                         "a {:,.2%} change".format(
            yoy_insight_df['order_item_id'][1],
            yoy_insight_df['order_item_id'][2],
            yoy_insight_oii,

        )
    else:
        yoy_insight_3 += " Just like the revenue, the number of items ordered increased from 2017 to 2018." \
                         " Going from {} items ordered to {} items order from Olist Merchants. This increase represents" \
                         "a {:,.2%} change".format(
            yoy_insight_df['order_item_id'][1],
            yoy_insight_df['order_item_id'][2],
            yoy_insight_oii,

        )

    cohort_cols = [
        # 'payment_value',
        'order_item_id',
        'freight_value',
    ]
    cohort_options = [
        {
            "label": x.replace("_", " ").title(),
            "value": x
        } for x in sorted(cohort_cols)
    ]

    rfm_cols = ['recency', 'frequency', 'monetary']
    rfm_options = [
        {
            "label": x,
            "value": x
        } for x in rfm_cols
    ]

    return yoy_insight, yoy_insight_2, yoy_insight_3, cohort_options, rfm_options


# @callback(
#     Output("download-dataframe-csv", "data"),
#     Input("btn_csv", "n_clicks"),
#     prevent_initial_call=True,
# )
# def download_datatable(n_clicks):
#     return dbc.Alert(
#         "You Tried Downloading the Datatable for the Top/Bottom Products."
#         "This will be coming shortly"
#     )
#     # return dcc.send_data_frame(df.to_csv, "mydf.csv")
#

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
    # a part of their decision to acquire Pax in 2020.
    # I will use Freight Value to say we will be offering free shipping to all customers during this time.
    tot_expenses = customers_by_month.freight_value.sum()
    profit_margin = (tot_revenue - tot_expenses) / tot_revenue
    tot_items_ordered = customers_by_month.order_item_id.sum()
    avg_items_ordered = tot_items_ordered / tot_orders
    avg_order_value = tot_revenue / tot_orders

    # This isn't really used in this section of the analysis and needs a
    # TODO to be moved to the proper section (marketing)
    repeat_rate = 0
    # repeat_rate_df = dff.groupby('customer_unique_id')['order_id'].count().reset_index()
    # repeat_rate = repeat_rate_df[repeat_rate_df['order_id'] >= 2].shape[0] / tot_customers
    churn_rate = 1 - repeat_rate

    customer_val = (avg_order_value / purchase_frequency) / churn_rate
    customer_lifetime_val = customer_val * profit_margin

    print("Customers by Month Dataframe\n", customers_by_month.head(10))

    # TODO Update the Model for this to be more accurate.
    # if lr_model is not None and lr_model_2 is not None:
    #     forecast3M = pd.date_range('2018-09-01', periods=3, freq='MS')
    #     forecast6M = pd.date_range('2018-09-01', periods=6, freq='MS')
    #     forecast9M = pd.date_range('2018-09-01', periods=9, freq='MS')
    #
    #     forecastDates = pd.to_numeric(pd.to_datetime(forecast9M))
    #     forecastDates = np.array(forecastDates).reshape(-1, 1)
    #     print("The Forecasted data being fed to the model is ", forecast9M)
    #
    #     pred_customers = lr_model.predict(forecastDates)
    #     pred_tot_customers = lr_model_2.predict(forecastDates)
    #     print("The model predicted the following customers ", pred_customers, "using the following intercept ",
    #           lr_model.intercept_, " and slope ", lr_model.coef_)
    #
    #     print("The model predicted the following customers ", pred_tot_customers, "using the following intercept ",
    #           lr_model_2.intercept_, " and slope ", lr_model_2.coef_)
    #
    #     forecast9Mpd = pd.Series(forecast9M).apply(pd.Series).stack().reset_index(drop=True)
    #     pred_customers_pd = pd.Series(pred_customers.tolist()).apply(pd.Series).stack().reset_index(drop=True)
    #     pred_tot_customers_pd = pd.Series(pred_tot_customers.tolist()).apply(pd.Series).stack().reset_index(drop=True)
    #     predicted_df = pd.concat([forecast9Mpd, pred_customers_pd, pred_tot_customers_pd], axis=1).reset_index(
    #         drop=True)
    #     predicted_df.rename(columns={0: 'order_month_date', 1: 'tot_unique_customers', 2: 'tot_customers'},
    #                         inplace=True)
    #
    #     print(predicted_df.head(10))
    #
    #     print(type(customers_by_month.order_month_date[0]))
    #     pg_utils.convert_to_datetime(customers_by_month, 'order_month_date')
    #     pg_utils.convert_to_datetime(predicted_df, 'order_month_date')
    #
    #     tot_customer_fig.add_bar(
    #         x=predicted_df.order_month_date,
    #         y=predicted_df.tot_customers,
    #         opacity=.2,
    #         row=1,
    #         col=1,
    #         # secondary_y=True,
    #         name='predicted tot_custs',
    #         hovertemplate="%{y:,}<extra></extra>",
    #         xaxis='x1',
    #         yaxis='y1',
    #         # visible='legendonly'
    #     )
    #
    #     tot_customer_fig.add_bar(
    #         x=predicted_df.order_month_date,
    #         y=predicted_df.tot_unique_customers,
    #         opacity=.4,
    #         row=1,
    #         col=1,
    #         # secondary_y=True,
    #         name='predicted tot_unique_custs',
    #         hovertemplate="%{y:,}<extra></extra>",
    #         xaxis='x1',
    #         yaxis='y1',
    #         # visible='legendonly'
    #     )

    # To remove the outlying Sept data that only had one customer.
    # customers_by_month = customers_by_month.iloc[:-1, :].append(predicted_df, ignore_index=True)

    # tot_customer_fig = go.Figure()

    # Function values = value, delta, title, rows=1, cols=1, x=[0, 1], y=[0, 1]

    tot_customer_fig = pg_utils.create_indicator_figure(
        value=tot_customers,
        delta=tot_customers,
        title="Total Customers",
        monetary=False
    )

    customers_by_month['tot_cust_pct_change'] = customers_by_month.customer_count.pct_change()
    customers_by_month['tot_unique_cust_pct_change'] = customers_by_month.tot_unique_customers.pct_change()

    tot_customer_fig.add_bar(
        x=customers_by_month.order_month_date,
        y=customers_by_month.customer_count,
        opacity=.2,
        row=1,
        col=1,
        name='tot-custs',
        # marker={'line': {'color': '#E4F2EF', 'width': 0.5, }},
        hovertemplate="<extra></extra> The total customers in %{x} was %{y:,} representing"
                      " a %{customdata:,.2%} MoM Change.<extra></extra>",
        customdata=customers_by_month.tot_cust_pct_change,
        xaxis='x1',
        yaxis='y1',
        text=customers_by_month.customer_count.apply(lambda x: pg_utils.human_format(x)),
        textfont_color='#FEFFF1'
    )

    tot_customer_fig.add_bar(
        x=customers_by_month.order_month_date,
        y=customers_by_month.tot_unique_customers,
        opacity=.2,
        row=1,
        col=1,
        # secondary_y=True,
        name='tot_unique_custs',
        hovertemplate="<extra></extra> The total unique customers in %{x} was %{y:,} "
                      "representing a %{customdata:,.2%} MoM Change.<extra></extra>",
        customdata=customers_by_month.tot_unique_cust_pct_change,
        xaxis='x1',
        yaxis='y1',
        visible='legendonly',
        text=customers_by_month.tot_unique_customers.apply(lambda x: pg_utils.human_format(x)),
        textfont_color='#FEFFF1',
        textangle=-90,
    )

    # tot_customer_fig.add_scatter(
    #     y=customers_by_month.customer_revenue,
    #     x=customers_by_month.order_month_date,
    #     opacity=.2,
    #     row=1,
    #     col=1,
    #     # secondary_y=True,
    #     name='revenue',
    #     hovertemplate="$%{y:,.2f}<extra></extra>",
    #     xaxis='x1',
    #     yaxis='y2',
    #     # visible='legendonly',
    # )

    tot_customer_fig.update_layout(
        barmode='group',
    )
    tot_customer_fig.layout.yaxis.visible = False
    tot_customer_fig.layout.hovermode = 'closest'

    tot_revenue_fig = pg_utils.create_indicator_figure(
        value=tot_revenue,
        delta=tot_revenue,
        title="Total Revenue",
        monetary=True
    )

    tot_revenue_fig.add_bar(
        y=customers_by_month.customer_revenue,
        x=customers_by_month.order_month_date,
        opacity=.2,
        row=1,
        col=1,
        name='revenue',
        hovertemplate="The total revenue<br> in %{x} was  $%{y:,.2f}<extra></extra>",
        xaxis='x1',
        yaxis='y1',
        text=customers_by_month.customer_revenue.apply(lambda x: pg_utils.human_format(x)),
        textfont_color='#FEFFF1',
        textangle=-90,

    )

    tot_revenue_fig.add_scatter(
        y=customers_by_month.revenue_per_customer,
        x=customers_by_month.order_month_date,
        opacity=.2,
        row=1,
        col=1,
        # secondary_y=True,
        name='revenue/cust',
        hovertemplate="The revenue per customer<br>in %{x} was $%{y:,.2f}<extra></extra>",
        # visible='legendonly',
        text=customers_by_month.revenue_per_customer,
        textfont_color='#FEFFF1'
    )

    # tot_revenue_fig.add_scatter(
    #     y=customers_by_month.profit_per_customer,
    #     x=customers_by_month.order_month_date,
    #     opacity=.2,
    #     row=1,
    #     col=1,
    #     secondary_y=True,
    #     name='profit/cust',
    #     hovertemplate="$%{y:,.2f}<extra></extra>",
    #     # visible='legendonly'
    # )

    tot_revenue_fig.layout.yaxis.visible = False
    tot_revenue_fig.layout.yaxis.showgrid = False
    tot_revenue_fig.layout.yaxis.zeroline = False
    tot_revenue_fig.layout.hovermode = 'closest'

    customer_lifetime_val_fig = pg_utils.create_indicator_figure(
        value=customer_lifetime_val,
        delta=customer_lifetime_val,
        title="CLTV",
        monetary=True
    )

    customer_lifetime_val_fig.add_bar(
        y=customers_by_month.customer_value,
        x=customers_by_month.order_month_date,
        opacity=.2,
        row=1,
        col=1,
        name='cust-lt-val',
        hovertemplate="The Customer LifeTime Value<br> in %{x} was $%{y:,.2f}<extra></extra>",
        xaxis='x1',
        yaxis='y1',
        text=customers_by_month.customer_value,
        textfont_color='#FEFFF1'
    )

    customer_lifetime_val_fig.add_scatter(
        y=customers_by_month.avg_order_value,
        x=customers_by_month.order_month_date,
        opacity=.2,
        row=1,
        col=1,
        # secondary_y=True,
        name='AoV',
        hovertemplate="The Average Order Value<br> in%{x} was $%{y:,.2f}<extra></extra>",
        # visible='legendonly',
        text=customers_by_month.avg_order_value,
        textfont_color='#FEFFF1'
    )

    # customer_lifetime_val_fig.add_scatter(
    #     y=customers_by_month.profit_per_customer,
    #     x=customers_by_month.order_month_date,
    #     opacity=.2,
    #     row=1,
    #     col=1,
    #     # secondary_y=True,
    #     name='profit/cust',
    #     visible='legendonly'
    # )
    #
    # customer_lifetime_val_fig.add_scatter(
    #     y=customers_by_month.revenue_per_customer,
    #     x=customers_by_month.order_month_date,
    #     opacity=.2,
    #     row=1,
    #     col=1,
    #     # secondary_y=True,
    #     name='revenue/cust',
    #     visible='legendonly',
    #     marker=dict(
    #         color='#4d675a'
    #     ),
    # )

    customer_lifetime_val_fig.layout.yaxis.visible = False
    customer_lifetime_val_fig.layout.hovermode = 'closest'

    avg_review_fig = pg_utils.create_indicator_figure(
        value=customers_by_month.review_score.mean(),
        delta=customers_by_month.review_score.mean(),
        title="Avg Review Score",
    )

    avg_review_fig.add_bar(
        x=customers_by_month.order_month_date,
        y=customers_by_month.review_score,
        opacity=.2,
        row=1,
        col=1,
        name='review-score',
        hovertemplate="The average review score<br> for %{x} was %{y:,.2f}<extra></extra>",
        xaxis='x1',
        yaxis='y1',
        text=customers_by_month.review_score,
        textfont_color='#FEFFF1'
    )

    # TODO Check that this number calcs for just the orders in whihc reveiew has been left
    # avg_review_fig.add_scatter(
    #     x=customers_by_month.order_month_date,
    #     y=customers_by_month.review_count,
    #     opacity=.2,
    #     row=1,
    #     col=1,
    #     secondary_y=True,
    #     name='review-count',
    #     hovertemplate="%{y:,.2f}",
    #     # visible='legendonly'
    # )

    avg_review_fig.layout.yaxis.visible = False
    avg_review_fig.layout.hovermode = 'closest'

    customer_shipping_fig = pg_utils.create_indicator_figure(
        value=tot_expenses,
        delta=tot_expenses,
        title="Tot Shipping Cost",
        monetary=True
    )

    customer_shipping_fig.add_bar(
        x=customers_by_month.order_month_date,
        y=customers_by_month.freight_value,
        opacity=.2,
        row=1,
        col=1,
        name='shipping cost',
        hovertemplate="The Shipping Cost<br> for %{x} was $%{y:,.2f}<extra></extra>",
        xaxis='x1',
        yaxis='y1',
        text=customers_by_month.freight_value.apply(lambda x: pg_utils.human_format(x)),
        textfont_color='#FEFFF1'

    )

    # customer_shipping_fig.add_scatter(
    #     x=customers_by_month.order_month_date,
    #     y=customers_by_month.order2cus_days,
    #     opacity=.2,
    #     row=1,
    #     col=1,
    #     secondary_y=True,
    #     name='days to receive',
    #     hovertemplate="%{y:,}",
    #     xaxis='x1',
    #     yaxis='y1',
    #     visible='legendonly',
    # )

    customer_shipping_fig.add_scatter(
        x=customers_by_month.order_month_date,
        y=customers_by_month.on_time_days,
        opacity=.2,
        row=1,
        col=1,
        # secondary_y=True,
        name='on time days',
        hovertemplate="The on-time delivery<br>days averaged<br>%{y:,.2f} for %{x}",
        xaxis='x1',
        yaxis='y1',
        # visible='legendonly',
    )

    customer_shipping_fig.layout.yaxis.visible = False
    customer_shipping_fig.layout.yaxis.showgrid = False
    customer_shipping_fig.layout.yaxis.zeroline = False
    customer_shipping_fig.layout.hovermode = 'closest'

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

    return tot_customer_fig, customer_lifetime_val_fig, tot_revenue_fig, avg_review_fig, customer_shipping_fig


@callback(
    Output('customers-map', 'figure'),
    Input('data-store', 'data'),
    Input('cs-map-selection-value', 'value')
    # Input('customer-map-slider', 'value'),
    # prevent_initial_call=True
)
def update_customer_map(data, map_view_value):
    # geolocation = './data/OListEcomData/olist_geolocation_dataset.csv'
    # geolocation = './data/customers_geo_data.csv'
    # geo_df = pd.read_csv(geolocation)
    geojson = pd.read_json('./data/external/brazil_geo.json')
    # geo_df.rename(columns={"geolocation_zip_code_prefix": "zip_code"}, inplace=True)
    # dff = pd.DataFrame(data)

    dff = customers_df.copy()

    print(geo_df.head(), dff.head())
    dff = dff[['customer_unique_id', 'zip_code', 'payment_value']]
    dff = dff.groupby('customer_unique_id', as_index=False)['payment_value'].sum()
    dff = dff.merge(geo_df, on='customer_unique_id')
    dff['code'] = "BRA"

    # This keeps all the columns in the dataframe when doing a groupby 'first' is equivalent
    # to 'keep this, and keep it movin' whenever there are no duplicates

    dff = dff.groupby('zip_code').agg(
        {
            'geolocation_lat': 'first',
            'geolocation_lng': 'first',
            'geolocation_city': 'first',
            'geolocation_state': 'first',
            'payment_value': 'sum',
            'customer_unique_id': 'count'
        }).reset_index()

    color_series = dff['payment_value'].quantile(0.95)
    dff['payment_value_scaled'] = np.log10(dff.payment_value)

    def create_text(x):
        text = "{} Customers living within the {} zip code of {},{} have ordered<br> a total of ${:,.2f} worth of products from OList.<extra></extra>".format(
            x['customer_unique_id'], x['zip_code'], str(x['geolocation_city']).title(),
            str(x['geolocation_state']).title(),
            x['payment_value']
        )

        return text

    dff['hover_data'] = dff.apply(
        lambda x: create_text(x), axis=1)

    # Create the choropleth map first
    # customer_map_fig = pg_utils.create_px_choropleth(dff=dff, geojson=geojson, locations='geolocation_state',
    #                                                  color='payment_value',
    #                                                  hover_data={
    #                                                      'geolocation_state': False,
    #                                                      'hover_text': True,
    #                                                      'payment_value': False,
    #                                                  },
    #                                                  color_continuous_midpoint=dff.payment_value.mean())
    # customer_map_fig = go.Figure()

    # dff['geolocation_state'] = dff.geolocation_state.apply(lambda x: x.lower)
    #
    # customer_map_fig.add_trace(
    #     go.Choropleth(
    #         locations=dff['geolocation_state'],
    #         locationmode='geojson-id',
    #         geojson=geojson,
    #         z=dff['payment_value'],
    #         # colorscale=pio.templates['atbAnalyticsGroupDefault'].layout.colorscale.diverging,
    #     )
    # )
    # customer_map_fig = pg_utils.create_scattergeo_map(geojson=geojson, lat=dff.geolocation_lat, lon=dff.geolocation_lng,
    #                                                   locations=dff.geolocation_state, color=dff.payment_value,
    #                                                   hover_data=dff.hover_data)

    # customer_map_fig = pg_utils.create_px_mapbox(dff,
    #                                              dff['payment_value'],
    #                                              # 8,
    #                                              dff['payment_value'] * 3,
    #                                              "Customers",
    #                                              dff['payment_value'].quantile(0.95),
    #                                              mapbox_style='open-street-map'
    #                                              )

    # customer_map_fig.update_layout(
    #     # height=800,
    #     # margin={
    #     #     "r": 0,
    #     #     "t": 0,
    #     #     "l": 0,
    #     #     "b": 0
    #     # },
    #     # showlegend=True,
    #     geo=dict(
    #         fitbounds='geojson',
    #         visible=False,
    #         resolution=110,
    #         showland=True,
    #         showocean=True,
    #         showlakes=True,
    #         showrivers=True,
    #         showcountries=True,
    #         showsubunits=True,
    #         showframe=False,
    #         showcoastlines=True,
    #         landcolor='#FEFFF1',
    #         countrycolor='#333333',
    #         oceancolor='#E4F2EF',
    #         lakecolor='#388895',
    #         rivercolor='#388895',
    #         subunitcolor="#42403f",
    #     )
    # )
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

    if map_view_value is None:
        map_view_value = dff.payment_value
    else:
        map_view_value = dff[f'{map_view_value}']

    customer_map_fig = go.Figure(
        go.Densitymapbox(
            lat=dff.geolocation_lat,
            lon=dff.geolocation_lng,
            z=map_view_value,
            radius=8,
            hovertemplate=dff.hover_data,
            opacity=.87,
            showlegend=False,
            customdata=dff.zip_code,
            # showscale=True,
            # colorbar=dict(
            #
            # )
            # name='Amt($) Ordered'
        )
    )

    customer_map_fig.update_layout(
        mapbox_style='open-street-map',
        height=500,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_center={
            'lat': dff.geolocation_lat.mode()[0],
            'lon': dff.geolocation_lng.mode()[0]
        },
        mapbox_zoom=3,
        showlegend=False,
        # showscale=True,
    )

    customer_map_fig.update(layout_coloraxis_showscale=True)
    customer_map_fig.update(layout_showlegend=False)

    # customer_map_fig.update_mapboxes(
    #     # color=dff['payment_value'],
    #     zoom=5,
    #     pitch=1,
    #     # width=1200,
    #     # height=800,
    #     size=dff['payment_value'],
    #     size_max=20,
    #     # hover_name=dff['customer_unique_id'],
    #     title='Customer Orders',
    #     range_color=[0, dff['payment_value'].quantile(0.95)],  # To negate ouliers
    #     color_continuous_scale=pio.templates[
    #         'atbAnalyticsGroupDefault'].layout.colorscale.diverging,
    #     center={
    #         'lat': dff.geolocation_lat.mode()[0],
    #         'lon': dff.geolocation_lng.mode()[0]
    #     },
    #
    # )

    return customer_map_fig


@callback(
    Output('cs-map-insight-1', 'children'),
    Input('customers-map', 'clickData')
)
def update_map_insights(clickData):
    geolocation = './data/customers_geo_data.csv'
    customers = './data/customers_df.csv'

    dff = pd.read_csv(customers)
    geo_df = pd.read_csv(geolocation)

    print(geo_df.head(), dff.head())
    dff = dff[['customer_unique_id', 'zip_code', 'payment_value',
               'order_id', 'order_item_id']]

    dff_gby = dff.groupby('customer_unique_id', as_index=False).agg({
        'payment_value': 'sum',
        'order_id': 'nunique',
        'order_item_id': 'sum'
    })
    dff_gby.rename(columns={
        'order_id': 'num_of_orders',
        'order_item_id': 'num_items_ordered'
    }, inplace=True)
    dff_gby = dff_gby.merge(geo_df, on='customer_unique_id')
    dff_gby['code'] = "BRA"

    customer_detail = html.P("Click on a location above to get more insights about the customers that ordered from "
                             "there.")

    if clickData is None:
        print("Nothing Clicked")
    else:
        clickData = clickData['points'][0]['customdata']
        print(clickData, " was clicked!")

        customer_detail_df = dff_gby.query('zip_code == @clickData')

        if len(customer_detail_df) > 1:
            customer_detail_df.sort_values(by='payment_value', ascending=False, inplace=True)

        customer_detail_insight = f"Of the {customer_detail_df.customer_unique_id.count():,} customers in " \
                                  f"{customer_detail_df.geolocation_city.iloc[0]}({clickData}) the top customer " \
                                  f"ordered a total of ${customer_detail_df.payment_value.iloc[0]:,.2f} worth " \
                                  f"of product from Olist."

        customer_detail = dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.P(
                            customer_detail_insight
                        ),
                        html.Br(),
                        dcc.Graph(
                            id='cs-map-detail',
                            figure=go.Figure(
                                go.Bar(
                                    x=customer_detail_df.customer_unique_id,
                                    y=customer_detail_df.payment_value,
                                    name='',
                                    text=customer_detail_df.payment_value,
                                    hovertemplate="%{x} ordered $%{text:,.2f} worth of merchandise.",
                                    texttemplate="$%{text:,.2f}",
                                    textfont_color='#FEFFF1',
                                    insidetextanchor='end',
                                ),
                                layout=go.Layout(
                                    yaxis=dict(
                                        visible=False,
                                    ),
                                    uniformtext=dict(
                                        minsize=8,
                                    ),
                                )
                            ),
                        ),
                        html.Br(),
                        dcc.Graph(
                            id='cs-customer-orders',
                        )
                    ],
                    className='col-md-12 col-sm-12'
                )
            ]
        )

    return customer_detail


@callback(
    Output('cs-customer-orders', 'figure'),
    Input('cs-map-detail', 'clickData')
)
def update_customer_products(clickData):
    dff = customers_df

    cust_product_fig = go.Figure(
        layout=
        go.Layout(
            yaxis=dict(
                visible=False,
            ),
            uniformtext=dict(
                minsize=8,
            ),
        )
    )
    if clickData is None:
        print("cs customer orders is None")
    else:
        print(clickData)
        customer_id = clickData['points'][0]['label']

        customer_orders = dff.query('customer_unique_id == @customer_id')

        # customer_orders_gby = customer_orders.groupby('order_id').reset_index()

        cust_product_fig.add_bar(
            x=customer_orders.order_month_date,
            y=customer_orders.order_item_id,
            textangle=45,
        )

    return cust_product_fig


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
    top_n_df_by_customer = pd.read_json(datasets['top_n']['customer'])

    # top_n_df_by_month.sort_values(by=f'{radio_value}', ascending=True),
    top_n_df_by_product.sort_values(by=f'{radio_value}', ascending=False, inplace=True)
    # top_n_df_by_product.reset_index()
    top_n_df_by_customer.sort_values(by=f'{radio_value}', ascending=False, inplace=True)
    # top_n_df_by_customer.reset_index()

    print("Top Product Categories by month\n", top_n_df_by_product.head(slider_value))
    print("Top Customers by month\n", top_n_df_by_customer.head(slider_value))

    top_n_df_by_product = top_n_df_by_product[:slider_value]
    # top_n_df_by_product.sort_values(by=f'{radio_value}', ascending=False, inplace=True)
    top_n_df_by_customer = top_n_df_by_customer[:slider_value]

    top_n_df_by_product = top_n_df_by_product.sort_values(by=radio_value, ascending=True)
    top_n_df_by_customer = top_n_df_by_customer.sort_values(by=radio_value, ascending=True)

    cs_top_prod_fig = make_subplots(rows=1, cols=1,
                                    specs=[[{"secondary_y": True}]])
    cs_top_prod_fig.add_traces(
        [
            # go.Scatter(
            #     y=top_n_df_by_product.product_category_name_english,
            #     x=[0] * len(top_n_df_by_product.index) + 1,
            #     mode='lines',
            #     name=f'{radio_value}',
            #     marker=dict(
            #         color='#333'
            #     )
            # ),
            go.Scatter(
                y=top_n_df_by_product.product_category_name_english.apply(lambda x: x.replace("_", " ").title()),
                x=top_n_df_by_product[radio_value],
                mode='markers+text',
                name=f'{radio_value}'.replace("_", " ").title(),
                marker=dict(
                    color='#9BCEB5',
                    size=30,
                ),
                hovertemplate="""
                the %{y} product category<br>had orders totaling $%{x:,.2f}
                <br>
                <extra></extra>
                """,
                text=top_n_df_by_product[radio_value].apply(lambda x: pg_utils.human_format(x)),
                texttemplate="%{text}",
                textposition='middle center'  # ['top left', 'top center', 'top right',
                # 'middle left','middle center', 'middle right',
                # 'bottom left', 'bottom center', 'bottom right']

            )]
    )

    cs_top_prod_fig.update_layout(
        hovermode='x',
        margin={"r": 0, "t": 75, "l": 0, "b": 0},
        uniformtext_minsize=8,
        uniformtext_mode='hide',
    )

    # # Creating the Top Product Bar Graph
    # cs_top_prod_fig.add_bar(
    #     x=sorted(np.log10(top_n_df_by_product.profit)),
    #     y=top_n_df_by_product.product_category_name_english,
    #     # opacity=.2,
    #     row=1,
    #     col=1,
    #     # secondary_y=True,
    #     name='profit',
    #     orientation='h',
    #     # visible='legendonly'
    #     # marker={'line': {'color': '#E4F2EF', 'width': 0.5, }},
    # )
    #
    # cs_top_prod_fig.add_bar(
    #     x=sorted(np.log10(top_n_df_by_product.freight_value)),
    #     y=top_n_df_by_product.product_category_name_english,
    #     # opacity=.2,
    #     row=1,
    #     col=1,
    #     # secondary_y=True,
    #     name='shipping_cost',
    #     orientation='h',
    #     # visible='legendonly'
    # )
    cs_top_prod_fig.update_layout(
        title=f'Top {slider_value} Prod Categories',
        barmode='stack',  # 'stack', 'group', 'overlay', 'relative',
        # clickmode='event+select',
    )
    # cs_top_prod_fig.layout.yaxis.title = "Product Category"
    cs_top_prod_fig.layout.xaxis.title = f'{radio_value}'
    cs_top_prod_fig.layout.xaxis.visible = False
    cs_top_prod_fig.layout.hovermode = 'closest'  # 'x', 'y', 'closest', False, 'x unified', 'y unified']

    def dumbell_plot_test(cs_bottom_prod_fig):
        from plotly import data
        df = data.gapminder()
        df = df.loc[(df.continent == "Europe") & (df.year.isin([1952, 2002]))]

        countries = (
            df.loc[(df.continent == "Europe") & (df.year.isin([2002]))]
            .sort_values(by=["lifeExp"], ascending=True)["country"]
            .unique()
        )

        data = {"x": [], "y": [], "colors": [], "years": []}

        for country in countries:
            data["x"].extend(
                [
                    df.loc[(df.year == 1952) & (df.country == country)]["lifeExp"].values[0],
                    df.loc[(df.year == 2002) & (df.country == country)]["lifeExp"].values[0],
                    None,
                ]
            )
            data["y"].extend([country, country, None]),
            data["colors"].extend(["green", "blue", "brown"]),
            data["years"].extend(["1952", "2002", None])

        cs_bottom_prod_fig = go.Figure(
            data=[
                go.Scatter(
                    x=data["x"],
                    y=data["y"],
                    mode="lines",
                    marker=dict(
                        color="grey",
                    ),
                ),
                go.Scatter(
                    x=data["x"],
                    y=data["y"],
                    mode="markers+text",
                    marker=dict(
                        color=data["colors"],
                        size=10,
                    ),
                    hovertemplate="""Country: %{y} <br> Life Expectancy: %{x} <br><extra></extra>""",
                ),
            ]
        )

        return cs_bottom_prod_fig

    # Bottom Product Fields
    # cs_bottom_prod_fig = ""
    # cs_bottom_prod_fig = dumbell_plot_test(cs_bottom_prod_fig)
    cs_bottom_prod_fig = make_subplots(rows=1, cols=1,
                                       specs=[[{"secondary_y": True}]])
    cs_bottom_prod_fig.add_trace(
        go.Bar(
            y=top_n_df_by_customer[radio_value],
            x=top_n_df_by_customer.customer_unique_id,
            # orientation='h',
            name=f'{radio_value}',
            text=top_n_df_by_customer[radio_value].apply(lambda x: pg_utils.human_format(x)),
            hovertemplate='%{x} has <br> ordered %{text} worth of products<br> from OList<extra></extra>',
            texttemplate="%{text}",
            textposition='inside'
        )
    )

    # adding customers by month bar chart to figure.
    # cs_bottom_prod_fig.add_bar(
    #     x=sorted(np.log10(top_n_df_by_customer.profit), reverse=True),
    #     y=top_n_df_by_customer.product_category_name_english,
    #     # opacity=.2,
    #     row=1,
    #     col=1,
    #     # secondary_y=True,
    #     name='profit',
    #     orientation='h'
    #     # marker={'line': {'color': '#E4F2EF', 'width': 0.5, }},
    # )
    #
    # cs_bottom_prod_fig.add_bar(
    #     x=sorted(np.log10(top_n_df_by_customer.freight_value), reverse=True),
    #     y=top_n_df_by_customer.product_category_name_english,
    #     # opacity=.2,
    #     row=1,
    #     col=1,
    #     # secondary_y=True,
    #     name='shipping_cost',
    #     orientation='h'
    # )

    cs_bottom_prod_fig.update_layout(
        title=f'Top  {slider_value} Customers',
        barmode='stack',  # 'stack', 'group', 'overlay', 'relative',
        margin={"r": 0, "t": 75, "l": 0, "b": 0},
        uniformtext_minsize=8,
        # uniformtext_mode='hide',
        xaxis_tickangle=-45,
        xaxis_tickfont_size=8,
        xaxis_visible=False,  # intentionally set to show a different way of doing this.
    )
    cs_bottom_prod_fig.layout.xaxis.title = "Customers"
    cs_bottom_prod_fig.layout.yaxis.title = f"{radio_value}"
    cs_bottom_prod_fig.layout.yaxis.visible = False
    cs_bottom_prod_fig.layout.hovermode = 'closest'

    # Customers Pivot Table Creation

    return cs_top_prod_fig, cs_bottom_prod_fig


@callback(
    Output('cs-customers-pivot-table', 'children'),
    Input('cs-n-radioitems', 'value'),
    Input('data-store', 'data'),
    Input('cs-top-customers', 'clickData'),
    Input('cs-top-products', 'clickData'),
    Input("btn_csv", "n_clicks"),
)
def drilldown_customers(radio_value, data, cus_clickData, prod_clickData, n_clicks):
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

        # User clicked on product will be used here.
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
    elif trigger_id == 'btn_csv':
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

        customers_gby.sort_values(by=f"{radio_value}", ascending=False, inplace=True)

        # Create Tooltip based off each row in groubpy.
        tooltip_data = [
            {
                'payment_value': {
                    'value': f"{row['customer_unique_id']} has purchased a total of ${row['payment_value']} from OList",
                    'type': 'markdown'
                }
            } for row in customers_gby.to_dict('records')
        ]

        cs_customers_pivot_table = pg_utils.generate_generic_dash_datatable(
            customers_gby,
            'cs-customers-pivot-table',
            tooltip_data,
            # tooltip_header
        )

        cs_customers_pivot_table = pg_utils.generate_generic_dash_datatable(
            customers_gby,
            'cs-customers-pivot-table',
            tooltip_data,
            # tooltip_header
        )



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

        customers_gby.sort_values(by=f"{radio_value}", ascending=False, inplace=True)

        # Create Tooltip based off each row in groubpy.
        tooltip_data = [
            {
                'payment_value': {
                    'value': f"{row['customer_unique_id']} has purchased a total of ${row['payment_value']} from OList",
                    'type': 'markdown'
                }
            } for row in customers_gby.to_dict('records')
        ]

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
    Input('cohort_selection_dd', 'value')
    # prevent_initial_call=True
)
def update_cohort_analysis_graphs(data, cohort_val):
    datasets = json.loads(data)

    # Customers Data for creating a customers cohort
    dff = pd.read_csv('./data/combined_olist_data.csv')

    # Marketing Data for creating a seller's cohort
    mql_df = pd.read_json(datasets['marketing_mql'])
    closed_df = pd.read_json(datasets['marketing_closed_deals'])

    marketing_df = mql_df.merge(closed_df, on='mql_id', how='left')

    # Finding the number of customers that belong to each cohort
    # cohortGrouping = dff.groupby(['cohort_month', 'cohort_index'])
    # cohortGrouping_df = cohortGrouping['seller_id'].apply(pd.Series.nunique).reset_index()
    if cohort_val is None:
        cohort_val = 'payment_value'
    cohortGrouping_counts, retention_cohort = pg_utils.create_cohort_analysis(df=dff, groupby_col=cohort_val,
                                                                              agg_val=pd.Series.mean)
    # print(cohortGrouping_counts, retenti)

    # # Calculating Cohort Retention Rates amoung the cusotmers.
    # total_cohort = cohortGrouping_counts.iloc[:, 0]
    # retention_cohort = cohortGrouping_counts.divide(total_cohort, axis=0)
    # print("Retention Cohort has a type of", type(retention_cohort))
    # retention_cohort = retention_cohort.round(3) * 100
    # print(retention_cohort)

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
    # retention_cohort['cohort_by'] = cohort_val.replace("_", " ").title()
    # retention_cohort = retention_cohort.sort_values(by=retention_cohort.columns, inplace=True)

    print(retention_cohort.head())
    print("Retention Cohort has a type of", type(retention_cohort))

    if cohort_val == 'order_item_id':
        hoverTemplate="""
                    Cohort %{y} in %{x| %B %Y} <br> ordered an average of <br> of %{z:,}
                    items.<extra></extra><extra></extra>
                   """
    else:
        hoverTemplate="""
                            Cohort %{y} in %{x| %B %Y} <br> had an <br> of $%{z:,.2f}<extra></extra><extra></extra>
                           """

    retention_cohort_fig = go.Figure()
    retention_cohort_fig.add_trace(
        go.Heatmap(z=retention_cohort.values,
                   x=retention_cohort.index,
                   y=retention_cohort.columns,
                   # text=retention_cohort.cohort_by,
                   hovertemplate=hoverTemplate,

                   # texttemplate="%{text}",
                   colorscale=pio.templates['atbAnalyticsGroupDefault'].layout.colorscale.diverging
                   ),
    )

    cohort_val = cohort_val.replace("_", " ").title()
    retention_cohort_fig.layout.yaxis.title = 'Cohort'
    retention_cohort_fig.layout.xaxis.title = f'{cohort_val}'
    retention_cohort_fig.layout.title = f"{cohort_val}"

    avg_price_cohort = avg_price_cohort.dropna(axis=0, how='all').fillna(0)
    avg_price_cohort_fig = go.Figure()
    avg_price_cohort_fig.add_trace(
        go.Heatmap(z=avg_price_cohort.values,
                   x=avg_price_cohort.index,
                   y=avg_price_cohort.columns,
                   hovertemplate="""
     Cohort %{y} in %{x} <br> had an average order value <br>of $%{z:,.2f} dollars<extra></extra><extra></extra>
    """,
                   # text=retention_cohort.values,
                   # texttemplate="%{text}",
                   colorscale=pio.templates['atbAnalyticsGroupDefault'].layout.colorscale.diverging,
                   ),
    )

    avg_price_cohort_fig.layout.xaxis.title = 'Avg Payment Value'
    avg_price_cohort_fig.layout.yaxis.title = 'Cohort'
    avg_price_cohort_fig.layout.title = 'Payment Value'

    return retention_cohort_fig, avg_price_cohort_fig


# TODO add interactivity to the rfm analysis - instead of monetary change to frequency, or recency
@callback(
    Output('rfm-date', 'children'),
    Output('rfm-analysis', 'figure'),
    Input('data-store', 'data'),
    Input('rfm_selection_dd', 'value')
    # prevent_initial_call=True
)
def update_rfm_analysis_graph(data, rfm_value):
    datasets = json.loads(data)

    # Customers Data for creating a customers cohort
    dff = pd.read_csv('./data/combined_olist_data.csv')

    # Marketing Data for creating a seller's cohort
    mql_df = pd.read_json(datasets['marketing_mql'])
    closed_df = pd.read_json(datasets['marketing_closed_deals'])

    marketing_df = mql_df.merge(closed_df, on='mql_id', how='left')

    # Calculating the Recency, Frequency and Monetary Value for
    # each customer
    pg_utils.convert_to_datetime(dff, 'order_purchase_timestamp')
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
    repeat_rate_df = dff.groupby('customer_unique_id').agg(
        {
            'most_recent_order': lambda day: (today - day.max()).days,
            'order_id': 'count',
            'payment_value': 'sum'
        }

    )

    rrdf = repeat_rate_df[repeat_rate_df['order_id'] > 1]  # Only the Orders that are greater than 1.
    repeat_percent = rrdf['order_id'].sum() / repeat_rate_df['order_id'].sum()
    print("Percent of repeat customers ", repeat_percent * 100)

    # repeat_rate = sum of cust order 2+ times/ sum of cust order 1+ times (tot customers)
    repeat_rate = rrdf['order_id'].count() / repeat_rate_df['order_id'].count()
    churn_rate = 1 - repeat_rate

    # rfm_s = dff[['customer_unique_id', 'most_recent_order', 'order_id', 'payment_value']]
    # rfm = rrdf
    # rfm = rfm.groupby('customer_unique_id').agg({
    #     'order_id': 'count',
    #     'most_recent_order': 'first',
    #     'payment_value': 'sum'
    # }).reset_index()
    if rfm_value is None:
        rfm_value = 'recency'
        rfm_value = rfm_value.lower()
    else:
        rfm_value = rfm_value.lower()
    rfm_cols = ['recency', 'frequency', 'monetary']
    rrdf.columns = rfm_cols
    rfm = rrdf
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

    # TODO Check that this is correct
    rfm['segment'] = rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str)
    rfm['segment'] = rfm['segment'].replace(seg_map, regex=True)

    rfm.groupby('segment', as_index=False).mean().sort_values('monetary')
    print(rfm)
    # rfm = rfm.fillna(0, inplace=True)
    # print(rfm)
    hover_template = ""

    if rfm_value == "recency":
        hover_template += """
        %{y} last ordered %{z} days ago,<br>and had a recency score of %{x} 
        <extra></extra>
        """
    elif rfm_value == "frequency":
        hover_template += """
        %{y} has shopped with us %{z} times<br> and had a frequency score of %{x}
        <extra></extra>
        """
    else:
        hover_template += """
        %{y} has spent $%{z:,.2f} with us <br> and has a monetary score of %{x}
        <extra></extra>
        """

    rfm_fig = go.Figure()
    rfm_fig.add_heatmap(
        y=rfm.segment,
        x=sorted(rfm[rfm_value + "_score"]),
        z=rfm[rfm_value],
        hovertemplate=hover_template,
        colorscale=pio.templates['atbAnalyticsGroupDefault'].layout.colorscale.diverging,

    )
    if rfm_value == 'recency':
        rfm_fig.update_xaxes(autorange='reversed')

    rfm_fig.layout.yaxis.type = 'category'
    rfm_fig.layout.xaxis.type = 'category'

    rfm_fig.layout.xaxis.title = '{}'.format(rfm_value.title())
    rfm_fig.layout.yaxis.title = 'Customer Segmentation'
    rfm_fig.layout.title = "{}".format(rfm_value.title())

    today = f"The date used for this analysis is {today}"

    return today, rfm_fig
