# This script reads the input excel sheet to generate a html file for each subpage under
# the Resources/gallery tab
#
# to run in python prompt
# import gallery2html
# gallery2html.gallery2html('../CCWJ_Website.xlsx')

import csv
import os
from datetime import datetime
import pandas as pd


excel_path = '../CCWJ_Website.xlsx'

def gallery2html(excel_path):
    # read sheet named resources_gallery excel file
    data = pd.read_excel(excel_path, sheet_name="Resources_Gallery")
    data.fillna('', inplace=True)
        

    # make filename the first word of section name, keeping only alphanumeric characters
    filename = 'gallery-modal.html'
    
    # open file to write into
    f = open(filename, 'w')
    
    f.write('<div class="row" id="gallery" data-bs-toggle="modal" data-bs-target="#exampleModal">\n')
    
    # write gallery images (section name, data)
    for index, row in data.iterrows():
        
        if row['Image_Code']:
            
            # find and write photo
            pic_folder = '../Assets/Resources/Gallery/' # folder containing all photos
            
            img_path = ''
            for filename in os.listdir(pic_folder):
                if filename.startswith(row['Image_Code']):
                    img_path = pic_folder + filename
                    
            if img_path:
                f.write('<div class="col-12 col-sm-6 col-lg-3 mb-3">\n')
                f.write('<img class="w-100" src="' + img_path + '" data-bs-target="#carouselExample" data-bs-slide-to="' + str(index) + '">\n')
                f.write('</div>\n')
    
    f.write('</div>\n\n <!--Modal--> \n')
    
    # write modal with carousel
    f.write('<div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-hidden="true">\n<div class="modal-dialog" role="document">\n')
    f.write('<div class="modal-content">\n<div class="modal-header">\n')
    f.write('<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\n</div>\n')
    
    f.write('<div class="modal-body">\n<div id="carouselExample" class="carousel slide" data-bs-ride="carousel">\n<div class="carousel-inner">\n')
    
    for index, row in data.iterrows():
        if index == 0:
            f.write('<div class="carousel-item active">')
        else:
            f.write('<div class="carousel-item">')
            
        if row['Image_Code']:
             # find and write photo
            pic_folder = '../Assets/Resources/Gallery/' # folder containing all photos
            
            img_path = ''
            for filename in os.listdir(pic_folder):
                if filename.startswith(row['Image_Code']):
                    img_path = pic_folder + filename
                    
            if img_path:
                f.write('<img class="d-block w-100" src="' + img_path + '">')
        
        if row['Heading']:
            f.write('<h5>' + row['Heading'] + '</h5>\n')
            
        if row['Description']:
            text = row['Description'].strip('\n').replace('\n', '<br>') # preserve newlines in html
            f.write('<p>' + text + '</p>\n')
        f.write('</div>\n')
        
    f.write('</div>\n<a class="carousel-control-prev" href="#carouselExample" role="button" data-bs-slide="prev">\n')
    f.write('<span class="carousel-control-prev-icon" aria-hidden="true"></span>\n</a>\n')
    f.write('<a class="carousel-control-next" href="#carouselExample" role="button" data-bs-slide="next">\n')
    f.write('<span class="carousel-control-next-icon" aria-hidden="true"></span>\n')
    f.write('</a>\n</div>\n</div>\n</div>\n</div>\n</div>')
    
    
    f.close()





    
