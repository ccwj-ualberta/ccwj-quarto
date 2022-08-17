#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script reads the input excel sheet to generate a html file for each subpage under
# the teaching tab
# All handouts/notes/supplementary materials should be 
#
# to run in python prompt
# import teaching2html
# teaching2html.teaching2html('../CCWJ_Website.xlsx')

import os
import pandas as pd
import numpy as np


def teaching2html(excel_path):
    # read sheet named Teaching in excel file 
    data = pd.read_excel(excel_path, sheet_name="Teaching")
    data.fillna('', inplace=True)
        
    

     # write each section (section name, data)
    for index, row in data.iterrows():
        if row['Section']:
            write_section(row['Section'], data, index)
            
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
                  <a class="nav-link active" aria-current="page" href="../Teaching/teaching.html">Teaching</a>
                  <a class="nav-link" href="../Resources/resources.html">Resources</a>
                  <a class="nav-link" href="../Join/joinus.html">Join us</a>
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
    
    # write left navbar for page sections
    nav_template = """    
        <main class="container-fluid d-flex flex-column flex-grow-1">
            <div class="row flex-fill d-flex">
                <div class="col-lg-2 border-end sidebar flex-grow-1">
                  <div id="nav-sidebar" class="list-group list-group-flush sticky-top"> """
                  
    f.write(nav_template)
                  
    sections = data.loc[:, 'Section'].replace('', np.nan).dropna()
    for section in sections[1:]:
        # use the first two words in section name as html file name
        nickname = "".join(x.lower() for x in section.split()[:2] if x.isalnum())
        f.write('<a class="list-group-item list-group-item-action" href="./' + nickname + '.html">' + section + '</a>\n')
    
        
    f.write('</div>\n</div>\n')
            


def write_section(section_name, data, index_start):
    # make filename the first two words of section name, keeping only alphanumeric characters
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
                f.write('<h4>' + value + '</h4>\n')
                
            elif header.startswith('Text_Block') and value:
                text = value.strip('\n').replace('\n', '<br>') # preserve newlines in html
                num = header.split('_')[-1] # gets text block number
                if row['Link_' + num]: # if Link exists, link to text block
                    f.write('<p><a href="' + row['Link_' + num] + '">' + text + '</a></p>\n')
                else:
                    f.write('<p>' + text + '</p>\n')
                
            elif header.startswith('Image') and value:
                # get image path, look in Assets/Teaching folder and section_name (with underscores) subfolder 
                img_folder = os.path.join('../Assets/Teaching/', section_name.replace(' ', '_'))
                img_path = ''
                for filename in os.listdir(img_folder):
                    if filename.startswith(value):
                        img_path = os.path.join(img_folder,filename)
                if img_path:
                    # write image html
                    f.write('<img src="' + img_path + '" class="img-scale mx-auto d-block">\n')
                else:
                    print('cannot find image ' + value)

            elif header.startswith('Video') and value:
                link = value
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
            
            elif header.startswith('Topic_Order') and value:
                # arrange teaching content/slides/handouts under each topic
                write_topics(row['Topic_Folder'], row['Topic_Order'], f)

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


def write_topics(folder_name, course_order, f):
    # folder that contains the class folder on website
    site_url = 'https://sites.ualberta.ca/~ccwj/test-content/Teaching/'

    # path to teaching folder (where this script is located)
    dir_path = os.path.dirname(os.path.realpath(__file__))

    for code in course_order.split(): # go through each topic code in course_order
        for topic_folder in os.scandir(os.path.join(dir_path,folder_name)): 
            topic_code = topic_folder.name.split('_')[0]
            if topic_code == code: # find folder according to code
                topic_name = topic_folder.name.split('_', 1)[1].replace('_', ' ') # get displayable topic name
                topic_html_id = topic_folder.name.split('_', 1)[1].lstrip('0123456789') # create html id for each topic, removing numbers from beginning
                needs_divider = False # check if | is needed between items

                f.write('<div class="topic-header"><h5>' + str(topic_name) + '</h5>\n') # writes topic title
                
                # writes slide pdf
                for entry in os.scandir(topic_folder):
                    if entry.name.startswith('Slides'): # look for slides as a .pdf in Slides folder
                        for file in os.scandir(entry.path):
                            if file.name.endswith('.pdf'):
                                f.write('<a target="_blank" href="' + site_url + folder_name + '/' + topic_folder.name + '/' + entry.name + '/' + file.name + '">Slides</a>')
                                needs_divider = True
                    elif entry.name.startswith(code) and entry.name.endswith('.pdf'): # look for slides as .pdf in the topic_folder
                        f.write('<a target="_blank" href="' + site_url + folder_name + '/' + topic_folder.name + '/' + entry.name + '">Slides</a>')
                        needs_divider = True
                
                # writes handout pdf
                for entry in os.scandir(topic_folder): 
                    if entry.is_dir() and entry.name.startswith('Handout'): # look for handout folder
                        for x in os.scandir(entry.path + '/LaTex/'):
                            if x.name.endswith('.pdf'):
                                href = site_url + folder_name + '/' + topic_folder.name + '/' + entry.name + '/LaTex/' + x.name
                                if needs_divider:
                                    f.write(' | ')
                                f.write('<a target="_blank" href="' + href + '">Handout</a>')
                                needs_divider = True
                    if entry.is_dir() and entry.name.startswith('Supplemental_Material'): # look for supplemental material
                        if needs_divider:
                            f.write(' | ')
                        f.write('<a data-bs-toggle="collapse" href="#' + topic_html_id + '_s' + '" role="button" aria-expanded="false" aria-controls="'+ topic_html_id + '_s' +'">Supplemental Material</a>')
                        needs_divider = True

                # write the dropdown boxes
                for entry in os.scandir(topic_folder):

                    if entry.is_dir() and entry.name.startswith('Supplemental_Material'): # search for supplemental material folder
                        count = 0
                        for x in os.scandir(entry.path):
                            if x.name.endswith('.pdf'): # write all .pdfs in the Supplemental Material folder
                                if count == 0: # write button and create div for links
                                    f.write('\n<div class="collapse indent" id="' + topic_html_id + '_s' + '">')
                                    count = 1

                                # write link
                                href = site_url + folder_name + '/' + topic_folder.name + '/' + entry.name + '/' + x.name
                                f.write('<a target="_blank" href="' + href + '">' + x.name.replace('_', ' ') + '</a><br>\n')
                        f.write('</div>\n')

                f.write('</div>\n')



