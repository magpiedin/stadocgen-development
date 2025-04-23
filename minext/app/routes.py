from app import app
from flask import render_template
from markupsafe import Markup
import markdown2
import pandas as pd
import yaml
import os.path, time

with open('app/meta.yml') as metadata:
    meta = yaml.safe_load(metadata)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html',
                           pageTitle='404 Error'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html',
                           pageTitle='500 Unknown Error'), 500


'''
@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('tango'), 200, {'Content-Type': 'text/css'}
'''

# Homepage with content stored in markdown file
@app.route('/')
def home():
    home_mdfile = 'app/md/home-content.md'
    md_lastModified = time.ctime(os.path.getmtime(home_mdfile))
    print("last modified: %s" % time.ctime(os.path.getmtime(home_mdfile)))

    with open(home_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read())
    return render_template('home.html',
                           home_markdown=Markup(marked_text),
                           pageTitle='Home',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           status=meta['status'],
                           landingPage=meta['documentation-landing-page'],
                           githubRepo=meta['github-repo'],
                           slug='home',
                           lastModified=md_lastModified
                           )

@app.route('/terms')
def terms():
    language_code = 'en'
    language_label = ''
    header_mdfile = 'app/md/termlist-header.md'
    with open(header_mdfile, encoding="utf-8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    # Terms
    terms_csv = 'app/data/output/minext-termlist.csv'
    terms_df = pd.read_csv(terms_csv, encoding='utf-8')

    terms = terms_df.sort_values(by=['class_name','term_local_name'])

    print(terms['rdf_type'])

    # Unique Class Names
    termsCls = terms_df['class_name'].dropna().unique()

    # Terms by Class
    grpdict2 = terms_df.groupby('class_name')[['term_ns_name', 'term_local_name', 'namespace', 'compound_name']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    termsByClass = []

    for i in grpdict2:
        termsByClass.append({
            'class': i,
            'termlist': grpdict2[i]
        })
    return render_template('term-list.html',
                           headerMarkdown=Markup(marked_text),
                           termsCls=termsCls,
                           terms=terms,
                           termsByClass=termsByClass,
                           uniqueTerms=terms,
                           pageTitle='Term List',
                           status=meta['status'],
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['documentation-landing-page'],
                           githubRepo=meta['github-repo'],
                           slug='terms',
                           languageCode=language_code,
                           languageLabel=language_label
                           )
