import csv
import os
import requests as rs
import  xml.etree.ElementTree as ET

"""A script that fetches the top 1000 artists on last.fm, then fetches their
associated tag data. We then save these to disk in CSV format.

USAGE: python3 fetch.py [NUMBER OF TOP ARTISTS TO FETCH]
"""

if len(sys.argv) < 2:
    print("USAGE: python3 fetch.py [NUMBER OF TOP ARTISTS TO FETCH]")
    sys.exit()

API_KEY = "b5f1c27242202b8aada75ce640693689"
NUM_ARTISTS = sys.argv[1]

# Parameters we are passing to the last.fm API
request = {
         'method' : "chart.gettopartists",
         'api_key': API_KEY,
         'limit': str(NUM_ARTISTS),
         'api_key': API_KEY,
}

# This gives us a big XML file containing the top X artists
top_artists = rs.get('http://ws.audioscrobbler.com/2.0/', params=request)

# Parse all of the artists found in the .xml
top_artists_root = ElementTree.fromstring(top_artists.text)
for name in top_artists_root.findall('name'):
    print(name)
