
# runs all python scripts 
# to run in terminal : python createallhtml.py

import footer2html
import home2html
import news2html
from Teaching.teaching2html import teaching2html
from Resources.gallery2html import gallery2html
from Resources.videos2html import videos2html
from Research.research2html import research2html
from Research.bibtex2html import bibtex2html
from People.people2html import people2html
from Join.joinus2html import joinus2html
from About.about2html import about2html
from About.board2html import board2html
from About.lab2html import lab2html
from About.sponsors2html import sponsors2html

import os

# keep CCWJ_Website spreadsheet in the main directory
path_to_excel = './CCWJ_Website.xlsx'
path_to_excel2 = '../CCWJ_Website.xlsx'

# name of bibtext file used to generate publications list
# keep in Research folder
bibfile = 'shorttest.bib'

# run all scripts
footer2html.footer2html(path_to_excel)
home2html.home2html(path_to_excel)
news2html.news2html(path_to_excel)

os.chdir('./Teaching')
teaching2html(path_to_excel2)

os.chdir('../Resources')
gallery2html(path_to_excel2)
videos2html(path_to_excel2)

os.chdir('../Research')
research2html(path_to_excel2)
bibtex2html('./' + bibfile, 'bib.html')

os.chdir('../People')
people2html(path_to_excel2)

os.chdir('../Join')
joinus2html(path_to_excel2)

os.chdir('../About')
about2html(path_to_excel2)
board2html(path_to_excel2)
lab2html(path_to_excel2)
sponsors2html(path_to_excel2)




