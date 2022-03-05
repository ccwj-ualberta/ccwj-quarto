"""
Convert course material to html divs that can be custom formatted using CSS.
Will create 

Usage (from Python or IPython prompt):

    >> import course2html
    >> course2html.course2html('MATE481')

"""

import os
import json

# the code each topic folder name starts with. Topics will be listed in this order
MATE481 = 'ITW CON SAF TER SYM WPA WPB WPR WPS WPC WPZ NWC FLX CWP BCS HRD SWM HAZ BSS ARC VAW MTR DAW MAS EFI TEM WEP DES DFW RES NDT CNS OVR'
CHE314 = '1 2 3 4 5 6 7 8 9 10 11 12 13 14'
COURSE_ORDER = MATE481 # default course order

# folder that contains the class folder
site_url = 'https://sites.ualberta.ca/~ccwj/test-content/Teaching/'



def course2html(folder_name):

    # open file to write into
    f = open(folder_name + '.html', 'w')

    # pick appropriate course order
    if folder_name == 'MATE481':
        COURSE_ORDER = MATE481
    elif folder_name == 'CHE314':
        COURSE_ORDER = CHE314

    for code in COURSE_ORDER.split(): # go through each topic code in COURSE_ORDER
        for topic_folder in os.scandir(os.path.join(os.getcwd(),folder_name)): 
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
                    # if entry.is_dir() and entry.name.startswith('Handout'): # search for handout folder
                    #     count = 0
                    #     for x in os.scandir(entry.path + '/LaTex/'):
                    #         if x.name.endswith('.pdf'): # write all .pdfs in folder /Handout/LaTeX/
                    #             if count == 0: # write button and create div for links
                    #                 f.write('\n<div class="collapse indent" id="' + topic_html_id + '_h' + '">')
                    #                 count = 1

                    #             # write link
                    #             href = site_url + folder_name + '/' + topic_folder.name + '/' + entry.name + '/LaTex/' + x.name
                    #             f.write('<a href="' + href + '">' + x.name.replace('_', ' ') + '</a><br>\n')
                    #     f.write('</div>\n')

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


    f.close()
