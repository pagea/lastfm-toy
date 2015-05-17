import csv
import os
import requests as rs
import sys
import xml.etree.ElementTree as ET

from time import sleep

"""A simple script that fetches the top N artists on last.fm, then fetches
their associated tag data. We then save these to disk in CSV format.

USAGE: python3 fetch.py [NUMBER OF TOP ARTISTS TO FETCH]

"""

if len(sys.argv) < 2:
    print("USAGE: python3 fetch.py [NUMBER OF TOP ARTISTS TO FETCH]")
    sys.exit()

API_KEY = "b5f1c27242202b8aada75ce640693689"
NUM_ARTISTS = sys.argv[1]

def get_top_tags(artist):
    """Retrieve the top tags for a given artist."""

    tag_request = {
        'method' : "artist.gettoptags",
        'api_key' : API_KEY,
        'artist' : artist,
    }

    top_tags = rs.get('http://ws.audioscrobbler.com/2.0/', params=tag_request)
    tags_root = ET.ElementTree(ET.fromstring(top_tags.text)).getroot()

    tags = []
    for tag in tags_root.iter('name'):
        tags.append(tag.text)
    return tags

# Parameters for requesting the top artists on last.fm
artist_request = {
    'method' : "chart.gettopartists",
    'api_key': API_KEY,
    'limit': str(NUM_ARTISTS),
    'api_key': API_KEY,
}

# This gives us a big XML file containing the top n artists
print("Fetching top ", NUM_ARTISTS, " artists... ")
top_artists = rs.get('http://ws.audioscrobbler.com/2.0/', params=artist_request)

# Parse all of the artists found in the .xml, store then in a list
print("Parsing XML...")
names = []
top_artists_root = ET.ElementTree(ET.fromstring(top_artists.text)).getroot()
for name in top_artists_root.iter('name'):
    names.append(name.text)

# Get top tags for every artist. Store names and their associated tags in a CSV
# file.
print("Fetching top tags...")
with open('artist_tags.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='|')
    writer.writerow(["artist", "tags"])
    for idx, name in enumerate(names):
        tags = get_top_tags(name)
        writeout = [name.replace(' ', '_'), ', '.join(tags)]
        writer.writerow(writeout)
        print(str(writeout), '\n')
        print(idx+1, '/', NUM_ARTISTS)
