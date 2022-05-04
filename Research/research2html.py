# This script reads the input excel sheet to generate a html file for each subpage under
# the Research tab
#
# to run in python prompt
# import research2html
# research2html.research2html('../CCWJ_Website.xlsx')

import csv
import os
from datetime import datetime
import pandas as pd


def write_section(section_name, data, index_start):
    # make filename the first word of section name, keeping only alphanumeric characters
    filename = "".join(x for x in section_name.split()[0].lower() if x.isalnum()) + '-text.html'
    
    # open file to write into
    f = open(filename, 'w')
    
    for i, row in data.iloc[index_start:].iterrows():
        print(row)
        
        # detect if next section has been reached, if so stop writing section
        if row['Section'] and row['Section'] != section_name:
            break
    
        for header, value in row.items():
    
            if header.startswith('Section_Heading') and value:
                f.write('<h4>' + value + '</h4>\n')
            elif header.startswith('Text_Block') and value:
                text = value.strip('\n').replace('\n', '<br>') # preserve newlines in html
                f.write('<p>' + text + '</p>\n')
            elif header.startswith('Image') and value:
                # get image path, look in Assets/Research folder and section_name (with underscores) subfolder 
                img_folder = os.path.join('../Assets/Research/', section_name.replace(' ', '_'))
                img_path = ''
                for filename in os.listdir(img_folder):
                    if filename.startswith(value):
                        img_path = os.path.join(img_folder,filename)
                if img_path:
                    # write image html
                    f.write('<img src="' + img_path + '" class="img-scale mx-auto d-block">\n')
                else:
                    print('cannot find image ' + value)
            elif header.startswith('Presenter') and value:
                f.write('<p>Presenter: ' + value.strip('\n').replace('\n', '<br>') + '</p>\n')
            elif header.startswith('Link') and value:
                # only keep first 11 characters after watch?v= to get video id
                video_id = value.split("watch?v=")[1][:11]
                
                f.write('<iframe width="560" height="315" src="https://www.youtube.com/embed/' + video_id + '" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n')
                


    f.close()

excel_path = '../CCWJ_Website.xlsx'
#def research2html(excel_path):
    # read sheet named researchin excel file
data = pd.read_excel(excel_path, sheet_name="Research")
data.fillna('', inplace=True)
    

# write each section (section name, data)
for index, section in data.iterrows():
    # if section['Section'].startswith('Advisory Boards'):
    #     # write special advisory page
    #     write_advisory(section['Section'], section)
    # elif section['Section'].startswith('Sponsors'):
    #     # write special sponsors page
    #     write_sponsors(section['Section'], section)
    # else:
        # write default page format
    if section['Section']:
        write_section(section['Section'], data, index)
    
