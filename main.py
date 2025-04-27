from flask import Flask, render_template
import plotly.express as px
import json
import plotly
import os
import requests
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

response = requests.get('https://data.austintexas.gov/resource/dx9v-zd7x.json')
body = response.json()
print(body)
crash_data = pd.DataFrame(body)

score = {1: ['LOOSE LIVESTOCK'], 2: ['TRFC HAZD/ DEBRIS'], 3: ['COLLISION'], 5: ['Crash Urgent']}
score_map = {desc: sev for sev, descs in score.items() for desc in descs}

crash_data['severity'] = crash_data['issue_reported'].map(score_map)

crash_data = crash_data.dropna(subset=['severity'])

@app.route('/')
def index():
    fig = px.density_mapbox(crash_data, lat='latitude', lon='longitude', z='severity', radius=10,
                                center=dict(lat=30.2672, lon=-97.7431), zoom=10,
                                mapbox_style="open-street-map")

    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Render the template, passing the JSON data
    return render_template('index.html', graph_json=graph_json)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))