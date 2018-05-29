import requests
from bson import ObjectId

from flask import (
    Flask,
    render_template,
    jsonify,
    request
)


app = Flask(__name__)
SAMPLE_SONG_DATA = {
    'play_count': 0,
    'exercise_name': 'basic bass',
    'doc_id': '5aaa819d4430ff1b4b925c6a',
    'avg_rating': 0,
    'artist': 'Metallica',
    'licensed': True,
    'mongo_id': '5aaa81a04430ff1b4b925c6d',
    'instrument': 'bass',
    'version': 'main',
    'has_audio': True,
    'song_title': 'Fade To Black',
    'owner': 'Vellu Halkosalmi',
    'level': 1,
    'type': 0,
    'public': True
}


def format_songs(es_response):
    songs = es_response.json()['hits']['hits']
    result = []
    for s in songs:
        song_data = s['_source']
        result.append(
            f'{song_data["artist"]} - '
            f'{song_data["song_title"]} - {s["_score"]}'
        )
    return result


@app.route('/song', methods=['POST'])
def add_song():
    artist, song = request.json['song'].split(' - ')
    data = SAMPLE_SONG_DATA.copy()
    data['artist'] = artist
    data['song_title'] = song
    requests.put(
        'http://localhost:9200/exercises/exercise/%s' % str(ObjectId()),
        json=data
    )
    return '{}'


@app.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    response = requests.post(
        'http://localhost:9200/exercises/exercise/_search',
        json={
            "query": {
                "bool": {
                    # "must": {
                    #     "match": {
                    #         "instrument": "guitar"
                    #     }
                    # },
                    "should": [
                        # {
                        #     "multi_match": {
                        #         "query": query,
                        #         "type": "best_fields",
                        #         "fields": ["artist", "song_title"],
                        #         "fuzziness": "AUTO",
                        #         "analyzer": "english"
                        #     }
                        # },
                        {
                            "match": {
                                "artist": {
                                    "query": query,
                                    "fuzziness": "AUTO",
                                    "analyzer": "english"
                                }
                            }
                        },
                        {
                            "match": {
                                "song_title": {
                                    "query": query,
                                    "fuzziness": "AUTO",
                                    "analyzer": "english",
                                }
                            }
                        },
                        {"match_phrase_prefix": {"artist": query}},
                        {
                            "match_phrase_prefix": {
                                "song_title": {
                                    "query": query
                                }
                            }
                        }
                    ]
                }
            },
            "size": 50,
        }
    )
    songs = format_songs(response)
    if not songs:
        # response = requests.get(
        #     'http://localhost:9200/exercises/exercise/_search?size=50'
        # )
        # songs = format_songs(response)
        songs = []

    return jsonify(songs)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5033)
