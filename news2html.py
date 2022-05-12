# This script reads the input excel sheet to generate a html file for 
# the news tab
#
# to run in python prompt
# import news2html
# news2html.news2html('./CCWJ_Website.xlsx')

import os
import pandas as pd


excel_path = '../CCWJ_Website.xlsx'
def news2html(excel_path):
    # read sheet named news in excel file
    data = pd.read_excel(excel_path, sheet_name="Home_News")
    data.fillna('', inplace=True)

    # open file to write into
    f = open("./news-text.html", 'w')
    
    # write each section 
    for index, row in data.iterrows():
        if row['Section']:
            write_section(row['Section'], data, index, f)

    f.close()


def write_section(section_name, data, index_start, f):
    # write section title
    f.write('<div class="news-container"><h4 class="font-goodtimes subheading1">' + section_name + '</h4></div>\n')
    
    # go through each row in the sheet starting from index_start
    for i, row in data.iloc[index_start:].iterrows():
        
        # detect if next section has been reached, if so stop writing section
        if row['Section'] and row['Section'] != section_name:
            break
        
        f.write('<div class="news-container">\n')

        # go through each column for the row
        for header, value in row.items():
    
            if header.startswith('Date') and value:
                f.write('<p class="news-date">' + value.month_name() + ' ' + str(value.day) + ', ' + str(value.year) + '</p>\n')
                
            elif header.startswith('Description') and value:
                text = value.strip('\n').replace('\n', '<br>') # preserve newlines in html
                if row['Link']:
                    f.write('<p class="news-text"><a href="' + row['Link'] + '" target="_blank">' + text + '</a></p>\n')
                else:
                    f.write('<p class="news-text">' + text + '</p>\n')
                
        
        f.write('</div>\n\n')
                    

                    
# news2html('./CCWJ_Website.xlsx')


    
