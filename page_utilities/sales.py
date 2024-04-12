import json

import dash
import numpy as np
from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import page_utilities.page_utilities as pg_utils

pg_utils = pg_utils.PageUtilities()

dash.register_page(__name__, path='/sales-analysis', name='Sales')

layout = dbc.Container(
    children=[
        html.H1("Financial Insights", className="Display-1"),
        html.Br(),

        # Financial Insights KPI Row - 1
        dbc.Row(
            children=[
                dbc.Card(
                    dbc.CardBody(
                        dcc.Loading(
                            dcc.Graph(
                                id="total-revenue",
                                responsive=True,
                                animate=True,
                            ),
                            type='dot',
                            color="AQUAMARINE",
                        )
                    ),
                    className='kpi-card'
                ),

                dbc.Card(
                    dbc.CardBody(
                        dcc.Loading(
                            dcc.Graph(
                                id="total-customers",
                                responsive=True,
                                animate=True,
                            ),
                            type='dot',
                            color="AQUAMARINE",
                        )
                    ),
                    className='kpi-card'
                ),
            ],
            className='card-group'
        ),

        dbc.Row(
            children=[
                dbc.Card(
                    dbc.CardBody(
                        dcc.Loading(
                            dcc.Graph(
                                id="total-shipping-costs",
                                responsive=True,
                                animate=True,
                            ),
                            type='dot',
                            color="AQUAMARINE",
                        )
                    ),
                    className='kpi-card'
                ),

                dbc.Card(
                    dbc.CardBody(
                        dcc.Loading(
                            dcc.Graph(
                                id="fi-avg-order-value",
                                responsive=True,
                                animate=True,
                            ),
                            type='dot',
                            color="AQUAMARINE",
                        )
                    ),
                    className='kpi-card'
                ),
            ],
            className='card-group'
        ),

        dbc.Row(
            children=[
                html.H2("Product Category Revenues"),
                html.Br(),
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    html.H6("Price Multiplier", ),
                                    html.P(
                                        'A cost multiple. We are going to use this to get our assumed product costs estimate.'),
                                    html.Br(),
                                    dcc.Input(
                                        id='fi-price-multiple',
                                        type='number',
                                        min=2,
                                        max=10,
                                        step=1,
                                        value=3,
                                        placeholder=3,
                                        inputMode='numeric'
                                    ),
                                ],
                            ),
                            className='user-selection-card'
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    html.H6("Select Value", className='text-center'),
                                    html.Br(),
                                    html.P(
                                        'Select the value that you would like to see the Product Revenue Compared too.'),
                                    html.Br(),
                                    dcc.RadioItems(
                                        id='fi-n-radioitems',
                                        options={
                                            'payment_value': 'Revenue',
                                            'seller_id': 'Merchant Count',
                                            'customer_unique_id': 'Customer Count',
                                            'freight_value': 'Shipping Cost',
                                            'prod_cost': 'Ass. Product Cost'
                                        },
                                        value='freight_value',
                                        inline=True,
                                        persistence=True,

                                    ),
                                ],
                            ),
                            className='user-selection-card'
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    html.H6("Select Number of Products"),
                                    html.P("Select the number of product categories that you would like to see."
                                           "That can be the Top 10, 20, 30, etc."
                                           ""),
                                    html.Br(),
                                    dcc.Slider(
                                        id='fi-n-slider',
                                        min=0,
                                        max=100,
                                        step=10,
                                        value=10,
                                        tooltip={
                                            "placement": "bottom",
                                            "always_visible": True
                                        },
                                        persistence=True,
                                    ),
                                ],
                            ),
                            className='user-selection-card'
                        ),
                    ],
                    width=12,
                    align='center',
                    className='kpi-card'
                ),
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Loading(
                                    dcc.Graph(
                                        id="product-revenue",
                                        responsive=True,
                                        animate=True,
                                    ),
                                    type='dot',
                                    color="AQUAMARINE",
                                )
                            ),
                            className='kpi-card'
                        ),
                    ],
                    width=12,
                    align='center',

                ),

                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Loading(
                                    dcc.Graph(
                                        id="product-category-seller-ids",
                                        responsive=True,
                                        animate=True,
                                    ),
                                    type='dot',
                                    color="AQUAMARINE",
                                )
                            ),
                            className='kpi-card'
                        ),
                    ],
                    width=6,
                    align='center',

                ),

                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Loading(
                                    dcc.Graph(
                                        id="product-category-profit-margin",
                                        responsive=True,
                                        animate=True,
                                    ),
                                    type='dot',
                                    color="AQUAMARINE",
                                )
                            ),
                            className='kpi-card'
                        ),
                    ],
                    width=6,
                    align='center',
                ),

            ]
        ),
    ],
    fluid=True,
)


@callback(
    Output('total-revenue', 'figure'),
    Output('total-customers', 'figure'),
    Output('total-shipping-costs', 'figure'),
    Output('fi-avg-order-value', 'figure'),
    # Output('product-category-seller-ids', 'figure'),
    # Output('product-category-profit-margin', 'figure'),
    Input('data-store', 'data'),
    Input('fi-n-radioitems', 'value'),
    # Input('fi-n-slider', 'value')
)
def update_fi_kpis(data, radio_value):
    datasets = json.loads(data)
    dff = pd.read_csv('./data/combined_olist_data.csv')

    dff['order_month_date'] = pd.to_datetime(dff['order_month_date'], errors='coerce',
                                             infer_datetime_format=True)
    tot_revenue = dff.payment_value.sum()
    tot_customers = dff.customer_unique_id.count()
    tot_shipping_costs = dff.freight_value.sum()
    tot_orders = dff.order_id.count()
    avg_order_value = dff.payment_value.sum() / tot_orders

    fi_data_by_month = dff[['order_month_date', 'customer_unique_id', 'order_id', 'seller_id',
                            'payment_value', 'freight_value']].groupby('order_month_date').agg(
        {
            'customer_unique_id': 'nunique',
            'order_id': 'nunique',
            'seller_id': 'nunique',
            'payment_value': 'sum',
            'freight_value': 'sum'
        }
    ).reset_index()

    fi_data_by_month['purchase_frequency'] = fi_data_by_month.order_id / fi_data_by_month.customer_unique_id
    fi_data_by_month['avg_order_value'] = fi_data_by_month.payment_value / fi_data_by_month.order_id
    fi_data_by_month['customer_value'] = (
                                                 fi_data_by_month.avg_order_value / fi_data_by_month.purchase_frequency) / 1  # Normally 1 is Churn Rate.

    tot_revenue_fig = make_subplots(rows=1, cols=1,
                                    specs=[[{"secondary_y": True}]])
    tot_revenue_fig.add_trace(
        go.Indicator(
            value=tot_revenue,
            number={
                'font': {
                    'family': 'Bebas Neue',
                    'size': 24,
                }
            },
            title={
                'text': "Total Revenue",
                'align': 'center',
                'font': {'family': 'Bebas Neue', 'size': 36}
            },
            domain={'x': [0, 1], 'y': [1, 0]},
        )
    )

    tot_revenue_fig.add_bar(
        x=fi_data_by_month.order_month_date,
        y=fi_data_by_month.payment_value,
        opacity=.2,
        row=1,
        col=1,
        name='revenue',
        hovertemplate="$%{y:,.2f}",
        xaxis='x1',
        yaxis='y1',
    )

    tot_revenue_fig.add_scatter(
        x=fi_data_by_month.order_month_date,
        y=fi_data_by_month.order_id,
        opacity=.2,
        row=1,
        col=1,
        name='orders',
        secondary_y=True,
        hovertemplate="%{y:,}",
        xaxis='x1',
        yaxis='y2',
    )

    tot_revenue_fig.add_scatter(
        x=fi_data_by_month.order_month_date,
        y=fi_data_by_month.freight_value,
        opacity=.2,
        row=1,
        col=1,
        name='shipping cost',
        secondary_y=False,
        hovertemplate="$%{y:,.2f}",
        xaxis='x1',
        yaxis='y2',
    )

    tot_revenue_fig.update_xaxes(title_text="Month Ordered", )
    tot_revenue_fig.update_yaxes(
        title_text='revenue/shipping cost',
        secondary_y=False,
        # anchor="free",
        # overlaying="y",
        # side="left",
    )
    tot_revenue_fig.update_yaxes(
        title_text='orders', secondary_y=True,
        # anchor="free",
        overlaying="y",
        # side="right",
    )

    # tot_revenue_fig.update_layout(legend=dict(
    #     orientation="h",
    #     yanchor="bottom",
    #     y=1.02,
    #     xanchor="right",
    #     x=1
    # ))

    tot_customers_fig = make_subplots(rows=1, cols=1,
                                      specs=[[{"secondary_y": True}]])
    tot_customers_fig.add_trace(
        go.Indicator(
            value=tot_customers,
            number={
                'font': {
                    'family': 'Bebas Neue',
                    'size': 24,
                }
            },
            title={
                'text': "Total Customers",
                'align': 'center',
                'font': {'family': 'Bebas Neue', 'size': 36}
            },
            domain={'x': [0, 1], 'y': [0, 1]},
        )
    )

    tot_customers_fig.add_bar(
        x=fi_data_by_month.order_month_date,
        y=fi_data_by_month.customer_unique_id,
        opacity=.2,
        row=1,
        col=1,
        name='customers',
        hovertemplate="%{y:,}"
    )

    tot_customers_fig.add_scatter(
        x=fi_data_by_month.order_month_date,
        y=fi_data_by_month.order_id,
        opacity=.2,
        row=1,
        col=1,
        name='orders',
        secondary_y=True,
        hovertemplate="%{y:,}"
    )

    tot_customers_fig.add_scatter(
        x=fi_data_by_month.order_month_date,
        y=fi_data_by_month.payment_value,
        opacity=.2,
        row=1,
        col=1,
        name='revenue',
        secondary_y=False,
        hovertemplate="$%{y:,.2f}"
    )

    tot_customers_fig.update_xaxes(title_text="Month Ordered", )
    tot_customers_fig.update_yaxes(
        title_text='customers/revenue',
        secondary_y=False,
        # anchor="free",
        # overlaying="y",
        # side="left",
    )
    tot_customers_fig.update_yaxes(
        title_text='orders',
        secondary_y=True,
        # anchor="free",
        overlaying="y",
        # side="right",
    )

    tot_shipping_costs_fig = make_subplots(rows=1, cols=1,
                                           specs=[[{"secondary_y": True}]])
    tot_shipping_costs_fig.add_trace(
        go.Indicator(
            value=tot_shipping_costs,
            number={
                'font': {
                    'family': 'Bebas Neue',
                    'size': 24,
                }
            },
            title={
                'text': "Total Shipping Cost",
                'align': 'center',
                'font': {'family': 'Bebas Neue', 'size': 36}
            },
            domain={'x': [0, 1], 'y': [0, 1]},
        )
    )

    tot_shipping_costs_fig.add_bar(
        x=fi_data_by_month.order_month_date,
        y=fi_data_by_month.freight_value,
        opacity=.2,
        row=1,
        col=1,
        name='Shipping Cost',
        hovertemplate="$%{y:,.2f}"
    )

    tot_shipping_costs_fig.add_scatter(
        x=fi_data_by_month.order_month_date,
        y=fi_data_by_month.order_id,
        opacity=.2,
        row=1,
        col=1,
        name='orders',
        secondary_y=True,
        hovertemplate="%{y:,}"
    )

    tot_shipping_costs_fig.add_scatter(
        x=fi_data_by_month.order_month_date,
        y=fi_data_by_month.payment_value,
        opacity=.2,
        row=1,
        col=1,
        name='revenue',
        secondary_y=False,
        hovertemplate="$%{y:,.2f}"
    )

    tot_shipping_costs_fig.update_xaxes(title_text="Month Ordered", )
    tot_shipping_costs_fig.update_yaxes(
        title_text='shipping costs/revenue',
        secondary_y=False,
        # anchor="free",
        # overlaying="y",
        # side="left",
    )
    tot_shipping_costs_fig.update_yaxes(
        title_text='orders',
        secondary_y=True,
        # anchor="free",
        overlaying="y",
        # side="right",
    )

    avg_order_value_fig = make_subplots(rows=1, cols=1,
                                        specs=[[{"secondary_y": True}]])
    avg_order_value_fig.add_trace(
        go.Indicator(
            value=avg_order_value,
            number={
                'font': {
                    'family': 'Bebas Neue',
                    'size': 24,
                }
            },
            title={
                'text': "Avg Order Value",
                'align': 'center',
                'font': {'family': 'Bebas Neue', 'size': 36}
            },
            domain={'x': [0, 1], 'y': [0, 1]},
        )
    )

    avg_order_value_fig.add_bar(
        x=fi_data_by_month.order_month_date,
        y=fi_data_by_month.avg_order_value,
        opacity=.2,
        row=1,
        col=1,
        name='avg-order-value',
        hovertemplate="$%{y:,.2f}"
    )

    avg_order_value_fig.add_scatter(
        x=fi_data_by_month.order_month_date,
        y=fi_data_by_month.customer_value,
        opacity=.2,
        row=1,
        col=1,
        name='customer-value',
        secondary_y=False,
        hovertemplate="$%{y:,.2f}"
    )

    avg_order_value_fig.add_scatter(
        x=fi_data_by_month.order_month_date,
        y=fi_data_by_month.payment_value,
        opacity=.2,
        row=1,
        col=1,
        name='revenue',
        secondary_y=True,
        hovertemplate="$%{y:,.2f}"
    )

    avg_order_value_fig.update_xaxes(title_text="Month Ordered", )
    avg_order_value_fig.update_yaxes(
        title_text='avg order value/customer value',
        secondary_y=False,
        # anchor="free",
        # overlaying="y",
        # side="left",
    )
    avg_order_value_fig.update_yaxes(
        title_text='revenue',
        secondary_y=True,
        # anchor="free",
        overlaying="y",
        # side="right",
    )

    all_figs = [tot_revenue_fig, tot_customers_fig, tot_shipping_costs_fig, avg_order_value_fig]

    # For things that need to be applied to all figures.  TODO make this a function in the utility class.
    for fig in all_figs:
        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=1.125,
                xanchor="right",
                x=1,
                bgcolor="#E4F2EF",
                title_text='Legend'
            ),
        )

    return tot_revenue_fig, tot_customers_fig, tot_shipping_costs_fig, avg_order_value_fig


@callback(
    Output('product-revenue', 'figure'),
    Output('product-category-seller-ids', 'figure'),
    Output('product-category-profit-margin', 'figure'),
    Input('data-store', 'data'),
    Input('fi-n-radioitems', 'value'),
    Input('fi-price-multiple', 'value'),
    Input('fi-n-slider', 'value'),
)
def update_product_category_graphs(data, radio_value, price_multiple, n_slider):
    datasets = json.loads(data)
    dff = pd.read_csv('./data/combined_olist_data.csv')

    dff['order_month_date'] = pd.to_datetime(dff['order_month_date'], errors='coerce',
                                             infer_datetime_format=True)
    tot_revenue = dff.payment_value.sum()
    tot_customers = dff.customer_unique_id.count()
    tot_shipping_costs = dff.freight_value.sum()
    tot_orders = dff.order_id.count()
    avg_order_value = dff.payment_value.sum() / tot_orders

    fi_data_by_month = dff[['order_month_date', 'customer_unique_id', 'order_id', 'seller_id',
                            'payment_value', 'freight_value', 'product_category_name_english']].groupby(
        'product_category_name_english').agg(
        {
            'customer_unique_id': 'nunique',
            'order_id': 'nunique',
            'seller_id': 'nunique',
            'payment_value': 'sum',
            'freight_value': 'sum',
            # 'product_category_name_english': 'first'
        }
    ).reset_index()

    fi_data_by_month['purchase_frequency'] = fi_data_by_month.order_id / fi_data_by_month.customer_unique_id
    fi_data_by_month['avg_order_value'] = fi_data_by_month.payment_value / fi_data_by_month.order_id
    fi_data_by_month['customer_value'] = (
                                                 fi_data_by_month.avg_order_value / fi_data_by_month.purchase_frequency) / 1  # Normally 1 is Churn Rate.

    # add in product cost and profit margin to the fi_data_by_month dataframe
    if price_multiple <= 0:
        price_multiple = 3
    fi_data_by_month['prod_cost'] = fi_data_by_month['payment_value'] / price_multiple
    fi_data_by_month['profit'] = fi_data_by_month['payment_value'] - fi_data_by_month['prod_cost']
    fi_data_by_month['profit_margin'] = fi_data_by_month['profit'] / fi_data_by_month['payment_value']

    # Sort Dataframe, break into top bottom analysis.
    fi_data_by_month.sort_values(by='payment_value', ascending=True)
    fi_data_by_month_bottom = fi_data_by_month.sort_values(by='payment_value', ascending=False)
    # TODO Add State Information to the dataframe so that we can make a top sales by state graph. if time permits.

    # product revenue figure
    product_revenue_fig = make_subplots(rows=1, cols=1,
                                        specs=[[{"secondary_y": True}]])

    product_revenue_fig.add_trace(
        go.Bar(
            x=fi_data_by_month.payment_value,
            y=fi_data_by_month.product_category_name_english,
            orientation='h',
            name='product-revenue',
        )
    )

    product_revenue_fig.add_bar(
        x=fi_data_by_month[radio_value],
        y=fi_data_by_month.product_category_name_english,
        # opacity=.2,
        row=1,
        col=1,
        # secondary_y=True,
        name=f'{radio_value}',
        orientation='h',
    )
    product_revenue_fig.update_layout(
        barmode='stack',
    )

    product_revenue_fig.update_xaxes(
        title_text=f"{radio_value}"
    )

    product_category_seller_id_fig = go.Figure(
        go.Bar(
            x=fi_data_by_month.payment_value,
            y=fi_data_by_month.seller_id,
            orientation='h',
            name='product-revenue',
        )
    )

    product_category_profit_margin_fig = go.Figure(
        go.Bar(
            x=fi_data_by_month.profit_margin * 100,
            y=fi_data_by_month.seller_id,
            orientation='h',
            name='product-profit-margin',
        )
    )

    return product_revenue_fig, product_category_seller_id_fig, product_category_profit_margin_fig
