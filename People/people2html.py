
# to run in python prompt
# import people2html
# people2html.people2html('/Users/Cotton/Desktop/CCWJ_site_bootstrap/People/bioform3.csv')

import csv
import os
from datetime import datetime
# csv_path = '/Users/Cotton/Desktop/CCWJ_site_bootstrap/bioforms.csv'

def people2html(csv_path):
    # parse csv here
    with open(csv_path, 'r', encoding='utf8') as file:
        reader = csv.reader(file)
        raw_data = list(reader)[1:] # skip the first line of headers
 
    # take most recent entry for duplicates (key column to use for comparison, data)
    data = remove_old_duplicates(2, raw_data)
        

    # open file to write into
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

def remove_old_duplicates(key_col, data):
    indices_to_remove = []
    for count, entry in enumerate(data):
        print('looking at ' + str(count))
        key = entry[key_col]
        for count2, x in enumerate(data):
            entry_time = datetime.strptime(entry[0], '%m/%d/%Y %H:%M:%S') # converts timestamps into datetime objects
            x_time = datetime.strptime(x[0], '%m/%d/%Y %H:%M:%S')
            if x[key_col] == key and entry_time <= x_time and count < count2: # if IDs match and current timestamp is less or equal
                indices_to_remove.append(count) # add index to be removed
                print(str(count) + ' entry is an old duplicate and will be removed')
                break # no need to look further

    # remove all the duplicate entries
    filtered_data = [entry for count, entry in enumerate(data) if count not in indices_to_remove]
    return filtered_data


def write_section(csv_key, section_title, section_id, data, f):
    f.write('<h2 class="subheading" id="' + section_id + '">' + section_title + '</h2>\n')
    f.write('<div class="row pb-3">')
    for entry in data:
        if entry[6] == csv_key and entry[15] not in ['x','X']: # type of involvement should match and entry included

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
            if str(entry[8]) not in ['N/A', 'none', 'None', 'n/a', '', ' ']:
                f.write('<p>Prior degrees: ' + str(entry[8]) + '</p>\n')

            # email in both spots
            f.write('<p>email: <a href="mailto:'+ str(entry[1]) +'">' + str(entry[1]) + '</a></p>\n')
            # bio
            f.write('<p>' + str(entry[11].strip('\n').replace('\n', '<br>')) + '</p>\n')

            if str(entry[12]) not in ['']:
                # project/thesis
                f.write('<p>Project: ' + str(entry[12]) + '<br>' + str(entry[13].strip('\n').replace('\n', '<br>'))+ '</p>\n')
            elif str(entry[9]) not in ['']:
                # description of your project
                f.write('<p>Project: ' + str(entry[9].strip('\n').replace('\n', '<br>')) + '</p>\n')

            f.write('</div>\n</div>\n\n')
    f.write('</div>')



