import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly import graph_objects as go
import pandas as pd
import os

import page_utilities.page_utilities as pg_utils

pg_utils = pg_utils.PageUtilities()

dash.register_page(__name__, path='/', name='Homepage')
layout = dbc.Container(
    [
        html.H1("A Giant in the Making.", className='display-1 mb-1s'),
        html.H3("Is Olist the Amazon of Brazil?", className='display-3 mb-2'),
        html.Br(),
        html.Br(),
        html.Span(
            children=[
                html.Span("OList", className='chip'), "|", html.Span("eCommerce", className='chip'), "|",
                html.Span("B2B2C", className='chip')
            ],
            className='chip-span'),
        html.Br(),
        html.Br(),

        # OList info and Biz Questions
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.Br(),
                        html.P(
                            [
                                dcc.Link("Olist", href="https://olist.com/pt-br/"),

                                " is a Brazilian eCommerce Marketplace Integrator "
                                "that connects small businesses to larger product marketplaces.",
                                html.Br(),
                                html.Br(),
                                """
                                By using OList the merchant's also get access to a host of other tools that help them 
                                manage, run, and grow their businesses as well.
                                """
                            ]
                        ),
                        html.P(
                            children=[

                                """
                                Olist was founded in 2015 by Tiago Dalvi, after realizing a gap in the market 
                                running his own brick and mortar shop. He noticed that there was not a single
                                software to connect merchants to larger audiences.
                                """,
                                html.Br(),
                                html.Br(),
                                """
                                Like the brick and mortar store that he originally ran, Dalvi's focus has always been on 
                                bringing smaller Brazilian and 
                                Latin American merchants,and artisans to a larger audience.                            
                                """
                            ]
                        ),
                        # html.Br(),
                        # html.H3("A Department Store within the Marketplace.", className="display-3"),
                        # html.Br(),
                        # html.P(
                        #     """
                        #     They describe themselves as a "department store within the marketplaces", and are in more
                        #     than 180 countries. In 2020 they acquired both Clickspace, an ecommerce solutions
                        #     company and Pax, a logistics company to add to their ecosystem. In 2021 they also acquired,
                        #     tinyERP and Vnda.Olist plans to expand through a fulfillment center, and expansion
                        #     throughout Latin America.
                        #     They have recently began operation in Mexico, and achieved unicorn status in Brazil.
                        #     """
                        # ),
                        html.Br(),
                    ],
                    width=6,
                ),

                dbc.Col(
                    children=[
                        dcc.Loading(
                            html.Img(
                                id='hero-img',
                                alt='Brazilian Merchant talking to a customer ',
                                className='img-fluid mb-3 img-responsive',
                                src='https://c.files.bbci.co.uk/14788/production/_107084838_brazilshopping_getty.jpg',
                                title='Brazilian merchant talking to a customer',
                                width="80%"
                            ),
                            type='dot',
                            color='AQUAMARINE',
                        ),
                        dcc.Loading(
                            html.Img(
                                id='hero-img-2',
                                alt='Olist ',
                                className='img-fluid mb-3 img-responsive',
                                src='https://officesnapshots.com/wp-content/uploads/2021/10/olist-offices-curitiba-700x700-compact.jpg',
                                title='OList Offices.',
                                width="80%"
                            ),
                            type='dot',
                            color='AQUAMARINE',
                        ),
                    ],
                    width=6,
                ),
            ]
        ),

        # Dataset KPI Row.
        dbc.Row(
            children=[
                html.Br(),
                html.H2("Dataset Information", className="display-2"),
                html.Br(),
                html.Ul(
                    children=[
                        html.P(
                            """
                            These datasets used in this analysis are broken into datasets supplied by Olist, and external data sourced from the internet
                            """
                        ),

                        html.Br(),
                        html.Div(
                            id='home-kpi-card-group-wrapper',
                            children=[
                                # Total Files KPI Card
                                dbc.Card(
                                    children=[
                                        dbc.CardBody(
                                            children=[

                                                dcc.Loading(
                                                    children=[
                                                        dcc.Graph(
                                                            id='total-files',
                                                            responsive=True,
                                                            style={
                                                                'height': '30%',
                                                                'font-family': "Bebas Neue, cursive"
                                                            }
                                                        ),
                                                    ],
                                                    type='dot',
                                                    color="AQUAMARINE",
                                                )

                                            ],
                                        )
                                    ],
                                    className="kpi-card"
                                ),

                                # Total Rows
                                dbc.Card(
                                    children=[
                                        dbc.CardBody(
                                            children=[
                                                dcc.Loading(
                                                    children=[
                                                        dcc.Graph(
                                                            id='total-rows',
                                                            style={
                                                                'height': '30%',
                                                            }
                                                        ),
                                                    ],
                                                    type='dot',
                                                    color="AQUAMARINE",
                                                )

                                            ],
                                        )
                                    ],
                                    className="kpi-card"
                                ),

                                dbc.Card(
                                    children=[
                                        dbc.CardBody(
                                            children=[
                                                # html.H2("Total Files", className='card-title'),
                                                dcc.Loading(
                                                    children=[

                                                        dcc.Graph(
                                                            id='total-cols',
                                                            style={
                                                                'height': '30%',
                                                            }
                                                        ),
                                                    ],
                                                    type='dot',
                                                    color="AQUAMARINE",
                                                )

                                            ],
                                        )
                                    ],
                                    className="kpi-card"
                                ),

                            ],
                            className='card-group',
                            # style={
                            #     'height': '33%'
                            # }
                        ),
                        html.Br(),

                        html.Li(
                            ["""
                            These datasets are the Olist supplied datasets, and can be found on Kaggle.
                            """,
                             html.Br(),
                             html.Ul(
                                 children=[
                                     html.Li("Closed Deals"),
                                     html.Li("Customers"),
                                     html.Li("Geolocation"),
                                     html.Li("Marketing Qualified Leads"),
                                     html.Li("Order Items"),
                                     html.Li("Order Payments"),
                                     html.Li("Order Reviews"),
                                     html.Li("Orders"),
                                     html.Li("Products"),
                                     html.Li("Sellers"),
                                     html.Li("Product Category Name Translation"),
                                 ]
                             ),
                             ]
                        ),
                        html.Li(
                            ["""
                            External Datasets gathered from various sources on the internet are listed below.
                            """,
                             html.Br(),
                             html.Ul(
                                 children=[
                                     html.Li("Brazil GDP vs Neighbors 2021"),
                                     html.Li("Brazil Geojson"),
                                     html.Li("Brazil nmw data 2022"),
                                     html.Li("Brazil Population 2010_2020"),
                                     # html.Li("Order Items"),
                                     # html.Li("Order Payments"),
                                     # html.Li("Order Reviews"),
                                     # html.Li("Orders"),
                                     # html.Li("Products"),
                                     # html.Li("Sellers"),
                                     # html.Li("Product Category Name Translation"),
                                 ]
                             ),
                             ]
                        ),

                        html.Li(
                            """
                            Datasets that are blended combination of the olist and external datasource.
                            """
                        ),
                    ]

                ),

            ]
        ),
        dbc.Row(
            children=[
                html.Br(),
                html.H2("Project Purpose.", className='display-2'),
                html.Br(),
                html.P(
                    """
                        The Purpose of this project is to showcase the power of 
                        seeing and visualizing your data through interactive visual 
                        analytics. 
                """
                ),
                html.Br(),
                html.P(
                    """
                        It also showcases the power of leveraging open-source projects
                        to help build and speed up adoption of best data practices through, 
                        using the right visual and text mix to truly tell the story of 
                        the data. 
                """
                ),
                html.Br(),
                dcc.Loading(
                    html.Img(
                        id='hero-img',
                        alt='Person paying with a mobile app in store ',
                        className='img-fluid mb-3 img-responsive',
                        src='https://images.unsplash.com/photo-1571867424488-4565932edb41?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80',
                        title='Person paying with a mobile app in store .',
                        # width="80%",
                        # height='10rem'
                    ),
                    type='dot',
                    color='AQUAMARINE',
                ),
                html.Br(),
                html.P(
                    [
                        """
                        Since Olist donated the data we will act as if they are have hired 
        
                    """,
                        dcc.Link("ATB Analytics Group", href='https://atb-analytics-group.webflow.io/'),
                        """
                         to help with adpoting better data visualization practices as well as
                          faster adoption of managers understanding when moving markets, 
                         and looking for ways to expand Olist's market reach.
                    """
                    ],
                ),
                html.Br(),
                html.P(
                    """
                    To help Olist with this, we came up with the proposed Business Suite. Giving a full background 
                    on the last two years worth of data. Presenting data in this way has many benefits, and once 
                    built can updated and maintained through data pipelining. 
                    """
                ),
                html.Br(),
                html.P(
                    """
                        Visualization empowers users to  intuitively learn how the data is connected,
                         ask and answer their own questions through interaction, 
                         and see what trends and gaps might be missing from
                         questions left un-answered.
                    """
                ),
                html.Br(),
                html.H4('How to use this Tool'),
                html.P(
                    [
                        """
                                            This is an interactive journey however the 'Business Suite' is broken down into the following
                                            pages:
                                            """,
                        html.Br(),

                        """
                        For many of the charts, if you hover or click certain data in them it will show you 
                        more drilled down information about that particualr area of interest. 
                        
                        For example on the, 
                        """,
                        dcc.Link("Marketing", href='#'),
                        """
                            page if you click in the channel or sales charts it filters the other to show you information 
                            specific too that click.
                        """

                    ]

                ),
                html.Br(),
                html.H4('Dataset sources, and other sources used to make this analysis.'),

                # TODO Finish adding in sources that were used to help build this suite.
                html.P(
                    children=[
                        """
                                            Kaggle Datasets: 
                        """,
                        html.Br(),
                        dcc.Link("Olist-Brazilian Ecommerce",
                                 href='https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce'),
                        html.Br(),
                        dcc.Link("Olist-Marketing Funnel",
                                 href='https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist'),
                        html.Br(),
                        """
                        Plotly:            
                        """,
                        dcc.Link("Documentation", href='https://plotly.com/'),
                        html.Br(),
                        """
                            I used this to help me with creating my own Templates.
                        """,
                        dcc.Link("Customizing Themes in Plotly",
                                 href="https://www.nelsontang.com/blog/2021-08-01-build-your-first-plotly-template"),
                        html.Br(),
                        """
                            Pandas Understanding and Help:
        
                        """,
                        html.Br(),
                        dcc.Link("Pivot Tables in Pandas",
                                 href="https://pbpython.com/pandas-pivot-table-explained.html"),
                        html.Br(),
                        """
                            Other Links used to complete various aspects and pages through out this project.
                            Various Other Links used to complete the suite:
                        """,
                        html.Br(),
                        """
                                                                        RFM Analysis:
        
                        """,
                        dcc.Link("RFM Analysis - Geeks For Geeks",
                                 href="https://www.geeksforgeeks.org/rfm-analysis-analysis-using-python/"),
                        html.Br(),
                        """
                                                                        Cohort Analysis:
        
                        """,
                        dcc.Link("Cohort Analysis - Data Driven Investor",
                                 href="https://medium.datadriveninvestor.com/marketing-data-science-segmentation-of-customers-e02e048b4d47"),
                        html.Br(),
                        """
                                                                        CLTV:
        
                        """,
                        dcc.Link("Customer Lifetime Value Calculations - Ulas Turker",
                                 href='https://medium.com/@ulasturker/customer-life-time-value-calculations-with-python-cltv-with-crm-analytics-2-in-data-science-7d39ca9ad2de'),
                        html.Br(),
                        """
                                                                        Marketing EDA:
        
                        """,
                        dcc.Link("Marketing EDA - Towards Data Science",
                                 href='https://towardsdatascience.com/exploratory-data-analysis-with-python-in-b2b-marketing-3e4b2b230a50'),
                        html.Br(),
                        """
                            Information about Brazil:
                        """,
                        html.Br(),
                        dcc.Link("Brazil Wiki", href='https://en.wikipedia.org/wiki/Brazil'),
                        html.Br(),
                        dcc.Link("Brazil Population by City",
                                 href='https://en.wikipedia.org/wiki/List_of_cities_in_Brazil_by_population '),
                        html.Br(),
                        dcc.Link("Brazilian Consumer",
                                 href='https://www.rws.com/blog/understanding-the-brazilian-consumer/'),
                        html.Br(),

                    ],

                ),
                html.Br(),
                # html.H4(),
            ]
        ),

        # # File-Names
        # dbc.Col(
        #     children=[
        #         # html.H2("Dataset Information Cards", className='card-title'),
        #         # html.Br(),
        #         dbc.Card(
        #             children=[
        #                 dbc.CardBody(
        #                     children=[
        #                         # html.H2("Total Files", className='card-title'),
        #                         dcc.Loading(
        #                             children=[
        #                                 html.Div(id='file-names', )
        #                                 # dcc.Graph(
        #                                 #     id='file-names',
        #                                 # ),
        #                             ],
        #                             color="AQUAMARINE",
        #                         )
        #
        #                     ],
        #                 )
        #             ],
        #             className="kpi-card"
        #         )
        #     ],
        #     width=6,
        # ),
        #
        # # column Names
        # dbc.Col(
        #     children=[
        #         # html.H2("Dataset Information Cards", className='card-title'),
        #         # html.Br(),
        #         dbc.Card(
        #             children=[
        #                 dbc.CardBody(
        #                     children=[
        #                         # html.H2("Total Files", className='card-title'),
        #                         dcc.Loading(
        #                             children=[
        #                                 html.Div(id='col-names', )
        #                                 # dcc.Graph(
        #                                 #     id='file-names',
        #                                 # ),
        #                             ],
        #                             color="AQUAMARINE",
        #                         )
        #
        #                     ],
        #                 )
        #             ],
        #             className="kpi-card"
        #         )
        #     ],
        #     width=6,
        # ),
        html.Br()
    ]
),

dbc.Row(
    children=[
        html.Br(),
        html.H2("Project Purpose.", className='display-2'),
        html.Br(),
        dcc.Loading(
            html.Img(
                id='hero-img',
                alt='Person paying with a mobile app in store ',
                className='img-fluid mb-3 img-responsive',
                src='https://images.unsplash.com/photo-1571867424488-4565932edb41?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=387&q=80',
                title='Person paying with a mobile app in store .',
                width="80%",
                height='10rem'
            ),
            type='dot',
            color='AQUAMARINE',
        ),
        html.Br(),
        html.P(
            """
                The Purpose of this project is to showcase the power of 
                seeing and visualizing your data through interactive visual 
                analytics. 
        """
        ),
        html.Br(),
        html.P(
            """
                It also showcases the power of leveraging open-source projects
                to help build and speed up adoption of best data practices through, 
                using the right visual and text mix to truly tell the story of 
                the data. 
        """
        ),
        html.Br(),
        html.P(
            [
                """
                Since Olist donated the data we will act as if they are have hired 
                 
            """,
                dcc.Link("ATB Analytics Group", href='https://atb-analytics-group.webflow.io/'),
                """
                 to help with adpoting better data visualization practices as well as
                  faster adoption of managers understanding when moving markets, 
                 and looking for ways to expand Olist's market reach.
            """
            ],
        ),
        html.Br(),
        html.P(
            """
            To help Olist with this, we came up with the proposed Business Suite. Giving a full background 
            on the last two years worth of data. Presenting data in this way has many benefits, and once 
            built can updated and maintained through data pipelining. 
            """
        ),
        html.Br(),
        html.P(
            """
                Visualization empowers users to  intuitively learn how the data is connected,
                 ask and answer their own questions through interaction, 
                 and see what trends and gaps might be missing from
                 questions left un-answered.
            """
        ),
        html.Br(),
        html.H4('How to use this Tool'),
        html.P(
            [
                """
                                    This is an interactive journey however the 'Business Suite' is broken down into the following
                                    pages:
                                    """,
                html.Br(),
                """
                -Home
                
                """,
                html.Br(),
                html.P("Information Page"),
                html.Br(),
                dcc.Link('About', href='http://127.0.0.1:8050/about'),
                html.Br(),
                html.P("Information Page"),
                html.Br(),
                dcc.Link("Customers", href='http://127.0.0.1:8050/customer-analysis'),
                html.Br(),
                html.P("Information Page"),
                html.Br(),
                dcc.Link("Marketing", href='http://127.0.0.1:8050/marketing-analysis'),
                html.Br(),
                html.P("Information Page"),
                html.Br(),
                dcc.Link("Merchants", href='http://127.0.0.1:8050/merchant-analysis'),
                html.Br(),
                html.P("Information Page"),
                html.Br(),
                dcc.Link("Sales", href='http://127.0.0.1:8050/sales-analysis'),
                html.Br(),
                html.P("Information Page"),
                html.Br(),
            ]

        ),
        html.Br(),
        html.H4('Dataset sources, and other sources used to make this analysis.'),

        # TODO Finish adding in sources that were used to help build this suite.
        html.P(
            children=[
                """
                                    Kaggle Datasets: 
                """,
                html.Br(),
                dcc.Link("Olist-Brazilian Ecommerce",
                         href='https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce'),
                html.Br(),
                dcc.Link("Olist-Marketing Funnel",
                         href='https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist'),
                html.Br(),
                """
                Plotly:            
                """,
                dcc.Link("Documentation", href='https://plotly.com/'),
                html.Br(),
                """
                    I used this to help me with creating my own Templates.
                """,
                dcc.Link("Customizing Themes in Plotly",
                         href="https://www.nelsontang.com/blog/2021-08-01-build-your-first-plotly-template"),
                html.Br(),
                """
                    Pandas Understanding and Help:
                                        
                """,
                html.Br(),
                dcc.Link("Pivot Tables in Pandas",
                         href="https://pbpython.com/pandas-pivot-table-explained.html"),
                html.Br(),
                """
                    Other Links used to complete various aspects and pages through out this project.
                    Various Other Links used to complete the suite:
                """,
                html.Br(),
                """
                                                                RFM Analysis:
                                                                    
                """,
                dcc.Link("RFM Analysis - Geeks For Geeks",
                         href="https://www.geeksforgeeks.org/rfm-analysis-analysis-using-python/"),
                html.Br(),
                """
                                                                Cohort Analysis:
                                                                    
                """,
                dcc.Link("Cohort Analysis - Data Driven Investor",
                         href="https://medium.datadriveninvestor.com/marketing-data-science-segmentation-of-customers-e02e048b4d47"),
                html.Br(),
                """
                                                                CLTV:
                                                                
                """,
                dcc.Link("Customer Lifetime Value Calculations - Ulas Turker",
                         href='https://medium.com/@ulasturker/customer-life-time-value-calculations-with-python-cltv-with-crm-analytics-2-in-data-science-7d39ca9ad2de'),
                html.Br(),
                """
                                                                Marketing EDA:
                                                                
                """,
                dcc.Link("Marketing EDA - Towards Data Science",
                         href='https://towardsdatascience.com/exploratory-data-analysis-with-python-in-b2b-marketing-3e4b2b230a50'),
                html.Br(),
                """
                    Information about Brazil:
                """,
                html.Br(),
                dcc.Link("Brazil Wiki", href='https://en.wikipedia.org/wiki/Brazil'),
                html.Br(),
                dcc.Link("Brazil Population by City",
                         href='https://en.wikipedia.org/wiki/List_of_cities_in_Brazil_by_population '),
                html.Br(),
                dcc.Link("Brazilian Consumer",
                         href='https://www.rws.com/blog/understanding-the-brazilian-consumer/'),
                html.Br(),

            ],

        ),
        html.Br(),
        # html.H4(),
    ]
)


# Quick Facts about the Brazilian economy at during the same time that our dataset is for.
# dbc.Row(
#     children=[
#         html.Br(),
#         html.H2("Brazil - Order and Progress.", className="display-2"),
#         html.Br(),
#         html.H5("A look at 2016-2018", className="display-5"),
#         html.Br(),
#         dbc.Col(
#             children=[
#                 html.Img(
#                     # id='hero-img',
#                     alt='A view with Sugar Loaf Mountain overlooking the bay,'
#                         ' and city of Rio De Janerio during the day.',
#                     className='img-fluid mb-3 img-responsive',
#                     src='https://cdn.cnn.com/cnnnext/dam/assets/220125121731-destination-brazil-hero-image.jpg',
#                     title='Rio De Janerio',
#                     width="100%",
#                 ),
#                 # Source - https://en.wikipedia.org/wiki/Brazil#Economy
#                 html.P(
#                     """
#                     Brazil is the 5th Largest Country in the world, and has a population North of 210 million people.
#                     The largest cities are Sao Paulo, Rio de Janerio, and Brasilia.\nThe capital is Brasilia, and its most,
#                     populous city is Sao Paulo.
#                     """
#                 ),
#
#                 html.P(
#                     """
#                     \nBrazil's official language is Portuguese, and is one of the most
#                     multicultural and ethnically diverse nations in the world due to over a century of mass immigration
#                     from all around the world. The main religion in Brazil is Roman-Catholic.
#                     """
#                 ),
#
#                 html.Br(),
#                 html.H3("Economy - How Brazilian's get Paid.", className="display-3"),
#                 html.Br(),
#                 html.Img(
#                     # id='hero-img',
#                     alt='Map of Bazil'
#                         ' and city of Rio De Janerio during the day.',
#                     className='img-fluid mb-3 img-responsive',
#                     src='https://www.worldatlas.com/r/w960-q80/upload/db/df/33/br-01.png',
#                     title='Map of Brazil from the World Atlas',
#                     width="100%"
#                 ),
#                 html.Br(),
#                 # Source - https://en.wikipedia.org/wiki/Brazil#Economy
#                 html.P(
#                     """
#                 Brazil is has the 9th largest economy in the world, and is the largest economy in all of Latin
#                 America. They have a labor force of about 107 million, and an unemployment rate that hovers around 6.2%.
#                 For the last 150 years Brazil has been the largest exporter of Coffee in the world. They are also
#                 major exporters of soy, iron ore, pulp (cellulose) to name a few.
#                 """
#                 ),
#                 html.Br(),
#                 html.Img(
#                     # id='hero-img',
#                     alt='A view with Sugar Loaf Mountain overlooking the bay,'
#                         ' and city of Rio De Janerio during the day.',
#                     className='img-fluid mb-3 img-responsive',
#                     src='https://www.icrc.org/sites/default/files/styles/amp_thumbnail_image_1-1/public/document/image_thumbnail/brasil-migrantes_se_beneficiam_de_acesso_a_agua_pelo_cicv_na_igreja_batista_em_pacaraima__0.jpg?itok=_J_iD7t1',
#                     title='Rio De Janerio',
#                     # width="100%"
#                 ),
#                 html.Br(),
#                 # Source - https://countryeconomy.com/national-minimum-wage/brazil
#                 html.P(
#                     """
#                         The Minimum wage in Brazil in 2016 is 880 Brazilian Reals, or about $252.10 \n
#                         By 2018, the minimum wage would rise to 954 Brazilian Reals, or about $261.10.
#                         This is an increase of 8.2% over two years.
#                     """
#                 ),
#                 html.Br(),
#
#             ],
#             width=12,
#         ),
#     ],
#
# )

# ]
# )

@callback(
    Output('total-files', 'figure'),
    # Output('file-names', 'children'),
    Output('total-rows', 'figure'),
    Output('total-cols', 'figure'),
    # Output('col-names', 'children'),
    [Input('data-store', 'data'),

     State('data-store', 'data')],
    suppress_callback_exceptions=True,
    prevent_inital_callbacks=True,
)
def update_homepage_kpi_row(data, data2):
    dir = os.listdir('./data/OlistEcomData')
    tot_files = 0
    path_names = []
    for path in dir:
        if os.path.isfile(os.path.join('./data/OListEcomData', path)):
            path_names.append(path)
            tot_files += 1

    # Total Files that are present in the data directory
    tot_fig = go.Figure()
    tot_fig.add_trace(
        go.Indicator(
            value=tot_files,
            title={'text': "Total OList Files"},
            domain={'x': [0, 1], 'y': [0, 1]}
        ),
    ),

    # File Names that are in the Data directory.
    path_names_dict = dict.fromkeys(path_names, "name")
    pn_df = pd.DataFrame(path_names, columns=["filename"])
    # pn_df.T.reset_index(inplace=True)
    # pn_df.transpose()
    path_name_table = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in pn_df.columns],
        data=pn_df.to_dict('records')
    )

    df = pd.read_csv('./data/combined_olist_data.csv', )

    cols = df.columns
    col_df = pd.DataFrame(cols.tolist(), columns=["Column Names"])
    columns_table = dash_table.DataTable(
        id='table',
        data=col_df.to_dict('records')
    )

    tot_rows = df.shape[0]
    tot_cols = df.shape[1]

    tot_rows_fig = go.Figure()
    tot_rows_fig.add_trace(
        go.Indicator(
            value=tot_rows,
            title={'text': "Total Rows"},
            domain={'x': [0, 1], 'y': [0, 1]}
        ),
    ),

    tot_cols_fig = go.Figure()
    tot_cols_fig.add_trace(
        go.Indicator(
            value=tot_cols,
            title={'text': "Columns used in Analysis"},
            domain={'x': [0, 1], 'y': [0, 1]}
        ),
    ),

    return tot_fig, tot_rows_fig, tot_cols_fig
