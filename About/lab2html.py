
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

def lab2html(excel_path):
    # read 3rd sheet in excel file (lab equipment)
    data = pd.read_excel(excel_path, sheet_name=2)
    data.fillna('', inplace=True)
    print(data)
        
    # open file to write into
    f = open('equipment.html', 'w')

    # write each section (csv key, webpage heading, list id)
    write_section('Characterization', 'Characterization', 'list-charac', data, f)
    write_section('Computer / Software', 'Computer / Software', 'list-software', data, f)
    write_section('Welding', 'Welding', 'list-weld', data, f)

    # write_section('Computer', 'Computer', 'list-computer', data, f)
    # write_section('Laserlab', 'Laserlab', 'list-laser', data, f)
    # write_section('Manufacturing', 'Manufacturing', 'list-manufac', data, f)
    # write_section('Metallography', 'Metallography', 'list-metal', data, f)
    # write_section('Storage Room Equipment', 'Storage', 'list-storage', data, f)
    

    # close file
    f.close()

def write_section(csv_key, section_title, section_id, data, f):
    f.write('<h4>' + section_title + '</h4>\n')
    f.write('<div class="row mb-2">\n\n')

    for index, row in data.iterrows(): # go through each row
        if row['Category'] == csv_key and row['Include on website'] == 'Yes':
            name = row['Equipment']
            called = row['"Called"']
            print(called)
            f.write('<div class="col-lg-4 col-md-6">\n<div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm bg-white h-md-200 position-relative">\n<div class="col p-4 d-flex flex-column position-static">\n')
            f.write('<strong class="d-inline-block mb-0 text-success">' + section_title + '</strong>\n')
            f.write('<h5 class="mb-3">'+ name +'</h5>\n')

            # description
            desc = ''
            f.write('<p class="card-text mb-auto">' + desc + '</p>\n</div>\n')

            # find and write photo
            equipment_folder = '../Assets/Equipment_Photos/' # folder containing all photos
            
            img_path = ''
            #img_path = '../Assets/hitachiTIG.png' # default picture
            for filename in os.listdir(equipment_folder):
                if filename.startswith(row['Code']):
                    img_path = equipment_folder + filename
            if img_path:
                f.write('<div class="equipment-pic col-auto d-flex overflow-hidden">\n<img class="fill-img" src="' + img_path + '" alt="pic">\n</div>\n')
            
            f.write('</div>\n</div>\n')

    f.write('</div>')




