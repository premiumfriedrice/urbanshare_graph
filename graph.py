import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import requests
import pprint


app = Dash(__name__)

# heatmap_df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')

response = requests.get('https://data.austintexas.gov/resource/dx9v-zd7x.json')
body = response.json()

# print(type(body))
crash_data = pd.DataFrame(body)
# print(crash_data)
# # print(crash_data.columns)
score = {1: ['LOOSE LIVESTOCK'], 2: ['TRFC HAZD/ DEBRIS'], 3: ['COLLISION'], 5: ['Crash Urgent']}
score_map = {desc: sev for sev, descs in score.items() for desc in descs}


crash_data['severity'] = crash_data['issue_reported'].map(score_map)
# print(crash_data['issue_reported'])
crash_data = crash_data.dropna(subset=['severity'])

# print(crash_data)

# austincrash_df = pd.read_csv('https://data.austintexas.gov/Transportation-and-Mobility/Real-Time-Traffic-Incident-Reports/dx9v-zd7x/data_preview')

# heatmap_fig = px.density_mapbox(austincrash_df, lat='Latitude', lon='Longitude', z='Magnitude', radius=10,
#                                 center=dict(lat=30.2672, lon=-97.7431), zoom=10,
#                                 mapbox_style="open-street-map")

heatmap_fig = px.density_map(crash_data, lat='latitude', lon='longitude', z='severity', radius=10,
                                center=dict(lat=30.2672, lon=-97.7431), zoom=10,
                                map_style="open-street-map")                               
heatmap_fig.update_layout(map_style="open-street-map")

app.layout = html.Div([

    # html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Graph(id='my_bee_map', figure=heatmap_fig)
])


# -------------------------------------------------------------------------------
# if __name__ == '__main__':
#     app.run(debug=True, port=3001)  # for running on a different port