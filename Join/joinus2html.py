#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script reads the input excel sheet to generate a html file for each subpage under
# the Join Us tab
#
# to run in python prompt
# import joinus2html
# joinus2html.joinus2html('../CCWJ_Website.xlsx')

import os
import pandas as pd
import numpy as np



def joinus2html(excel_path):
    # read sheet named Join_us in excel file (Join Us)
    data = pd.read_excel(excel_path, sheet_name="Join_Us")
    data.fillna('', inplace=True)
        
     # write each section (section name, data)
    for index, row in data.iterrows():
        if row['Section']:
            write_section(row['Section'], data, index)
    
    print('joinus2html complete')
            
def write_page_beginning(section_name, data, index_start, f):
    
    template = """
    <!doctype html>
    <html lang="en">
      <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    
        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" crossorigin="anonymous">
        <!-- Bootstrap CSS icons -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css">
    
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script>$(function () { $("#footer").load("../footer.html"); });</script>
        <script src="https://cse.google.com/cse.js?cx=805eed77643236949"></script>
    
        <title>CCWJ</title>
        <link href="../index.css" rel="stylesheet">
      </head>
    
    
      <body class="d-flex flex-column min-vh-100" style="position:relative;">
        <nav class="navbar navbar-expand-lg navbar-dark fixed-top"> <!-- include fixed-top to stick it -->
          <div class="container-fluid">
            <a class="navbar-brand" href="#"><img src="../Assets/CCWJ_white_logo.png" height="70"></a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse pt-2" id="navbarCollapse">
              <div class="navbar-nav ms-auto me-4">
                  <a class="nav-link" href="../index.html">Home</a>
                  <a class="nav-link" href="../About/about.html">About Us</a>
                  <a class="nav-link" href="../People/people.html">People</a>
                  <a class="nav-link" href="../Research/research.html">Research</a>
                  <a class="nav-link" href="../Teaching/teaching.html">Teaching</a>
                  <a class="nav-link" href="../Resources/resources.html">Resources</a>
                  <a class="nav-link active" aria-current="page" href="../Join/joinus.html">Join us</a>
              </div>
              <form class="d-flex justify-content-start">
                <div class="search-container">
                  <div class="gcse-searchbox-only"></div>
                </div>
              </form>
            </div>
          </div>
      </nav>
    
    """
    f.write(template)
    
    nav_template = """    
        <main class="container-fluid d-flex flex-column flex-grow-1">
            <div class="row flex-fill d-flex">
                <div class="col-lg-2 border-end sidebar flex-grow-1">
                  <div id="nav-sidebar" class="list-group list-group-flush sticky-top"> """
                  
    f.write(nav_template)
                  
    sections = data.loc[:, 'Section'].replace('', np.nan).dropna()
    for section in sections[1:]:
        nickname = "".join(x.lower() for x in section.split()[:2] if x.isalnum())
        f.write('<a class="list-group-item list-group-item-action" href="./' + nickname + '.html">' + section + '</a>\n')
    
        
    f.write('</div>\n</div>\n')
            


def write_section(section_name, data, index_start):
    # make filename the first word of section name, keeping only alphanumeric characters
    filename = "".join(x.lower() for x in section_name.split()[:2] if x.isalnum()) + '.html'
    
    # open file to write into
    f = open(filename, 'w')
    
    write_page_beginning(section_name, data, index_start, f)
    
    # write section name
    f.write('<div class="col p-3 pt-4 order-sm-last">')
    f.write('<h2 class="subheading subheading1">' + section_name + '</h2>')
    
    # go through each row in the sheet
    for i, row in data.iloc[index_start:].iterrows():
        
        # detect if next section has been reached, if so stop writing section
        if row['Section'] and row['Section'] != section_name:
            break
        
        # go through each column for the row
        for header, value in row.items():
    
            if header.startswith('Section_Heading') and value:
                
                # make header a link if applicable
                if row['Link']:
                    f.write('<h4><a href="' + row['Link'] + '" target="_blank">' + value + '</a></h4>\n')
                else:
                    f.write('<h4>' + value + '</h4>\n')
                
            elif header.startswith('Text_Block') and value:
                text = value.strip('\n').replace('\n', '<br>') # preserve newlines in html
                f.write('<p>' + text + '</p>\n')
                
            elif header.startswith('Image') and value:
                # get image path, look in Assets/Research folder and section_name (with underscores) subfolder 
                img_folder = os.path.join('../Assets/Join_Us/', section_name.replace(' ', '_'))
                img_path = ''
                for filename in os.listdir(img_folder):
                    if filename.startswith(value):
                        img_path = os.path.join(img_folder,filename)
                if img_path:
                    # write image html
                    f.write('<img src="' + img_path + '" class="img-scale mx-auto d-block">\n')
                else:
                    print('cannot find image ' + value)
                
    f.write('</div>')
    
    ending = """
             </div>
        </main>
        
        <div id="footer"></div>
    
    
        <!-- Option 1: Bootstrap Bundle with Popper -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-gtEjrD/SeCtmISkJkNUaaKMoLD0//ElJ19smozuHV6z3Iehds+3Ulb9Bn9Plx0x4" crossorigin="anonymous"></script>
    
       
      </body>
    </html>"""
    
    f.write(ending)

    f.close()



