from flask import Flask, Response
import json
from models import recent_rankings, recent_rankings_for_entry

app = Flask(__name__, static_url_path='', static_folder='./public')

api_headers = {'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'}


@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route("/api/")
def api_history():

    for ranking in recent_rankings(hour_range=3):

        print(
            ranking.rank,
            ranking.entry.name,
            ranking.ranking_log.created.isoformat(timespec='seconds'),
        )


@app.route("/api/entry/<entry_name>")
def api_entry(entry_name):
    response = []
    for ranking in recent_rankings_for_entry(entry_name, hour_range=24 * 12):
        response.append({
            'rank': ranking.rank,
            'name': ranking.entry.name,
            'timestamp': ranking.ranking_log.created.isoformat(timespec='seconds'),
        })
    return Response(
        json.dumps(response, ensure_ascii=False),
        mimetype='application/json',
        headers=api_headers,
    )
