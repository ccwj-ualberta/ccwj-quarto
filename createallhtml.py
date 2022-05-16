
# runs all python scripts 

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


footer2html.footer2html('./CCWJ_Website.xlsx')
home2html.home2html('./CCWJ_Website.xlsx')
news2html.news2html('./CCWJ_Website.xlsx')

teaching2html('./CCWJ_Website.xlsx')
gallery2html('./CCWJ_Website.xlsx')
videos2html('./CCWJ_Website.xlsx')
research2html('./CCWJ_Website.xlsx')
bibtex2html('./CCWJ_Website.xlsx')
people2html('./CCWJ_Website.xlsx')
joinus2html('./CCWJ_Website.xlsx')
about2html('./CCWJ_Website.xlsx')
board2html('./CCWJ_Website.xlsx')
lab2html('./CCWJ_Website.xlsx')
sponsors2html('./CCWJ_Website.xlsx')




