
# to run in python prompt
# import people2html
# people2html.people2html('../CCWJ_Website.xlsx')

import os
from datetime import datetime
import pandas as pd

def people2html(excel_path):

    raw_data = pd.read_excel(excel_path, sheet_name='People')
    raw_data.fillna('', inplace=True)
 
    # take most recent entry for duplicates (key column to use for comparison, data)
    data = remove_old_duplicates(2, raw_data)
        

    # open file to write into
    f = open('bios.html', 'w')

    # write each section (section key, webpage heading, list id, data, file)
    write_section('CCWJ Director', 'CCWJ Director', 'list-director', data, f)
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
    for count, entry in data.iterrows():
        
        key = entry.iloc[key_col] # person's ID
        #print('looking at ' + str(count) + ' key ' + str(key))
        for count2, x in data.iterrows():
            if count == count2: 
                continue # skip self-counting
            #entry_time = pd.to_datetime(entry.iloc[0], unit='s')
            #x_time = pd.to_datetime(x.iloc[0], unit='s')
            #entry_time = datetime.strptime(entry.iloc[0], '%m/%d/%Y %H:%M:%S') # converts timestamps into datetime objects
            #x_time = datetime.strptime(x.iloc[0], '%m/%d/%Y %H:%M:%S')
            entry_time = entry.iloc[0]
            x_time = x.iloc[0]
            if x.iloc[key_col] == key:
                if x.iloc[key_col] == key and entry_time <= x_time: # if IDs match and current timestamp is less or equal
                    indices_to_remove.append(count) # add index to be removed
                    print(str(count) + ' entry is an old duplicate and will be removed')
                    break # no need to look further

    # remove all the duplicate entries
    filtered_data = data.drop(data.index[indices_to_remove])

    # filtered_data = [entry for count, entry in enumerate(data) if count not in indices_to_remove]
    return filtered_data


def write_section(section_key, section_title, section_id, data, f):
    f.write('<h2 class="subheading" id="' + section_id + '">' + section_title + '</h2>\n')
    f.write('<div class="row pb-3">')
    for i, entry in data.iterrows():

        if entry.iloc[6] == section_key and entry.iloc[15] not in ['x','X']: # type of involvement should match and entry included

            f.write('<div class="col-12 pb-3">\n')

            # look for picture with matching ID number
            portraits_folder = '../Assets/Member_Photos/'
            for filename in os.listdir(portraits_folder):
                if filename.startswith(str(entry.iloc[2])):
                    f.write('<div class="person-pic">\n')
                    f.write('<img src="' + portraits_folder + filename + '" class="img-fluid" alt="bio_picture">\n</div>\n')
                    break

            f.write('<div class="person">\n')
            # given name, family name, and degree
            f.write('<p><b>' + str(entry.iloc[3]).strip() + ' ' + str(entry.iloc[4]) + '</b><br>'+ str(entry.iloc[7]) + '</p>\n')
            if str(entry.iloc[8]) not in ['N/A', 'none', 'None', 'n/a', '', ' ']:
                f.write('<p>Prior degrees: ' + str(entry.iloc[8]) + '</p>\n')

            # email in both spots
            f.write('<p>email: <a href="mailto:'+ str(entry.iloc[1]) +'">' + str(entry.iloc[1]) + '</a></p>\n')
            # bio
            f.write('<p>' + str(str(entry.iloc[11]).strip('\n').replace('\n', '<br>')) + '</p>\n')

            if str(entry.iloc[12]) not in ['']:
                # project/thesis
                f.write('<p>Project: ' + str(entry.iloc[12]) + '<br>' + str(str(entry.iloc[13]).strip('\n').replace('\n', '<br>'))+ '</p>\n')
            elif str(entry.iloc[9]) not in ['']:
                # description of your project
                f.write('<p>Project: ' + str(str(entry.iloc[9]).strip('\n').replace('\n', '<br>')) + '</p>\n')

            f.write('</div>\n</div>\n\n')
    f.write('</div>')



