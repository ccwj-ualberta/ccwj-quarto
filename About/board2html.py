
# This script reads the input excel sheet to generate an html file (equipment.html)
# of all the equipment in the lab. Items are sorted by category.
#
# to run in python prompt
# import lab2html
# lab2html.lab2html('../CCWJ_Website.xlsx')

import csv
import os
from datetime import datetime
import pandas as pd

def board2html(excel_path):
    data = pd.read_excel(excel_path, sheet_name='About_Advisory_Boards')
    data.fillna('', inplace=True)
    print(data)
        
    # open file to write into
    f = open('board-members.html', 'w')
    
    needs_closing_div = False
    
    for i, entry in data.iterrows():
            
        if entry['Type']:
            if needs_closing_div:
                f.write('</div>\n\n')
                
            if entry['Section'].startswith('Past Member'): # write header for past members
                f.write('<h4 class="subheading">Past Members</h4>\n')
                
            needs_closing_div = True
            f.write('<h4>' + entry['Type'] + '</h4>\n')
            f.write('<div class="row mb-2">\n\n')
        
        if entry['Name']:
            f.write('<div class="col-lg-4 col-md-6">\n<div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-200 position-relative">\n<div class="col p-4 d-flex flex-column position-static">\n')
            f.write('<strong class="d-inline-block mb-0 text-success">' + entry['Company'] + '</strong>\n')
            f.write('<h5 class="mb-3">'+ entry['Name'] +'</h5>\n')
            f.write('<p class="card-text mb-auto">' + entry['Role_Board'] + '</p>\n</div>\n')
            
            if entry['Picture']:
                # find and write photo
                pic_folder = '../Assets/About_Us/Equipment_Photos/' # folder containing all photos
                
                img_path = ''
                for filename in os.listdir(pic_folder):
                    if filename.startswith(entry['Picture']):
                        img_path = pic_folder + filename
                if img_path:
                    f.write('<div class="equipment-pic col-auto d-flex overflow-hidden">\n<img class="fill-img" src="' + img_path + '" alt="pic">\n</div>\n')
            
            f.write('</div>\n</div>\n')
    

    # close file
    f.close()





