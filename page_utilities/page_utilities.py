from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.io as pio
from dash import dash_table

from sklearn.preprocessing import LabelEncoder

"""
This class helps by allowing the pages to share common 
chart and visualization components as well as helper 
functions 
"""


class PageUtilities:
    DIVERGING = pio.templates['atbAnalyticsGroupDefault'].layout.colorscale.diverging
    SEQUENTIAL = pio.templates['atbAnalyticsGroupDefault'].layout.colorscale.sequential

    def __init__(self):
        print("Page Utilities Initialized")

    # Taken from this answer on stack overflow. https://stackoverflow.com/questions/579310/formatting-long-numbers-as-strings/45846841#45846841
    def human_format(self, num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

    """

    Update all figure layouts for the provided figures

    """

    def create_standard_legend(self, figs):
        for fig in figs:
            fig.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-1.0,
                    xanchor="right",
                    x=1,
                    # bgcolor="#E4F2EF",
                    # title_text='Legend'
                ),
            )

    """
    
    Creating Indicator Figures that are mainly used in the KPI Cards for this application
    
    """

    def create_indicator_figure(self, value, delta, title, rows=1, cols=1, x=[0, 1], y=[0, 1], default=True,
                                monetary=False, percent=False):
        fig = make_subplots(rows=rows, cols=cols,
                            specs=[[{"secondary_y": True}]])

        prefix = " "
        suffix = " "
        valueFormat = "%{:,}"

        if monetary:
            prefix = "$"
            valueFormat = "%{:,.2f}"

        if default:
            prefix = " "

        if percent:
            suffix = "%"

        if delta > 0:
            delta = value

        fig.add_trace(
            go.Indicator(
                value=value,
                mode="number",  # number+delta
                delta={
                    'position': 'bottom',
                    # 'reference': delta,
                    'relative': True,
                    # "valueformat": valueFormat,
                    # "prefix": "$",
                    # "suffix": "m",
                },
                gauge={
                    'axis': {
                        'visible': False
                    }
                },
                number={
                    'font': {
                        'family': 'Bebas Neue',
                        'size': 36,
                    },
                    'prefix': f"{prefix}",
                    # 'valueformat': valueFormat,
                    'suffix': f"{suffix}"

                },
                title={
                    'text': f"{title}",
                    'align': 'center',
                    'font': {
                        'family': 'Bebas Neue',
                        'size': 48,
                    }
                },
                domain={
                    'x': x,
                    'y': y
                },
            ),
            # row=1,
            # col=1
        )

        return fig

    """
    
    Converting and getting the integers for date maths
    
    """

    def get_date_int(self, df, col):
        year = df[col].dt.year
        month = df[col].dt.month
        day = df[col].dt.day
        return year, month, day

    """
    
    Converting either a single column to a pd datetime like object, 
    or converting the provide list of columns to datetime like objects
    
    """

    def convert_to_datetime(self, df, col):
        if type(col) is list:

            for c in col:
                df[c] = pd.to_datetime(df[c],
                                       errors='coerce',
                                       infer_datetime_format=True)

        else:
            df[col] = pd.to_datetime(df[col],
                                     errors='coerce',
                                     infer_datetime_format=True)

    """
    
    Create Hover Text and Text columns that are used throughout various visualizations. 
    
    """

    def create_hover_text(self, df, col_name, text_to_show, cols_to_show):

        # Sub Routine to apply the text row by row.
        def create_text(x):
            cols_to_show_str = ""
            for col in cols_to_show:
                col = x + "." + col

            text = text_to_show.format(
                cols_to_show
            )

            return text

        df[col_name] = df.apply(
            lambda htext: create_text(htext),
            axis=1,
        )

        return df

    """

    Creating the User Selection card with a Dropdown
  

    """

    # TODO MAKE IT SO YOU CAN PASS A UI SELECTOR COMPONENT INSTEAD OF DEFAULT DROPDOWN
    def create_uis_card(self, classname='kpi-card', title="User Selection",
                        paragraph="User Makes selections below", ui_selection_id="select-component-id", ):

        return dbc.Card(
            dbc.CardBody(
                dcc.Loading(
                    children=[
                        html.H3(title),
                        html.Br(),
                        html.P(
                            paragraph
                        ),
                        dcc.Dropdown(
                            id=ui_selection_id,
                            multi=True,
                        ),
                    ],
                    type='dot',
                    color="AQUAMARINE",
                ),
            ),
            className=classname
        )

    """
    
    Creating the KPI card 
    
    """

    def create_kpi_card(self, graph_id, classname='kpi-card', title=None, paragraph=None):

        return dbc.Card(
            dbc.CardBody(
                dcc.Loading(
                    dcc.Graph(
                        id=f"{graph_id}",
                        responsive=True,
                        animate=True,
                    ),
                    type='dot',
                    color="AQUAMARINE",
                )
            ),
            className=classname
        )

    """
        Create Choropleth Map
        Need to provide both a dataframe and the geojson.
    
    """

    def create_px_choropleth(self, dff, geojson, locations, color, hover_data, color_continuous_midpoint):

        DIVERGING = pio.templates['atbAnalyticsGroupDefault'].layout.colorscale.diverging
        SEQUENTIAL = pio.templates['atbAnalyticsGroupDefault'].layout.colorscale.sequential

        map = go.Figure()
        map.add_trace(
            go.Choropleth(
                locations=dff[locations],
                geojson=geojson,
                z=dff[color].astype(float),
                # featureidkey='geojson.features.geometry.coordinates',  # property of geoJSON file
                locationmode='geojson-id',
                colorscale=DIVERGING,
                autocolorscale=False,
                # text=dff[hover_data],  # hover text
                hovertemplate=dff[hover_data],
                # marker_line_color='white',  # line markers between states
                # colorbar_title="Millions USD",
                # showscale=False,
            )
        )

        # map = px.choropleth(dff,
        #                     locations=locations,
        #                     geojson=geojson,
        #                     color=color,
        #                     # featureidkey= "features.properties.geometry.coordinates",
        #                     # hover_name=hover_data,
        #                     # hover_data=f"{hover_data}",  # Must be a list of columns or a string
        #                     color_continuous_scale=DIVERGING,
        #                     color_continuous_midpoint=color_continuous_midpoint
        #                     )

        map.update_geos(
            fitbounds="geojson",  # False | "locations" | "geojson"
            visible=False,
            resolution=110,
            showland=True,
            showocean=True,
            showlakes=True,
            showrivers=True,
            showcountries=True,
            showsubunits=True,
            showframe=False,
            showcoastlines=True,
            landcolor='#FEFFF1',
            countrycolor='#333333',
            oceancolor='#E4F2EF',
            lakecolor='#E4F2EF',
            rivercolor='#E4F2EF',
            subunitcolor="#42403f",
            # projection_type='orthographic',
            # scope='world', # 'africa', 'asia', 'europe', 'north america', 'south america', 'usa', 'world'
            lataxis_showgrid=True,
            lonaxis_showgrid=True
        )

        map.update_layout(
            height=500,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            showlegend=False,
        )

        return map

    # TODO figure out how to create this with the go.Mapbox instead
    """"
    Creating plotly px.mapbox Figures 
   
    
    """

    def create_px_mapbox(self, dff, color, size, title, color_rng_max, labels={}, mapbox_style='stamen-terrain'):

        color_rng_max = dff['payment_value'].quantile(0.95)

        map_fig = px.scatter_mapbox(dff,
                                    labels=labels,
                                    # {
                                    #     'payment_value': 'Tot Amt Sold'
                                    # },
                                    lat='geolocation_lat',
                                    lon='geolocation_lng',
                                    color=color,  # can be int, or a numeric series in dff
                                    zoom=2,
                                    # width=1200,
                                    height=500,
                                    size=size * 5,  # can be int, or a numeric series in dff
                                    size_max=50,
                                    # title='Merchant Locations',
                                    # hover_name='seller_id',
                                    hover_data=[dff['customer_unique_id'], dff['customer_city'],
                                                dff['payment_value']],

                                    # For this use  dff['payment_value'].quantile(0.95)
                                    range_color=[0, color_rng_max],  # To negate ouliers
                                    color_continuous_scale=self.SEQUENTIAL,
                                    center={
                                        'lat': dff.geolocation_lat.mode()[0],
                                        'lon': dff.geolocation_lng.mode()[0]
                                    },
                                    # text="Customer has paid a total of " + str(dff.payment_value)
                                    )
        map_fig.update_mapboxes(
            bearing=2,
            pitch=10,
        )
        map_fig.update_layout(
            mapbox_style=mapbox_style,
            mapbox_layers=[
                #             {
                #                 "below": 'traces',
                #                 "sourcetype": "raster",
                #                 "source": [
                #                     "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                #                 ]
                #             }

                {"below": 'traces',
                 'sourcetype': 'vector',
                 "source": ["http://openmaptiles.org/tilejson.json"]
                 }

            ],
            margin={"r": 20, "t": 50, "l": 20, "b": 20},
            title=title,
            hoverlabel=dict(
                bgcolor="#E4F2EF",
                bordercolor="#709784",
            )
        )
        return map_fig

    """
    
    Creating plotly px.scattergeo Figures
    
    """

    def create_px_scattergeo(self, dff):
        pass

    """
    
    Creating a Go ScatterGeo Map
    
    """

    def create_scattergeo_map(self, geojson, lat, lon, locations, color, hover_data):
        cmin = 0
        cmax = 100

        if color is not None:
            cmax = color.max() * .95
            cmin = color.min()

        # Create initial ScatterGeo Graph
        map_fig = go.Figure(
            go.Scattergeo(
                geojson=geojson,
                locations=locations,
                locationmode='geojson-id',
                lat=lat.astype(float),
                lon=lon.astype(float),
                mode="markers",
                marker=dict(
                    color=color,
                    colorscale=self.DIVERGING,
                    opacity=.85,
                    cmin=cmin,
                    cmax=cmax,
                    size=5,
                    colorbar=dict(
                        thickness=10,
                        titleside="right",
                        outlinecolor="rgba(68, 68, 68, 0)",  # #42403f
                        # tickvals=[-50, -30, -15, 0, 15, 30, 50],
                        ticks="outside",
                        ticklen=3,
                        # ticksuffix=" C",
                        showticksuffix="all"
                    )
                ),
                text=hover_data
            )
        )

        # Create Hover Text.

        map_fig.update_geos(
            fitbounds='geojson',  # False | "locations" | "geojson"
            #         resolution=110,
            # 'world', 'usa', 'europe', 'asia', 'africa', 'north america', 'south america'
            scope='world',
            # 'equirectangular', 'mercator', 'orthographic', 'natural earth',
            # 'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', \
            # 'azimuthal equidistant', 'conic equal area', 'conic conformal',
            # 'conic equidistant', 'gnomonic', 'stereographic', 'mollweide',
            # 'hammer', 'transverse mercator', 'albers usa', 'winkel tripel',
            # 'aitoff' and 'sinusoidal'
            projection_type='orthographic',
            projection_rotation=dict(lat=lat.mode()[0],
                                     lon=lon.mode()[0],
                                     roll=5,
                                     ),
            showland=True,
            showocean=True,
            showlakes=True,
            showrivers=True,
            showcountries=True,
            showframe=True,
            showcoastlines=True,
            landcolor='#FEFFF1',
            countrycolor='#333333',
            oceancolor='#E4F2EF',
            lakecolor='#E4F2EF',
            rivercolor='#E4F2EF',
            showsubunits=True,
            subunitcolor="Blue",
            center=dict(
                lat=lat.mode()[0],
                lon=lon.mode()[0]
            ),
            # text=["Customer:" + dff['customer_unique_id'] + " paid an amount of " + str(dff['payment_value'])],
        )
        return map_fig

    """
    
    Create Generic Dash Table
    
    """

    def generate_generic_dash_datatable(self, dataframe, id, tooltip_data=None, tooltip_header=None):

        # columns = [{"name": i, "id": i, 'type': 'numeric', 'format': FormatTemplate.money(2)} for i in
        #            dataframe.columns]  # for when the column names can change

        if tooltip_data is None:
            tooltip_data = []

        if tooltip_header is None:
            tooltip_header = {}
        columns = [{"name": i, "id": i} for i in
                   dataframe.columns]

        return dash_table.DataTable(
            id=id,
            columns=columns,
            data=dataframe.to_dict('records'),
            # fixed_rows={'headers': True},
            filter_action='native',
            row_selectable="multi",
            selected_rows=[],
            selected_columns=[],
            sort_action="native",
            sort_mode="multi",
            style_header={
                'backgroundColor': '#709784',
                'fontWeight': 'bold',
                'font-style': 'Montserrat',
            },
            style_cell={
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 0,
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'backgroundColor': '#FEFFF1'
            },
            style_table={
                'height': '400px',
                'overflowY': 'auto'
            },
            style_as_list_view=True,
            tooltip_delay=0,
            tooltip_duration=None,
            tooltip_header=tooltip_header,
            tooltip_data=tooltip_data,
            page_action="native",
            page_current=0,
            page_size=25,
            export_format='csv'
        )

    """
        
        Create user selection card group
        
    """

    # TODO make this dynamic
    def create_user_selection_card_group(self):

        return dbc.Col(
            html.Div(
                children=[
                    dbc.Card(
                        dbc.CardBody(
                            children=[
                                html.H3("Top n Value Selector", className='text-center'),
                                html.P(
                                    "Select a value to see the our customers Top/Bottom "
                                    "ordered product categories are."),
                                html.Br(),
                                dcc.Slider(
                                    id='cs-n-slider',
                                    min=0,
                                    max=50,
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
        )

    """
    
    Turn Categorical Variables into Numeric, can be used for colorscaling features
    for scaling features for ml etc.
    
    """

    def convert_categorical_to_numeric(df, col_to_change):
        # Creating a instance of label Encoder.
        le = LabelEncoder()

        # Using .fit_transform function to fit label
        # encoder and return encoded label
        if col_to_change is list:
            for col in col_to_change:
                label = le.fit_transform(df[col])
                print(label)
        else:
            label = le.fit_transform(df[col_to_change])
            print(label)

    def create_cohort_analysis(self, df, groupby_col='customer_unique_id', agg_val=pd.Series.nunique, ):
        # Convert index to a datetime so it will filter properly.
        self.convert_to_datetime(df, 'cohort_month')
        # df['cohort_month'] = df.cohort_month.dt.date()

        cohort_df = df.groupby(['cohort_month', 'cohort_index'])[groupby_col].apply(agg_val).reset_index()
        # Create Cohort Count Pivot Table
        cohortGrouping_counts = cohort_df.pivot(index='cohort_month', columns='cohort_index',
                                                values=groupby_col)
        print("The Cohort Counts for {} are :\n".format(groupby_col), cohortGrouping_counts)

        cohort = cohortGrouping_counts.iloc[:, 0]
        retention = cohortGrouping_counts.divide(cohort, axis=0)
        retention = retention.round(3) * 100

        print("The Retention Counts for {} are :\n".format(groupby_col), retention)

        return cohortGrouping_counts, retention

    def create_cohort_retention(self, cohortGrouping_counts, ):
        # Calculating Cohort Retention Rates amoung the cusotmers.
        # #TODO turn this into a function that takes 3 col name parameters
        total_cohort = cohortGrouping_counts.iloc[:, 0]
        retention_cohort = cohortGrouping_counts.divide(total_cohort, axis=0)
        retention_cohort.round(2) * 100
        print(retention_cohort)

        return retention_cohort

    def create_cohort_avg_price(self, df, ):
        # Calculating Cohort Average Payment Value
        # #TODO turn this into a function that takes 3 col name parameters
        avg_price_cohortGrouping = df.groupby(['cohort_month', 'cohort_index'])
        avg_price_cohortGrouing_df = avg_price_cohortGrouping['payment_value'].mean().reset_index()
        avg_price_cohort = avg_price_cohortGrouing_df.pivot(
            index='cohort_month',
            columns='cohort_index',
            values='payment_value'
        ).round(1)
        print(avg_price_cohort)

        return avg_price_cohort
