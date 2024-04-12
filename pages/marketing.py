import json
from os.path import exists

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.io as pio
from dash import dcc, html, Input, Output, State, callback
from joblib import load
from plotly import graph_objects as go

from page_utilities.page_utilities import PageUtilities

DIVERGING = pio.templates['atbAnalyticsGroupDefault'].layout.colorscale.diverging
SEQUENTIAL = pio.templates['atbAnalyticsGroupDefault'].layout.colorscale.sequential

pg_utils = PageUtilities()

dash.register_page(__name__,
                   path='/marketing-analysis',
                   name='Marketing',
                   title='Olist - Marketing Analysis', )

# if not exists('ml/models/marketing_signup_knnReg.joblib'):
#     from ml.sales_models import ForecastingModel as fcastModel
#
#     fcastModel = fcastModel()
#
#     mql_df = pd.read_csv('./data/OlistEcomData/olist_marketing_qualified_leads_dataset.csv')
#     closed_df = pd.read_csv('./data/OlistEcomData/olist_closed_deals_dataset.csv')
#     marketing_df = mql_df.merge(closed_df, on='mql_id', how='left')
#
#     pg_utils.convert_to_datetime(marketing_df, ['won_date', 'first_contact_date'])
#
#     marketing_df['days_to_close'] = (marketing_df.won_date - marketing_df.first_contact_date).dt.days
#     print(marketing_df.head(20))
#     print("Origin Values\n", marketing_df.origin.unique())
#     print("Business Segment Values\n", marketing_df.business_segment.unique())
#     print("Lead Behaviour Profile Values\n", marketing_df.lead_behaviour_profile.unique())
#     print("Lead Type Values\n", marketing_df.lead_type.unique())
#
#     # converting the categorical features to numerical for use in the ml models.
#     # KNN Regressor should help us predict whether or not we can predict the days to close
#     # based on their origin, business_segment, lead_type, and/or behaviour profile
#     # because none of these features besides origin can be considered ordinal we are going to
#     # use Target Encoding to avoid one hot encoding and dimensionality in the business segment
#     marketing_df['won_target'] = marketing_df.won_date.apply(lambda x: 0 if x is pd.NaT else 1)
#     print(marketing_df[['won_date', 'won_target']])
#     for c in ['origin', 'business_segment', 'lead_type', 'lead_behaviour_profile']:
#         marketing_df[c].fillna("")
#
#     marketing_df = fcastModel.encode_categorical_feature(df=marketing_df,
#                                                          col=['origin', 'business_segment', 'lead_type',
#                                                               'lead_behaviour_profile'])
#     marketing_ml_df = marketing_df[
#         ['origin_encoded', 'business_segment_encoded', 'lead_type_encoded', 'lead_behaviour_profile_encoded',
#          'won_target']]
#     for c in marketing_ml_df.columns:
#         print(c, "has ", marketing_ml_df[c].isnull().sum(), " missing values")
#     marketing_ml_df.fillna(0, inplace=True)
#     print(marketing_ml_df.head())
#     X = marketing_ml_df.iloc[:, 0:4]
#     y = marketing_ml_df.iloc[:, 4:5]
#     model = fcastModel.knn_regression(X=X, y=y, filename='marketing_signup_knnReg', save=True, save_path='ml/models')
# else:
#     prediction1 = [[.162875, 0, 0, 0]]
#     prediction2 = [[.162875, 1, 1, 1]]
#     prediction3 = [[.532725, 1, 0, 0]]
#
#     knnReg_model = load('ml/models/marketing_signup_knnReg.joblib')
#     print(knnReg_model.predict(prediction1), knnReg_model.kneighbors_graph(prediction1).toarray())
#     print(knnReg_model.predict(prediction2), knnReg_model.kneighbors_graph(prediction2).toarray())
#     print(knnReg_model.predict(prediction3), knnReg_model.kneighbors_graph(prediction3).toarray())
#     # print(knnReg_model.score([prediction3, prediction1, prediction2], [0, 1, 1]))

# Loading data that is used as the base for all the callbacks.

# TODO figure out why these aren't global and accessible in the callbacks
dff = pd.read_csv('./data/merchants_df.csv')
geo_df = pd.read_csv('./data/suppliers_geo_data.csv')
mql_df = pd.read_csv('./data/OlistEcomData/olist_marketing_qualified_leads_dataset.csv')
closed_df = pd.read_csv('data/OlistEcomData/olist_closed_deals_dataset.csv')

# Master Marketing Dataframe
marketing_df = mql_df.merge(closed_df, on='mql_id', how='left')

"""
Layout for Marketing Page
"""
layout = dbc.Container(
    children=[
        html.H1("Marketing Insights", className='display-1'),
        html.Br(),
        html.P(
            children=[
                """
                As you go through the Marketing Insights page, there a few things to keep in mind. 

            """,

            ],

        ),
        html.Br(),
        html.Ul(
            children=[
                html.Li(
                    id='mkt-insight-1',
                    children=[
                        """
                        Generating Automated Insights...
                        """
                    ]
                ),
                html.Br(),
                html.Li(
                    id='mkt-insight-2',
                    children=[
                        """
                        Generating Automated Insights...
                        """
                    ]
                ),
                html.Br(),
                # html.Li(
                #     """
                #     The closed leads data starts in December 2017 and goes until November 2018.
                #     Using this data we can look at conversion rates,
                #     the most successful sales directors or the most successful
                #     reps as well. They also classified each lead into a type and behavior profile as well, giving
                #     us even more ways to slice the data.
                #     """
                # ),
                html.Li(
                    id='mkt-insight-3',
                    children=[
                        """
                        Generating Automated Insights
                        """
                    ]
                ),
                html.Br(),
                html.Li(
                    children=[
                        """
                        The KPI's below are pre-filtered to the Marketing data, you can see how that stacks against
                        the totals for the time period, but to get a better understanding of the 
                        """,
                        dcc.Link("Customers", href='http://127.0.0.1:8050/customer-analysis'),
                        """
                         or the 
                        """,
                        dcc.Link("Merchants", href='http://127.0.0.1:8050/merchants-analysis'),
                        """
                            visit their pages to get more detailed information.
                        """

                    ]
                ),
                html.Br(),
            ],
        ),
        html.Br(),
        # Marketing KPI Row -1
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.Div(
                            # id='customer-seller-kpi-card-group-wrapper',
                            children=[
                                pg_utils.create_kpi_card('mkt-conversion-rate'),

                            ],
                            className='card-group',
                        )
                    ],
                    width=12,
                    align='center',
                ),
            ],
        ),
        dbc.Row(
            children=[
                html.Div(
                    children=[
                        dbc.Col(
                            children=[
                                pg_utils.create_kpi_card('mkt-tot-orders'),
                            ],
                            align='center',
                            className='col-md-6 col-sm-12'
                        ),
                        dbc.Col(
                            children=[
                                pg_utils.create_kpi_card('mkt-revenue'),
                            ],
                            align='center',
                            className='col-md-6 col-sm-12'
                        ),

                    ],
                    className='card-group'
                )
            ]
        ),
        # Marketing KPI Row - 2
        dbc.Row(
            children=[
                html.Div(
                    children=[
                        dbc.Col(
                            children=[
                                pg_utils.create_kpi_card('mkt-merchant-value'),
                            ],
                            align='center',
                            className='col-md-6 col-sm-12'
                        ),
                        dbc.Col(
                            children=[

                                pg_utils.create_kpi_card('mkt-time-to-signup'),
                            ],
                            align='center',
                            className='col-md-6 col-sm-12'
                        ),

                    ],
                    className='card-group'
                )
            ],
        ),
        html.Br(),
        html.H2("Campaign Analysis", className='display-2'),
        html.Br(),
        html.P(
            id='map-explainer-pg',
            children=[
                """
                Below is the marketing campaign success by state location. Hover or Click on the map to get more 
                specific information pertaining to that location.
                """
            ]
        ),
        html.Br(),

        dbc.Row(
            children=[
                # User Selection Dropdowns
                # dbc.Col(
                #     children=[
                #         html.Div(
                #             children=[
                #
                #                 dbc.Card(
                #                     dbc.CardBody(
                #                         children=[
                #                             html.H3("Lead Source", className='text-center'),
                #                             html.Br(),
                #                             html.P(
                #                                 """
                #                                 The channel that the marketing lead originated from.
                #                                 """
                #                             ),
                #                             dcc.Dropdown(
                #                                 id='dd-channel',
                #                                 # multi=True,
                #                                 searchable=True,
                #                                 clearable=False,
                #                                 placeholder="Select a Lead Source",
                #                                 disabled=False,
                #                                 optionHeight=50,
                #                                 className='ui-selection-dropdown',
                #                             ),
                #
                #                         ]
                #                     ),
                #                     className='user-selection-card'
                #                 ),
                #
                #                 dbc.Card(
                #                     dbc.CardBody(
                #                         children=[
                #                             html.H3("Lead Type", className='text-center'),
                #                             html.Br(),
                #                             html.P(
                #                                 """
                #                                     How the lead has been classified during this
                #                                     campaign.
                #                                 """
                #                             ),
                #                             dcc.Dropdown(
                #                                 id='dd-lead-type',
                #                                 # multi=True,
                #                                 searchable=True,
                #                                 clearable=False,
                #                                 placeholder="Select a Lead Type",
                #                                 disabled=False,
                #                                 optionHeight=50,
                #                                 className='ui-selection-dropdown',
                #                             ),
                #
                #                         ]
                #                     ),
                #                     className='user-selection-card'
                #                 ),
                #
                #                 dbc.Card(
                #                     dbc.CardBody(
                #                         children=[
                #                             html.H3("Sales Team - SDR", className='text-center'),
                #                             html.Br(),
                #                             html.P(
                #                                 """
                #                                     The sales team statistics during the Marketing
                #                                     campaign by Director.
                #                                 """
                #                             ),
                #                             dcc.Dropdown(
                #                                 id='sdr-sales-team',
                #                                 # multi=True,
                #                                 searchable=True,
                #                                 clearable=False,
                #                                 placeholder="Select a Sales Director",
                #                                 disabled=False,
                #                                 optionHeight=50,
                #                                 className='ui-selection-dropdown',
                #                             ),
                #
                #                         ]
                #                     ),
                #                     className='user-selection-card'
                #                 ),
                #             ],
                #             className='card-group',
                #         )
                #     ],
                #     width=12,
                #     align='center',
                # ),

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
                                                id='map-selection-value',
                                                options=[{'label': 'Merchant signups', 'value': 'merchant_count'},
                                                         {'label': 'Payment value', 'value': 'payment_value'},
                                                         # {'label': 'Payment value(Scaled)',
                                                         #  'value': 'payment_value_scaled'}
                                                         ],

                                                inline=True,
                                                value='merchant_count'
                                            )
                                        ]
                                    ),
                                    className='user-selection-card'
                                )
                            ]
                        ),
                        pg_utils.create_kpi_card('won-merchant-map'),
                        html.P(
                            id='map-insight-1',
                            children=[
                                'Generating Automated Campaign Map Insight'
                            ]
                        )
                    ],
                    width=12,
                    align='center',
                ),
                dbc.Row(
                    children=[
                        html.H2("Channels and Sales"),

                        dbc.Col(
                            children=[
                                # pg_utils.create_kpi_card()
                                html.Div(
                                    children=[
                                        html.P(
                                            children=[
                                                """
                                                The Marketing Campaign data we are analyzing was started in June 2017
                                                and ended in May of 2018. Without more information on operating costs, 
                                                marketing channel, lead costs etc. we cannot really quanitfy the 
                                                effectiveness of the campaign. 
                                                """,
                                                html.Br(),
                                                html.Br(),
                                                html.H3("Lead Qualifying Process"),
                                                html.Br(),
                                                """
                                                Currently the process for qualifying a lead is, they land on a landing 
                                                page fill out a form. After the Lead fills out the form on the 
                                                landing page, they are contacted by the Sales Development 
                                                Rep (SDR) where more information is gathered for the Sales Representative (SR)
                                                """,
                                                # html.Ul(
                                                #     children=[
                                                #         html.Li(
                                                #             children=[
                                                #                 """
                                                #                 Since OList did not provide any Marketing Expenses, you would  have to make some
                                                #                 assumptions about these.
                                                #                 """,
                                                #                 html.Ol(
                                                #                     children=[
                                                #                         html.Li(
                                                #                             """
                                                #                                 Assume the cost of the SDR and SR are included in the
                                                #                                 Marketing Cost's and will have to see if we can find the average
                                                #                                 salary for Brazil for these roles. This will not include any type
                                                #                                 of incentive structure for simplicity, and to keep the base case
                                                #                                 simple, we will also assume that these are yearly salaries.
                                                #                             """
                                                #                         ),
                                                #                         html.Br(),
                                                #                         html.Li(
                                                #                             """
                                                #                                 Assume that the landing pages that were created
                                                #                                 were created by an in-house design team, and has more than enough
                                                #                                 capacity to handle
                                                #                                 the landing page design,development, and launch. This means the cost for
                                                #                                  this should be less than if they were to hire an agency, freelancers,
                                                #                                  or a combination of the two.
                                                #                             """
                                                #                         ),
                                                #                         html.Br(),
                                                #                         html.Li(
                                                #                             """
                                                #                                 Assume a base tax rate, discount rate,
                                                #                                 as well as a standard YoY Growth rate in our assumptions about the base
                                                #                                 case. We could try and track these numbers down but for the sake of
                                                #                                 simplicity we will assume them.
                                                #                             """
                                                #                         )
                                                #                     ]
                                                #                 )
                                                #             ]
                                                #         ),
                                                #         html.Br(),
                                                #         html.Li(
                                                #             children=[
                                                #                 """
                                                #                     Once the base case is established things such as revenue lift, if any,
                                                #                     can be calculated to
                                                #                     try to quantify the success of this campaign.
                                                #                 """
                                                #             ]
                                                #         )
                                                #     ]
                                                # ),
                                                html.Br(),
                                            ]
                                        ),
                                        html.Br(),
                                        dbc.Card(
                                            dbc.CardBody(
                                                children=[
                                                    html.H3("Marketing Channels and Sales"),
                                                    html.P("Choose how you would like to view top channels and top "
                                                           "sales charts"),
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Col(
                                                                children=[
                                                                    dbc.Card(
                                                                        dbc.CardBody(
                                                                            children=[
                                                                                html.H4("Marketing Channel",
                                                                                        className='text-center'),
                                                                                html.Br(),
                                                                                html.P(
                                                                                    """
                                                                                    The channel that the marketing lead 
                                                                                    originated from.
                                                                                    """
                                                                                ),
                                                                                dcc.Dropdown(
                                                                                    id='dd-channel',
                                                                                    # multi=True,
                                                                                    searchable=True,
                                                                                    clearable=False,
                                                                                    placeholder="Select a Marketing "
                                                                                                "Channel",
                                                                                    disabled=False,
                                                                                    options=[
                                                                                        # {'label': 'Origin',
                                                                                        #  'value': 'origin'},
                                                                                        {'label': 'Lead Type',
                                                                                         'value': 'lead_type'},
                                                                                        {'label': 'Lead Profile Type',
                                                                                         'value': 'lead_behaviour_profile'},
                                                                                    ],
                                                                                    optionHeight=50,
                                                                                    className='ui-selection-dropdown',
                                                                                ),

                                                                            ]
                                                                        ),
                                                                        className='user-selection-card nested'
                                                                    )
                                                                ],
                                                                className='col-md-6 col-sm-12',
                                                                align='center',
                                                            ),

                                                            dbc.Col(
                                                                children=[
                                                                    dbc.Card(
                                                                        dbc.CardBody(
                                                                            children=[
                                                                                html.H3("Sales by Channel",
                                                                                        className='text-center'),
                                                                                html.Br(),
                                                                                html.P(
                                                                                    """
                                                                                    View the sales by this Channel
                                                                                    """
                                                                                ),
                                                                                dcc.Dropdown(
                                                                                    id='dd-sales',
                                                                                    # multi=True,
                                                                                    searchable=True,
                                                                                    clearable=False,
                                                                                    placeholder="Select a Sales "
                                                                                                "Channel",
                                                                                    disabled=False,
                                                                                    options=[
                                                                                        {'label': 'Sales Rep',
                                                                                         'value': 'sr_id'},
                                                                                        {'label': 'Sales Dev Rep',
                                                                                         'value': 'sdr_id'},
                                                                                        # {'label': 'Landing Page',
                                                                                        #  'value': 'landing_page_id'},
                                                                                    ],
                                                                                    optionHeight=50,
                                                                                    className='ui-selection-dropdown',
                                                                                ),

                                                                            ]
                                                                        ),
                                                                        className='user-selection-card nested'
                                                                    )
                                                                ],
                                                                className='col-md-6 col-sm-12',
                                                                align='center',
                                                            ),

                                                        ]
                                                    ),

                                                ]
                                            ),
                                            className='user-selection-card'
                                        )
                                    ]
                                )
                            ],
                            width=12,
                            align='center',
                        ),
                        dbc.Col(
                            children=[
                                pg_utils.create_kpi_card('top-channels-chart'),
                                html.P(
                                    id='channel-insight-1',
                                    children=[
                                        'Generating Automated Marketing Channel Insight'
                                    ]
                                )
                            ],
                            className='col-md-6 col-sm-12'
                        ),
                        dbc.Col(
                            children=[
                                pg_utils.create_kpi_card('top-sales-by-chart'),
                                html.P(
                                    id='sales-insight-1',
                                    children=[
                                        'Generating Automated Sales Insight'
                                    ]
                                )
                            ],
                            className='col-md-6 col-sm-12'
                        ),

                    ],
                    # width=12,
                    align='center',
                ),
                dbc.Col(
                    children=[
                        pg_utils.create_kpi_card('sales-team-chart'),
                        html.Div(
                            id='sales-insight-1',
                            children=[
                                'Generating Automated Sales Team Insight'
                            ]
                        )
                    ],
                    width=12,
                    align='center',
                ),
            ]
        ),
    ],
)

# @callback(
#
#     Output('dd-channel', 'options'),
#     Output('dd-sales', 'options'),
#     # Output('sdr-sales-team', 'options'),
#     Input('data-store', 'data'),
#     suppress_callback_exceptions=True,
#     # prevent_initial_call=True
# )
# def update_dropdowns(data):
#     datasets = json.loads(data)
#     mql_df = pd.read_json(datasets['marketing_mql'])
#     closed_df = pd.read_json(datasets['marketing_closed_deals'])
#     merchants_geo = pd.read_csv('./data/suppliers_geo_data.csv')
#
#     # To add a component as the label to the dropdown.
#     # {
#     #     "label": html.Div(
#     #         [
#     #             html.Img(src="/assets/images/language_icons/python_50px.svg", height=20),
#     #             html.Div("Python", style={'font-size': 15, 'padding-left': 10}),
#     #         ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
#     #     ),
#     #     "value": "Python",
#     # }
#
#     origin = [{'label': i, 'value': i} for i in list(closed_df['business_type'].fillna("None").unique())]
#     leadType = [{'label': i, 'value': i} for i in list(closed_df['lead_type'].fillna("None").unique())]
#     sdr = [{'label': i, 'value': i} for i in list(closed_df['sdr_id'].fillna("None").unique())]
#
#     return origin, leadType

# TODO Turn this into a page utility function since this is used across different pages.
'''
Updates the KPI's that are being populated in the beginning of the page. 
'''


@callback(
    Output('mkt-insight-1', 'children'),
    Output('mkt-insight-2', 'children'),
    Output('mkt-insight-3', 'children'),
    Input('data-store', 'data'),
)
def marketing_insights(data):
    datasets = json.loads(data)
    mql_df = pd.read_json(datasets['marketing_mql'])
    closed_df = pd.read_json(datasets['marketing_closed_deals'])

    # Master Marketing Dataframe
    marketing_df = mql_df.merge(closed_df, on='mql_id', how='left')

    marketing_only_df = marketing_df[
        ['seller_id', 'mql_id', 'landing_page_id', 'origin', 'lead_type', 'lead_behaviour_profile', 'business_segment',
         'business_type', 'first_contact_date', 'won_date']]

    merchants_df = pd.read_json(datasets['seller_cust_pivot_df'])
    merchants_df['last_order'] = merchants_df['order_month_date']

    merchants_df = merchants_df.groupby(['seller_id']).agg({
        'order_month_date': 'first',
        'last_order': 'last',
        'customer_unique_id': 'nunique',
        'payment_value': 'sum',
        'order_item_id': 'sum'
    }).reset_index()
    marketing_df = marketing_only_df.merge(merchants_df, on='seller_id', how='left')

    pg_utils.convert_to_datetime(marketing_df, ['first_contact_date', 'won_date'])

    tot_leads = marketing_df.mql_id.nunique()
    won_leads = marketing_df.won_date.count()
    tot_landing_pages = marketing_df.landing_page_id.nunique()
    first_contact_date = marketing_df.first_contact_date.min()
    last_contatct_date = marketing_df.first_contact_date.max()
    first_won_date = marketing_df.won_date.min()
    last_won_date = marketing_df.won_date.max()
    lead_type_count = marketing_df.lead_type.nunique()
    revenue_generated = marketing_df.payment_value.sum()
    items_sold = marketing_df.order_item_id.sum()
    # tot_orders = marketing_df.order_id.nuique()

    tot_campaign_days = last_contatct_date.date() - first_contact_date.date()
    # Basic campaign info
    insight_1 = """
                The campaign ran for a total of {} days. Starting in {:%B %Y} and ending
                in {:%B %Y} with a few conversions happening after completion.
                During which time {:,} leads were targeted by {:,} different 
                landing pages, across {:,} different Marketing Channels,
                 resulting in {:,} ({:,.2%}) new merchant signups.
              """.format(
        tot_campaign_days.days,
        first_contact_date.date(),
        last_contatct_date.date(),
        tot_leads,
        tot_landing_pages,
        lead_type_count,
        won_leads,
        (won_leads / tot_leads),
    )

    # Check the time it took to get the first sign up when starting the campaign
    days_to_first_conversion = first_won_date.date() - first_contact_date.date()

    # Amount generated by the Marketing Merchants
    insight_2 = """
            From the start of the campaign it took, {} days to get the first conversion. This Marketing campaign resulted
             in ${:,.2f} worth of revenue generated from {:,} items sold and an average item value of ${:,.2f} for 
             merchants that joined as a result of the campaign.
            """.format(days_to_first_conversion.days,
                       revenue_generated,
                       items_sold,
                       revenue_generated / items_sold
                       )
    # print(marketing_only_df)

    # Information about the top merchant business types, top acquisition channel etc.
    insight3_df = marketing_df[['business_segment', 'origin']]
    insight3_df['business_segment_count'] = insight3_df['business_segment']
    bs_df = marketing_df.groupby(['business_segment', 'origin']).count().reset_index()
    bs_df = bs_df.sort_values(by=['seller_id', 'business_segment'], ascending=False).reset_index()
    insight_3 = """
                Of the {} total merchant signups, most of the businesses are in the {} niche with {} ({:.2f}%) merchants
                 signed up. The second largest business niche was {} with {} merchants signing up.
                The largest marketing channel for these business came through the {} and {} channels, respectively.
                """.format(
        won_leads,
        bs_df.business_segment[0].replace("_", " ").title(),
        bs_df.seller_id[0],
        bs_df.seller_id[0] / won_leads,
        bs_df.business_segment[1].replace("_", " ").title(),
        bs_df.seller_id[1],
        bs_df.origin[0],
        bs_df.origin[1],

    )
    return insight_1, insight_2, insight_3


@callback(
    Output('mkt-conversion-rate', 'figure'),
    Output('mkt-tot-orders', 'figure'),
    Output('mkt-revenue', 'figure'),
    Output('mkt-time-to-signup', 'figure'),
    Output('mkt-merchant-value', 'figure'),
    # Output('cs-avg-order-items', 'figure'),
    # Output('cs-purchase-frequency', 'figure'),
    # Output('mkt-customer-merchants', 'figure'),
    # Output('mkt-avg-customer-value', 'figure'),
    # Output('mkt-avg-clv', 'figure'),
    Input('data-store', 'data'),
    #     suppress_callback_exceptions=True,
    #     prevent_initial_call=True
)
def update_marketing_kpis(data):
    # * Although some of this stuff says customer it is really for the marketing

    datasets = json.loads(data)

    dff = pd.read_csv('./data/merchants_df.csv')  # All merchants including the Won Leads
    mql_df = pd.read_json(datasets['marketing_mql'])
    closed_df = pd.read_json(datasets['marketing_closed_deals'])
    merchants_geo = pd.read_csv('./data/suppliers_geo_data.csv')

    # Creating Combined Marketing DF.
    merchants_geo = merchants_geo[[
        'seller_id', 'zip_code',
        'seller_city', 'seller_state',
        'geolocation_lat', 'geolocation_lng']]
    marketing_df = mql_df.merge(closed_df, on='mql_id', how='left')
    marketing_df = marketing_df.merge(merchants_geo, on='seller_id', how='left')

    total_marketing_leads = marketing_df.first_contact_date.count()
    won_leads = marketing_df.won_date.count()
    conversion_rate = won_leads / total_marketing_leads

    pg_utils.convert_to_datetime(dff, 'won_date')
    pg_utils.convert_to_datetime(dff, 'first_contact_date')

    pg_utils.convert_to_datetime(marketing_df, 'won_date')
    pg_utils.convert_to_datetime(marketing_df, 'first_contact_date')

    dff['time_to_close'] = (dff.won_date - dff.first_contact_date).dt.days
    marketing_df['time_to_close'] = (marketing_df.won_date - marketing_df.first_contact_date).dt.days

    # marketing_df = marketing_df.merge(dff[['seller_id', 'time_to_close']], on='seller_id', how='left')
    tot_sdrs = marketing_df.sdr_id.nunique()
    tot_sr = marketing_df.sr_id.nunique()
    # Won Leads Only DF
    # won_marketing_df = marketing_df[marketing_df.won_date.replace(pd.NAN, "0") != "0"]

    # TODO Double check that these numbers make senses
    # Filters the large DF to only the Merchants that joined due to Marketing. this will only capture those that have
    # actually had an order though since the new ones that haven't had an order would not be captured in the larger
    # dataset which was joined on the merchant/customer/order id keys.
    dff = dff[dff.won_date.replace(pd.NaT, "0") != "0"]

    # Would filter only to the Won Marketing Orders
    # won_marketing_df = marketing_df[marketing_df.won_date.replace(pd.NaT, "0") != "0"]

    marketing_orders = dff[['seller_id', 'customer_unique_id', 'order_id', 'order_item_id', 'payment_value']]
    marketing_orders = dff.groupby('seller_id').agg({
        'customer_unique_id': 'nunique',
        'order_id': 'nunique',
        'order_item_id': 'sum',
        'payment_value': 'sum'
    }).reset_index()

    marketing_df = marketing_df.merge(marketing_orders, on='seller_id', how='left')
    orders_df = dff[['order_id', 'order_month_date', 'seller_id', 'order_item_id', 'payment_value']]

    tot_customers = marketing_df.customer_unique_id.sum()
    tot_merchants = marketing_df.order_id.sum()
    # This is for the Marketing Orders
    tot_orders = marketing_df.order_id.sum()
    purchase_frequency = tot_orders / tot_customers
    tot_revenue = marketing_df.payment_value.sum()

    design_team = 0
    dev_team = 0
    # The actual expenses for Olist would be the SDR, SR, and Design and Development team costs.
    # We are going to say that the design team is in house already and at a fixed cost and labor force
    #  people, that put together the landing pages for the campaign and this cost is
    #
    #                           Max    |     Min | Avg | URL
    # SDR Cost -                R$114,050 | R$60,220 | R$88,990 | https://www.salary.com/research/br-salary/alternate/inside-sales-prospect-development-representative-salary/br
    # SR Cost -                 R$134,786|R$32,846|R$81,808|https://www.salary.com/research/br-salary/alternate/b2b-channel-sales-representative-i-salary/br
    # Design Team        -      R$83,253|R$33,841|$R58,559|https://www.salary.com/research/br-salary/alternate/graphic-designer-ii-salary/br
    # Development Team        - R$103,978|$R53,834|R$76,850|https://www.salary.com/research/br-salary/benchmark/web-applications-developer-ii-salary/br
    #
    #
    # Total Cost - ,,306,207
    #
    marketing_costs = {
        'sdr_cost': [114050, 60220, 88990, 36000],
        'sr_cost': [134786, 32846, 81808, ],
        'design_cost': [83253, 33841, 58559],
        'dev_cost': [103978, 53834, 76850]
    }
    tot_expenses = marketing_costs['sdr_cost'][3] * tot_sdrs + marketing_costs['sr_cost'][1] * tot_sr + \
                   marketing_costs['design_cost'][1] * design_team + marketing_costs['dev_cost'][1] * dev_team
    profit_margin = (tot_revenue - tot_expenses) / tot_revenue
    net_revenue = tot_revenue - tot_expenses
    tot_items_ordered = marketing_df.order_item_id.sum()
    avg_items_ordered = tot_items_ordered / tot_orders
    avg_order_value = marketing_df.payment_value.sum() / tot_orders

    # pg_utils.convert_to_datetime(marketing_df, 'time_to_close')
    # print(type(marketing_df.time_to_close[4]))
    avg_time_to_close = marketing_df.time_to_close.mean()

    # Checking the number of repeat customers. This is good to know so we can tell the sales reps what type of small
    # Businesses we're looking to Target to bring onto the platform.
    order_dff = dff[
        ['customer_unique_id', 'order_id', 'order_month_date', 'first_contact_date', 'order_item_id', 'payment_value',
         'landing_page_id', 'won_date', 'seller_id']]
    repeat_rate_df = dff.groupby('customer_unique_id')['order_id'].count().reset_index()

    # Only the Orders that are greater than 1. Will be basis for RFM analysis in customer app
    rrdf = repeat_rate_df[repeat_rate_df['order_id'] > 1]
    repeat_percent = rrdf['order_id'].sum() / repeat_rate_df['order_id'].sum()
    print("Percent of repeat customers ", repeat_percent * 100)

    # repeat_rate = sum of cust order 2+ times/ sum of cust order 1+ times (tot customers)
    repeat_rate = rrdf['order_id'].sum() / repeat_rate_df['order_id'].sum()
    churn_rate = 1 - repeat_rate

    customer_val = (avg_order_value / purchase_frequency) / churn_rate
    customer_val_mkt = net_revenue * churn_rate

    customer_lifetime_val = customer_val * (1 - profit_margin)  # TODO Check that this the correct maths

    dff['order_month_date'] = pd.to_datetime(dff['order_month_date'], errors='coerce',
                                             infer_datetime_format=True)

    # Create the conversion_rate_df and the conversion rates by month
    # conversion_rate_df = dff[
    #     ['order_month_date', 'first_contact_date', 'won_date', 'days_to_close_seller',
    #      'landing_page_id', 'origin', 'sdr_id', 'sr_id', 'seller_id', 'lead_type',
    #      'lead_behaviour_profile', 'business_segment', 'business_type', 'payment_value',
    #      'order_item_id', 'mql_id']]

    # All the marketing leads and closed deals can be associated to a landing page id or mql id.
    # conversion_rate_df = dff[dff['landing_page_id'].fillna("0") != "0"].reset_index()
    print("First Contact Date has ", dff['first_contact_date'].isnull().sum(), " missing dates.")
    print("Won Date has ", dff['won_date'].isnull().sum(), " missing dates.")
    print("Landing page has ", dff['landing_page_id'].value_counts(), "and has this many ",
          dff['landing_page_id'].isnull().sum(), " missing values")
    # print("The MQL Id's that have matching merchants are ", conversion_rate_df[conversion_rate_df['mql_id'].dropna()]['mql_id'].count())
    print(dff.info(memory_usage='deep'))

    # Creating Conversion Rate DF so that we can get the conversion rates per month, and by different sgenments
    # leads and behaviours.
    # conversion_rate_df = dff[['mql_id', 'sdr_id', 'sr_id', 'landing_page_id', 'seller_id',
    #                           'origin', 'lead_type', 'lead_behaviour_profile', 'business_segment',
    #                           'business_type', 'first_contact_date', 'won_date'
    #                           ]]

    # Updating the date column datatypes
    pg_utils.convert_to_datetime(dff, ['first_contact_date', 'won_date'])
    pg_utils.convert_to_datetime(marketing_df, ['first_contact_date', 'won_date'])

    # Creating the Contact date Month and Won Date Month Columns
    marketing_df['contact_date_month'] = pd.to_datetime(marketing_df['first_contact_date'], errors='coerce',
                                                        infer_datetime_format=True).apply(
        lambda x: x.replace(day=1)).dt.date

    marketing_df['won_date_month'] = pd.to_datetime(marketing_df['won_date'], errors='coerce',
                                                    infer_datetime_format=True).apply(
        lambda x: x.replace(day=1)).dt.date

    # Creating columns to store the Counts by Month
    marketing_df['first_contact_date_count'] = marketing_df.first_contact_date
    marketing_df['won_date_count'] = marketing_df.won_date

    # Splitting and Creating a df to count the number of contacts per month
    contact_df = marketing_df[[
        'contact_date_month', 'first_contact_date_count'
    ]]

    # Marketing Campaign Contacts per month If we know how much each one of these cost we could do figure out AC
    # for the campaign
    contact_df.sort_values(by='contact_date_month', ascending=False)
    contact_df.rename(columns={'contact_date_month': 'date_month'}, inplace=True)
    contact_df = contact_df.groupby('date_month').agg({'first_contact_date_count': 'count'}).reset_index()

    # Splitting and Creating a df that were won and what month
    won_df = marketing_df[[
        'won_date_month', 'won_date_count'
    ]]
    won_df.sort_values(by='won_date_month', ascending=False)
    won_df.rename(columns={'won_date_month': 'date_month'}, inplace=True)
    won_df = won_df.groupby('date_month').agg({'won_date_count': 'count'}).reset_index()

    # Making Conversion Rate by Month DF for analysis
    conversion_rate_by_month = contact_df.merge(won_df, on='date_month', how='outer')

    # Filling the first contact date count with the average,
    # this is done so that we can get the conversion rate of trailing converts.
    # TODO Check if this should be out of the total since the campaign is over.
    conversion_rate_by_month = conversion_rate_by_month.fillna({
        'won_date_count': 0,
        'first_contact_date_count': conversion_rate_by_month['first_contact_date_count'].mean()
    })
    # Adding additional columns to the dataframe
    conversion_rate_by_month[
        'contact_pct_change'] = conversion_rate_by_month.first_contact_date_count.pct_change().fillna(0)

    conversion_rate_by_month['won_pct_change'] = conversion_rate_by_month.won_date_count.pct_change().replace(
        [np.inf, -np.inf, np.nan], 0)

    conversion_rate_by_month['contact_cumsum'] = conversion_rate_by_month.first_contact_date_count.cumsum().fillna(0)

    conversion_rate_by_month[
        'conversion_rate'] = conversion_rate_by_month.won_date_count / conversion_rate_by_month.contact_cumsum

    conversion_rate_by_month['conversion_pct_change'] = conversion_rate_by_month.conversion_rate.pct_change().replace(
        [np.inf, -np.inf, np.nan], 0)

    conversion_rate_fig = pg_utils.create_indicator_figure(value=conversion_rate * 100,
                                                           delta=0,
                                                           title="Campaign Conversion Rate",
                                                           # monetary=False,
                                                           percent=True)

    conversion_rate_fig.add_bar(
        y=conversion_rate_by_month.conversion_rate * 100,
        x=conversion_rate_by_month.date_month,
        opacity=.3,
        name='conversion rate',
        hovertemplate="<extra></extra> The conversion rate in %{x| %B %Y} was %{y:,.2f}%"
                      "<br> with %{customdata[0]:,} leads converted out of %{customdata[2]:,} targeted."
                      "<br> representing a %{customdata[1]:.2%} change MoM <br><extra></extra>",
        text=conversion_rate_by_month.conversion_rate,
        customdata=np.stack(
            (conversion_rate_by_month.won_date_count, conversion_rate_by_month.conversion_pct_change,
             conversion_rate_by_month.contact_cumsum),
            axis=1),
        texttemplate="%{text:,.2%}",
        textfont_color='#FEFFF1',
        insidetextanchor='end',
        # secondary_y=True,
    )

    conversion_rate_fig.update_layout(
        barmode='group',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-.8,
        ),
        yaxis_visible=False,
        # xaxis_visible=False,
    )

    # create month by month bar graph for customers orders

    orders_df['order_id_count'] = orders_df['order_id']
    # orders_by_month = orders_df.groupby(['order_month_date', 'seller_id', 'order_id']).agg(
    #     {
    #         'order_id_count': 'nunique',
    #         'order_item_id': 'sum',
    #         # 'payment_value': 'sum'
    #     }
    # ).reset_index()

    # orders_by_month = orders_by_month.merge(dff[['order_id', 'payment_value']], how='left', on='order_id')
    orders_df['order_month_date'] = pd.to_datetime(orders_df['order_month_date'], errors='coerce',
                                                   infer_datetime_format=True).apply(
        lambda x: x.replace(day=1)).dt.date

    # Sellers that joined as a result of our marketing campaign.
    # conversion_rate_df_sellers = dff[~dff['won_date'].isnull()]
    # conversion_rate_df_sellers['order_month_date'] = pd.to_datetime(conversion_rate_df['won_date'], errors='coerce',
    #                                                                 infer_datetime_format=True).apply(
    #     lambda x: x.replace(day=1)).dt.date
    # print(conversion_rate_df_sellers.head(10))

    # adding columns to the conversion_rate_df_sellers to enrich the data
    # conversion_rate_df_sellers = conversion_rate_df_sellers.merge(orders_df, left_on=['seller_id', 'order_month_date'],
    #                                                               right_on=['seller_id', 'order_month_date'],
    #                                                               how='left')

    # orders_by_month = orders_by_month.merge(dff[['seller_id', 'won_date_month']], on='seller_id',
    #                                         how='left')

    # Both of these groupby's are needed to get the proper KPI's
    orders_by_month_payment = orders_df.groupby(['order_id']).agg({
        'order_month_date': 'first',
        'seller_id': 'nunique',
        'order_item_id': 'sum',
        'payment_value': 'sum',
    }).reset_index()

    print(orders_by_month_payment.payment_value.sum())

    # Grouping the Order ID groupby information to get it by month. Done instead of having multindex DF.
    orders_by_month_payment = orders_by_month_payment.groupby(['order_month_date']).agg({
        'seller_id': 'sum',
        'order_item_id': 'sum',
        'order_id': 'count',
        'payment_value': 'sum'
    }).reset_index()

    print(orders_by_month_payment.payment_value.sum())

    # won_orders_by_month = orders_by_month[~orders_by_month['won_date_month'].isnull()]

    # orders_by_month = orders_by_month_payment.groupby(['order_month_date']).agg(
    #     {
    #         'seller_id': 'nunique',
    #         'order_id': 'count',
    #         'order_id_count': 'sum',
    #         'order_item_id': 'sum',
    #         'payment_value': 'first',
    #     }
    # ).reset_index()
    orders_by_month_payment['AoV'] = orders_by_month_payment['payment_value'] / orders_by_month_payment['order_id']
    orders_by_month_payment['seller_freq'] = orders_by_month_payment['order_id'] / orders_by_month_payment['seller_id']
    orders_by_month_payment['seller_val'] = orders_by_month_payment['AoV'] / orders_by_month_payment['seller_freq']
    orders_by_month_payment['payment_value_pct_change'] = orders_by_month_payment.payment_value.pct_change().fillna(0)
    orders_by_month_payment['AoV_pct_change'] = orders_by_month_payment.AoV.pct_change().fillna(0)

    # won_orders_by_month = won_orders_by_month.groupby('won_date_month').agg(
    #     {
    #         'seller_id': 'nunique',
    #         # 'won_date_month': 'count',
    #         'order_id_count': 'count',
    #         'order_item_id': 'sum',
    #         'payment_value': 'sum'
    #     }
    # ).reset_index()
    # won_orders_by_month['AoV'] = won_orders_by_month['payment_value'] / won_orders_by_month['order_id_count']
    # won_orders_by_month['seller_freq'] = won_orders_by_month['order_id_count'] / won_orders_by_month['seller_id']
    # won_orders_by_month['seller_val'] = won_orders_by_month['AoV'] / won_orders_by_month['seller_freq']

    tot_orders_fig = pg_utils.create_indicator_figure(value=tot_orders,
                                                      delta=0,
                                                      title="Total Orders",
                                                      monetary=False,
                                                      percent=False,
                                                      default=True,
                                                      )
    # tot_orders_fig.add_trace(
    #     go.Indicator(
    #         value=tot_orders,
    #         title={'text': "Total Orders"},
    #         domain={'x': [0, 1], 'y': [0, 1]}
    #     ),
    # )

    print(orders_by_month_payment.info())

    tot_orders_fig.add_bar(
        x=orders_by_month_payment.order_month_date,
        y=orders_by_month_payment.order_id,
        # marker={'line': {'color': '#E4F2EF', 'width': 0.5, }},
        opacity=.3,
        name='Orders from Marketing',
        hovertemplate="<extra></extra> The number of orders<br> in %{x| %B %Y} "
                      "for marketing merchants was %{y:,}.<br>"
                      ""
                      " this resulted in an AoV of $%{customdata:.2f}<br>"
                      "<extra></extra>",
        customdata=np.stack((orders_by_month_payment.AoV)),
        # visible='legendonly',
        text=orders_by_month_payment.order_id,
        texttemplate="%{text:,}",
        textfont_color='#FEFFF1',
        insidetextanchor='end',
    )

    # tot_orders_fig.add_bar(
    #     x=orders_by_month_payment.order_month_date,
    #     y=orders_by_month_payment.order_id_count,
    #     opacity=.2,
    #     name='Orders from Marketing',
    #     hovertemplate="%{y:,}",
    #     text=orders_by_month_payment.order_id_count,
    #     texttemplate="%{text:,}",
    #     textfont_color='#FEFFF1'
    #
    # )

    tot_orders_fig.update_layout(
        barmode='overlay',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-.8,
        ),
        yaxis_visible=False,
    )

    # seller_val = orders_by_month.AoV.sum() / (
    #         orders_by_month.order_id_count.count() / orders_by_month.seller_id.nunique())

    # Creating the Customer Lifetime Value Figure
    revenue_fig = pg_utils.create_indicator_figure(value=tot_revenue,
                                                   delta=0,
                                                   title="Total Revenue",
                                                   monetary=True)

    revenue_fig.add_bar(
        x=orders_by_month_payment.order_month_date,
        y=orders_by_month_payment.payment_value,
        opacity=.3,
        name='revenue',
        hovertemplate="<extra></extra>In %{x| %B %Y} <br>the merchants that signed "
                      "up via the campaign<br> generated $%{y:,.2f} in revenue."
                      "<br>had an AoV of %{customdata[0]:,.2f} and a<br>"
                      "%{customdata[1]:.2%} change MoM<extra></extra>",
        customdata=np.stack((orders_by_month_payment.AoV, orders_by_month_payment.payment_value_pct_change), axis=1),
        # visible='legendonly',
        text=orders_by_month_payment.payment_value,
        texttemplate="$%{text:,.2f}",
        textfont_color='#FEFFF1',
        insidetextanchor='end',
    )

    # revenue_fig.add_bar(
    #     x=orders_by_month_payment.order_month_date,
    #     y=orders_by_month_payment.payment_value,
    #     opacity=.2,
    #     name='won seller val',
    #     text=orders_by_month_payment.payment_value,
    #     texttemplate="%{text:,.2f}",
    #     textfont_color='#FEFFF1'
    # )

    revenue_fig.update_layout(
        barmode='group',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-.8,
        ),
        yaxis_visible=False,

    )

    signup_df = marketing_df[['contact_date_month', 'time_to_close']]
    # pg_utils.convert_to_datetime(signup_df, ['order_month_date', 'first_contact_date', 'won_date'])
    # signup_df['time_to_close'] = (signup_df.first_contact_date - signup_df.won_date)
    signup_df = signup_df.groupby('contact_date_month').agg({
        'time_to_close': 'mean'
    }).reset_index()

    time_to_signup_fig = pg_utils.create_indicator_figure(
        value=avg_time_to_close,
        delta=0,
        title="Avg Days 2 Close",
    )

    time_to_signup_fig.add_bar(
        x=signup_df.contact_date_month,
        y=signup_df.time_to_close,
        opacity=.3,
        name='Avg Days to Signup',
        # visible='legendonly',
        hovertemplate="<extra></extra>The average days for merchants<br>"
                      " to sign up in %{x| %B %Y} was %{y:,.2f}<extra></extra>",
        text=signup_df.time_to_close,
        texttemplate="%{text:,.2f}",
        textfont_color='#FEFFF1',
        insidetextanchor='end',

    )

    time_to_signup_fig.update_layout(
        barmode='group',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-.8,
        ),
        yaxis_visible=False,
    )

    aov_fig = pg_utils.create_indicator_figure(
        value=avg_order_value,
        delta=0,
        title="Avg. Order Value",
        monetary=True,
    )

    aov_fig.add_bar(
        x=orders_by_month_payment.order_month_date,
        y=orders_by_month_payment.AoV,
        opacity=.3,
        name='AoV',
        # visible='legendonly',
        hovertemplate="<extra></extra>The Average Order Value for  merchants<br>"
                      " to sign up in %{x| %B %Y} was %{y:,.2f}"
                      "<br>represeting a %{customdata:,.2%} MoM change.<extra></extra>",
        customdata=np.stack((orders_by_month_payment.AoV_pct_change)),
        text=orders_by_month_payment.AoV,
        texttemplate="%{text:,.2f}",
        textfont_color='#FEFFF1',
        insidetextanchor='end',

    )

    aov_fig.update_layout(
        barmode='group',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-.8,
        ),
        yaxis_visible=False,
    )

    return conversion_rate_fig, tot_orders_fig, revenue_fig, time_to_signup_fig, aov_fig


@callback(
    Output('won-merchant-map', 'figure'),
    # Output('map-insight-1', 'children'),
    # Output(' top-channels-chart', 'figure'),
    # Output('top-sales-by-chart', 'figure'),
    # Output('sales-team-chart', 'figure'),
    Input('map-selection-value', 'value'),
    # Input('won-merchant-map', 'hoverData'),
    Input('data-store', 'data')
    #     suppress_callback_exceptions=True,
    #     prevent_initial_call=True
)
def update_campaign_map(map_selection, data):
    datasets = json.loads(data)
    # ctx = dash.callback_context
    # trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # seller_cust_pivot = pd.read_json(datasets['seller_cust_pivot_df'])
    seller_cust_pivot = pd.read_csv('./data/merchants_df.csv')  # Has customer orders and order ids
    geo_df = pd.read_csv('./data/suppliers_geo_data.csv')
    # geo_df["code"] = 'BRA'
    geo_df['won_date'] = pd.to_datetime(geo_df['won_date'], errors='coerce',
                                        infer_datetime_format=True).apply(
        lambda x: x.replace(day=1)).dt.date

    seller_cust_pivot['order_month_date'] = pd.to_datetime(seller_cust_pivot['order_month_date'], errors='coerce',
                                                           infer_datetime_format=True).apply(
        lambda x: x.replace(day=1)).dt.date

    seller_cust_pivot = seller_cust_pivot.groupby('seller_id').agg(
        {
            'customer_unique_id': 'nunique',
            'order_item_id': 'sum',
            'payment_value': 'sum',
            'freight_value': 'sum',
            'order_month_date': 'first',
            'review_score': 'mean'
        }
    ).reset_index()
    print(seller_cust_pivot.payment_value.sum())

    geo_df = geo_df.merge(seller_cust_pivot, on='seller_id', how='left')
    geo_df['time_to_first_order'] = geo_df['won_date'] - geo_df['order_month_date']
    geo_df['payment_value_scaled'] = np.log10(geo_df['payment_value'])

    # Filtering to only the won marketing data.
    geo_df = geo_df[geo_df.won_date.replace(pd.NaT, "0") != "0"]
    print(geo_df.payment_value.sum())

    # Used for creating the map
    geo_json_file = open("./data/external/brazil_geo.json")
    geojson = json.load(geo_json_file)

    # brazil_state_ids = {}
    # for feature in geojson['features']:
    #     brazil_state_ids[feature['id']] = feature['id']

    # used for gettting the id to be by lat,lng insrtead
    geo_df['id'] = geo_df.apply(lambda row: [row['geolocation_lat'], row['geolocation_lng']], axis=1)

    # geo_orig = geo_df.copy(deep=True)

    # if trigger_id == 'dd-channel':
    #     geo_df = geo_df.query('business_type in @origin_val')
    #
    # elif trigger_id == 'dd-lead-type':
    #     geo_df = geo_df.query('lead_type in @lead_type_val')
    #
    # elif trigger_id == 'dd-sales-team':
    #     geo_df = geo_df.query('sdr_id in @sdr_team_val')
    # else:
    #     geo_df = geo_orig
    #     pass

    def create_text(x):
        text = "{} merchants have had {} signups generating a total of ${:,.2f} worth" \
               " of revenue through OList.".format(
            x['geolocation_state'], x['merchant_count'], x['payment_value']
        )

        return text

    # Stripping dataframe down to only the relevant columns.
    geo_df = geo_df[['seller_id', 'geolocation_city', 'geolocation_state', 'id', 'geolocation_lat', 'geolocation_lng',
                     'payment_value', 'payment_value_scaled']]

    # adding a merchant count by state to the df so that we can show signups by merchant count,
    # payment value, payment value scaled.

    geo_pivot = geo_df.groupby('geolocation_state').agg({
        'seller_id': 'count'
    }).reset_index()
    geo_pivot.rename(columns={'seller_id': 'merchant_count'}, inplace=True)
    geo_df = geo_df.merge(geo_pivot, how='left', on='geolocation_state')

    geo_df_hover = geo_df.groupby('geolocation_state').agg({
        'payment_value': 'sum',
        'payment_value_scaled': 'mean',
        'merchant_count': 'first'
    }).reset_index()

    geo_df_hover['hover_data'] = geo_df_hover.apply(
        lambda x: create_text(x), axis=1)
    geo_df_hover = geo_df_hover[['geolocation_state', 'hover_data']]
    geo_df = geo_df.merge(geo_df_hover, how='left', on='geolocation_state')

    geo_df_insight = geo_df[
        ['geolocation_state', 'geolocation_city', 'payment_value', 'payment_value_scaled', 'seller_id',
         'hover_data']]

    geo_df = geo_df[['geolocation_state', 'geolocation_city', 'payment_value', 'payment_value_scaled', 'merchant_count',
                     'hover_data']]

    geo_df_insight = geo_df_insight.groupby(['geolocation_state', 'geolocation_city']).agg(
        {
            'payment_value': 'sum',
            'payment_value_scaled': 'mean',
            'seller_id': 'nunique',
        }
    ).reset_index()
    geo_df_insight.rename(columns={'seller_id': 'merchant_count'}, inplace=True)
    geo_df_insight.sort_values(by=['geolocation_state', 'geolocation_city', f'{map_selection}'])
    # geo_df_insight['merchant_cnt_cumsum'] =

    color_continuous_midpoint = 0,
    # if type(geo_df[map_selection].values) is "str":
    #     color_continuous_midpoint = 1
    # else:
    #     color_continuous_midpoint = geo_df[map_selection].mean()

    map = pg_utils.create_px_choropleth(
        geo_df,
        geojson,
        'geolocation_state',
        map_selection,
        'hover_data',
        geo_df[map_selection].mean()
    )
    map.update_layout(
        autosize=True,
    )
    map.update_traces()

    return map


@callback(
    Output('map-insight-1', 'children'),
    Input('map-selection-value', 'value'),
    Input('won-merchant-map', 'clickData'),
    Input('data-store', 'data')
)
def update_map_insight(map_selection, clickData, data):
    datasets = json.loads(data)
    # ctx = dash.callback_context
    # trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # seller_cust_pivot = pd.read_json(datasets['seller_cust_pivot_df'])
    seller_cust_pivot = pd.read_csv('./data/merchants_df.csv')
    geo_df = pd.read_csv('./data/suppliers_geo_data.csv')
    geo_df['code'] = 'BRA'
    geo_df['won_date'] = pd.to_datetime(geo_df['won_date'], errors='coerce',
                                        infer_datetime_format=True).apply(
        lambda x: x.replace(day=1)).dt.date

    seller_cust_pivot['order_month_date'] = pd.to_datetime(seller_cust_pivot['order_month_date'], errors='coerce',
                                                           infer_datetime_format=True).apply(
        lambda x: x.replace(day=1)).dt.date
    seller_cust_pivot.sort_values(by='seller_id', ascending=False)

    # seller_cust_pivot.to_csv('./data/seller_cust_pivot_dump.csv')

    # seller_cust = pd.pivot_table(seller_cust_pivot, index='order_month_date',
    #                              columns=['seller_id', 'product_category_name_english'],
    #                              values=['payment_value', 'customer_unique_id'],
    #                              aggfunc=['sum', 'nunique'],
    #                              fill_value=0)

    seller_cust_pivot_gby = seller_cust_pivot.groupby('seller_id').agg(
        {
            'customer_unique_id': 'nunique',
            'order_item_id': 'sum',
            'payment_value': 'sum',
            'freight_value': 'sum',
            'order_month_date': 'first',
            'review_score': 'mean'
        }
    ).reset_index()
    # seller_gby = seller_cust_pivot.groupby(['seller_id', 'order_month_date'])
    # print(seller_cust_pivot_gby.groups)
    # print(seller_cust_pivot_gby.get_group('0015a82c2db000af6aaaf3ae2ecb0532'))
    seller_cust_pivot_gby.sort_values(by='seller_id', ascending=False)

    # Creating a Seller Product Pivot Table to see the different categories that sellers sold in.
    seller_prod_pivot = pd.pivot_table(seller_cust_pivot,
                                       index="seller_id",
                                       columns="product_category_name_english",
                                       values="payment_value",
                                       aggfunc=np.sum,
                                       fill_value=0,
                                       dropna=False)
    seller_prod_pivot['total'] = seller_prod_pivot.sum(axis=1)
    seller_prod_pivot.index.sort_values(ascending=False)

    print(f"Total Amount Sold by {seller_prod_pivot.index.size} merchants was ${seller_prod_pivot.total.sum():,.2f}")

    geo_df = geo_df.merge(seller_cust_pivot_gby, on='seller_id', how='left')
    geo_df['time_to_first_order'] = geo_df['won_date'] - geo_df['order_month_date']
    geo_df['payment_value_scaled'] = np.log10(geo_df['payment_value'])

    # Filtering to only the won marketing data.
    geo_df = geo_df[geo_df.won_date.replace(pd.NaT, "0") != "0"]
    # Used for creating the map
    geo_json_file = open("./data/external/brazil_geo.json")
    geojson = json.load(geo_json_file)

    # brazil_state_ids = {}
    # for feature in geojson['features']:
    #     brazil_state_ids[feature['id']] = feature['id']

    # used for gettting the id to be by lat,lng insrtead
    geo_df['id'] = geo_df.apply(lambda row: [row['geolocation_lat'], row['geolocation_lng']], axis=1)

    # geo_orig = geo_df.copy(deep=True)

    # if trigger_id == 'dd-channel':
    #     geo_df = geo_df.query('business_type in @origin_val')
    #
    # elif trigger_id == 'dd-lead-type':
    #     geo_df = geo_df.query('lead_type in @lead_type_val')
    #
    # elif trigger_id == 'dd-sales-team':
    #     geo_df = geo_df.query('sdr_id in @sdr_team_val')
    # else:
    #     geo_df = geo_orig
    #     pass

    def create_text(x):
        text = "{} merchants have had {} signups generating a total of ${:,.2f} worth" \
               " of revenue through OList.".format(
            x['geolocation_state'], x['merchant_count'], x['payment_value']
        )

        return text

    # Stripping dataframe down to only the relevant columns.
    geo_df = geo_df[['seller_id', 'geolocation_city', 'geolocation_state', 'id', 'geolocation_lat', 'geolocation_lng',
                     'payment_value', 'payment_value_scaled']]

    # adding a merchant count by state to the df so that we can show signups by merchant count,
    # payment value, payment value scaled.

    geo_pivot = geo_df.groupby('geolocation_state').agg({
        'seller_id': 'count'
    }).reset_index()
    geo_pivot.rename(columns={'seller_id': 'merchant_count'}, inplace=True)
    geo_df = geo_df.merge(geo_pivot, how='left', on='geolocation_state')

    geo_df_hover = geo_df.groupby('geolocation_state').agg({
        'payment_value': 'sum',
        'payment_value_scaled': 'mean',
        'merchant_count': 'first'
    }).reset_index()

    geo_df_hover['hover_data'] = geo_df_hover.apply(
        lambda x: create_text(x), axis=1)
    geo_df_hover = geo_df_hover[['geolocation_state', 'hover_data']]
    geo_df = geo_df.merge(geo_df_hover, how='left', on='geolocation_state')

    geo_df_insight = geo_df[
        ['geolocation_state', 'geolocation_city', 'payment_value', 'payment_value_scaled', 'seller_id',
         'hover_data']]

    geo_df_insight = geo_df_insight.merge(seller_prod_pivot, how='left', on='seller_id')

    geo_df = geo_df[['geolocation_state', 'geolocation_city', 'payment_value', 'payment_value_scaled', 'merchant_count',
                     'hover_data']]

    geo_df_insight_location = geo_df_insight.groupby(['geolocation_state', 'geolocation_city']).agg(
        {
            'payment_value': 'sum',
            'payment_value_scaled': 'mean',
            'seller_id': 'nunique',
        }
    ).reset_index()
    geo_df_insight_location.rename(columns={'seller_id': 'merchant_count'}, inplace=True)
    geo_df_insight_location.sort_values(by=['geolocation_state', 'geolocation_city', f'{map_selection}'])
    # geo_df_insight['merchant_cnt_cumsum'] =
    insight_1 = html.P(
        f"Click on a state in the Map to generated additional automated insights."
    )

    if clickData is not None:
        location = clickData['points'][0]['location']
        hovertemplate = ""

        if location is not None:
            geo_df_insight_mask = geo_df_insight_location.query("geolocation_state == @location")
            geo_df_insight_mask = geo_df_insight_mask.sort_values(by=[f'{map_selection}'], ascending=False)

            if geo_df_insight_mask.shape[0] > 2:
                insight = f"Out of the {geo_df_insight_mask.geolocation_city.count():,} cities in {geo_df_insight_mask.geolocation_state.iloc[0]}, " \
                          f" this marketing campaign was most successful in {geo_df_insight_mask.geolocation_city.iloc[0].title()}," \
                          f" with {geo_df_insight_mask[{map_selection}].iloc[0][0]} merchants signed up." \
                          f" {geo_df_insight_mask.geolocation_city.iloc[1].title()} and {geo_df_insight_mask.geolocation_city.iloc[2].title()} " \
                          f" followed closely behind with {geo_df_insight_mask[{map_selection}].iloc[1][0]} and " \
                          f" {geo_df_insight_mask[{map_selection}].iloc[2][0]} merchants signed up respectively.",

                if map_selection == "payment_value" or map_selection == "payment_value_scaled":
                    insight = f"Out of the {geo_df_insight_mask.geolocation_city.count():,} cities in {geo_df_insight_mask.geolocation_state.iloc[0]} " \
                              f" the marketing campaign was most successful in  {geo_df_insight_mask.geolocation_city.iloc[0].title()} " \
                              f"with ${geo_df_insight_mask[{map_selection}].iloc[0][0]:,.2f} in revenue generated." \
                              f",{geo_df_insight_mask.geolocation_city.iloc[1].title()} and  {geo_df_insight_mask.geolocation_city.iloc[2].title()} " \
                              f"followed closely behind generating ${geo_df_insight_mask[{map_selection}].iloc[1][0]:,.2f} and " \
                              f"{geo_df_insight_mask[{map_selection}].iloc[2][0]:,.2f}) respectively.",

                    hovertemplate = "<extra></extra><br>%{x} has <br> generated $%{y:,.2f} worth of revenue <br>"
                    " through the platform<br><extra></extra>"
                else:
                    hovertemplate = "<extra></extra><br>%{x} had %{y:,} merchants sign up <br>" \
                                    " to the platform<br><extra></extra>",

                insight_graph_location = dcc.Graph(
                    id='cities-in-state-interactive',
                    figure=go.Figure(
                        go.Bar(
                            x=geo_df_insight_mask.geolocation_city,
                            y=geo_df_insight_mask[f"{map_selection}"],
                            name=f'{map_selection}',
                            hovertemplate=hovertemplate,
                            text=geo_df_insight_mask[f"{map_selection}"],
                            texttemplate="%{text:,}",
                            textfont_color='#FEFFF1',
                            insidetextanchor='end',
                        ),
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
                )

                geo_df_insight_mask = geo_df_insight.query('geolocation_state == @location')
                geo_df_insight_mask = geo_df_insight_mask.loc[:, "seller_id":"total"]
                geo_df_insight_mask.fillna(0, inplace=True)
                geo_df_insight_mask = geo_df_insight_mask.drop(columns=['hover_data'])

                print(f"The total revenue generated ")
                print(f"The Total for revenue generated by these merchants is {geo_df_insight_mask.total.sum()}")

                insight_graph_merchant = dcc.Graph(
                    id='merchants-in-state-interactive',
                    figure=go.Figure(
                        go.Bar(
                            x=geo_df_insight_mask.seller_id,
                            y=sorted(geo_df_insight_mask.total, reverse=True),
                            name='seller_id',
                            hovertemplate="<extra></extra><br>%{x} has <br> generated $%{y:,.2f} worth of revenue <br>"
                                          " through the platform<br><extra></extra>",
                            text=sorted(geo_df_insight_mask.total, reverse=True),
                            texttemplate="%{text:,.2f}",
                            textfont_color='#FEFFF1',
                            insidetextanchor='end',
                        ),
                        layout=
                        go.Layout(
                            yaxis=dict(
                                visible=False,
                            ),
                            uniformtext=dict(
                                minsize=8,
                            )
                        )
                    )
                )

                insight_graph_merchant_prods = html.Div(
                    id='ig-merchant-prod'
                )

                insight_1 = html.P(
                    children=[
                        html.P(insight),
                        insight_graph_location,
                        insight_graph_merchant,
                        insight_graph_merchant_prods
                    ])
        else:

            insight = f"The top city in {geo_df_insight_location.geolocation_state.iloc[0].title()}" \
                      f" was {geo_df_insight_location.geolocation_city.iloc[0]} with {geo_df_insight_location[{map_selection}].iloc[0][0]}" \
                      f" merchants signed up."

            insight_1 = html.P(
                children=[
                    insight,
                    # f"{geo_df_insight_mask.geolocation_city.iloc[1]}({geo_df_insight_mask[{map_selection}].iloc[0]}), "
                    #     f"{geo_df_insight_mask.geolocation_city.iloc[2]}({geo_df_insight_mask[{map_selection}].iloc[0]}) respectively.",
                    # insight_graph
                ]
            )

    return insight_1


# TODO add in seller product category sales on hover.
@callback(
    Output('ig-merchant-prod', 'children'),
    Input('merchants-in-state-interactive', 'clickData'),
    Input('data-store', 'data'),
    # suppress_callback_exceptions=True,
    # prevent_initial_call=True,
)
def update_insight_merchant_products(clickData, data):
    datasets = json.loads(data)

    if clickData is None:
        print("No seller clicked from State")
        return html.Div(
            children=[
                html.Br(),
                html.P("Click on a Seller's Sold Amount for more details."),
                html.Br(),
            ]
        )
    else:

        seller_id = clickData['points'][0]['label']
        seller_cust_pivot = pd.read_json(datasets['seller_cust_pivot_df'])
        seller_cust_pivot['order_month_date'] = pd.to_datetime(seller_cust_pivot['order_month_date'], errors='coerce',
                                                               infer_datetime_format=True).apply(
            lambda x: x.replace(day=1)).dt.date

        seller_prod_pivot = pd.pivot_table(seller_cust_pivot, values="payment_value", index="seller_id",
                                           columns="product_category_name_english", fill_value=0)
        seller_prod_pivot['total'] = seller_prod_pivot.sum(axis=1)
        seller_prod_pivot.fillna(0, inplace=True)
        # seller_prod_pivot.reset_index(inplace=True)
        seller_prod_pivot = seller_prod_pivot.query(f"seller_id == '{seller_id}'")
        print(seller_prod_pivot)

        merchant_prod_graph = go.Figure()
        merchant_prod_graph.add_bar(
            x=seller_prod_pivot.columns,
            y=seller_prod_pivot.values[0],
        )
        merchant_prod_graph.layout = dict(
            uniformtext=dict(
                minsize=8,
            ),
        )

        merchant_prod_graph = dcc.Graph(
            figure=merchant_prod_graph,
        )

        return merchant_prod_graph


@callback(
    # Output('won-merchant-map', 'figure'),
    Output('top-channels-chart', 'figure'),
    Output('top-sales-by-chart', 'figure'),
    Output('sales-team-chart', 'figure'),
    Input('dd-channel', 'value'),
    Input('dd-sales', 'value'),
    # Input('sdr-sales-team', 'value'),
    Input('data-store', 'data'),
    Input('top-channels-chart', 'clickData'),
    Input('top-sales-by-chart', 'clickData'),
    #     suppress_callback_exceptions=True,
    #     prevent_initial_call=True
)
def update_campaign_charts(origin_val, sales_val, data, origin_click, sales_click):
    datasets = json.loads(data)

    # dff = pd.read_csv('./data/merchants_df.csv')
    geo_df = pd.read_csv('./data/suppliers_geo_data.csv')
    geo_df['code'] = 'BRA'

    geo_df['won_date'] = pd.to_datetime(geo_df['won_date'], errors='coerce',
                                        infer_datetime_format=True).apply(
        lambda x: x.replace(day=1)).dt.date

    # Creating a geo based df that is based only on the won leads of the marketing merchants
    geo_df = geo_df[~geo_df['won_date'].isnull()]
    # seller_cust_pivot = pd.read_json(datasets['seller_cust_pivot_df'])

    seller_cust_pivot = pd.read_csv('./data/merchants_df.csv')
    seller_cust_pivot['order_month_date'] = pd.to_datetime(seller_cust_pivot['order_month_date'], errors='coerce',
                                                           infer_datetime_format=True).apply(
        lambda x: x.replace(day=1)).dt.date

    seller_cust_pivot = seller_cust_pivot.groupby('seller_id').agg(
        {
            'customer_unique_id': 'nunique',
            'order_item_id': 'sum',
            'payment_value': 'sum',
            'freight_value': 'sum',
            'order_month_date': 'first',
            'review_score': 'mean'
        }
    ).reset_index()

    geo_df = geo_df.merge(seller_cust_pivot, on='seller_id', how='left')
    geo_df['time_to_first_order'] = geo_df['won_date'] - geo_df['order_month_date']
    geo_df['payment_value_scaled'] = np.log10(geo_df['payment_value'])

    # Filtering to only the won marketing data.
    geo_df = geo_df[geo_df.won_date.replace(pd.NaT, "0") != "0"]
    # Used for creating the map

    # Used for creating the map
    # geo_json_file = open("./data/external/brazil_geo.json")
    # geojson = json.load(geo_json_file)

    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == origin_click:
        print(f"Channel Selected - {origin_click}")

    if trigger_id == sales_click:
        print(f"Sales Selected - {sales_click}")

    lead_type_fig = go.Figure()
    sales_team_fig = go.Figure()
    landing_page_fig = go.Figure()

    # Figure out what graph cased the change.
    # geo_df_orig = geo_df.copy(deep=True)
    # if origin_val is None and lead_type_val is None and sdr_team_val is None:
    #     geo_df = geo_df.copy(deep=True)
    #     print(geo_df.head(10))
    # elif trigger_id == 'dd-channel':
    #     geo_df = geo_df.query('business_segment in @origin_val')
    # elif trigger_id == 'dd-lead-type':
    #     # geo_df = geo_df[geo_df['lead_type'] == lead_type_val]
    #     geo_df = geo_df.query('lead_type in @lead_type_val')
    # elif trigger_id == 'sdr-sales-team':
    #     # geo_df = geo_df[geo_df['sdr_id'] == sdr_team_val]
    #     geo_df = geo_df.query('sdr_id in @sdr_team_val')
    # else:
    #     geo_df = geo_df_orig
    #     pass

    # map = px.scatter_geo(
    #     geo_df,
    #     lat='geolocation_lat',
    #     lon='geolocation_lng',
    #     locations='seller_state',
    #     locationmode='country names',
    #     scope='south america'
    # )
    # brazil_state_ids = {}
    # for feature in geojson['features']:
    #     brazil_state_ids[feature['id']] = feature['id']
    #
    # geo_df['id'] = geo_df['geolocation_state'].apply(lambda x: brazil_state_ids[x])
    #
    # map = pg_utils.create_px_choropleth(geo_df, geojson, 'id', 'payment_value_scaled', ['payment_value'],
    #                                     geo_df['payment_value_scaled'].mean())
    # map.update_layout(
    #     autosize=True,
    # )
    if origin_val is None:
        origin_val = 'lead_type'

    lead_dff = geo_df[
        ['origin', 'landing_page_id', 'lead_type', 'lead_behaviour_profile', 'geolocation_state', 'geolocation_city',
         'payment_value', 'sr_id', 'sdr_id']]
    lead_dff[f'{origin_val}_lead_count'] = 1
    lead_count_dff = lead_dff.groupby([f'{origin_val}']).agg(
        {
            f'{origin_val}_lead_count': 'count',
        }
    ).reset_index()

    # Add the lead count by origin to the dataframe.
    lead_dff.drop(columns=f'{origin_val}_lead_count', inplace=True)
    lead_dff = lead_dff.merge(lead_count_dff, how='left', on=f'{origin_val}')

    lead_dff_pie = lead_dff.groupby([f'{origin_val}']).agg({
        f'{origin_val}_lead_count': 'first',
        'payment_value': 'sum'
    }).reset_index()
    print(f"lead pie lead count-{lead_dff_pie[f'{origin_val}_lead_count'].sum()}")
    print(f"lead pie payment value -{lead_dff_pie.payment_value.sum()}")
    lead_dff_pie[f'{origin_val}_lead_value'] = lead_dff_pie.payment_value / lead_dff_pie[f'{origin_val}_lead_count']
    lead_dff_pie[f'{origin_val}_pct_total'] = lead_dff_pie.payment_value / lead_dff_pie.payment_value.sum()
    print(f"Percent Total is  {lead_dff_pie[f'{origin_val}_pct_total'].sum()}")

    if sales_click is not None:
        sales_rep = sales_click['points'][0]['label']
        print(sales_rep)
        if sales_rep and sales_val is not None:
            lead_dff_pie = lead_dff_pie.query(f'{sales_val} == "{sales_rep}"')
        elif sales_rep and sales_val is None:
            sales_val = 'sr_id'
            lead_dff_rep = lead_dff.query(f'{sales_val}  =="{sales_rep}"')
            lead_dff_rep.drop(columns={
                f'{origin_val}_lead_count',
            }, inplace=True)
            lead_dff_rep.rename(columns={
                'payment_value': f'{sales_val}_payment_value'
            }, inplace=True)

            lead_dff_rep = lead_dff_rep.groupby(f'{origin_val}').agg({
                'landing_page_id': 'count',
                f'{sales_val}_payment_value': 'sum',
            }).reset_index()
            lead_dff_pie = lead_dff_rep.merge(lead_dff_pie, on=f'{origin_val}', how='left')
        else:
            pass

    lead_type_fig.add_trace(
        go.Pie(
            values=lead_dff_pie[f"{origin_val}_lead_count"],
            labels=lead_dff_pie[f"{origin_val}"],
            hole=.40,
            name='tot lead contacts',
            # pull=.125,
            # title='Marketing Channels',
            hovertemplate="%{label:.replace('_',' ').title()} has brought in a total of %{value} leads"
                          "<br>accounting for $%{customdata[0][0]:,.2f}, or %{customdata[0][2]:,.2%}  of<br>"
                          "the total marketing revenue($%{customdata[0][3]:,.2f).<br>This leads to a lead "
                          "value of $%{customdata[0][1]:,.2f}"
                          ".<extra></extra>",
            customdata=np.stack((lead_dff_pie.payment_value, lead_dff_pie[f'{origin_val}_lead_value'],
                                 lead_dff_pie[f'{origin_val}_pct_total'],
                                 [lead_dff_pie.payment_value.sum()] * len(lead_dff_pie.payment_value)), axis=1),
        )
    )
    print(lead_type_fig.data)
    lead_type_fig.update_layout(
        margin=dict(t=100, l=0, r=0, b=0),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-.8,
        ),
        # For showing the total in the center of the pie hole.
        annotations=[
            {
                # "font": {
                #     "size": 20,
                #     "family": 'Bebas Neue, cursive',
                # },
                "showarrow": False,
                "text": f"{lead_dff_pie[f'{origin_val}_lead_count'].sum():,.0f}",
                "x": 0.5,
                "y": 0.5,
            },
        ]
    )
    lead_type_fig.layout.title = f"{origin_val.replace('_', ' ').title()}"

    # Creating the sales team Ranking chart.
    sr_dff = geo_df[['sdr_id', 'sr_id', 'landing_page_id', 'won_date',
                     'mql_id', 'origin', 'lead_type',
                     'lead_behaviour_profile', 'geolocation_city', 'payment_value']]
    sr_dff['team_count'] = sr_dff['sdr_id']

    gby = ['sr_id']
    if sales_val == None:
        sales_val = "sr_id"

    if sales_val == 'sr_id':
        gby = [f'{sales_val}', 'sdr_id']
    if sales_val == "sdr_id":
        gby = [f'{sales_val}', 'sr_id']
    else:
        gby = [f'{sales_val}']

    sr_gby_dff = sr_dff.groupby(gby).agg(
        {
            # 'landing_page_id': 'nunique',
            'won_date': 'nunique',
            'mql_id': 'nunique',
            'payment_value': 'sum',
            'team_count': 'nunique'
        }
    ).reset_index()
    sr_gby_dff['conversion_rate'] = sr_gby_dff.won_date / sr_gby_dff.mql_id
    sr_gby_dff.rename(columns={
        'payment_value': f'{sales_val}_tot_payment_value',
        'mql_id': 'mql_id_count',
        'won_date': 'won_date_count',

    }, inplace=True)
    sr_dff = sr_dff.merge(sr_gby_dff, on=f'{sales_val}', how='left')

    # sales_team_dff.merge(sr_dff, on='sdr_id', how='left')

    # Heirarchial Sales Team Analysis
    # labels = sr_dff.sr_id.unique().tolist()
    # parents = sr_dff.sdr_id.tolist()
    # values = sr_dff.team_count.tolist()
    #
    # # Add root node to parent
    # parents.insert(0, "CSO")
    # # parents.insert(0,"")

    if origin_click is not None:
        ocValue = origin_click['points'][0]['label']
        print(ocValue)
        print(origin_val)
        print(f'{origin_val}=={ocValue}')
        sr_dff = sr_dff.query(f'{origin_val}=="{ocValue}"')

    sales_team_fig.add_trace(
        # go.Treemap(
        #     # ids=sales_team_dff.index,
        #     labels=labels,
        #     parents=parents,
        #     values=values,
        #     # branchvalues="total",
        #     # insidetextorientation='tangential',  # radial, tangential,
        #     marker=dict(
        #         colors=sr_dff.conversion_rate,
        #         cmid=sr_dff.conversion_rate.mean(),
        #         colorscale=DIVERGING
        #     ),
        #     hovertemplate='<b>%{label} </b><b></b> <br> Sales Reps: %{value}<br> Conversion rate: %{color:.2%}',
        #     # maxdepth=4,
        #     # sort=False,
        #     # level="",
        #
        # )
        go.Bar(
            y=sr_gby_dff[f'{sales_val}'].unique(),
            x=sorted(sr_gby_dff[f'{sales_val}_tot_payment_value']),
            # x=sorted(sr_dff[f'{sales_val}_tot_payment_value']),
            orientation='h',
            # opacity=.3,
            name=f'{sales_val}',
            # visible='legendonly',
            hovertemplate="<extra></extra> %{y}<br> handled leads generated $%{x:,.2f} "
                          "revenue<extra></extra>",
            text=sorted(sr_gby_dff[f'{sales_val}_tot_payment_value']),
            # text=sorted(sr_dff[f'{sales_val}_tot_payment_value']),
            texttemplate="%{text:,}",
            textfont={
                'color': '#FEFFF1',
            },
            insidetextanchor='end',
        )
    )

    # sales_team_fig.layout.xaxis.title = 'Leads'
    # sales_team_fig.layout.yaxis.title = 'Landing Page'

    sales_team_fig.update_layout(
        margin=dict(t=100, l=0, r=0, b=0),
        title=f"Sales by {sales_val.replace('_', ' ').title()}",
        yaxis_visible=False,
        xaxis_visible=False,
        hovermode='closest'
    )
    # sales_team_fig.layout.title = f"Sales by {sales_val}"

    # Creating the Marketing Bubble Chart to show the Channel (Marketing & Sales) by Payment Value
    landing_page_dff = geo_df[
        ['sdr_id', 'sr_id', 'landing_page_id', 'won_date', 'mql_id', 'origin', 'lead_type', 'lead_behaviour_profile',
         'payment_value']]

    landing_page_pivot = pd.pivot_table(landing_page_dff,
                                        index='landing_page_id',
                                        columns="origin",
                                        values="payment_value",
                                        aggfunc=np.sum,
                                        fill_value=0,
                                        dropna=False)
    # landing_page_gby_dff = landing_page_dff.groupby('landing_page_id').agg(
    #     {
    #         'sdr_id': 'nunique',
    #         'sr_id': 'nunique',
    #         'won_date': 'nunique',
    #         'mql_id': 'count',
    #         'payment_value': 'sum',
    #         'origin': 'first'
    #     }
    # ).reset_index()
    #
    # origin_gby = landing_page_dff.groupby('origin').agg({
    #     'sdr_id': 'nunique',
    #     'sr_id': 'nunique',
    #     'won_date': 'nunique',
    #     'mql_id': 'count',
    #     'payment_value': 'sum',
    # }).reset_index()
    #
    # origin_gby.rename(columns={
    #     'sdr_id': 'origin_sdr_id',
    #     'sr_id': 'origin_sr_id',
    #     'won_date': 'origin_won_date',
    #     'mql_id': 'origin_mql_id',
    #     'payment_value': 'origin_payment_value'
    # }, inplace=True)
    #
    # landing_page_gby_dff = landing_page_gby_dff.merge(origin_gby, on='origin', how='left')

    # landing_page_gby_dff['conversion_rate'] = landing_page_gby_dff.won_date / landing_page_gby_dff.mql_id
    # landing_page_dff = geo_df[
    #     ['landing_page_id', 'origin', 'lead_type', 'lead_behaviour_profile', 'geolocation_city']]
    # landing_page_dff = landing_page_dff.merge(landing_page_gby_dff, how='left', on='landing_page_id')
    # landing_page_dff['payment_value_scaled'] = np.log10(landing_page_dff.payment_value)

    # landing_page_fig.add_bar(
    # landing_page_fig.add_bar(
    #     x=landing_page_dff.conversion_rate,
    #     y=landing_page_dff.landing_page_id,
    #     orientation='h',
    #     name='conversion rate'
    # )
    #
    # landing_page_fig.update_layout(
    #     barmode='group'
    # )

    landing_page_fig.add_trace(
        go.Heatmap(
            x=landing_page_pivot.columns,
            y=landing_page_pivot.index,
            z=np.log10(landing_page_pivot.values),
            customdata=np.stack((landing_page_pivot.values)),
            hovertemplate="%{y} from %{x} landing page generated $%{customdata:,.2f}",
            colorscale=pio.templates['atbAnalyticsGroupDefault'].layout.colorscale.diverging
            # mode='markers',
            # marker=dict(
            #     # sizemode='diameter',
            #     # sizeref=750,
            #     size=landing_page_dff.payment_value_scaled,
            #     color=DIVERGING
            # ),

        )
        # go.Scatter3d(
        #     x=landing_page_dff.sr_id,
        #     y=landing_page_dff.origin,
        #     z=landing_page_dff.payment_value,
        #     mode="markers",
        #     marker=dict(
        #         sizemode='diameter',
        #         sizeref=750,
        #         size=landing_page_dff.conversion_rate,
        #         color=landing_page_dff.payment_value,
        #     )
        # )
    )
    landing_page_dff.hovermode = 'x unified'
    landing_page_fig.layout.title = "Marketing Results by Landing Page"
    landing_page_fig.layout.yaxis.title = 'Landing Page'
    landing_page_fig.layout.xaxis = dict(
        title='Lead Type',
        # visible=False,
    )
    landing_page_fig.layout.showlegend = False
    landing_page_fig.layout.height = 1000

    return lead_type_fig, sales_team_fig, landing_page_fig
