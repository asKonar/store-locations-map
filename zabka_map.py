import plotly.express as px
import pandas as pd

import dash
from dash import dcc, html, Dash

zabka = pd.read_csv('https://raw.githubusercontent.com/asKonar/zabka-locations-map/main/zabka_map_data.csv')

fig = px.scatter_mapbox(
    zabka,
    lat="Latitude",
    lon="Longitude",
    hover_name="City",
    hover_data=["Voivodeship", "Powiat", "Street"],
    color_discrete_sequence=["blue"],
    zoom=6,
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(height=900),
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
# fig.update_layout(mapbox_bounds={"west": 0, "east": 0, "south": 0, "north": 0})

app = Dash(__name__)
server = app.server
app.layout = html.Div(children=[
    html.Div(
        dcc.Graph(figure=fig),
    )
])

app.run_server()
