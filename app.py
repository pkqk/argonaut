import os
from flask import Flask, request, make_response
from geojson import GoogleMapLayer

app = Flask(__name__)
app.debug = os.environ.get('DEBUG', 'False') == 'True'

@app.route('/')
def home():
    return "", 204

@app.route('/kml.jsonp')
def kml():
    callback = request.args.get('callback')
    map = GoogleMapLayer(request.args.get('map'))
    response = make_response("%s(%s)" % (callback, map.to_json()))
    response.headers['Content-Type'] = 'application/javascript'
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
