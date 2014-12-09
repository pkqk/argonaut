# encoding: utf-8
from __future__ import unicode_literals, print_function, division

import sys
import xml.sax
import json
from collections import defaultdict

class KMLHandler(xml.sax.ContentHandler):
    KEYS = ['name', 'description', 'coordinates', 'href', 'styleUrl']

    def __init__(self):
        self.node = 'root'
        self.placemarks = []
        self.placemark = None
        self.key = None
        self.style_key = None
        self.styles = {}

    def startElement(self, name, attrs):
        if name == "Placemark":
            self.placemark = defaultdict(unicode)
            self.node = 'placemark'
        elif name == "Style":
            self.node = 'style'
            self.style_key = attrs['id']
        if name in self.KEYS:
            self.key = name

    def endElement(self, name):
        self.key = None
        if name == "Placemark":
            self.save_placemark()
            self.node = 'root'
        elif name == 'Style':
            self.node = 'root'

    def characters(self, content):
        if (self.node, self.key) == ('style', 'href'):
            self.styles[self.style_key] = content
        elif self.key and self.placemark is not None:
            self.placemark[self.key] += content

    def save_placemark(self):
        place, self.placemark = self.placemark, None
        place['style'] = place.pop('styleUrl').replace('#', '')
        self.extract_coordinates(place)
        self.placemarks.append(place)

    def extract_coordinates(self, place):
        lon, lat, alt = place['coordinates'].split(',')
        place.update({
            'latitude': lat,
            'longitude': lon,
            'altitude': alt
        })

    def to_json(self):
        return json.dumps({'placemarks': self.placemarks, 'styles': self.styles})

def kml_json(stream):
    handler = KMLHandler()
    xml.sax.parse(stream, handler)
    return handler.to_json()

if __name__ == "__main__":
    print(kml_json(open(sys.argv[1])))
