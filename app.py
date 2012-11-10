import os
from urllib import urlopen
from flask import Flask, request, make_response
import geojson

app = Flask(__name__)
app.debug = True

@app.route('/')
def home():
    return 'filler'

@app.route('/kml.jsonp')
def kml():
    callback = request.args.get('callback')
    map = request.args.get('map')
    response = make_response("%s(%s)" % (callback, geojson.kml_json(urlopen(map))))
    response.headers['Content-Type'] = 'application/javascript'
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
