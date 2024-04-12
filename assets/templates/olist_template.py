import plotly.graph_objects as go
import plotly.io as pio

# Theme Colors
WHITE = '#FFFFFF'
BLACK = '#000000'
GAINSBORO = '#DBDBDB'

PERSIAN_BLUE = '#1c39bb'
ALICE_BLUE = '#F3F7FF'
MISTY_ROSE = '#fbe4e0'
SOLITUDE = '#e6eeff'
GRAY = '#808080'  # This is actually a dark version for Aquamarine and a light version for DarkSlateGreen
PAUA = '#312f4f'
WAIKAWA_GRAY = '#696D8C'

# Default Font and  Heading Sizes
FONT_1 = 'Noto Sans'  # Heading Type
FONT_2 = 'Noto Sans Bold'  # Heading Type
FONT_3 = 'Noto Sans'  # Main body type

TITLE_SIZE = 30
FONT_SIZE = 16

"""
Use this to assign colors to specific values. A for example could be Sales, and B could be Expenses. Add new entries
as needed. This is only if you know the names ahead of time.
"""
COLORS_MAPPER = {
    "A": "#38BEC9",
    "B": "#D64545"
}

pio.templates["olist_template"] = go.layout.Template(
    # LAYOUT
    # {
    #     'annotationdefaults': {'arrowcolor': '#2a3f5f', 'arrowhead': 0, 'arrowwidth': 1},
    #     'autotypenumbers': 'strict',
    #     'coloraxis': {'colorbar': {'outlinewidth': 0, 'ticks': ''}},
    #     'colorscale': {'diverging': [[0, '#8e0152'], [0.1, '#c51b7d'], [0.2,
    #                                  '#de77ae'], [0.3, '#f1b6da'], [0.4, '#fde0ef'],
    #                                  [0.5, '#f7f7f7'], [0.6, '#e6f5d0'], [0.7,
    #                                  '#b8e186'], [0.8, '#7fbc41'], [0.9, '#4d9221'],
    #                                  [1, '#276419']],
    #                    'sequential': [[0.0, '#0d0887'], [0.1111111111111111,
    #                                   '#46039f'], [0.2222222222222222, '#7201a8'],
    #                                   [0.3333333333333333, '#9c179e'],
    #                                   [0.4444444444444444, '#bd3786'],
    #                                   [0.5555555555555556, '#d8576b'],
    #                                   [0.6666666666666666, '#ed7953'],
    #                                   [0.7777777777777778, '#fb9f3a'],
    #                                   [0.8888888888888888, '#fdca26'], [1.0,
    #                                   '#f0f921']],
    #                    'sequentialminus': [[0.0, '#0d0887'], [0.1111111111111111,
    #                                        '#46039f'], [0.2222222222222222, '#7201a8'],
    #                                        [0.3333333333333333, '#9c179e'],
    #                                        [0.4444444444444444, '#bd3786'],
    #                                        [0.5555555555555556, '#d8576b'],
    #                                        [0.6666666666666666, '#ed7953'],
    #                                        [0.7777777777777778, '#fb9f3a'],
    #                                        [0.8888888888888888, '#fdca26'], [1.0,
    #                                        '#f0f921']]},
    #     'colorway': [#636efa, #EF553B, #00cc96, #ab63fa, #FFA15A, #19d3f3, #FF6692,
    #                  #B6E880, #FF97FF, #FECB52],
    #     'font': {'color': '#2a3f5f'},
    #     'geo': {'bgcolor': 'white',
    #             'lakecolor': 'white',
    #             'landcolor': '#E5ECF6',
    #             'showlakes': True,
    #             'showland': True,
    #             'subunitcolor': 'white'},
    #     'hoverlabel': {'align': 'left'},
    #     'hovermode': 'closest',
    #     'mapbox': {'style': 'light'},
    #     'paper_bgcolor': 'white',
    #     'plot_bgcolor': '#E5ECF6',
    #     'polar': {'angularaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''},
    #               'bgcolor': '#E5ECF6',
    #               'radialaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''}},
    #     'scene': {'xaxis': {'backgroundcolor': '#E5ECF6',
    #                         'gridcolor': 'white',
    #                         'gridwidth': 2,
    #                         'linecolor': 'white',
    #                         'showbackground': True,
    #                         'ticks': '',
    #                         'zerolinecolor': 'white'},
    #               'yaxis': {'backgroundcolor': '#E5ECF6',
    #                         'gridcolor': 'white',
    #                         'gridwidth': 2,
    #                         'linecolor': 'white',
    #                         'showbackground': True,
    #                         'ticks': '',
    #                         'zerolinecolor': 'white'},
    #               'zaxis': {'backgroundcolor': '#E5ECF6',
    #                         'gridcolor': 'white',
    #                         'gridwidth': 2,
    #                         'linecolor': 'white',
    #                         'showbackground': True,
    #                         'ticks': '',
    #                         'zerolinecolor': 'white'}},
    #     'shapedefaults': {'line': {'color': '#2a3f5f'}},
    #     'ternary': {'aaxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''},
    #                 'baxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''},
    #                 'bgcolor': '#E5ECF6',
    #                 'caxis': {'gridcolor': 'white', 'linecolor': 'white', 'ticks': ''}},
    #     'title': {'x': 0.05},
    #     'xaxis': {'automargin': True,
    #               'gridcolor': 'white',
    #               'linecolor': 'white',
    #               'ticks': '',
    #               'title': {'standoff': 15},
    #               'zerolinecolor': 'white',
    #               'zerolinewidth': 2},
    #     'yaxis': {'automargin': True,
    #               'gridcolor': 'white',
    #               'linecolor': 'white',
    #               'ticks': '',
    #               'title': {'standoff': 15},
    #               'zerolinecolor': 'white',
    #               'zerolinewidth': 2}
    # }
    layout={
        # Fonts
        # Note - 'family' must be a single string, NOT a list or dict!
        'title':
            {'font': {
                'family': f'{FONT_1}, {FONT_2}, Helvetica, Sans',
                'size': TITLE_SIZE,
                'color': BLACK
            },
            },
        'font': {
            'family': f'{FONT_3}, Helvetica Neue, Helvetica, Sans',
            'size': FONT_SIZE,
            'color': BLACK,
        },
        # Coloring
        'coloraxis': {
            'colorbar': {
                'outlinewidth': 0,
                'ticks': '',
            }
        },
        'colorscale': {
            'diverging': [
                [0, '#696D8C'],
                [0.1, '#787994'],
                [0.2, '#86859D'],
                [0.3, '#9591A5'],
                [0.4, '#A39DAE'],
                [0.5, '#B2A9B6'],
                [0.6, '#C1B4BE'],
                [0.7, '#CFC0C7'],
                [0.8, '#DECCCF'],
                [0.9, '#ECD8D8'],
                [1, '#FBE4E0']
            ],
            # 'diverging': [
            #     [0, '#CFA42F'],
            #     [0.1, '#CAA83C'],
            #     [0.2, '#C5AC4A'],
            #     [0.3, '#BFB157'],
            #     [0.4, '#BAB565'],
            #     [0.5, '#B5B972'],
            #     [0.6, '#B0BD7F'],
            #     [0.7, '#ABC18D'],
            #     [0.8, '#A5C69A'],
            #     [0.9, '#A0CAA8'],
            #     [1, '#9BCEB5']
            # ],
            # 'diverging': [
            #     [0, '#388895'],
            #     [0.1, '#428F98'],
            #     [0.2, '#4C969B'],
            #     [0.3, '#569D9F'],
            #     [0.4, '#60A4A2'],
            #     [0.5, '#6AABA5'],
            #     [0.6, '#73B2A8'],
            #     [0.7, '#7DB9AB'],
            #     [0.8, '#87C0AF'],
            #     [0.9, '#91C7B2'],
            #     [1, '#9BCEB5']
            # ],

            'sequential': [
                [0.0, '#1C39BB'],
                [0.1111111111111111, '#304BC2'],
                [0.2222222222222222, '#445DC9'],
                [0.3333333333333333, '#596FCF'],
                [0.4444444444444444, '#6D81D6'],
                [0.5555555555555556, '#8194DD'],
                [0.6666666666666666, '#95A6E4'],
                [0.7777777777777778, '#A9B8EB'],
                [0.8888888888888888, '#BECAF1'],
                [1.0, '#E6EEFF']
            ],
            'sequentialminus': [
                [0.0, '#1C39BB'],
                [0.1111111111111111, '#445DC9'],
                [0.2222222222222222, '#596FCF'],
                [0.3333333333333333, '#6D81D6'],
                [0.4444444444444444, '#8194DD'],
                [0.5555555555555556, '#95A6E4'],
                [0.6666666666666666, '#A9B8EB'],
                [0.7777777777777778, '#BECAF1'],
                [0.8888888888888888, '#D2DCF8'],
                [1.0, '#E6EEFF']
            ],

        },


        'colorway': [
            WAIKAWA_GRAY,
            PAUA,
            PERSIAN_BLUE,
            GRAY,
            ALICE_BLUE,
            SOLITUDE,
            MISTY_ROSE,
        ],
        # Keep adding others as needed below
        'hovermode': 'closest',
        'hoverdistance': 100,
        'spikedistance': 1000,
        'paper_bgcolor': WHITE,
        'plot_bgcolor': WHITE,
        'xaxis': {
            'automargin': True,
            'gridcolor': GAINSBORO,
            'linecolor': GRAY,
            'ticks': '',
            'title': {
                'standoff': 15
            },
            'zerolinecolor': GAINSBORO,
            'zerolinewidth': 2,
            'showspikes': True,
            'spikethickness': 2,
            'spikedash': "dot",
            'spikecolor': "#999999",
            'spikemode': "across",

        },
        'yaxis': {
            'automargin': True,
            'gridcolor': GAINSBORO,
            'linecolor': GRAY,
            'ticks': '',
            'title': {
                'standoff': 15
            },
            'zerolinecolor': GAINSBORO,
            'zerolinewidth': 2,
            'showspikes': True,
            'spikethickness': 2,
            'spikedash': "dot",
            'spikecolor': "#999999",
            'spikemode': "across",
        },

    },
    # DATA
    data={
        # Each graph object must be in a tuple or list for each trace

        #
        # 'sequentialGoldAqua':
        # [
        #     [0.0, '#CFA42F'],
        #     [0.1111111111111111, '#CAA83C'],
        #     [0.2222222222222222, '#C5AC4A'],
        #     [0.3333333333333333, '#BFB157'],
        #     [0.4444444444444444, '#BAB565'],
        #     [0.5555555555555556, '#B5B972'],
        #     [0.6666666666666666, '#B0BD7F'],
        #     [0.7777777777777778, '#ABC18D'],
        #     [0.8888888888888888, '#A5C69A'],
        #     [1.0, '#9BCEB5']
        # ],
        # 'sequentialSlateGreenAqua':
        #     [
        #         [0.0, '#CFA42F'],
        #         [0.1111111111111111, '#CAA83C'],
        #         [0.2222222222222222, '#C5AC4A'],
        #         [0.3333333333333333, '#BFB157'],
        #         [0.4444444444444444, '#BAB565'],
        #         [0.5555555555555556, '#B5B972'],
        #         [0.6666666666666666, '#B0BD7F'],
        #         [0.7777777777777778, '#ABC18D'],
        #         [0.8888888888888888, '#A5C69A'],
        #         [1.0, '#9BCEB5']
        #     ],

        # {
        #     'bar': [{'error_x': {'color': '#2a3f5f'},
        #              'error_y': {'color': '#2a3f5f'},
        #              'marker': {'line': {'color': '#E5ECF6', 'width': 0.5},
        #                         'pattern': {'fillmode': 'overlay', 'size': 10, 'solidity': 0.2}},
        #              'type': 'bar'}],
        #     'barpolar': [{'marker': {'line': {'color': '#E5ECF6', 'width': 0.5},
        #                              'pattern': {'fillmode': 'overlay', 'size': 10, 'solidity': 0.2}},
        #                   'type': 'barpolar'}],
        #     'carpet': [{'aaxis': {'endlinecolor': '#2a3f5f',
        #                           'gridcolor': 'white',
        #                           'linecolor': 'white',
        #                           'minorgridcolor': 'white',
        #                           'startlinecolor': '#2a3f5f'},
        #                 'baxis': {'endlinecolor': '#2a3f5f',
        #                           'gridcolor': 'white',
        #                           'linecolor': 'white',
        #                           'minorgridcolor': 'white',
        #                           'startlinecolor': '#2a3f5f'},
        #                 'type': 'carpet'}],
        #     'choropleth': [{'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'type': 'choropleth'}],
        #     'contour': [{'colorbar': {'outlinewidth': 0, 'ticks': ''},
        #                  'colorscale': [[0.0, '#0d0887'], [0.1111111111111111, '#46039f'],
        #                                 [0.2222222222222222, '#7201a8'],
        #                                 [0.3333333333333333, '#9c179e'],
        #                                 [0.4444444444444444, '#bd3786'],
        #                                 [0.5555555555555556, '#d8576b'],
        #                                 [0.6666666666666666, '#ed7953'],
        #                                 [0.7777777777777778, '#fb9f3a'],
        #                                 [0.8888888888888888, '#fdca26'], [1.0, '#f0f921']],
        #                  'type': 'contour'}],
        #     'contourcarpet': [{'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'type': 'contourcarpet'}],
        'heatmap': [
            {
                'colorbar':
                    {
                        'outlinewidth': 0,
                        'ticks': ''
                    },
                'colorscale': [
                    [0.0, '#1C39BB'],
                    [0.1111111111111111, '#304BC2'],
                    [0.2222222222222222, '#445DC9'],
                    [0.3333333333333333, '#596FCF'],
                    [0.4444444444444444, '#6D81D6'],
                    [0.5555555555555556, '#8194DD'],
                    [0.6666666666666666, '#95A6E4'],
                    [0.7777777777777778, '#A9B8EB'],
                    [0.8888888888888888, '#BECAF1'],
                    [1.0, '#E6EEFF']
                ],
                'type': 'heatmap'
            }
        ],
        #     'heatmapgl': [{'colorbar': {'outlinewidth': 0, 'ticks': ''},
        #                    'colorscale': [[0.0, '#0d0887'], [0.1111111111111111,
        #                                   '#46039f'], [0.2222222222222222, '#7201a8'],
        #                                   [0.3333333333333333, '#9c179e'],
        #                                   [0.4444444444444444, '#bd3786'],
        #                                   [0.5555555555555556, '#d8576b'],
        #                                   [0.6666666666666666, '#ed7953'],
        #                                   [0.7777777777777778, '#fb9f3a'],
        #                                   [0.8888888888888888, '#fdca26'], [1.0,
        #                                   '#f0f921']],
        #                    'type': 'heatmapgl'}],
        #     'histogram': [{'marker': {'pattern': {'fillmode': 'overlay', 'size': 10, 'solidity': 0.2}}, 'type': 'histogram'}],
        #     'histogram2d': [{'colorbar': {'outlinewidth': 0, 'ticks': ''},
        #                      'colorscale': [[0.0, '#0d0887'], [0.1111111111111111,
        #                                     '#46039f'], [0.2222222222222222, '#7201a8'],
        #                                     [0.3333333333333333, '#9c179e'],
        #                                     [0.4444444444444444, '#bd3786'],
        #                                     [0.5555555555555556, '#d8576b'],
        #                                     [0.6666666666666666, '#ed7953'],
        #                                     [0.7777777777777778, '#fb9f3a'],
        #                                     [0.8888888888888888, '#fdca26'], [1.0,
        #                                     '#f0f921']],
        #                      'type': 'histogram2d'}],
        #     'histogram2dcontour': [{'colorbar': {'outlinewidth': 0, 'ticks': ''},
        #                             'colorscale': [[0.0, '#0d0887'], [0.1111111111111111,
        #                                            '#46039f'], [0.2222222222222222,
        #                                            '#7201a8'], [0.3333333333333333,
        #                                            '#9c179e'], [0.4444444444444444,
        #                                            '#bd3786'], [0.5555555555555556,
        #                                            '#d8576b'], [0.6666666666666666,
        #                                            '#ed7953'], [0.7777777777777778,
        #                                            '#fb9f3a'], [0.8888888888888888,
        #                                            '#fdca26'], [1.0, '#f0f921']],
        #                             'type': 'histogram2dcontour'}],
        #     'mesh3d': [{'colorbar': {'outlinewidth': 0, 'ticks': ''}, 'type': 'mesh3d'}],
        #     'parcoords': [{'line': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'type': 'parcoords'}],
        #     'pie': [{'automargin': True, 'type': 'pie'}],
        #     'scatter': [{'fillpattern': {'fillmode': 'overlay', 'size': 10, 'solidity': 0.2}, 'type': 'scatter'}],
        #     'scatter3d': [{'line': {'colorbar': {'outlinewidth': 0, 'ticks': ''}},
        #                    'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}},
        #                    'type': 'scatter3d'}],
        #     'scattercarpet': [{'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'type': 'scattercarpet'}],
        #     'scattergeo': [{'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'type': 'scattergeo'}],
        #     'scattergl': [{'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'type': 'scattergl'}],
        #     'scattermapbox': [{'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'type': 'scattermapbox'}],
        #     'scatterpolar': [{'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'type': 'scatterpolar'}],
        #     'scatterpolargl': [{'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'type': 'scatterpolargl'}],
        #     'scatterternary': [{'marker': {'colorbar': {'outlinewidth': 0, 'ticks': ''}}, 'type': 'scatterternary'}],
        #     'surface': [{'colorbar': {'outlinewidth': 0, 'ticks': ''},
        #                  'colorscale': [[0.0, '#0d0887'], [0.1111111111111111, '#46039f'],
        #                                 [0.2222222222222222, '#7201a8'],
        #                                 [0.3333333333333333, '#9c179e'],
        #                                 [0.4444444444444444, '#bd3786'],
        #                                 [0.5555555555555556, '#d8576b'],
        #                                 [0.6666666666666666, '#ed7953'],
        #                                 [0.7777777777777778, '#fb9f3a'],
        #                                 [0.8888888888888888, '#fdca26'], [1.0, '#f0f921']],
        #                  'type': 'surface'}],
        #     'table': [{'cells': {'fill': {'color': '#EBF0F8'}, 'line': {'color': 'white'}},
        #                'header': {'fill': {'color': '#C8D4E3'}, 'line': {'color': 'white'}},
        #                'type': 'table'}]
        # }

        # 'bar': [
        #     go.Bar(
        #         texttemplate='%{value:$.2s}',
        #         textposition='outside',
        #         textfont={
        #             'family': 'Helvetica Neue, Helvetica, Sans-serif',
        #             'size': 20,
        #             'color': BLACK
        #         }
        #     )
        # ],
        # 'line': [
        #     go.Line(
        #
        #     )
        # ],
    }
)
