from flask import Flask, Response, abort, redirect, render_template
import json
from models import recent_rankings, recent_rankings_for_entry

app = Flask(__name__, static_url_path='', static_folder='./public', template_folder='./public')

api_headers = {'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'}

# OMG, entries weren't normalized!
entries = [
    "星宮いちご",
    "霧矢あおい",
    "紫吹蘭",
    "神崎美月",
    "有栖川おとめ",
    "藤堂ユリカ",
    "一ノ瀬かえで",
    "北大路さくら",
    "三ノ輪ヒカリ",
    "神谷しおん",
    "音城セイラ",
    "冴草きい",
    "風沢そら",
    "夏樹みくる",
    "音城ノエル",
    "大空あかり",
    "氷上スミレ",
    "新条ひなき",
    "紅林珠璃",
    "服部ユウ",
    "天羽まどか",
    "黒沢凛",
    "姫里マリア",
    "藤原みやび",
    "栗栖ここね",
    "堂島ニーナ",
    "大地のの",
    "白樺リサ",
    "星宮りんご",
    "光石織姫",
    "星宮らいち",
    "ジョニー別府",
    "涼川直人",
    "瀬名翼",
    "四ツ葉春",
]


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/entry/<entry_name>")
def entry(entry_name):
    if entry_name not in entries:
        abort(404)
    print(entry_name)
    return render_template('entry.html', entry=entry_name)


@app.route("/api/v1/history/")
def api_history():
    for ranking in recent_rankings(hour_range=3):
        print(
            ranking.rank,
            ranking.entry.name,
            ranking.ranking_log.created.isoformat(timespec='seconds'),
        )


@app.route("/api/v1/entry/<entry_name>")
def api_entry(entry_name):
    response = []

    rankings = recent_rankings_for_entry(entry_name, hour_range=24 * 60)

    if len(rankings) > 1000:    # Seems bad access
        abort(404)

    for ranking in rankings:
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


@app.errorhandler(404)
def error_handler(error):
    return redirect("/")
