
# to run in python prompt
# import people2html
# people2html.people2html('/Users/Cotton/Desktop/CCWJ_site_bootstrap/People/bioform3.csv')

import csv
import os
csv_path = '/Users/Cotton/Desktop/CCWJ_site_bootstrap/bioforms.csv'

def people2html(csv_path):
    # parse csv here
    with open(csv_path, 'r', encoding='utf8') as file:
        reader = csv.reader(file)
        data = list(reader)
 
        print(data[1])

    # open file
    f = open('bios.html', 'w')

    # write each section (csv key, webpage heading, list id)
    write_section('Staff', 'Staff', 'list-staff', data, f)
    write_section('Post-Doc', 'Postdoctorate Fellows', 'list-postdoc', data, f)
    write_section('PhD student', 'PhD Students', 'list-phd', data, f)
    write_section('Master\'s student', 'MSc Students', 'list-msc', data, f)
    write_section('Bachelor\'s student', 'BSc Students', 'list-bsc', data, f)
    write_section('Visitor', 'Visitors', 'list-visitors', data, f)
    write_section('External', 'External', 'list-external', data, f)
    write_section('Alumnus', 'Alumni', 'list-alumni', data, f)
    
    

    # close file
    f.close()

def write_section(csv_key, section_title, section_id, data, f):
    f.write('<h2 class="subheading" id="' + section_id + '">' + section_title + '</h2>\n')
    f.write('<div class="row pb-3">')
    for entry in data:
        if entry[6] == csv_key: # type of involvement should match
            f.write('<div class="col-12 pb-3">\n')

            # look for picture with matching ID number
            portraits_folder = '../Assets/portraits/'
            for filename in os.listdir(portraits_folder):
                if filename.startswith(str(entry[2])):
                    f.write('<div class="person-pic">\n')
                    f.write('<img src="' + portraits_folder + filename + '" class="img-fluid" alt="bio_picture">\n</div>\n')

            f.write('<div class="person">\n')
            # given name, family name, and degree
            f.write('<p><b>' + str(entry[3]).strip() + ' ' + str(entry[4]) + '</b><br>'+ str(entry[7]) + '</p>\n')
            # email in both spots
            f.write('<p>email: <br><a href="mailto:'+ str(entry[1]) +'">' + str(entry[1]) + '</a></p>\n')
            # bio
            f.write('<p>' + str(entry[11].strip('\n').replace('\n', '<br>')) + '</p>\n')
            f.write('</div>\n</div>\n\n')
    f.write('</div>')


