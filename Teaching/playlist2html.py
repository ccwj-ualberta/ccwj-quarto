"""
Extract video titles and links from a youtube playlist (not used currently)
Usage (from Python or IPython prompt):

    >> import playlist2html
    >> playlist2html.playlist2html('https://www.youtube.com/playlist?list=PLp0pALmMwc6v2ScmEGbvNSpNKcYA8GiGA', 'mig1.txt')

Must have youtube-dl installed
"""

import os
import json


def playlist2html(url, file):
    # get json file from url
    os.system("youtube-dl --get-title --get-id --skip-download " + url + " > " + file)

    with open(file) as f:
        count = 0
        titles = []
        ids = []
        for line in f:
            if count % 2 == 0:
                titles.append(line.strip())
            elif count % 2 == 1:
                ids.append(line.strip())
            count+= 1

    print(titles)
    print(ids)

    # open file to write into
    f = open('playlist.html', 'w')

    for title, id in zip(titles, ids):
        f.write('<p><a href="https://www.youtube.com/watch?v=' + id + '">' + str(title) + '</a></p>\n')

    f.close()
