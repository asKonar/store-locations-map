from dash import dcc, html, Dash, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


zabka = pd.read_csv('https://raw.githubusercontent.com/asKonar/zabka-locations-map/main/zabka_map_data.csv').sort_values(by=['Voivodeship'], ascending=True)

external_stylesheets = [dbc.themes.LUX]

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    dbc.Container([
        html.Div([
            dbc.Col(html.H1('Żabka location map'))
        ]),
        dcc.Dropdown(
            options=zabka['Voivodeship'].unique(),
            value='All',
            id='voivodeship_list',
            clearable=False
        ),
        html.Br(),
        html.Div([
            dcc.Graph(id='graph'),
        ])
    ])
])


@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='voivodeship_list', component_property='value')
)
def graph_update(voivodeship):
    if voivodeship == "All":
        fig = px.scatter_mapbox(
            zabka,
            lat="Latitude",
            lon="Longitude",
            hover_name="City",
            hover_data=["Voivodeship", "Powiat", "Street"],
            color_discrete_sequence=["blue"],
            zoom=6,
        )
    else:
        fig = px.scatter_mapbox(
            zabka.loc[zabka['Voivodeship'] == voivodeship],
            lat="Latitude",
            lon="Longitude",
            hover_name="City",
            hover_data=["Voivodeship", "Powiat", "Street"],
            color_discrete_sequence=["blue"],
        )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(height=800),
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    return fig


app.run_server()
