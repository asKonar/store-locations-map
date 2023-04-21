from dash import dcc, html, Dash, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

zabka_map_data = pd.read_csv(
    'https://raw.githubusercontent.com/asKonar/zabka-locations-map/main/zabka_map_data.csv'
).sort_values(by=['Voivodeship'], ascending=True)
zabka_voivodeship_chart_data = pd.read_csv(
    'https://raw.githubusercontent.com/asKonar/zabka-locations-map/main/voivodeship_locations.csv'
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = html.Div(style={'width': '100%'}, children=[
    html.Div([
        dbc.Row([
            dbc.Col(html.H1(
                'Żabka location map'
            ), width={'size': 5, 'offset': 2}, align='start', className='pt-3'),
            dbc.Col(html.H4(dcc.Dropdown(
                options=zabka_map_data['Voivodeship'].unique(),
                value='All',
                id='voivodeship_map_list',
                clearable=False,
                searchable=False
            )), width={'size': 3}, align='center', className='pt-3'),
        ], style={'width': '100%'}),

        dbc.Row([
            dbc.Col(
                dcc.Graph(id='map_graph'), width={'size': 8, 'offset': 2}
            )
        ], style={'width': '100%'})
    ]),

    html.Div([
        dbc.Row([
            dbc.Col(html.H4(dcc.Dropdown(
                options=[
                    'Locations in Voivodeships',
                    'Locations per 100k people',
                    'Locations per 100km\u00b2'
                ],
                value='Locations in Voivodeships',
                clearable=False,
                searchable=False,
                id='voivodeship_data_list'
            )), width={'size': 8, 'offset': 2}, className='pt-5'),
        ], style={'width': '100%'}),

        dbc.Row([
            dbc.Col(
                dcc.Graph(id='data_graph'), width={'size': 8, 'offset': 2}, class_name='pb-5, pt-3'
            )
        ], style={'padding-bottom': '10px', 'margin-bottom': '20px', 'width': '100%'})
    ])
])


@app.callback(
    Output(component_id='map_graph', component_property='figure'),
    Input(component_id='voivodeship_map_list', component_property='value')
)
def map_graph_update(voivodeship_map_list):
    if voivodeship_map_list == "All":
        zabka_map_fig = px.scatter_mapbox(
            zabka_map_data,
            lat="Latitude",
            lon="Longitude",
            hover_name="City",
            hover_data=["Voivodeship", "Powiat", "Street"],
            color_discrete_sequence=["blue"],
            zoom=6,
        )
    else:
        zabka_map_fig = px.scatter_mapbox(
            zabka_map_data.loc[zabka_map_data['Voivodeship'] == voivodeship_map_list],
            lat="Latitude",
            lon="Longitude",
            hover_name="City",
            hover_data=["Voivodeship", "Powiat", "Street"],
            color_discrete_sequence=["blue"],
            zoom=6,
        )

    zabka_map_fig.update_layout(
        mapbox_style="open-street-map",
        height=1100,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return zabka_map_fig


@app.callback(
    Output(component_id='data_graph', component_property='figure'),
    Input(component_id='voivodeship_data_list', component_property='value')
)
def data_graph_update(voivodeship_data_list):
    match voivodeship_data_list:
        case 'Locations in Voivodeships':
            data_fig = px.bar(
                zabka_voivodeship_chart_data,
                x='Voivodeship',
                y='Locations',
                text_auto='1'
            )
        case 'Locations per 100k people':
            data = []
            for csv_data in zabka_voivodeship_chart_data.iterrows():
                x = round(csv_data[1][1] / csv_data[1][2] * 100000, 2)
                data.append(x)
            data_fig = px.bar(
                zabka_voivodeship_chart_data,
                x='Voivodeship',
                y=data,
                labels={'y': 'Locations'},
                text_auto='1'
            )
        case 'Locations per 100km\u00b2':
            data = []
            for csv_data in zabka_voivodeship_chart_data.iterrows():
                x = round(csv_data[1][1] / csv_data[1][3] * 100, 2)
                data.append(x)
            data_fig = px.bar(
                zabka_voivodeship_chart_data,
                x='Voivodeship',
                y=data,
                labels={'y': 'Locations'},
                text_auto='1'
            )

    data_fig.update_layout(
        font=dict(size=20),
        height=600,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    data_fig.update_traces(width=1)

    return data_fig


app.run_server(debug=True)
