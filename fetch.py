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

def get_top_artists(n):
    # Parameters for requesting the top n charting artists
    artist_request = {
        'method' : "chart.gettopartists",
        'api_key': API_KEY,
        'limit': str(n),
        'api_key': API_KEY,
    }
    print("Fetching top ", NUM_ARTISTS, " artists... ")
    top_artists = rs.get('http://ws.audioscrobbler.com/2.0/', params=artist_request)
    # For purposes of fulfilling the assignment, we save this XML to disk.
    with open("raw.xml", "w") as raw:
        raw.write(top_artists.text)
    return top_artists

def parse_top_artists(xml):
    print("Parsing XML...")
    names = []
    top_artists_root = ET.ElementTree(ET.fromstring(xml.text)).getroot()
    for name in top_artists_root.iter('name'):
        names.append(name.text)
    return names

def get_top_artist_tags(filepath, artists):
    """ Get top tags for every artist. Store names and their associated tags in a
    CSV file.
    """
   
    print("Fetching top tags...")
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|')
        writer.writerow(["artist", "tags"])
        for idx, artist in enumerate(artists):
            tags = get_top_tags(artist)
            writeout = [artist.replace(' ', '_'), ', '.join(tags)]
            writer.writerow(writeout)
            print(str(writeout), '\n')
            print(idx+1, '/', NUM_ARTISTS)
            sleep(0.2) # respect last.fm's rate limit

if __name__ == '__main__':
    top_artists_xml = get_top_artists(NUM_ARTISTS)
    top_artists = parse_top_artists(top_artists_xml)
    get_top_artist_tags('artist_tags.csv', top_artists)
