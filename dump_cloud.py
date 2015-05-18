# Dump tag occurrence data to a text file so we can turn it into a word cloud
import sys
import os

from associations import load_tag_data, get_similar_tags


tagdata = load_tag_data("artist_tags.csv")
similar_tags = get_similar_tags(sys.argv[1], tagdata)

out = ""
for tag, value in similar_tags:
    for x in range(value):
        out += tag + " "

with open('dump.txt', 'w') as outfile:
    outfile.write(out)

