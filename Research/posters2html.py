
# This script reads the input excel sheet to generate an html file (equipment.html)
# of all the equipment in the lab. Items are sorted by category.
#
# to run in python prompt
# import posters2html
# posters2html.posters2html('../CCWJ_Website.xlsx')

import os
import pandas as pd
import fitz

poster_folder = '../Assets/Research/Posters/' # folder containing all posters as images

def posters2html(excel_path):
    # read 3rd sheet in excel file (lab equipment)
    data = pd.read_excel(excel_path, sheet_name='Research_Posters')
    data.fillna('', inplace=True)
        
    # open file to write into
    f = open('posters-embed.html', 'w')

    # write each section (csv key, webpage heading, list id)
    write_section('Posters', 'Posters', 'list-charac', data, f)
    
    # close file
    f.close()

    print('posters2html complete')

def write_section(csv_key, section_title, section_id, data, f):

    f.write('<div class="row mb-2">\n\n')

    for index, row in data.iterrows(): # go through each row

        f.write('<div class="col-xl-4 col-md-6">\n<div class="row card g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm bg-white h-md-200 position-relative">\n')
        
        # find and write image or pdf with link
        img_path = ''
       
        for filename in os.listdir(poster_folder):
            if filename.startswith(row['Poster_Code']):
                img_path = os.path.join(poster_folder,filename)
                if filename.endswith('.pdf'): # for pdf files, generate image thumbnail
                    print('posters2html: generating img thumbnail for pdf ' + filename)
                    doc = fitz.open(os.path.join(poster_folder,filename))
                    thumbnail = doc[0].get_pixmap()
                    thumbnail_name = filename.split('.')[0] + '.png'
                    thumbnail.save(os.path.join(poster_folder,'Thumbnails/',thumbnail_name))
                break
        if img_path:
            if img_path.endswith('.pdf'):
                thumbnail_name = img_path.split('/')[-1].split('.')[0] + '.png'
                thumbnail_path = os.path.join(poster_folder, 'Thumbnails/',thumbnail_name)
                f.write('<a target="_blank" href="' + img_path + '"><img src="' + thumbnail_path + '" class="card-img-top poster-img"></a>\n')
            else:
                f.write('<a target="_blank" href="' + img_path + '"><img src="' + img_path + '" class="card-img-top poster-img"></a>\n')
        else:
            print('posters2html: could not find poster ' + str(row['Poster_Code']))

        # write body
        f.write('<div class="card-body">\n')
        if row['Poster_Title']:
            f.write('<h5 class="card-title">'+ row['Poster_Title'] +'</h5>\n')
        if row['Presenter']:
            f.write('<p class="card-text">'+ row['Presenter'] +'</p>\n')
        if row['Description']:
            f.write('<p class="card-text">' + row['Description'] + '</p>\n')

        f.write('</div>\n</div>\n</div>\n')

    f.write('</div>')




