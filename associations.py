import csv
import os
import sys

from collections import OrderedDict
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
    tagdata = dict()
    for artist, tags in data:
        # Strip superfluous whitespace and casing while we're at it
        tagdata[artist] = [tag.strip().lower() for tag in tags.split(',')]

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
    # Clean out junk tags
    if tag in associated:
        associated.pop(tag)
    for key in associated.keys():
        if associated[key] < 5:
            associated.pop(key)
    # Sort by number of co-occurrences.
    return sorted(associated.items(), key=lambda x:x[1])

if __name__ == '__main__':
    tagdata = load_tag_data("artist_tags.csv")
    print(get_similar_tags(sys.argv[1], tagdata))
