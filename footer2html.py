
# to run in python prompt
# import footer2html
# footer2html.footer2html('../CCWJ_Website.xlsx')

import csv
import os
from datetime import datetime
import pandas as pd

def footer2html(excel_path):
    
    raw_data = pd.read_excel(excel_path, sheet_name='Footer')
    raw_data.fillna('', inplace=True)
    #print(raw_data)
    keep_writing = False
            
    # open file to write into
    f = open('footer.html', 'w')
    
    f.write('<footer class="footer mt-auto py-3 container-fluid border-top">\n')
    f.write('<div class="container-fluid">\n<div class="row">\n')
    f.write('<div class="col-lg-2 text-center pb-3"></div>\n')
    
    
    for i, entry in raw_data.iterrows():
        if entry.eq('').all(): # if row is empty, stop writing section or skip
            if keep_writing:
                keep_writing = False
                f.write('</div>\n') # close div
            else:
                continue
            
        if entry['Column Headers']: # write column header
            keep_writing = True
            
            # write new column and header
            f.write('<div class="col-sm">\n')
            f.write('<h5>' + entry['Column Headers'] + '</h5>\n')
            
           
        # write entry info
        if entry['Name']:
            f.write('<p>' + entry['Name'] + '\n')
            f.write('<br>' + entry['Email'] + '</p>\n')
        if entry['Address']:
            f.write('<p>' + entry['Address'].strip('\n').replace('\n', '<br>') + '</p>\n')
        if entry['Link Label']:
            f.write('<a href="' + entry['Link Address'] + '" target="_blank">' + entry['Link Label'] +'</a><br>\n')
                
            
    
    f.write('</div></div></footer>\n')
        # close file
    f.close()





