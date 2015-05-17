import csv
import os
import sys


def load_tag_data(filepath):
    """Load all of our artist and tag information from a CSV file and put it
    into a hash table of the following form:
    {"artist" : ["tag1", "tag2", "tag3", ... ]}
    """

    # Open the file and parse it.
    data = []
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            data.append(row)

    # Map artist names to their tags in a hashtable.
    tagdata = dict()
    for artist, tags in data:
        tagdata[artist] = [tag.strip() for tag in tags.split(',')]

    return tagdata
