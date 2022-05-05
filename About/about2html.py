#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script reads the input excel sheet to generate a html file for each subpage under
# the About Us tab
#
# to run in python prompt
# import about2html
# about2html.about2html('../CCWJ_Website.xlsx')

import csv
import os
from datetime import datetime
import pandas as pd



def about2html(excel_path):
    # read sheet named About_Us in excel file (About Us)
    data = pd.read_excel(excel_path, sheet_name="About_Us")
    data.fillna('', inplace=True)
        
    

    # write each section (section name, data)
    for index, section in data.iterrows():
        if section['Section'].startswith('Advisory Boards'):
            # write special advisory page
            write_advisory(section['Section'], section)
        elif section['Section'].startswith('Sponsors'):
            # write special sponsors page
            write_sponsors(section['Section'], section)
        else:
            # write default page format
            write_section(section['Section'], section)
    

def write_section(section_name, section):
    print(section)
    # make filename the first word of section name, keeping only alphanumeric characters
    filename = "".join(x for x in section_name.split()[0] if x.isalnum()) + '-text.html'
    
    # open file to write into
    f = open(filename, 'w')
    
    for header, value in section.items():
        
        if not value or value == 'LINK_TO_TAB': # if entry is empty skip header
            continue

        if header.startswith('Section_Heading_1'):
            f.write('<h2 class="subheading subheading1">' + value + '</h2>\n')
            
        elif header.startswith('Section_Heading'):
            f.write('<h4 class="subheading">' + value + '</h4>\n')
            
        elif header.startswith('Text_Block'):
            text = value.strip('\n').replace('\n', '<br>') # preserve newlines in html
            f.write('<p>' + text + '</p>')
            
        elif header.startswith('Image'):
            # get image path, look in Assets/About_Us folder and section_name (with underscores) subfolder 
            img_folder = os.path.join('../Assets/About_Us/', section_name.replace(' ', '_'))
            img_path = ''
            for filename in os.listdir(img_folder):
                if filename.startswith(value):
                    img_path = os.path.join(img_folder,filename)
            if img_path:
                # write image html
                f.write('<img src="' + img_path + '" class="img-scale mx-auto d-block">\n')
            else:
                print('cannot find image ' + value)


    f.close()
    
def write_advisory(section_name, section):
    print('write boards')

def write_sponsors(section_name, section):
    print('write sponsors')

#about2html('../CCWJ_Website.xlsx')




