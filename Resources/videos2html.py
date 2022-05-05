# This script reads the input excel sheet to generate a html file for each subpage under
# the Resources/Videos tab
#
# to run in python prompt
# import videos2html
# videos2html.videos2html('../CCWJ_Website.xlsx')

import csv
import os
from datetime import datetime
import pandas as pd


excel_path = '../CCWJ_Website.xlsx'
def videos2html(excel_path):
    # read sheet named resources_videos excel file
    data = pd.read_excel(excel_path, sheet_name="Resources_Videos")
    data.fillna('', inplace=True)
        

    # make filename the first word of section name, keeping only alphanumeric characters
    filename = 'videos-embed.html'
    
    # open file to write into
    f = open(filename, 'w')
    
    # write each section (section name, data)
    for index, row in data.iterrows():
        
        if row['Playlist Name']:
            f.write('<h4>' + row['Playlist Name'] + '</h4>\n')
            
        if row['Description']:
            text = row['Description'].strip('\n').replace('\n', '<br>') # preserve newlines in html
            f.write('<p>' + text + '</p>\n')
            
        if row['Link']:
            link = row['Link']
            # grab video type (either 'watch' for video or 'playlist' for playlist) as the word 
            # sitting between com/ and ? in the url
            video_type = link[link.index('com/') + len('com/'):link.index('?')]
            
            if video_type.startswith('playlist'):
                playlist_id = link.split("list=")[1]
                
                f.write('<iframe width="560" height="315" src="https://www.youtube.com/embed/videoseries?list=' + playlist_id + '" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n')
                
            else:
                # only keep first 11 characters after watch?v= to get video id
                video_id = link.split("watch?v=")[1][:11]
                
                f.write('<iframe width="560" height="315" src="https://www.youtube.com/embed/' + video_id + '" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n')
        
    
    f.close()





    
