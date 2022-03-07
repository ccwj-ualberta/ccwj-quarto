#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script reads the input excel sheet to generate a html file 
#
# to run in python prompt
# import about2html
# about2html.about2html('../CCWJ_Website.xlsx')

import csv
import os
from datetime import datetime
import pandas as pd



def about2html(excel_path):
    # read 2nd sheet in excel file (About Us)
    data = pd.read_excel(excel_path, sheet_name=1)
    data.fillna('', inplace=True)
        
    

    # write each section (section name, data)
    for index, section in data.iterrows():
        if section['Section'].startswith('Advisory Boards'):
            # write advisory
            write_advisory(section['Section'], section)
        elif section['Section'].startswith('Sponsors'):
            # write sponsors
            write_sponsors(section['Section'], section)
        else:
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

        if header.startswith('Section Heading 1'):
            f.write('<h2 class="subheading subheading1">' + value + '</h2>\n')
        elif header.startswith('Section Heading'):
            f.write('<h4 class="subheading">' + value + '</h4>\n')
        elif header.startswith('Text Block'):
            text = value.strip('\n').replace('\n', '<br>') # preserve newlines in html
            f.write('<p>' + text + '</p>')

    f.close()
    
def write_advisory(section_name, section):
    print('write boards')

def write_sponsors(section_name, section):
    print('write sponsors')

about2html('../CCWJ_Website.xlsx')




