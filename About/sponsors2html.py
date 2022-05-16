
# This script reads the input excel sheet to generate an html file (sponsor-cards.html)
# of all the sponsors 
#
# to run in python prompt
# import sponsors2html
# sponsors2html.sponsors2html('../CCWJ_Website.xlsx')

import os
import pandas as pd

def sponsors2html(excel_path):
    data = pd.read_excel(excel_path, sheet_name='About_Sponsors')
    data.fillna('', inplace=True)
        
    # open file to write into
    f = open('sponsor-cards.html', 'w')
    
    needs_closing_div = False
    
    for i, entry in data.iterrows():
            
        if entry['Sponsors']:
            if needs_closing_div:
                f.write('</div>\n\n')
                
            needs_closing_div = True
            f.write('<h4>' + entry['Sponsors'] + '</h4>\n')
            f.write('<div class="row mb-2 mt-1">\n\n')
        
        if entry['Company']:
            f.write('<div class="col-lg-4 col-md-6">\n<div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm bg-white h-md-200 position-relative">\n<div class="col p-4 d-flex flex-column position-static">\n')
            f.write('<h5 class="mb-3">'+ entry['Company'] +'</h5>\n')
            f.write('<p class="card-text mb-auto">' + entry['Sponsorship Details'] + '</p>\n</div>\n')
            
            if entry['Code']:
                # find and write photo
                pic_folder = '../Assets/About_Us/Sponsors_Logos/' # folder containing all photos
                
                img_path = ''
                for filename in os.listdir(pic_folder):
                    if filename.startswith(entry['Code']):
                        img_path = pic_folder + filename
                if img_path:
                    f.write('<div class="equipment-pic col-auto d-flex overflow-hidden p-3">\n<a href="' + entry['Sponsor Link'] + '" target="_blank"><img class="fill-img" src="' + img_path + '" alt="pic"></a>\n</div>\n')
            
            f.write('</div>\n</div>\n')
    

    # close file
    f.close()

    print('sponsors2html complete')





