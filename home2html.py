# This script reads the input excel sheet to generate a html file for 
# the Home tab
#
# to run in python prompt
# import home2html
# home2html.home2html('./CCWJ_Website.xlsx')

import os
import pandas as pd


excel_path = '../CCWJ_Website.xlsx'
def home2html(excel_path):
    # read sheet named Home in excel file
    data = pd.read_excel(excel_path, sheet_name="Home")
    data.fillna('', inplace=True)

    # open file to write into
    f = open("./home-text.html", 'w')
    
    write_carousel(data, f)


    f.write('<!-- Text below -->\n<div class="p-4">\n')

    # write each section 
    for index, section in data.iterrows():
        if section['Section']:
            write_section(section['Section'], data, index, f)

    f.write('</div>')
    f.close()

def write_carousel(data, f):
    count = 0

    carousel_imgs = data.loc[:,data.columns.str.startswith('Carousel')].squeeze().tolist()

    f.write('<!-- Carousel -->\n')
    f.write('<div id="carousel" class="carousel slide ratio-16x9" data-bs-ride="carousel">\n')
    f.write('<div class="carousel-inner">\n')

    for img_name in carousel_imgs:
        if img_name:
            count += 1
            
            print(img_name)
            # get image path, look in Assets/Home folder 
            img_folder = './Assets/Home/'
            img_path = ''
            for filename in os.listdir(img_folder):
                if filename.startswith(img_name):
                    img_path = os.path.join(img_folder,filename)
                    
            if img_path:
                # write image html if image found
                
                if count == 1: # make first image active
                    f.write('<div class="carousel-item active" data-bs-interval="4000">\n')
                else:
                    f.write('<div class="carousel-item" data-bs-interval="4000">\n')
                    
                f.write('<img src="' + img_path + '" class="d-block w-100">\n')
                f.write('</div>\n')
                
            else:
                print('cannot find image ' + img_name)

    f.write('</div>\n')

    # arrows to control carousel
    f.write("""<button class="carousel-control-prev" type="button" data-bs-target="#carousel" data-bs-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#carousel" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>\n""")
    
    f.write('</div>\n')


def write_section(section_name, data, index_start, f):
    # write section title
    f.write('<h1>' + section_name + '</h1>\n')
    
    # go through each row in the sheet starting from index_start
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
                f.write('<p>' + text + '</p>\n')
                
            elif header.startswith('Image') and value:
                # get image path, look in Assets/Home folder 
                img_folder = './Assets/Home/'
                img_path = ''
                for filename in os.listdir(img_folder):
                    if filename.startswith(value):
                        img_path = os.path.join(img_folder,filename)
                if img_path:
                    # write image html
                    f.write('<img src="' + img_path + '" class="img-scale mx-auto d-block">\n')
                else:
                    print('cannot find image ' + value)
                    
                    
                    
           


    
