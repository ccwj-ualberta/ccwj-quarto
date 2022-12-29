# This script reads the input excel sheet to generate a html file for each subpage under
# the Research tab
#
# to run in python prompt
# import research2html
# research2html.research2html('../CCWJ_Website.xlsx')

import os
import pandas as pd
import numpy as np


excel_path = '../CCWJ_Website.xlsx'
def research2html(excel_path):
    # read sheet named researchin excel file
    data = pd.read_excel(excel_path, sheet_name="Research")
    data.fillna('', inplace=True)
        
    
    # write each section (section name, data)
    for index, section in data.iterrows():
        if section['Section']:
            write_section(section['Section'], data, index)
    
    print('research2html complete')


def write_section(section_name, data, index_start):
    print('research: writing ' + section_name)

    # make filename the first word of section name, keeping only alphanumeric characters
    filename = "".join(x.lower() for x in section_name.split()[:2] if x.isalnum()) + '.html'
    
    # open file to write into
    f = open(filename, 'w')

    # write starting section
    write_page_beginning(section_name, data, f)

    # write section name
    f.write('<div class="col p-3 pt-4 order-sm-last content-container">\n')
    f.write('<h2 class="subheading subheading1">' + section_name + '</h2>\n')
    
    # go through each row in the sheet
    for i, row in data.iloc[index_start:].iterrows():
        
        # detect if next section has been reached, if so stop writing section
        if row['Section'] and row['Section'] != section_name:
            break
        
        # go through each column for the row
        for header, value in row.items():
            
            if value == 'LINK_TO_TAB':
                if section_name == 'Publications':
                    f.write('<div id="bib-html" class="pe-md-5 me-md-5"></div>\n')
                elif section_name == 'Posters':
                    f.write('<div id="posters-embed-html"></div>\n')
                continue

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
                    
            elif header.startswith('Sponsor') and value:
                sponsor_num = header.split('_')[-1]
                
                if sponsor_num == '1': # for first sponsor create row div
                    f.write('<div class="row mb-2 mt-1">\n\n')
                
                f.write('<div class="col-lg-4 col-md-6">\n<div class="row g-0 border rounded overflow-hidden flex-md-row mb-4 shadow-sm bg-white h-md-200 position-relative">\n<div class="col p-4 d-flex flex-column position-static">\n')
                f.write('<h5 class="mb-3">'+ value +'</h5>\n</div>\n')
                
                if row['Logo_Sponsor_' + sponsor_num]:
                    # find and write photo
                    pic_folder = '../Assets/About_Us/Sponsors_Logos/' # folder containing all photos
                    
                    img_path = ''
                    for filename in os.listdir(pic_folder):
                        if filename.startswith(row['Logo_Sponsor_' + sponsor_num]):
                            img_path = pic_folder + filename
                    if img_path:
                        f.write('<div class="card-pic col-auto d-flex overflow-hidden p-3">\n<img class="fill-img" src="' + img_path + '" alt="pic">\n</div>\n')
                
                f.write('</div>\n</div>\n')
                
                # for last sponsor close row div
                next_sponsor = 'Sponsor_' + str(int(sponsor_num) + 1)
                if not row[next_sponsor]:
                    f.write('</div>\n\n')
                
            elif header.startswith('Presenter') and value:
                f.write('<p>Presenter: ' + value.strip('\n').replace('\n', '<br>') + '</p>\n')
                
            elif header.startswith('Video') and value:
                # only keep first 11 characters after watch?v= to get video id
                video_id = value.split("watch?v=")[1][:11]
                
                f.write('<iframe width="560" height="315" src="https://www.youtube.com/embed/' + video_id + '" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n')

                # <iframe src="https://drive.google.com/file/d/1bEoXR0wJZqaYtEoKP4B5z1C0qSBY9q1P/preview" width="640" height="480" allow="autoplay"></iframe>

    f.write('</div>\n')

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

    
def write_page_beginning(section_name, data, f):
    
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
        """
    f.write(template)

    # import html for publications
    if section_name == 'Publications':
        f.write('<script>$(function () { $("#bib-html").load("./bib.html"); });</script>\n')
    elif section_name == 'Posters':
        f.write('<script>$(function () { $("#posters-embed-html").load("./posters-embed.html"); });</script>\n')

    template2 = """
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
                  <a class="nav-link active" aria-current="page" href="../Research/research.html">Research</a>
                  <a class="nav-link" href="../Teaching/teaching.html">Teaching</a>
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
    f.write(template2)
    
    # create subpage navbar on the left
    nav_template = """    
        <main class="container-fluid d-flex flex-column flex-grow-1">
            <div class="row flex-fill d-flex">
                <div class="col-lg-2 border-end sidebar flex-grow-1">
                  <div id="nav-sidebar" class="list-group list-group-flush sticky-top"> 
                  """
                  
    f.write(nav_template)
                  
    sections = data.loc[:, 'Section'].replace('', np.nan).dropna()
    for section in sections[1:]: # go through each section, skipping the first one
        # name for html file is first two words of section name, lowercase and no spaces
        nickname = "".join(x.lower() for x in section.split()[:2] if x.isalnum())
        f.write('<a class="list-group-item list-group-item-action" href="./' + nickname + '.html">' + section + '</a>\n')
    
        
    f.write('</div>\n</div>\n')
