import json

import dash
import numpy as np
from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly import graph_objects as go
import pandas as pd
import os
import plotly.io as pio
import page_utilities.page_utilities as pg_utils

pg_utils = pg_utils.PageUtilities()

dash.register_page(__name__, path='/about', name='About', title="About Olist and the Brazilian Economy")
layout = dbc.Container(
    [
        html.H1("Olist, Brazil, and Fostering Connections Worldwide.", className='display-1'),
        html.Br(),

        # OList info and Biz Questions
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.P(
                            """
                            Olist is a Brazilian eCommerce Marketplace Integrator that connects small businesses
                            to larger product marketplaces and was founded in 2015
                            by Tiago Dalvi."""
                        ),
                        html.Br(),
                        html.P(
                            """
                            He saw an opportunity to build the middleware necessary to 
                            connect marketplaces and merchants in Brazil. Unlike the US where this is dominatied by the Amazon's of the world,
                            Amazon has only recently started operations in Brazil, Olist's came about at the right time. 
                            Through their technology Olist helps small 
                            merchants gain market share by linking them to the global marketplaces that they may 
                            not have gained access too otherwise due to technological hindrances and infrastructure. 
                            """
                        ),
                        html.Br(),
                        html.H3("A Department Store within the Marketplace.", className="display-3"),
                        html.Br(),
                        html.P(
                            """
                            They describe themselves as a "department store within the marketplaces", and are available in more 
                            than 180 countries. In 2020 they acquired both Clickspace, an ecommerce solutions 
                            company and Pax, a logistics company to add to their ecosystem. In 2021 they also acquired, 
                            tinyERP and Vnda to further bolster their offerings to help merchants manage and grow their
                            businesses.
                        """),
                        html.Br(),
                        html.P(
                            """
                            Olist plans to expand through a fulfillment center, as well as a planned expansion 
                                throughout Latin America. 
                                They have recently began operation in Mexico, and Nigeria, and 
                                have achieved unicorn status in Brazil. 
                                """
                        ),
                        html.Br(),
                        # html.H3("A Few question's from past performance.", className="display-3"),
                        # html.Br(),
                        # html.P(
                        #     """
                        #     OList is looking to understand a few business questions from some past sales data.
                        #     They have provided us with a about two years worth of data from 2016-2018, and have
                        #     given us about 9 different files on these operations. In this analysis we will try
                        #     and utilize as much of this data as necessary to tell the story of OList from 2016-2018.
                        #     At least from the point of view of this dataset.
                        #     """
                        # ),
                        # html.Br(),
                        # html.P(
                        #     """
                        #     What are the sales per month, per year.
                        #     Trend of Sales per year
                        #     Where do most of our customers come from
                        # """
                        # ),
                        # html.Br(),
                        # html.P(
                        #     """
                        #     What and how much their customers are ordering
                        #     Can we segment customers into cohorts
                        #     RFM
                        #     Market Basket
                        #     """
                        # ),
                        #
                        # html.Br(),
                        # html.P(
                        #     """
                        #     What is the top/bottom 5 products and their suppliers
                        #     What suppliers provide the majority of the products that OList supplies
                        #     """
                        # ),

                    ],
                    width=6,
                ),

                dbc.Col(
                    children=[
                        dcc.Loading(
                            html.Img(
                                id='hero-img',
                                alt='Olist ',
                                className='img-fluid mb-3 img-responsive',
                                src='https://valorcapitalgroup.com/wp-content/uploads/2020/06/case_study_4_olist_1.jpg',
                                title='Tiago Dalvi, the founder and CEO of Olist.',
                                width="80%"
                            ),
                            type='dot',
                            color="AQUAMARINE",
                        ),
                        dcc.Loading(
                            html.Img(
                                id='hero-img',
                                alt='Olist ',
                                className='img-fluid mb-3 img-responsive',
                                src='https://techcrunch.com/wp-content/uploads/2021/04/Olist-HQ-in-Brazil-1.jpg',
                                title='OList office entrance at night.',
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

                        # html.Img(
                        #     id='hero-img-2',
                        #     alt='Olist ',
                        #     className='img-fluid',
                        #     src='https://officesnapshots.com/wp-content/uploads/2021/10/olist-offices-curitiba-700x700-compact.jpg',
                        #     title='OList Offices.',
                        #     # width="100%"
                        # ),
                    ],
                    width=6,
                ),
            ]
        ),

        # Quick Facts about the Brazilian economy at during the same time that our dataset is for.
        dbc.Row(
            children=[
                html.Br(),
                html.H2("Brazil - Order and Progress.", className="display-2"),
                html.Br(),
                dcc.Loading(
                    html.Img(
                        # id='hero-img',
                        alt='Christ the Redeemer Looking over Rio De Janerio and the Sugar Loaf Mountains',
                        className='img-fluid mb-3 img-responsive',
                        src='https://i.natgeofe.com/k/33e48abd-f2e7-4430-b7bf-cc9a18c14cc6/brazil-christ-the-redeemer_2x1.jpg',
                        title='Christ the Redeamer Looking over Rio De Janerio',
                        width="80%",
                        height="12.5rem",
                    ),
                    type='dot',
                    color='AQUAMARINE'
                ),
                html.Br(),
                html.P(
                    """
                    Brazil is the 5th largest country in the world, and has a population north of 210 million people. It occupies
                    almost half of South America's total land mass, and is dissected by both the Equator, and the Tropic of Capricorn. 
                    This makes Brazil an ideal place for beautiful tropical weather most of the time, as well as the ideal 
                    place for growing Coffee, Soy, and other tropic environment loving exports. 
                    """
                ),
                # html.Br(),
                # html.H5("A look at 2016-2018", className="display-5"),
                html.Br(),
                html.P(
                    """
                    Brazil is considered an emerging world power and has the 12th largest Gross Domestic Product(GDP)
                     in the world as well as the largest GDP in all of Latin America. They are also the world's 10th 
                     largest consumer of energy, however much of that energy is produced
                      from renewable sources, such as hydroelectricity and ethanol.
                    """
                ),
                html.Br(),
                # html.H5("A look at 2016-2018", className="display-5"),
                html.Br(),
                dbc.Col(
                    children=[

                        # Source - https://en.wikipedia.org/wiki/Brazil#Economy
                        # html.P(
                        #     """
                        #     Brazil is the 5th Largest Country in the world, and has a population North of 210 million people. It occupies
                        #     almost half of South America's total land mass and is dissected by both the Equator and the Tropic of Capricorn.
                        #     This makes Brazil an ideal place for tropical weather and sunshine.
                        #
                        #     """
                        # ),
                        # html.Br(),
                        html.P(
                            """
                            The capital city of Brazil is Brasilia and is where all three branches of the Brazilian government are located. 
                            It was founded in April 1960 by President Juscelino Kubitschek, with the intention to have the capital in a more 
                            central location. Brasilia, is estimated to be the third most populous city in Brazil.
                            """),
                        html.Br(),
                        dcc.Loading(
                            dcc.Graph(
                                id='brazil-population-map',
                                animate=True,
                                # responsive=True,
                            ),
                            type='dot',
                            color='AQUAMARINE',
                        ),
                        html.Br(),
                        html.P(
                            """                            
                            The largest cities are Sao Paulo, Rio de Janerio, and Brasilia.\nThe  most, 
                            populous city is Sao Paulo, with an estimated population of 12 million people.
                            Brazil borders all countries in South America expect for Chile and 
                            Equador, accouting for 47.8% of the land mass in South America.
                            """
                        ),
                        html.Br(),

                        dcc.Loading(
                            html.Img(
                                # id='hero-img',
                                alt='Brazilians in a busy street heading to work from the Phiadelphia Inquirer',
                                className='img-fluid mb-3 img-responsive',
                                src='https://cloudfront-us-east-1.images.arcpublishing.com/pmn/VTOYS5GQXNFNNHE2FEO7QFCG2A.jpg',
                                title='Brazilians in a busy street heading to work',
                                width="80%",
                                height="12.5rem",
                            ),
                            type='dot',
                            color='AQUAMARINE'
                        ),
                        html.Br(),
                        html.P(
                            """
                            Brazil's official language is Portuguese. It's culture is also mainly derived in Portuguese roots, 
                             however Brazil is one of the most 
                            multicultural and ethnically diverse nations in the world due to over a century of mass immigration
                            from a variety of countries. 
                            """
                        ),

                        html.Br(),
                        html.H3("Brazil's Economy.", className="display-3"),
                        html.Br(),
                        html.P(
                            children=["""
                        Brazil is has the 9th largest economy in the world, and is the largest economy in all of Latin 
                        America.
                         
                         They have a labor force of about 107 million, and an unemployment rate that hovers around 6.2%.
                        The industrial sector in Brazil accounts for about a third of overall""",
                            dcc.Link(children=["GDP"], href="https://www.investopedia.com/terms/g/gdp.asp",),
                            """
                            production.
                            the majority of Brazil's industrial sector is housed in the south and the southeast of the country.
                            They also have a sophisticated services and financial servicing industries as well.
                            """]),
                        html.Br(),
                        dcc.Loading(
                            dcc.Graph(
                                id='brazil-gdp-chart',
                                animate=True,
                                responsive=True,
                            ),
                            # html.Img(
                            #     # id='hero-img',
                            #     alt='Map of Brazil'
                            #         ' and city of Rio De Janerio during the day.',
                            #     className='img-fluid mb-3 img-responsive',
                            #     src='https://www.worldatlas.com/r/w960-q80/upload/db/df/33/br-01.png',
                            #     title='Map of Brazil from the World Atlas',
                            #     width="80%",
                            #     height="12.5rem",
                            # ),
                            type='dot',
                            color='AQUAMARINE',
                        ),
                        html.Br(),
                        # Source - https://en.wikipedia.org/wiki/Brazil#Economy

                        html.Br(),
                        dcc.Loading(
                            html.Img(
                                # id='hero-img',
                                alt='A coffee producer in Cerrado, Brazil from Comunicaffe.com',
                                className='img-fluid mb-3 img-responsive',
                                src='https://www.comunicaffe.com/wp-content/uploads/2017/01/Brasile-Cerrado-e1659340569121.jpg',
                                title='Coffee Producer',
                            ),
                            type='dot',
                            color='AQUAMARINE',
                        ),
                        html.Br(),

                        html.P("""
                        
                        For the last 150 years Brazil has been the largest exporter of Coffee in the world. They are also
                        major exporters of soy, iron ore, pulp (cellulose) to name a few. The national currency is the 
                        Brazilian Real and they have an overall GDP around $1.75 trillion dollars.
                        """
                               ),
                        html.Br(),
                        dcc.Loading(
                            html.Img(
                                # id='hero-img',
                                alt='A view with Sugar Loaf Mountain overlooking the bay,'
                                    ' and city of Rio De Janerio during the day.',
                                className='img-fluid mb-3 img-responsive',
                                src='https://www.icrc.org/sites/default/files/styles/amp_thumbnail_image_1-1/public/document/image_thumbnail/brasil-migrantes_se_beneficiam_de_acesso_a_agua_pelo_cicv_na_igreja_batista_em_pacaraima__0.jpg?itok=_J_iD7t1',
                                title='Rio De Janerio',
                                # width="100%"
                            ),
                            type='dot',
                            color='AQUAMARINE',
                        ),
                        html.Br(),
                        # Source - https://countryeconomy.com/national-minimum-wage/brazil
                        # Source - http://www.xinhuanet.com/english/2017-03/08/c_136110450.htm
                        html.P(
                            """
                                In 2016 Brazil started the year in a recession with GDP that fell 3.6%. This was the 
                                first time in history that Brazil seen two years of negative growth since 1931.
                                In 2017 the economy rebounded and grew by 1.0%, and in 2018 the economy again expanded
                                by 1.1%.
                            """),

                        html.Br(),
                        dcc.Graph(
                            id='brazil-nmw-chart',
                            animate=True,
                            responsive=True,
                        ),
                        html.Br(),

                        html.P("""
                                
                                The Minimum wage in Brazil in 2016 is 880 Brazilian Reals, or about $252.10 \n
                                By 2018, the minimum wage would rise to 954 Brazilian Reals, or about $261.10.
                                This is an increase of 8.2% over two years.
                            """
                               ),

                        html.P(
                            [
                                """
                            Many Brazilian's are price-sensitive and that is due in part to the 2016 recession
                            that the country experienced. Before the recession Luxury spending was a norm, 
                            however now, according to RWS.com 'It’s the norm to shop at discount chains, 
                            atacarejos (stores that combine retail and wholesale) and retailers 
                            selling luxury products at the lowest price'.Check out the 
                            """,
                                dcc.Link("Customers", href='http://127.0.0.1:8050/customer-analysis'),
                                """
                                or the 
                                """,
                                dcc.Link("Marketing", href='http://127.0.0.1:8050/marketing-analysis'),
                                """ For more information."""
                            ]
                        ),
                        html.Br(),
                        html.P(
                            """
                            Brazil has also become one of the largest eCommerce markets in the world, with around 
                            51% of shoppers regularly purchasing online. There is little threat from Amazon 
                            currently since they are fairly new in the market, which is good for OList. 
                            The most common payment methods in Brazil are payments, and installments, allowing 
                            lower income families to afford better quality goods and services. 
                            """
                        )

                    ],
                    width=12,
                ),
            ],

        )

    ]
)


@callback(
    Output('brazil-population-map', 'figure'),
    Input('data-store', 'data')
)
def update_population_map(data):
    import unidecode

    dff = pd.read_csv('./data/external/brazilian_population_2010_2020.csv')
    geo_df = pd.read_csv('./data/customers_geo_data.csv')

    geo_json_file = open("./data/external/brazil_geo.json")
    geojson = json.load(geo_json_file)

    dff['code'] = "BRA"
    # Done to remove special characters from the city and state names
    dff['City'] = dff.City.apply(lambda x: unidecode.unidecode(x).lower())
    dff['State'] = dff.State.apply(lambda x: unidecode.unidecode(x).lower())
    dff.rename(columns={"City": "geolocation_city", "State": "geolocation_state"}, inplace=True)
    # combine geolocation data with population
    geo_df = geo_df[['geolocation_city', 'geolocation_state',
                     'zip_code', 'geolocation_lat', 'geolocation_lng']]
    dff = dff.merge(geo_df,
                    how='left', on='geolocation_city').drop_duplicates(subset='geolocation_city')

    dff['2021_scaled'] = np.log10(dff['2021'])
    dff['2010_scaled'] = np.log10(dff['2010'])

    # Creating the Hover Text for this map.
    def create_text(x):
        text = "{} had a population of {:,.2f} people in 2020.\nThe most recent census has the population at {:,.2f} people in 2021." \
               "\nThat is a {:.2%} change overall.".format(
            x['geolocation_state_y'],
            x['2010'],
            x['2021'],
            x['Change'],
        )
        return text

    # Creating hover text based of columns in dataframe for the map, don't forget axis=1 to go row by row.
    dff['hover_text'] = dff.apply(
        lambda x: create_text(x), axis=1)

    pop_map = pg_utils.create_px_choropleth(dff, geojson, 'geolocation_state_y', '2021_scaled',
                                            {
                                                'geolocation_state_y': False,
                                                'hover_text': True,
                                                '2021_scaled': False,
                                            }, dff['2021'].mean())

    # pop_map.update_layout(
    #
    # )

    return pop_map


@callback(
    Output('brazil-gdp-chart', 'figure'),
    Input('data-store', 'data')
)
def update_brazil_economic_chart(data):
    dff = pd.read_csv('./data/external/brazil_gdp_vs_neighbors_2021.csv')

    print("Year has a type of {}\nGDP Columns have a type of{}".format(type(dff['Year'][0]), type(dff['GDP-BRA'][0])))

    for col in dff:
        colType = type(dff[col][0])
        if colType == np.float64:
            dff[col] = dff[col] / 100

    economic_chart_fig = go.Figure()
    economic_chart_fig.add_trace(
        go.Scatter(
            x=dff['Year'],
            y=dff['GDP-BRA'],
            name='BRA',
            opacity=1,
            mode='lines',
            line=dict(
                color="#42403f",
                width=4,
            ),
            hovertemplate="%{y:,.2%}",
        )
    )

    df_2016 = dff[dff['Year'] == 2016]
    df_2017 = dff[dff['Year'] == 2017]
    df_2018 = dff[dff['Year'] == 2018]

    # Adding Markers for Years of interest.
    economic_chart_fig.add_trace(
        go.Scatter(
            x=[df_2016['Year'].values[0], df_2017['Year'].values[0], df_2018['Year'].values[0]],
            y=[df_2016['GDP-BRA'].values[0], df_2017['GDP-BRA'].values[0], df_2018['GDP-BRA'].values[0]],
            mode='markers',
            marker=dict(
                color='#42403f',
                size=12,
            ),
            name='Yrs. of Interest',
            hovertemplate="%{y:,.2%}",
            visible='legendonly',
        )
    )

    # Removing Brazil from dataframe to create comparisons with neighbors
    dff = dff.drop(columns=['GDP-BRA'])

    for country_gdp in dff.columns:
        if country_gdp == 'Year':
            pass
        else:
            economic_chart_fig.add_scatter(
                x=dff['Year'],
                y=dff[country_gdp],
                name=country_gdp[4:],
                opacity=.2,
                hovertemplate="%{y:,.2%}",
            )

    # economic_chart_fig.add_scatter(
    #     x=dff['Year'],
    #     y=dff['GDP-COL'],
    #     name='Columbia',
    #     opacity=.2,
    #     hovertemplate="%{y:,.2%}",
    # )
    #
    # economic_chart_fig.add_scatter(
    #     x=dff['Year'],
    #     y=dff['GDP-GUY'],
    #     name='Guyana',
    #     opacity=.2,
    #     hovertemplate="%{y:,.2%}",
    # )
    #
    # economic_chart_fig.add_scatter(
    #     x=dff['Year'],
    #     y=dff['GDP-PER'],
    #     name='Peru',
    #     opacity=.2,
    #     hovertemplate="%{y:,.2%}",
    # )
    #
    # economic_chart_fig.add_scatter(
    #     x=dff['Year'],
    #     y=dff['GDP-PRY'],
    #     name='Paraguay',
    #     opacity=.2,
    #     hovertemplate="%{y:,.2%}",
    # )
    #
    # economic_chart_fig.add_scatter(
    #     x=dff['Year'],
    #     y=dff['GDP-URY'],
    #     name='Uraguay',
    #     opacity=.2,
    #     hovertemplate="%{y:,.2%}",
    # )
    #
    # economic_chart_fig.add_scatter(
    #     x=dff['Year'],
    #     y=dff['GDP-VEN'],
    #     name='Venezula',
    #     opacity=.2,
    #     hovertemplate="%{y:,.2%}",
    # )
    #
    # economic_chart_fig.add_scatter(
    #     x=dff['Year'],
    #     y=dff['GDP-WLD'],
    #     name='World',
    #     opacity=.5,
    #     hovertemplate="%{y:,.2%}",
    # )

    economic_chart_fig.update_xaxes(
        title='Year'
    )

    economic_chart_fig.update_yaxes(
        title='GDP (%)'
    )

    economic_chart_fig.update_layout(
        title='Brazil GDP(%) vs Neighbors'
    )

    return economic_chart_fig


@callback(
    Output('brazil-nmw-chart', 'figure'),
    Input('data-store', 'data')
)
def update_brazil_nwm_chart(data):
    dff = pd.read_csv('./data/external/brazilian_nmw_data_2022.csv')
    economic_chart_fig = go.Figure()

    # year_df = dff[(dff['Year'] >= 2016) and (dff['Year'] <= 2018)]

    economic_chart_fig.add_scatter(
        x=dff['Year'],
        y=dff['NMW(Reals)'],
        name='BRL',
        fill='tozeroy',
        opacity=.8,
    )

    economic_chart_fig.add_scatter(
        x=dff['Year'],
        y=dff['NMW(Dollars)'],
        name="$",
        fill='tozeroy',
        # opacity=.8,
    )

    # Years of interest markers
    # economic_chart_fig.add_trace(
    #     go.Scatter(
    #         x=[year_df[year_df['Year'] == 2016].values[0], year_df[year_df['Year'] == 2018].values[0]],
    #         y=[year_df[year_df['NMW(Reals)'] == 2016]['NMW(Reals)'].values[0],
    #            year_df[year_df['Year'] == 2018]['NMW(Reals)'].values[0]],
    #         mode="markers",
    #         marker=dict(
    #             size=10,
    #         )
    #     )
    # )

    economic_chart_fig.update_yaxes(
        title="National Minimum Wage"
    )

    economic_chart_fig.update_xaxes(
        title="Year"
    )

    economic_chart_fig.update_layout(
        title='National Minimum Wage (BRL v $)'
    )

    return economic_chart_fig
