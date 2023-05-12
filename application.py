from dash import dcc, html, Dash, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# CSV data imports
biedronka_map_data = pd.read_csv(
    'https://raw.githubusercontent.com/asKonar/zabka-locations-map/main/data/biedronka_map_data.csv')
chata_polska_map_data = pd.read_csv(
    'https://raw.githubusercontent.com/asKonar/zabka-locations-map/main/data/chatapolska_map_data.csv')
delikatesy_centrum_map_data = pd.read_csv(
    'https://raw.githubusercontent.com/asKonar/zabka-locations-map/main/data/delikatesycentrum_map_data.csv')
dino_map_data = pd.read_csv(
    'https://raw.githubusercontent.com/asKonar/zabka-locations-map/main/data/dino_map_data.csv')
lewiatan_map_data = pd.read_csv(
    'https://raw.githubusercontent.com/asKonar/zabka-locations-map/main/data/lewiatan_map_data.csv')
polomarket_map_data = pd.read_csv(
    'https://raw.githubusercontent.com/asKonar/zabka-locations-map/main/data/polomarket_map_data.csv')
zabka_map_data = pd.read_csv(
    'https://raw.githubusercontent.com/asKonar/zabka-locations-map/main/data/zabka_map_data.csv')
voivodeship_chart_data = pd.read_csv(
    'https://raw.githubusercontent.com/asKonar/zabka-locations-map/main/data/voivodeship_locations.csv')


def main():
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server

    # Site layout
    app.layout = html.Div(style={'width': '100%'}, children=[
        html.Div([
            dbc.Row([
                dbc.Col(html.H2(
                    'Location map'
                ), width={'size': 2, 'offset': 2}, align='start', className='pt-3'),
                # Shop dropdown
                dbc.Col(html.H5(dcc.Dropdown(
                    options=['Biedronka', 'Chata Polska', 'Delikatesy Centrum', 'Dino',
                             'Lewiatan', 'Polomarket', 'Żabka'],
                    value='Biedronka',
                    id='locations_list',
                    clearable=False,
                    searchable=False
                )), width={'size': 3}, align='center', className='pt-3'),
                # Voivodeship dropdown
                dbc.Col(html.H5(dcc.Dropdown(
                    options=['All', 'Dolnośląskie', 'Kujawsko-pomorskie', 'Lubelskie', 'Lubuskie',
                             'Łódzkie', 'Małopolskie', 'Mazowieckie', 'Opolskie',
                             'Podkarpackie', 'Podlaskie', 'Pomorskie', 'Śląskie',
                             'Świętokrzyskie', 'Warmińsko-mazurskie', 'Wielkopolskie', 'Zachodniopomorskie'],
                    value='All',
                    id='voivodeship_map_list',
                    clearable=False,
                    searchable=False
                )), width={'size': 3}, align='center', className='pt-3'),
            ], style={'width': '100%'}),
            # Map element
            dbc.Row([
                dbc.Col(
                    dcc.Graph(id='map_graph'), width={'size': 8, 'offset': 2}
                )
            ], style={'width': '100%'})
        ]),
        # Data dropdown and graph based on 'Shop dropdown'
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

    # Map function
    @app.callback(
        Output(component_id='map_graph', component_property='figure'),
        Input(component_id='voivodeship_map_list', component_property='value'),
        Input(component_id='locations_list', component_property='value')
    )
    def map_graph_update(voivodeship_map_list, locations_list):
        chosen_store = {'Biedronka': biedronka_map_data, 'Chata Polska': chata_polska_map_data,
                        'Delikatesy Centrum': delikatesy_centrum_map_data,
                        'Dino': dino_map_data, 'Lewiatan': lewiatan_map_data,
                        'Polomarket': polomarket_map_data, 'Żabka': zabka_map_data}
        chosen_data_load = chosen_store.get(locations_list)
        if voivodeship_map_list == "All":
            map_fig = px.scatter_mapbox(
                chosen_data_load,
                lat="Latitude",
                lon="Longitude",
                color_discrete_sequence=["blue"],
                zoom=6,
            )
        else:
            map_fig = px.scatter_mapbox(
                chosen_data_load.loc[chosen_data_load['Voivodeship'] == voivodeship_map_list],
                lat="Latitude",
                lon="Longitude",
                color_discrete_sequence=["blue"],
            )

        map_fig.update_layout(
            mapbox_style="open-street-map",
            height=900,
            margin=dict(l=0, r=0, t=0, b=0)
        )

        return map_fig

    # Data graph function
    @app.callback(
        Output(component_id='data_graph', component_property='figure'),
        Input(component_id='voivodeship_data_list', component_property='value'),
        Input(component_id='locations_list', component_property='value')
    )
    def data_graph_update(voivodeship_data_list, locations_list):
        match voivodeship_data_list:
            case 'Locations in Voivodeships':
                data_fig = px.bar(
                    voivodeship_chart_data,
                    x='Voivodeship',
                    y=locations_list,
                    text_auto='1'
                )
            case 'Locations per 100k people':
                data = []
                i = 0
                while i < 16:
                    x = round(voivodeship_chart_data[str(locations_list)][i] / voivodeship_chart_data['Population'][
                        i] * 100000, 2)
                    data.append(x)
                    i += 1
                data_fig = px.bar(
                    voivodeship_chart_data,
                    x='Voivodeship',
                    y=data,
                    labels={'y': locations_list},
                    text_auto='1'
                )
            case 'Locations per 100km\u00b2':
                data = []
                i = 0
                while i < 16:
                    x = round(
                        voivodeship_chart_data[str(locations_list)][i] / voivodeship_chart_data['Size'][i] * 100, 2)
                    data.append(x)
                    i += 1
                data_fig = px.bar(
                    voivodeship_chart_data,
                    x='Voivodeship',
                    y=data,
                    labels={'y': locations_list},
                    text_auto='1'
                )

        data_fig.update_layout(
            font=dict(size=20),
            height=600,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        data_fig.update_traces(width=1)

        return data_fig

    app.run_server()


if __name__ == "__main__":
    main()
