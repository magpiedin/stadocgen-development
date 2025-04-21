from app import app
from flask import render_template, abort, redirect
from markupsafe import Markup
import markdown2
import pandas as pd
import yaml
import glob


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
    with open(home_mdfile, encoding="utf-8") as f:
        marked_text = markdown2.markdown(f.read())
    return render_template('home.html',
                           home_markdown=Markup(marked_text),
                           pageTitle='Home',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['documentation-landing-page'],
                           githubRepo=meta['github-repo'],
                           slug='home'
                           )

# Write French Translation of Terms Page
@app.route('/terms/', defaults={'lang': None})
@app.route('/terms/<lang>/', methods=['GET'])
def terms(lang = None):

    # Read translations YAML file
    translations_yml = 'app/utils/translations.yml'
    yml_dict = []
    for yf in glob.glob(translations_yml, recursive=True):
        with open(yf, 'r', encoding='utf8') as f:
            lang_meta = yaml.load(f, Loader=yaml.FullLoader)
            yml_dict.append(lang_meta)


    # Load Translated Markdown Content
    if lang:
        print(lang)
        for item in lang_meta['Languages']:
            if item['code'] == lang:
                language_code = item['code']
                language_label = item['label']
                header_mdfile = 'app/md/termlist-header-'+lang+'.md'
                with open(header_mdfile, encoding="utf-8") as f:
                    marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])
            else:
                abort(404)
    else:
        language_code = 'en'
        language_label = ''
        header_mdfile = 'app/md/termlist-header.md'
        with open(header_mdfile, encoding="utf-8") as f:
            marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])



    # Terms
    #terms_csv = 'app/data/output/ltc-translations-termlist.csv'
    terms_csv = 'app/data/output/ltc-fr-termlist.csv'
    terms_df = pd.read_csv(terms_csv, encoding='utf-8')

    sssom_csv = 'app/data/output/ltc-sssom.csv'
    sssom_df = pd.read_csv(sssom_csv, encoding='utf-8')

    # Merge SSSOM Mappings with Terms
    terms_skos_df = pd.merge(
        terms_df, sssom_df[['compound_name', 'predicate_label', 'object_id', 'object_category', 'object_label', 'mapping_justification' ]],
        on=['compound_name'], how='left'
    )

    terms = terms_skos_df.sort_values(by=['class_name','term_local_name'])

    # Unique Class Names
    ltcCls = terms_df['class_name'].dropna().unique()

    # Terms by Class
    grpdict2 = terms_df.groupby('class_name')[['term_ns_name', 'term_local_name', 'namespace', 'compound_name','term_version_iri','term_modified']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    termsByClass = []

    for i in grpdict2:
        termsByClass.append({
            'class': i,
            'termlist': grpdict2[i]
        })
    print(terms.columns.to_list())
    return render_template('term-list.html',
                           headerMarkdown=Markup(marked_text),
                           ltcCls=ltcCls,
                           terms=terms,
                           sssom=sssom_df,
                           termsByClass=termsByClass,
                           uniqueTerms=terms,
                           pageTitle='Term List',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['documentation-landing-page'],
                           githubRepo=meta['github-repo'],
                           slug='term-list',
                           languageCode=language_code,
                           languageLabel=language_label
                           )


@app.route('/quick-reference')
def quickReference():
    header_mdfile = 'app/md/quick-reference-header.md'
    marked_text = ''
    with open(header_mdfile, encoding="utf-8") as f:
        marked_text = markdown2.markdown(f.read())

    # Quick Reference Main
    df = pd.read_csv('app/data/output/ltc-termlist.csv', encoding='utf-8')
    df['examples'] = df['examples'].str.replace(r'"', '')
    df['definition'] = df['definition'].str.replace(r'"', '')
    df['usage'] = df['usage'].str.replace(r'"', '')
    df['notes'] = df['notes'].str.replace(r'"', '')

    # Group by Class
    grpdict = df.fillna(-1).groupby('class_name')[['namespace', 'term_local_name', 'label', 'definition',
                                                   'usage', 'notes', 'examples', 'rdf_type', 'class_name',
                                                   'is_required', 'is_repeatable', 'compound_name',
                                                   'datatype', 'term_ns_name', 'term_iri', 'term_version_iri','term_modified']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    grplists = []
    for i in grpdict:
        grplists.append({
            'class': i,
            'termlist': grpdict[i]
        })

    # Required values
    terms_df = df[['namespace', 'term_local_name', 'label', 'class_name',
                   'is_required', 'rdf_type', 'compound_name']].sort_values(by=['class_name'])

    required_df = terms_df.loc[(terms_df['is_required'] == True) &
                               (terms_df['rdf_type'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property')]

    required_classes_df = terms_df.loc[(terms_df['is_required'] == True) &
                           (terms_df['rdf_type'] == 'http://www.w3.org/2000/01/rdf-schema#Class')]


    return render_template('quick-reference.html',
                           headerMarkdown=Markup(marked_text),
                           grplists=grplists,
                           requiredTerms=required_df,
                           requiredClasses=required_classes_df,
                           pageTitle='Home',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['documentation-landing-page'],
                           githubRepo=meta['github-repo'],
                           slug='quick-reference'
    )

@app.route('/resources')
def docResources():
    header_mdfile = 'app/md/resources-header.md'
    marked_text = ''
    with open(header_mdfile, encoding="utf-8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    sssom_mdfile = 'app/md/sssom-reference.md'
    marked_sssom = ''
    with open(sssom_mdfile, encoding="utf-8") as f:
        marked_sssom = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    return render_template('resources.html',
                           headerMarkdown=Markup(marked_text),
                           sssomRefMarkdown=Markup(marked_sssom),
                           pageTitle='Home',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['documentation-landing-page'],
                           githubRepo=meta['github-repo'],
                           slug='resources'
    )


