import csv
import os
import sys

from collections import OrderedDict
from operator import itemgetter
#TODO: Parameter documentation. Return type documentation.


def load_tag_data(filepath):
    """Load all of our artist and tag information from a CSV file and put it
    into a hash table of the following form:
    {"Artist_Name" : ["tag1", "tag2", "tag3", ... ]}
    """

    # Open the CSV and parse it.
    data = []
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            data.append(row)

    # Map artist names to their tags in a hashtable.
    tagdata = {}
    for artist, tags in data:
        # Strip superfluous whitespace and casing while we're at it
        tagdata[artist.lower()] = [tag.strip().lower() for tag in tags.split(',')]

    return tagdata

def get_similar_tags(tag, tagdata):
    """Return a dict of tags mapped to co-occurring tags ranked by their
    similarity.
    """
    
    # Find co-occurring tags and count how many times we see them throughout the
    # dataset. The tags with the highest counts become the most strongly
    # associated tags.
    associated = OrderedDict()
    for tags in tagdata.values():
        if tag in tags:
            for val in tags:
                if val in associated.keys():
                    associated[val] += 1
                else:
                    associated[val] = 1
    # Clean out junk tags (tags that co-occur less than 4 times)
    if tag in associated:
        associated.pop(tag)
    for key in associated.keys():
        if associated[key] < 4:
            associated.pop(key)
    # Sort by number of co-occurrences.
    return sorted(associated.items(), key=lambda x:x[1], reverse=True)

def get_similar_artists(artist_name, tagdata):
    # Get the tags from the artist we're analyzing
    try:
        artist_tags = tagdata[artist_name.lower()]
    except KeyError:
        print("Artist not found.")

    # To find artists similar to, say, Nirvana, we retrieve Nirvana's
    # tags and intersect them with everyone else's tags in our dataset. This
    # effectively finds all of the tags Nirvana has in common with every
    # artist.
    intersections = {}
    for artist, tags in tagdata.items():
        intersections[artist] = set(artist_tags).intersection(tagdata[artist])

    # Table mapping artist names to their similarity with the artist we are
    # analyzing.
    similarity = {}
    for artist in intersections:
        similarity[artist] = len(intersections[artist])
    if artist_name in similarity:
        similarity.pop(artist_name)
    
    return sorted(similarity.items(), key=lambda x:x[1], reverse=True)

if __name__ == '__main__':
    tagdata = load_tag_data("artist_tags.csv")
    # We only show the top 20 results for each function.
    print("Similar tags:\n", get_similar_tags(sys.argv[1], tagdata)[:20])
    print("Similar artists:\n", get_similar_artists(sys.argv[2], tagdata)[:20])
