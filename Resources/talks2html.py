# This script reads the input excel sheet to generate html for talks
#
# to run in python prompt
# import talks2html
# talks2html.talks2html('../CCWJ_Website.xlsx')

import os
import pandas as pd

excel_path = '../CCWJ_Website.xlsx'
# folder with .pdf presentation slides, named starting with presentation code
presentations_folder = '../Assets/Resources/Tech_Talks_Presentations'

def talks2html(excel_path):
    # read sheet named resources_videos excel file
    data = pd.read_excel(excel_path, sheet_name="Resources_Talks")
    data.fillna('', inplace=True)
        
    filename = 'talks-embed.html'
    
    # open file to write into
    f = open(filename, 'w')
    
    # write each section (section name, data)
    for index, row in data.iterrows():
        
        if row['Presentation_Title']:
            f.write('<h4>' + row['Presentation_Title'] + '</h4>\n')
        
        if row['Presenter']:
            f.write('<p>Presenter: ' + row['Presenter'].strip('\n').replace('\n', '<br>'))
        
        if row['Presentation_Code']: # look for pdf file starting with presentation_code in presentations_folder
            for filename in os.listdir(presentations_folder):
                if filename.startswith(str(row['Presentation_Code'])) and filename.endswith('.pdf'):
                    f.write(' [<a target="_blank" href="' + os.path.join(presentations_folder,filename) + '">Slides</a>]</p>\n')
                    break
            else: # presentation code exists but pdf slides not found
                f.write('</p>\n')
                print('Resources/Talks: missing presentation slides code ' + row['Presentation_Code']) 
        else: # if no presentation code, write closing p tag
            f.write('</p>\n')

        if row['Date']: # format date as Mar 4, 2014
            date = row['Date'].strftime("%b %-d, %Y")
            f.write('<p>Date: ' + date.strip('\n').replace('\n', '<br>') + '</p>\n')
            
        if row['Abstract']:
            text = row['Abstract'].strip('\n').replace('\n', '<br>') # preserve newlines in html
            f.write('<p>' + text + '</p>')
            
        if row['Link']: # youtube video
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
        
        if row['File_Location']: # google drive video

            video_id = row['File_Location'].partition('/d/')[2].partition('/view')[0]
            f.write('<iframe src="https://drive.google.com/file/d/' + video_id + '/preview" width="560" height="315" allow="autoplay" allowfullscreen="true"></iframe>')
    
    
    
    f.close()





    
