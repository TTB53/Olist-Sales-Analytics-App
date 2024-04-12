import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly import graph_objects as go
import pandas as pd
import numpy as np
import plotly.io as pio
import page_utilities.page_utilities as pg_utils
import json

pg_utils = pg_utils.PageUtilities()

dash.register_page(__name__,
                   path='/merchants-analysis',
                   name='Merchants',
                   title='Olist - Merchants Analysis - ATB Analytics Group'
                   )

layout = dbc.Container(
    children=[
        html.H1(
            children='Merchants Insight\'s',
            className="display-1",
        ),
        html.Br(),
        html.P(
            children=[
                """
                As you go through the Merchant's insights page, there a few things to keep in mind. 
        
            """,

            ],

        ),
        html.Br(),
        html.Ul(
            children=[
                html.Li(
                    id='merchant-insight-1',
                    children=["""
                    Olist was founded in Feb 2015, the provided dataset starts in October 2016 however, it has missing
                    data from Nov and has very little data from Dec 2016. That aside, I decided to leave it as it 
                    shows that every dataset has flaws and characteristics that need to be cleansed.
                    """]
                ),
                html.Br(),
                html.Li(
                    id='merchant-insight-2',
                    children=["""
Generating Automated Insights ... 
                    """]
                ),
                html.Br(),
                html.Li(
                    id='merchant-insight-3',
                    children=[
                        """
Generating Automated Insights ...
                    """]
                ),
                html.Br(),
                html.Li(
                    children=[
                        """
                        The KPI's below are pre-filtered to the Merchant data, you can see how that stacks against
                        the totals for the time period, but to get a better understanding of the 
                        """,
                        dcc.Link("Customers", href='http://127.0.0.1:8050/customer-analysis'),
                        """
                         or the 
                        """,
                        dcc.Link("Marketing", href='http://127.0.0.1:8050/marketing-analysis'),
                        """
                            campaign that was run, visit their pages to get more detailed information.
                        """

                    ]
                ),
                html.Br(),
            ],
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                                pg_utils.create_kpi_card('tot-merchants'),
                                # dbc.Card(
                                #     children=[
                                #         dbc.CardBody(
                                #             children=[
                                #                 dcc.Loading(
                                #                     children=[
                                #                         dcc.Graph(
                                #                             id='tot-merchants'
                                #                         ),
                                #                     ],
                                #                     type='dot',
                                #                     color='AQUAMARINE',
                                #                 )
                                #             ]
                                #         )
                                #     ],
                                #     className="kpi-card"
                                # ),
                            ],
                            className="card-group",
                        ),
                    ],
                    width=12,
                    align='center',
                ),
            ]
        ),
        dbc.Row(
            children=[

                html.Div(
                    children=[
                        dbc.Col(
                            children=[
                                pg_utils.create_kpi_card('tot-revenue')
                            ],
                            align='center',
                            className='col-md-6 col-sm-12'
                        ),
                        dbc.Col(
                            children=[
                                pg_utils.create_kpi_card('avg-freight-value')

                            ],
                            align='center',
                            className='col-md-6 col-sm-12'
                        ),
                        # dbc.Card(
                        #     children=[
                        #         dbc.CardBody(
                        #             children=[
                        #                 dcc.Loading(
                        #                     children=[
                        #                         dcc.Graph(
                        #                             id='tot-revenue'
                        #                         ),
                        #                     ],
                        #                     type='dot',
                        #                     color='AQUAMARINE',
                        #                 )
                        #             ]
                        #         )
                        #     ],
                        #     className="kpi-card"
                        # ),
                        #
                        # dbc.Card(
                        #     children=[
                        #         dbc.CardBody(
                        #             children=[
                        #                 dcc.Loading(
                        #                     children=[
                        #                         dcc.Graph(
                        #                             id='tot_units'
                        #                         ),
                        #                     ],
                        #                     type='dot',
                        #                     color='AQUAMARINE',
                        #                 )
                        #             ]
                        #         )
                        #     ],
                        #     className="kpi-card"
                        # ),
                    ],
                    className='card-group'
                ),
            ]
        ),
        dbc.Row(
            children=[
                # KPI-Row-2
                html.Div(
                    children=[
                        dbc.Col(
                            children=[
                                pg_utils.create_kpi_card('avg-ship-days')
                            ],
                            align='center',
                            className='col-md-6 col-sm-12'
                        ),
                        dbc.Col(
                            children=[
                                pg_utils.create_kpi_card('tot_units')
                            ],
                            align='center',
                            className='col-md-6 col-sm-12'
                        ),
                        # dbc.Card(
                        #     children=[
                        #         dbc.CardBody(
                        #             children=[
                        #                 dcc.Loading(
                        #                     children=[
                        #                         dcc.Graph(
                        #                             id='avg-ship-days'
                        #                         ),
                        #                     ],
                        #                     type='dot',
                        #                     color='AQUAMARINE',
                        #                 )
                        #             ]
                        #         )
                        #     ],
                        #     className="kpi-card"
                        # ),

                        # dbc.Card(
                        #     children=[
                        #         dbc.CardBody(
                        #             children=[
                        #                 dcc.Loading(
                        #                     children=[
                        #                         dcc.Graph(
                        #                             id='avg-freight-value'
                        #                         ),
                        #                     ],
                        #                     type='dot',
                        #                     color='AQUAMARINE',
                        #                 )
                        #             ],
                        #         )
                        #     ],
                        #     className="kpi-card"
                        # ),
                    ],
                    className="card-group"
                ),
                # dbc.Col(
                #     children=[
                #
                #     ],
                #     width=12,
                #     align='center'
                # ),
            ]
        ),
        html.Br(),
        # Merchant Map
        # TODO add interactivity to show by not just merchant sales, but order items, and fastest shipper's etc.
        html.H2('Where are our Merchants are Located.', className='display-2'),
        html.Br(),
        html.P("""
            
            Where are merchants are located, and how they are distributed across Brazil, and other parts of the 
            world.
            
        """),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        pg_utils.create_kpi_card('merchants-map'),
                        html.Div(
                            id='merchant-map-insight'
                        )

                    ],
                    width=12,
                    align='center',
                ),
            ]
        ),
        html.Br(),
        html.H2('Top Merchant Analysis', className='display-2'),
        html.Br(),
        dbc.Row(
            children=[
                # html.H5("Top Merchants.", className='display-5'),
                dbc.Col(
                    children=[
                        html.Div(
                            id='merchant-top-n-filter-wrapper',
                            children=[

                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            html.H3("Select A Value", className='text-center'),
                                            html.P("Select a value to see the Top Merchants by different categories."
                                                   "Once the graph has loaded click on a merchant in the by "
                                                   "Revenue chart below to see their ranking in the other charts"
                                                   ",if available."),
                                            html.Br(),
                                            dcc.Slider(
                                                id='top-n-merchant-slider',
                                                min=0,
                                                max=20,
                                                step=5,
                                                value=10,
                                                tooltip={
                                                    "placement": "bottom",
                                                    "always_visible": True
                                                },
                                                className='ui-selection-slider',
                                            ),
                                        ]
                                    ),
                                    className='user-selection-card',
                                ),
                                html.Br(),
                                # dbc.Card(
                                #     dbc.CardBody(
                                #         dcc.Dropdown(
                                #             id="merchant-product-category-dd",
                                #             # options=[{"label": x, "value": x} for x in
                                #             #          dff.product_category_name_english.unique()],
                                #             optionHeight=40,
                                #             # value=options[0],
                                #             clearable=False,
                                #             style={"width": "100%"},
                                #             persistence=True,
                                #             persistence_type="session"
                                #         )
                                #     )
                                # )

                            ],
                            className='card-group',
                        )
                    ],
                    width=12,
                    align='center'
                ),
            ]
        ),
        dbc.Row(
            children=[
                html.Br(),
                dbc.Col(
                    children=[
                        dcc.RadioItems(
                            id='top-producing-radio',
                            options=[
                                {'label': 'Payment Value ', 'value': 'payment_value'},
                                {'label': 'Items Ordered ', 'value': 'order_item_id'},
                                # {'label': 'San Francisco', 'value': 'San Francisco'},
                            ],
                            value='payment_value',
                            inline=True
                        ),
                        dcc.Loading(
                            dcc.Graph(
                                id='merchants-by-payment-value'
                            ),
                            type='dot',
                            color='AQUAMARINE'
                        )
                    ],
                    className='col-md-6 col-sm-12',
                    align='center'
                ),
                # dbc.Col(
                #     children=[
                #         dcc.Loading(
                #             dcc.Graph(
                #                 id='merchants-by-order-items'
                #             ),
                #             type='dot',
                #             color='AQUAMARINE'
                #         )
                #     ],
                #     className='col-md-6 col-sm-12',
                #     align='center'
                # ),

                html.Br(),
                dbc.Col(
                    children=[
                        dcc.RadioItems(
                            id='top-shipping-radio',
                            options=[
                                {'label': 'Fastest Shipping ', 'value': 'm2wh_ship_days'},
                                {'label': 'Freight Value ', 'value': 'freight_value'},
                                # {'label': 'San Francisco', 'value': 'San Francisco'},
                            ],
                            value='m2wh_ship_days',
                            inline=True
                        ),
                        dcc.Loading(
                            dcc.Graph(
                                id='merchants-by-freight-value'
                            ),
                            type='dot',
                            color='AQUAMARINE'
                        )
                    ],
                    className='col-md-6 col-sm-12',
                    align='center'
                ),
                # dbc.Col(
                #     children=[
                #         dcc.Loading(
                #             dcc.Graph(
                #                 id='merchants-by-avg-ship-days'
                #             ),
                #             type='dot',
                #             color='AQUAMARINE'
                #         )
                #     ],
                #     className='col-md-6 col-sm-12',
                #     align='center'
                # ),
                #
                # dbc.Col(
                #     children=[
                #         dcc.Loading(
                #             dcc.Graph(
                #                 id='merchants-by-products'
                #             ),
                #             type='dot',
                #             color='AQUAMARINE'
                #         )
                #     ],
                #     width=12,
                #     align='center'
                # ),
            ]
        ),
        html.H2('Revenue Prediction', className='display-2'),
        html.Br(),
        dbc.Row(
            children=[
                # html.H5("Revenue Prediction", className='display-5'),
                dbc.Col(
                    children=[
                        html.Div(
                            id='revenue-prediction-wrapper',
                            children=[

                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            html.H3("Select A Value", className='text-center'),
                                            html.P("""
                                                Select a revenue share percentage with the merchants.
                                            """),
                                            html.Br(),
                                            dcc.Slider(
                                                id='revenue-prediction-slider',
                                                min=1,
                                                max=7,
                                                step=.5,
                                                value=3.5,
                                                tooltip={
                                                    "placement": "bottom",
                                                    "always_visible": True
                                                },
                                                className='ui-selection-slider',
                                            ),
                                        ]
                                    ),
                                    className='user-selection-card',
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            html.H3("Select A Value", className='text-center'),
                                            html.P("""
                Select The number of Product Categories to see. This is sorted by Revenue Share. 
            """),
                                            html.Br(),
                                            dcc.Slider(
                                                id='revenue-category-slider',
                                                min=0,
                                                max=40,
                                                step=5,
                                                value=15,
                                                tooltip={
                                                    "placement": "bottom",
                                                    "always_visible": True
                                                },
                                                className='ui-selection-slider',
                                            ),
                                        ]
                                    ),
                                    className='user-selection-card',
                                ),
                                html.Br(),
                                # dbc.Card(
                                #     dbc.CardBody(
                                #         dcc.Dropdown(
                                #             id="merchant-product-category-dd",
                                #             # options=[{"label": x, "value": x} for x in
                                #             #          dff.product_category_name_english.unique()],
                                #             optionHeight=40,
                                #             # value=options[0],
                                #             clearable=False,
                                #             style={"width": "100%"},
                                #             persistence=True,
                                #             persistence_type="session"
                                #         )
                                #     )
                                # )

                            ],
                            className='card-group',
                        )
                    ],
                    width=12,
                    align='center'
                ),
            ]
        ),
        dbc.Row(
            children=[
                html.Br(),
                dbc.Col(
                    children=[
                        dcc.Loading(
                            dcc.Graph(
                                id='revenue-prediction-value'
                            ),
                            type='dot',
                            color='AQUAMARINE'
                        )
                    ],
                    width=12,
                    align='center'
                ),
            ]
        ),

    ]
)


@callback(
    Output('merchant-insight-1', 'children'),
    Output('merchant-insight-2', 'children'),
    Output('merchant-insight-3', 'children'),
    Input('data-store', 'data'),
)
def merchant_insights(data):
    datasets = json.loads(data)

    merchant_insight_1 = """
            Olist provided us data on their platform from October 2016 to November of 2018.
        Since there is very little data for the 2016 year, we will compare the 2017 and 2018 data.
        During that time, the number of merchants selling on the platform
    """

    merchant_insight_2 = """
    
    """

    merchant_insight_3 = """
    
    """

    merchants_by_month = pd.read_json(datasets['merchants_by_month_df'])
    pg_utils.convert_to_datetime(merchants_by_month, "order_month_date")
    merchants_by_month['year'] = merchants_by_month['order_month_date'].dt.year
    year_df = merchants_by_month.groupby('year').agg(
        {
            'seller_id': 'sum',
            'customer_unique_id': 'sum',
            'payment_value': 'sum',
            'order_item_id': 'sum',
            'freight_value': 'sum',
            'avg_ship_days': 'sum'
        }
    ).reset_index()

    # YoY Insights for Merchants, Revenue, Shipping Costs
    yoy_insight_mc = year_df['seller_id'].pct_change()[2]
    yoy_insight_rc = year_df['payment_value'].pct_change()[2]
    yoy_insight_sc = year_df['freight_value'].pct_change()[2]

    if yoy_insight_mc > 0:
        merchant_insight_1 += " grew from {:,} in {} to {:,} in {} or by {:.2%}.".format(
            year_df['seller_id'].iloc[1],
            year_df['year'].iloc[1],
            year_df['seller_id'].iloc[2],
            year_df['year'].iloc[2],
            yoy_insight_mc)
        if yoy_insight_rc > 0:
            merchant_insight_2 += "As the merchants grew so did revenue," \
                                  "increasing from ${:,.2f} in {} to ${:,.2f} in {} or {:.2%} change.".format(
                year_df['payment_value'].iloc[1],
                year_df['year'].iloc[1],
                year_df['payment_value'].iloc[2],
                year_df['year'].iloc[2],
                yoy_insight_rc)

            if yoy_insight_sc > 0:
                merchant_insight_3 += "As expected, shipping costs also rose with Merchants and Revenue, " \
                                      "increasing from ${:,.2f} in {} to ${:,.2f} in {} or {:.2%} change.".format(
                    year_df['freight_value'].iloc[1],
                    year_df['year'].iloc[1],
                    year_df['freight_value'].iloc[2],
                    year_df['year'].iloc[2],
                    yoy_insight_sc
                )

            else:
                merchant_insight_3 += " fell by {:.2%}.".format(yoy_insight_sc)
        else:
            merchant_insight_2 += "Unlike the growth in merchants, revenues (${:,.2f}) fell by as {:.2%}.".format(
                year_df['payment_value'].iloc[2], yoy_insight_rc)
    else:
        merchant_insight_1 += " fell by {:.2%}.".format(yoy_insight_mc)

    return merchant_insight_1, merchant_insight_2, merchant_insight_3


@callback(
    Output('tot-merchants', 'figure'),
    Output('tot_units', 'figure'),
    Output('tot-revenue', 'figure'),
    Output('avg-freight-value', 'figure'),
    # Output('on-time-delivery', 'figure'),
    Output('avg-ship-days', 'figure'),
    # Output('avg-review-score', 'figure'),
    # Output('merchant-product-category-dd', 'options'),
    Input('data-store', 'data'),
    # prevent_initial_call=True
)
def update_merchant_kpis(data):
    datasets = json.loads(data)

    dff = pd.read_csv('./data/combined_olist_data.csv')
    closed_deals = pd.read_csv('./data/OlistEcomData/olist_closed_deals_dataset.csv')

    closed_deals = closed_deals[['seller_id', 'business_segment', 'business_type']]
    merchants_df = dff[
        ['order_month_date', 'seller_id', 'product_category_name_english',
         'order_item_id', 'payment_value', 'freight_value', 'review_score',
         'shipping_limit_date', 'order_delivered_carrier_date', 'order_delivered_customer_date',
         'order_estimated_delivery_date', 'order_status'
         ]]
    merchants_df.rename(
        columns={
            "shipping_limit_date": "ship_to_wh_date",
            "order_delivered_carrier_date": "wh_received_date",
            "order_delivered_customer_date": "customer_received_date",
            "order_estimated_delivery_date": "est_customer_receive_date",
        },
        inplace=True)

    pg_utils.convert_to_datetime(df=merchants_df, col='order_month_date')
    pg_utils.convert_to_datetime(df=dff, col='order_month_date')

    # left join to keep all the records from merchant_df
    merchants_df = merchants_df.merge(closed_deals, on='seller_id', how='left')
    print(merchants_df.dtypes)
    # Total merchants in Dataset
    tot_merchants = dff['seller_id'].nunique()
    merchants_per_month = merchants_df.groupby(['order_month_date'], as_index=False)['seller_id'].nunique()

    merchants_per_month.sort_values(by=['order_month_date'], inplace=True)

    tot_seller_fig = pg_utils.create_indicator_figure(
        value=tot_merchants,
        delta=tot_merchants,
        title="Total Merchants",
        monetary=False
    )

    tot_seller_fig.add_bar(
        x=sorted(merchants_per_month.order_month_date),
        y=merchants_per_month.seller_id,
        opacity=.2,
        name='merchants/m',
        hovertemplate="%{x} had a total of %{y:,} unique merchants",
        text=merchants_per_month.seller_id,
        textfont_color='#FEFFF1'
    )

    # Total Units Figure
    tot_units_ordered = dff.order_item_id.sum()
    tot_units_per_month = merchants_df.groupby(['order_month_date'], as_index=False)['order_item_id'].sum()
    tot_units_fig = pg_utils.create_indicator_figure(
        value=tot_units_ordered,
        delta=tot_units_ordered,
        title="Total Units Ordered",
        monetary=False
    )

    tot_units_fig.add_bar(
        x=sorted(tot_units_per_month.order_month_date),
        y=tot_units_per_month.order_item_id,
        opacity=.2,
        name='units/m',
        hovertemplate="There were %{y:,} units purchased in %{x}",
        text=tot_units_per_month.order_item_id.apply(lambda x: pg_utils.human_format(x)),
        textfont_color='#FEFFF1'

    )

    # Tot Revenue Figure.
    tot_revenue = dff.payment_value.sum()
    tot_revenue_per_month = dff.groupby(['order_month_date'], as_index=False).agg(
        {
            'payment_value': 'sum',
            'seller_id': 'nunique',
        }
    )
    tot_revenue_per_month['rev_per_merchant'] = tot_revenue_per_month.payment_value / tot_revenue_per_month.seller_id
    tot_revenue_fig = pg_utils.create_indicator_figure(
        value=tot_revenue,
        delta=tot_revenue,
        title="Total Revenue",
        monetary=True,
    )

    tot_revenue_fig.add_bar(
        x=sorted(tot_revenue_per_month.order_month_date),
        y=tot_revenue_per_month.payment_value,
        opacity=.2,
        hovertemplate="The total Revenue for %{x} was $%{y:,.2f}",
        name='tot rev',
        text=tot_revenue_per_month.payment_value.apply(lambda x: pg_utils.human_format(x)),
        textfont_color='#FEFFF1'
    )

    tot_revenue_fig.add_bar(
        x=sorted(tot_revenue_per_month.order_month_date),
        y=tot_revenue_per_month.rev_per_merchant,
        opacity=.2,
        # secondary_y=True,
        visible='legendonly',
        hovertemplate="The total revenue per merchant for %{x} was $%{y:,.2f}",
        name='rev/merchant'

    )

    tot_revenue_fig.update_layout(
        barmode='relative'
    )
    # Average Freight Value Figure
    avg_freight_value = dff.freight_value.mean()
    avg_freight_value_per_month = merchants_df.groupby(['order_month_date'], as_index=False)['freight_value'].mean()

    avg_freight_fig = pg_utils.create_indicator_figure(
        value=avg_freight_value,
        delta=avg_freight_value,
        title="Avg Freight Value",
        monetary=True
    )

    avg_freight_fig.add_bar(
        x=sorted(avg_freight_value_per_month.order_month_date),
        y=avg_freight_value_per_month.freight_value,
        opacity=.2,
        name='avg shipping cost',
        hovertemplate="The avereage shipping cost in %{x} was %{y:,.2f}",
        text=avg_freight_value_per_month.freight_value.apply(lambda x: pg_utils.human_format(x)),
        textfont_color='#FEFFF1',
    )

    # On Time Delivery Figure 
    # TODO needs to be updated, using the wrong delivery percentage needs to be based on est time to customer
    #  and actual reception of the item by customer 
    # merchants_df['order_status_count'] = merchants_df['order_status']
    # otd_df = merchants_df.groupby(['order_status'], as_index=False)['order_status_count'].count()
    # # print(otd_df.head(5))
    #
    # delivered_orders = otd_df.query('order_status == "delivered"').reset_index()
    # delivered_percentage = (delivered_orders['order_status_count'][0] / otd_df['order_status_count'].sum()) * 100
    # delivery_pct_by_month = merchants_df.groupby(['order_month_date'], as_index=False)['order_status'].count()
    # #
    # delivery_percent_fig = go.Figure(
    #     go.Indicator(
    #         value=delivered_percentage,
    #         title={'text': 'Delivery Percentage'},
    #         domain={'x': [0, 1], 'y': [0, 1]},
    #     )
    # )
    #
    # delivery_percent_fig.add_bar(
    #     x=delivery_pct_by_month.order_month_date,
    #     y=delivery_pct_by_month.order_status,
    #     #opactiy=.2
    # )

    # Avg Ship Days Figure

    # Getting the Shipped days for the orders that we're delivered.
    merchants_df = merchants_df.query('order_status=="delivered"')

    merchants_df['ship_days'] = merchants_df['order_status']
    # Finding out how long it took the merchant to ship to Olist Warehouse.
    merchant_to_wh_df = merchants_df[
        ['seller_id', 'order_month_date', 'ship_to_wh_date', 'wh_received_date', 'ship_days']]
    merchant_to_wh_df['ship_to_wh_date'] = pd.to_datetime(merchant_to_wh_df['ship_to_wh_date'], errors='coerce',
                                                          infer_datetime_format=True)
    merchant_to_wh_df['wh_received_date'] = pd.to_datetime(merchant_to_wh_df['wh_received_date'], errors='coerce',
                                                           infer_datetime_format=True)

    # Getting Days between when the Order was shipped to Olist Warehouse by the merchant and receiving it.
    merchant_to_wh_df['ship_days'] = abs(
        (merchant_to_wh_df['wh_received_date'] - merchant_to_wh_df['ship_to_wh_date']).dt.days)
    # merchant_to_wh_df['ship_days'] = (
    #             merchant_to_wh_df['wh_received_date'] - merchant_to_wh_df['ship_to_wh_date']).days

    avg_ship_days = merchant_to_wh_df['ship_days'].mean()
    avg_ship_days_by_month = merchant_to_wh_df.groupby(['order_month_date'], as_index=False)['ship_days'].mean()
    avg_ship_days_by_month['ship_days'] = abs(avg_ship_days_by_month['ship_days'])
    # # print(otd_df.head(5))
    #
    # delivered_orders = otd_df.query('order_status == "delivered"').reset_index()
    # delivered_percentage = (delivered_orders['order_status_count'][0] / otd_df['order_status_count'].sum()) * 100
    # delivery_pct_by_month = merchants_df.groupby(['order_month_date'], as_index=False)['order_status'].count()
    # #
    avg_ship_days_fig = pg_utils.create_indicator_figure(
        value=avg_ship_days,
        delta=avg_ship_days,
        title="Merchant ship to OList",
    )

    #
    avg_ship_days_fig.add_bar(
        x=sorted(avg_ship_days_by_month.order_month_date),
        y=avg_ship_days_by_month.ship_days,
        opacity=.2,
        name='avg days in transit',
        hovertemplate="it takes<br><br> on average %{y:,.2f} days to reach Olist Warehouses.",
        text=avg_ship_days_by_month.ship_days.apply(lambda x: pg_utils.human_format(x)),
        textfont_color='#FEFFF1'
    )

    # Avg Review Score Figure

    # Getting the Avg Review Score.
    avg_review_score = merchants_df['review_score'].mean()
    avg_review_score_by_month = merchants_df.groupby(['order_month_date'], as_index=False)['review_score'].mean()
    avg_review_score_fig = pg_utils.create_indicator_figure(
        value=avg_review_score,
        delta=avg_review_score,
        title="Avg Review Score",
        monetary=True
    )

    #
    avg_review_score_fig.add_bar(
        x=sorted(avg_review_score_by_month.order_month_date),
        y=avg_review_score_by_month.review_score,
        opacity=.2,
        name='avg review score',
        text=avg_review_score_by_month.review_score.apply(lambda x: pg_utils.human_format(x)),
        textfont_color='#FEFFF1'
    )

    merchants_prod_dropdown = dcc.Dropdown(
        options=[{"label": x, "value": x} for x in
                 dff.product_category_name_english.unique()],
        optionHeight=40,
        value=dff.product_category_name_english.unique()[0],
        clearable=False,
        style={"width": "100%"},
        persistence=True,
        persistence_type="session"
    )

    figs = [tot_seller_fig, tot_units_fig, tot_revenue_fig, avg_freight_fig, avg_ship_days_fig]
    pg_utils.create_standard_legend(figs)

    for fig in figs:
        fig.layout.yaxis.visible = False

    return tot_seller_fig, tot_units_fig, tot_revenue_fig, avg_freight_fig, avg_ship_days_fig
    # merchants_prod_dropdown


@callback(
    Output('merchants-map', 'figure'),
    Input('data-store', 'data'),
    # prevent_initial_call=True
)
def update_supplier_map(data):
    geolocation = './data/suppliers_geo_data.csv'
    geo_df = pd.read_csv(geolocation)
    geo_df['code'] = 'BRA'

    # Used for creating the map
    geo_json_file = open("./data/external/brazil_geo.json")
    geojson = json.load(geo_json_file)

    brazil_state_ids = {}
    for feature in geojson['features']:
        brazil_state_ids[feature['id']] = feature['id']

    geo_df['id'] = geo_df['geolocation_state'].apply(lambda x: brazil_state_ids[x])

    closed_deals = pd.read_csv('./data/OlistEcomData/olist_closed_deals_dataset.csv')
    closed_deals = closed_deals[['seller_id', 'business_segment', 'business_type']]

    dff = pd.read_csv('./data/combined_olist_data.csv')

    print(geo_df.head(5), dff.head(5), closed_deals.head(5))

    dff = dff[['seller_id', 'zip_code', 'payment_value']]
    dff.merge(closed_deals, on='seller_id')

    dff = dff.groupby('seller_id', as_index=False)['payment_value'].sum()
    dff = dff.merge(geo_df, on='seller_id')
    dff['payment_value_scaled'] = np.log10(dff['payment_value'])

    def create_text(x):
        text = "Merchants from {}, in {},<br> operating in {} zip code,<br> have sold a total of ${:,.2f} " \
               "<br>worth of products through OList.".format(
            x['geolocation_city'], x['geolocation_state'], x['zip_code'], x['payment_value']
        )

        return text

    dff['hover_data'] = dff.apply(
        lambda x: create_text(x), axis=1)

    # This keeps all the columns in the dataframe when doing a groupby 'first' is equivalent
    # to 'keep this, and keep it movin' whenever there are no duplicates

    # dff.groupby('zip_code', as_index=False).agg(
    #     {'geolocation_lat': 'first', 'geolocation_lng': 'first', 'geolocation_city': 'first',
    #      'geolocation_state': 'first', 'payment_value': 'sum'})

    supplier_map_fig = go.Figure(
        go.Densitymapbox(
            lat=dff.geolocation_lat,
            lon=dff.geolocation_lng,
            z=np.log10(dff.payment_value),
            radius=8,
            hovertemplate=dff.hover_data,
            opacity=1,
            customdata=dff.zip_code,
        )
    )

    supplier_map_fig.update_layout(
        mapbox_style='open-street-map',
        height=500,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_center={
            'lat': dff.geolocation_lat.mode()[0],
            'lon': dff.geolocation_lng.mode()[0]
        },
        mapbox_zoom=2,
        showlegend=False,
    )

    # supplier_map_fig = px.scatter_mapbox(dff,
    #                                      # locations=geo_df['iso_alpha'],
    #                                      labels={
    #                                          'payment_value': 'Tot Amt Sold'
    #                                      },
    #                                      lat='geolocation_lat',
    #                                      lon='geolocation_lng',
    #                                      color='payment_value',
    #                                      zoom=2,
    #                                      # width=1200,
    #                                      height=800,
    #                                      size='payment_value',
    #                                      # size_max=30,
    #                                      # title='Merchant Locations',
    #                                      hover_name='seller_id',
    #                                      # hover_data=[dff['seller_id'], " located in  ", dff['seller_city'],
    #                                      #             " has sold a total of amount of ", dff['payment_value']],
    #                                      range_color=[0, dff['payment_value'].quantile(0.95)],  # To negate ouliers
    #                                      color_continuous_scale=pio.templates[
    #                                          'atbAnalyticsGroupDefault'].layout.colorscale.diverging,
    #                                      center={
    #                                          'lat': dff.geolocation_lat.mode()[0],
    #                                          'lon': dff.geolocation_lng.mode()[0]
    #                                      },
    #                                      )
    # supplier_map_fig.update_geos(fitbounds="locations", visible=True)
    # Free Mapbox styles are 'open-street-map', 'white-bg', 'carto-positron', 'carto-darkmatter',
    # 'stamen-terrain', 'stamen-toner', 'stamen-watercolor'
    # supplier_map_fig.update_layout(mapbox_style="open-street-map")
    # supplier_map_fig.update_layout(
    #     margin={"r": 20, "t": 50, "l": 20, "b": 20},
    #     autosize=True,
    #     showlegend=False
    # )
    return supplier_map_fig


@callback(
    Output('merchant-map-insight', 'children'),
    Input('merchants-map', 'clickData')
)
def update_merchant_map_insight(clickData):
    # TODO see if this is faster than using the smaller files and combining.
    dff = pd.read_csv('./data/combined_data/combined_olist_data.csv',
                      usecols=['order_month_date', 'seller_id', 'zip_code', 'product_category_name_english',
                               'order_item_id', 'payment_value', 'freight_value', 'review_score',
                               'shipping_limit_date', 'order_delivered_carrier_date', 'order_delivered_customer_date',
                               'order_estimated_delivery_date', 'order_status'
                               ])

    merchant_insight_fig = go.Figure(
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
        print("Merchant Map Click Data is None.")
        return html.P("Click on a location in the map for more details.")
    else:
        zipcode = clickData['points'][0]['customdata']
        print(f"Merchant {zipcode} was clicked.")

        merchant_detail_df = dff.query('zip_code == @zipcode')
        merchant_detail_df = merchant_detail_df.groupby('product_category_name_english').agg({
            'payment_value': 'sum',
            'order_month_date': 'first'
        }).reset_index()
        merchant_detail_df.sort_values(by='order_month_date', ascending=False)

        merchant_insight_fig.add_heatmap(
            x=merchant_detail_df.order_month_date,
            y=merchant_detail_df.product_category_name_english.replace("_", " "),
            z=merchant_detail_df.payment_value.fillna(0),
            texttemplate='$%{z:,.2f}',
            hovertemplate='%{y:y.replace("_"," ")} in %{x} sold a total of $%{z:,.2f}',
            colorscale=pio.templates['atbAnalyticsGroupDefault'].layout.colorscale.diverging,
        )

        merchant_insight_fig.layout.yaxis.visible = True
        merchant_insight_fig.layout.title = f"{zipcode} Merchants"

        merchant_detail = dbc.Row(
            children=[
                dbc.Col(
                    dcc.Graph(
                        id='merchant_detail',
                        figure=merchant_insight_fig,
                    )
                )
            ]
        )

        return merchant_detail


@callback(
    Output('merchants-by-payment-value', 'figure'),
    Output('merchants-by-freight-value', 'figure'),
    # Output('merchants-by-order-items', 'figure'),
    # Output('merchants-by-avg-ship-days', 'figure'),
    # Output('merchants-by-products', 'figure'),
    Input('data-store', 'data'),
    Input('top-n-merchant-slider', 'value'),
    Input('top-producing-radio', 'value'),
    Input('top-shipping-radio', 'value')
    # prevent_initial_call=True
)
def update_merchant_analysis_figures(data, value, top_producing_value, top_shipping_value):
    datasets = json.loads(data)

    dff = pd.read_csv('./data/combined_olist_data.csv')

    merchants_df = dff[
        ['order_month_date', 'seller_id', 'product_category_name_english',
         'order_item_id', 'payment_value', 'freight_value', 'review_score',
         'shipping_limit_date', 'order_delivered_carrier_date', 'order_delivered_customer_date',
         'order_estimated_delivery_date', 'order_status'
         ]]
    merchants_df.rename(
        columns={
            "shipping_limit_date": "ship_to_wh_date",
            "order_delivered_carrier_date": "wh_received_date",
            "order_delivered_customer_date": "customer_received_date",
            "order_estimated_delivery_date": "est_customer_receive_date",
        },
        inplace=True)
    merchants_df['ship_to_wh_date'] = pd.to_datetime(merchants_df['ship_to_wh_date'], errors='coerce',
                                                     infer_datetime_format=True)
    merchants_df['wh_received_date'] = pd.to_datetime(merchants_df['wh_received_date'], errors='coerce',
                                                      infer_datetime_format=True)
    merchants_df['customer_received_date'] = pd.to_datetime(merchants_df['customer_received_date'], errors='coerce',
                                                            infer_datetime_format=True)
    merchants_df['est_customer_receive_date'] = pd.to_datetime(merchants_df['est_customer_receive_date'],
                                                               errors='coerce',
                                                               infer_datetime_format=True)

    merchants_df['m2wh_ship_days'] = abs(
        (merchants_df['wh_received_date'] - merchants_df['ship_to_wh_date']).dt.days)

    merchants_df['wh2c_ship_days'] = abs(
        (merchants_df['wh_received_date'] - merchants_df['customer_received_date']).dt.days)

    merchants_stats_df = merchants_df.groupby("seller_id", as_index=False).agg(
        {
            'order_month_date': 'first',
            'payment_value': 'sum',
            'freight_value': 'sum',
            'order_item_id': 'sum',
            'm2wh_ship_days': 'mean'
        }
    )
    # merchants_stats_df['color'] = '#42403f'
    if top_producing_value is None:
        top_producing_value = 'payment_value'

    if top_shipping_value is None:
        top_shipping_value = 'm2wh_ship_days'

    tpv_title = f'Top {value} by {top_producing_value.replace("_", " ").title()}'

    print(merchants_stats_df.head(10))
    merchants_payments_fig = px.bar(
        merchants_stats_df[:value].sort_values(by=f'{top_producing_value}', ascending=True),
        x='seller_id',
        y=f'{top_producing_value}',
        # color='color',
        title=tpv_title,
        text=merchants_stats_df[f'{top_producing_value}'][:value].apply(lambda x: pg_utils.human_format(x))
        # orientation='h',
    )

    tsv_title = f'Top {value} by {top_shipping_value.replace("_", " ").title()}'

    # merchants_order_items_fig = px.bar(
    #     merchants_stats_df[:value].sort_values(by=f'{top_shipping_value}', ascending=True),
    #     x='seller_id',
    #     y=f'{top_shipping_value}',
    #     # color='color',
    #     title=tsv_title,
    #
    #     # orientation='h'
    # )

    merchants_freight_value_fig = px.bar(
        merchants_stats_df[:value].sort_values(by=f'{top_shipping_value}', ascending=True),
        x='seller_id',
        y=f'{top_shipping_value}',
        # color='color',
        title=tpv_title,
        text=merchants_stats_df[f'{top_shipping_value}'][:value]
        # orientation='h'
    )

    merchants_avg_ship_days_fig = px.bar(
        # Done because faster shipping merchants are better. It's like golf lowest score fam.
        merchants_stats_df[:value].sort_values(by='m2wh_ship_days', ascending=False),
        x='seller_id',
        y='m2wh_ship_days',
        # color='color',
        title=f'Top {value} Merchants by Avg Ship days',
        orientation='h'
    )

    merchants_by_products_fig = go.Figure(
        # go.Scatter3d(
        #     y=merchants_df.product_category_name_english,
        #     x=merchants_df.order_month_date,
        #     z=merchants_df.payment_value,
        #     mode="markers",
        #     marker=dict(
        #         size=8,
        #         color=merchants_df.payment_value,  # set color to an array/list of desired values
        #         # colorscale='Viridis',  # choose a colorscale
        #         opacity=0.8
        #     ),
        #     showlegend=True,
        #
        # )
    )
    merchants_df_gby = merchants_df.groupby("product_category_name_english").agg(
        {
            'payment_value': 'sum',
        }
    ).reset_index()
    merchants_by_products_fig.add_bar(
        # ids=merchants_df
        x=merchants_df_gby.product_category_name_english,
        y=merchants_df_gby.payment_value,
    )

    merchants_by_products_fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0)
    )

    merchants_payments_fig.update_layout(
        hovermode='closest',
        yaxis_visible=False,
        xaxis_visible=False,
        uniformtext_minsize=8,
    )

    merchants_freight_value_fig.update_layout(
        hovermode='closest',
        yaxis_visible=False,
        xaxis_visible=False,
        uniformtext_minsize=8,
    )

    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # if trigger_id == 'merchants-by-payment-value' or trigger_id == 'merchants-by-freight-value' or trigger_id == 'merchants-by-order-value':
    #     merchants_stats_df = update_hover_color(clickData, merchants_stats_df)
    #     merchants_df = merchants_df[
    #         ['order_month_date', 'seller_id', 'product_category_name_english', 'payment_value']]
    #
    #     label = clickData['points'][0]['label']
    #
    #     merchants_payments_fig = px.bar(
    #         merchants_stats_df[:value].sort_values(by='payment_value', ascending=True),
    #         y='seller_id',
    #         x='payment_value',
    #         title=f'Top {value} Merchants by Revenue',
    #         orientation='h',
    #         color='color',
    #         # color_discrete_map=color_discrete_map
    #     )
    #
    #     merchants_order_items_fig = px.bar(
    #         merchants_stats_df[:value].sort_values(by='order_item_id', ascending=True),
    #         y='seller_id',
    #         x='order_item_id',
    #         title=f'Top {value} Merchants by Items Ordered',
    #         orientation='h',
    #         color='color',
    #         # color_discrete_map=color_discrete_map
    #     )
    #
    #     merchants_freight_value_fig = px.bar(
    #         merchants_stats_df[:value].sort_values(by='freight_value', ascending=True),
    #         y='seller_id',
    #         x='freight_value',
    #         title=f'Top {value} Merchants by Shipping Total',
    #         orientation='h',
    #         color='color'
    #         # color_discrete_map=color_discrete_map
    #     )
    #
    #     merchants_avg_ship_days_fig = px.bar(
    #         # Done because faster shipping merchants are theoretically better/closer to Olist
    #         # warehouses and therefore can meet demand if their product surges due to market demand
    #         # or changing tastes.But It's like golf lowest score wins fam.
    #         merchants_stats_df[:value].sort_values(by='m2wh_ship_days', ascending=False),
    #         y='seller_id',
    #         x='m2wh_ship_days',
    #         title=f'Top {value} Merchants by Avg Ship days',
    #         orientation='h',
    #         color='color',
    #         hover_data=['{} on average gets their<br>product to Olist warehouses in about {} days'.format(
    #             merchants_stats_df.seller_id, merchants_stats_df.m2wh_ship_days)]
    #         # color_discrete_map=color_discrete_map
    #     )
    #
    #     merchants_payments_fig.update_layout(
    #         hovermode='closest'
    #     )
    #
    #     if label is not None:
    #         merchants_df = merchants_df[merchants_df.seller_id == label]
    #         merchants_df = merchants_df.groupby('product_category_name_english').agg(
    #             {
    #                 'payment_value': 'sum',
    #             }
    #         ).reset_index()
    #         merchants_by_products_fig = go.Figure()
    #         merchants_by_products_fig = merchants_by_products_fig.add_bar(
    #             x=merchants_df.product_category_name_english,
    #             y=merchants_df.payment_value,
    #             name='{} prod_categories'.format(label)
    #         )
    #
    #         # merchants_by_products_fig.add_scatter3d(
    #         #     x=merchants_pivot_table.columns,
    #         #     y=merchants_pivot_table.index,
    #         #     z=merchants_pivot_table.values,
    #         #     mode='markers',
    #         #     marker=dict(
    #         #         size=8,
    #         #         color=merchants_pivot_table.values,  # set color to an array/list of desired values
    #         #         # colorscale='Viridis',  # choose a colorscale
    #         #         opacity=0.8
    #         #     ),
    #         #     showlegend=True,
    #         #     name='product category',
    #         # )
    #
    #         merchants_by_products_fig.update_layout(
    #             margin=dict(l=0, r=0, t=0, b=0)
    #         )
    #
    #     return merchants_payments_fig, merchants_freight_value_fig, merchants_order_items_fig, merchants_avg_ship_days_fig, merchants_by_products_fig

    return merchants_payments_fig, merchants_freight_value_fig
    # merchants_order_items_fig, merchants_avg_ship_days_fig, merchants_by_products_fig


@callback(
    Output('revenue-prediction-value', 'figure'),
    Input('revenue-prediction-slider', 'value'),
    Input('revenue-category-slider', 'value'),
    Input('data-store', 'data'),
    # prevent_initial_call=True,

)
def update_revenue_share_figure(share_pct, top_n_val, data):
    datasets = json.loads(data)
    dff = pd.read_csv('./data/combined_olist_data.csv')  # TODO change to USECOLS

    merchants_df = dff[
        ['order_month_date', 'seller_id', 'product_category_name_english',
         'order_item_id', 'payment_value', 'freight_value', 'review_score',
         'shipping_limit_date', 'order_delivered_carrier_date', 'order_delivered_customer_date',
         'order_estimated_delivery_date', 'order_status', 'zip_code', 'customer_state'
         ]]

    rev_prediction_fig = go.Figure()

    if share_pct is None:
        pass
    else:
        merchants_df = merchants_df.groupby(['product_category_name_english']).agg(
            {
                'order_month_date': 'first',
                'seller_id': 'nunique',
                'order_item_id': 'nunique',
                'payment_value': 'sum',
                'zip_code': 'nunique',
                'customer_state': 'nunique'
            }
        ).reset_index()
        merchants_df['rev_share'] = merchants_df.payment_value * (share_pct / 100)

        merchants_df = merchants_df.sort_values(by='rev_share', ascending=False)
        merchants_df = merchants_df[:top_n_val]

        customdata = [
            '{} has {} merchants, and has had {} orders starting {}'.format(merchants_df.product_category_name_english,
                                                                            merchants_df.seller_id,
                                                                            merchants_df.order_item_id,
                                                                            merchants_df.order_month_date)]
        bubble_size = []
        hover_text = []

        for index, row in merchants_df.iterrows():
            hover_text.append(('{prod_cat} has {merchant_count} merchants,<br>' +
                               ' and has had {order_count} orders,<br>' +
                               ' starting in {order_start}.<br>' +
                               ' Merchants selling this product have<br> '
                               ' sold a total of ${sold_product:,.2f} <br> '
                               'and shipped to {state_count} states in Brazil.').format(
                prod_cat=row['product_category_name_english'],
                merchant_count=row['seller_id'],
                order_count=row['order_item_id'],
                order_start=row['order_month_date'],
                sold_product=row['payment_value'],
                state_count=row['customer_state'],
            ))
            bubble_size.append(np.sqrt(row['payment_value']))

        merchants_df['hover_text'] = hover_text
        merchants_df['bubble_size'] = bubble_size
        sizeref = 2. * max(merchants_df['bubble_size']) / (100 ** 2)
        # sizeref = 32


        # rev_prediction_fig = px.scatter(merchants_df, x='seller_id', y='payment_value', size='rev_share',
        #                                 color='product_category_name_english', log_x=True, log_y=True, size_max=60
        #                                 )
        rev_prediction_fig.add_scatter(
            x=merchants_df.seller_id,
            y=merchants_df.payment_value,
            mode='markers',
            # marker_color=merchants_df.product_category_name_english,
            marker=dict(
                size=merchants_df.bubble_size,
                color=merchants_df.rev_share,
                sizemode='area',
                sizeref=sizeref,
                line_width=2,
            ),
            # marker_size=merchants_df.bubble_size,
            # name='rev share',
            # text=['{} has {} merchants, and has had {} orders starting {}'.format(
            #     merchants_df.product_category_name_english,
            #     merchants_df.seller_id,
            #     merchants_df.order_item_id,
            #     merchants_df.order_month_date)
            # ],
            # customdata=customdata,
            hovertemplate=merchants_df.hover_text,
            text=merchants_df['payment_value'].apply(lambda x: pg_utils.human_format(x)),
        )
        rev_prediction_fig.add_bar(
            x=merchants_df.seller_id,
            y=merchants_df.payment_value,
        )
        rev_prediction_fig.add_bar(
            x=merchants_df.seller_id,
            y=merchants_df.rev_share,
        )
        rev_prediction_fig.update_traces(
            hoverlabel_namelength=0,
        )
        rev_prediction_fig.update_layout(
            hovermode='x unified',  # values are 'x', 'y', 'closest', False, 'x unified', 'y unified'
            height=850,
            showlegend=False,
            barmode='overlay',
            yaxis_visible=False,
            xaxis_visible=False,

        )

        return rev_prediction_fig

    #
    # @callback(
    #     # Output('merchants-by-payment-value', 'figure'),
    #     Input('merchants-by-payment-value', 'clickData'),
    #     Input('merchants-by-freight-value', 'clickData'),
    #     Input('merchants-by-order-items', 'clickData'),
    #     Input('merchants-by-avg-ship-days', 'clickData'),
    #     Input('data-store', 'data'),
    # )
    # def merchants_drilldown_hover(payment_value, freight_value, order_items, ship_days, data):
    #     datasets = json.loads(data)
    #
    #     ctx = dash.callback_context
    #     trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # if trigger_id == 'merchants-by-payment-value':
    #     print(payment_value)

    # return payment_value_hover

    def update_hover_color(clickData, dff):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger_id == 'merchants-by-payment-value' or trigger_id == 'merchants-by-freight-value':
            print(clickData)
            label = clickData['points'][0]['label']
            point_no = clickData['points'][0]['pointNumber']
            dff.loc[dff['seller_id'] == label, 'color'] = '#9BCEB5'
            color_discrete_map = {
                point_no: '#9BCEB5'}

            return dff
