"""
Convert bibtex files (.bib) to html divs that can be custom formatted using CSS.
Organized by citation type (Book, article, etc)
Usage (from Python or IPython prompt):

    >> import bibtex2html
    >> bibtex2html.bibtex2html('../Assets/Research/shorttest.bib','bib.html')

"""
import os
import pybtex.database

# This may need to be changed for other machines/users
# the place where publication images are kept
img_path = r'/Users/Cotton/Desktop/CCWJ_site_bootstrap/Assets/'

# This may need to be changed for other sites
# the url where publication images are hosted
img_dest = 'http://localhost:8080/Assets/'
# paperlinks_path = '/Users/ketch/Research/Projects/labnotebook/assets/paperlinks.txt'

def bibtex2html(bibfile,htmlfile='bib.html'):
    publications=parsefile(bibfile)
    writebib(publications,htmlfile)
    print('bibtex2html complete')

def compile_name(person):
    first = ' '.join([x.render_as('text') for x in person.rich_first_names])
    middle = ' '.join([x.render_as('text') for x in person.rich_middle_names])
    last = ' '.join([x.render_as('text') for x in person.rich_last_names])
    return first+' '+middle+' '+last

def parsefile(filename):
    """
    Takes a file name (string, including path) and returns a list of dictionaries,
    one dictionary for each bibtex entry in the file.

    Uses the bibliograph.parsing package.
    """
    with open(filename) as f:
        db = pybtex.database.parse_string(f.read(),'bibtex')
    blist = [db.entries[key] for key in db.entries.keys()]
    publications = []
    for entry in blist:
        publications.append({x:entry.fields[x] for x in entry.fields.keys()})
        publications[-1]['pid'] = entry.key
        publications[-1]['reference_type'] = entry.type
        publications[-1]['author'] = [compile_name(p) for p in entry.persons['Author']]

    # Parsing errors give strings, so keep only dicts:
    #publications=[x for x in ents if x.__class__ is dict]
    return publications

def normalize_authors(authors):
    """
    Takes the authors string from a bibtex entry and rewrites it with
    first names first.
    """
    authorlist = authors
    authornames=[]
    for author in authorlist:
        if ',' in author:
            lastname, firstname = author.split(',')
            authornames.append(firstname.strip()+' '+lastname.strip())
        else:
            authornames.append(author.strip())
    if len(authorlist)>1:
        authornames[-1] = ' and '+authornames[-1]
    if len(authorlist)>2:
        return ', '.join(authornames)
    else:
        return ' '.join(authornames)


def writebib(publications,filename='bib.html'):
    """
    Writes html citation entries.
    This only works well for articles so far; for other citation types,
    it merely writes the author, title, and year.  It should be easy to
    add better functionality for other types.
    """
    f=open(filename,'w')

    # 2nd arg = the types of citations the script will look for
    write_section('Submitted preprints','unpublished',publications,f)
    write_section('Refereed Journal Articles','article',publications,f)
    write_section('Books','inbook',publications,f)
    write_section('Conference Proceedings','inproceedings',publications,f)
    write_section('Technical Reports','techreport',publications,f)
    write_section('PhD Theses','phdthesis',publications,f)
    write_section('MSc Theses','mastersthesis',publications,f)

    f.close()


def write_section(title,reference_type,publications,f):
    """
    Write out all entries of type reference_type, in reverse chronological order
    """
    these_pubs = [pub for pub in publications if pub['reference_type']==reference_type]
    these_pubs=sort_by_year(these_pubs)

    if len(these_pubs)>0:
        f.write('<h4>'+title+'</h4>\n')
        for pub in these_pubs: write_entry(pub,f)


def write_entry(pub,f):
    pub['author'] = normalize_authors(pub['author'])

    f.write('<div id="pub" class="pub filterable ')
    if 'keywords' in pub:
        f.write(pub['keywords'].lower().replace(';',' ').replace(',',' '))
    f.write('">\n')
    img_file = img_path + pub['pid'] + '.png'

    if os.path.isfile(os.path.abspath(img_file)):
        f.write('<img src="' + img_dest + pub['pid'] + '.png" align="right" />\n')
    if 'url' in pub: # create link to pdf file
        f.write('<a target="_blank" href="'+pub['url'].split()[0].replace('\_','_')+'">')
    elif 'doi' in pub.keys():
        f.write('<a href="https://doi.org/'+pub['doi']+'">')
    elif 'arxivid' in pub:
        f.write('<a href="http://arxiv.org/abs/'+pub['arxivid']+'">')

    # write paper title
    f.write('<name> %s </name><br>\n' % pub['title'].replace('{','').replace('}',''))
    if ('url' in pub) or ('doi' in pub) or ('arxivid' in pub):
        f.write('</a>\n')

    f.write('<authors> %s</authors>,\n' % pub['author'])
    if 'journal' in pub.keys():
        f.write('<journal> %s</journal>' % pub['journal'])
        if 'volume' in pub.keys():
            f.write(", %s" % pub['volume'])
            if 'number' in pub.keys():
                f.write("(%s)" % pub['number'])
                if 'pages' in pub.keys():
                    f.write(":%s" % pub['pages'].replace('&ndash;','-'))
    if 'annote' in pub.keys():
        f.write(" %s" % pub['annote'])
    if 'school' in pub.keys():
        f.write(" %s," % pub['school'])
    if 'booktitle' in pub.keys():
        f.write("in %s." % pub['booktitle'])
    if pub['year'] != '':
        f.write(" (%s)" % pub['year'])

    # Write links line
    linkstring = ''

    # if 'url' in pub.keys():
    #     if 'arxiv' not in pub['url'].split()[0]:
    #         if 'davidketchson' in pub['url'].split()[0]:
    #             linkstring += ' | <a href="'+pub['url'].split()[0]+'">Free PDF</a> '
    if 'doi' in pub.keys():
        linkstring += ' | <a href="https://doi.org/'+pub['doi']+'">Published version</a> '
    if 'arxivid' in pub.keys():
        linkstring += ' | <a href="http://arxiv.org/abs/'+pub['arxivid']+'">arXiv version</a> '

    # with open(paperlinks_path, 'r') as f2:
    #     links = ast.literal_eval(f2.read())
    # if pub['pid'] in links.keys():
    #     publinks = links[pub['pid']]
    #     for name, link in publinks.items():
    #         linkstring += ' | <a href="'+link+'">'+name+'</a> '

    if len(linkstring)>0:
        f.write('<br>\n<links> ')
        f.write(linkstring)
        f.write('|</links>')
    f.write('<div style="clear:both"></div>\n')
    f.write('\n</div>\n\n')

def sort_by_year(publications):
    """Takes a list of publications and return it sorted in reverse chronological order."""
    return sorted(publications, key=lambda p: p.setdefault('year',''),reverse=True)
