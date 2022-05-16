
# Testing
To run the website with python server, run this in terminal from the main folder:
`python3 -m http.server 8080`

Then visit http://localhost:8080/ in browser
Note that some things like links to pdfs, etc. may not work properly until you upload the content to the real site.

# Styles
All styles are defined in the index.css file.
- Fonts, font sizes
- Colors

# Images
In general the scripts will look for images in the Assets/section_tab/section_name folder, with all spaces replaced with underscores '_'
For example, images in the 'What we do' section under the About Us tab should be placed in Assets/About_Us/What_we_do

# Generating publications
The publication list can be generated from a BibTeX file (.bib) using a python script (bibtex2htmldiv.py)
This has been taken from: https://github.com/ketch/tex2_rst_html

To run, open terminal (navigate to the Research folder) and run
`import bibtex2htmldiv`
`bibtex2htmldiv.bib2html('/path/to/myfile.bib')`

This should generate a bib.html file in the Research folder, which is imported with JS to the research page.

*To include url in publication title:* add 'url' entry to .bib file
*To include thumbnail image:* upload image to folder specified in img_path ('Assets') named with the pub's id (eg. RN3335)
Any DOIs or Arxiv id's added will also be displayed below in a link

*To change headings to keywords instead of reference type:*
- Make sure each .bib entry has a keywords associated with it
- use bibtex2htmldivkw.py to generate a bibkw.html
- Load the bibkw.html in the JS of the research.html page



# Bootstrap Ref
m = margin 

mb, mt, ms, me = margin bottom, margin top, margin start, margin end

p = padding


# Git Ref
`git pull` to pull new updates
`git status` to check current branch/staging
`git add .` add all changes for staging
`git commit -m "commit message"` to commit
`git push` to push to origin


