from flask import Flask, render_template
from flask_frozen import Freezer
from markupsafe import Markup
import sys
import markdown2
import pandas as pd
import yaml
app = Flask(__name__, template_folder='templates')
freezer = Freezer(app)

#app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['FREEZER_DESTINATION'] = 'build'
app.config['FREEZER_RELATIVE_URLS'] = True
#app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True

# Resolve differences in relative paths with routes.py file
relpath = ''

with open('meta.yml') as metadata:
    meta = yaml.safe_load(metadata)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html',
                           pageTitle='404 Error'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html',
                           pageTitle='500 Unknown Error'), 500


# Homepage with content stored in markdown file
# Homepage with content stored in markdown file
# Homepage with content stored in markdown file
@app.route('/')
def home():
    home_mdfile = str(relpath) + 'md/home-content.md'
    with open(home_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])
    return render_template('home.html',
                           home_markdown=Markup(marked_text),
                           pageTitle='Home',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['links']['landing_page'],
                           githubRepo=meta['links']['github_repository'],
                           slug='home'
                           )

@app.route('/information-elements/')
def information_elements():
    home_mdfile = str(relpath) + 'md/information-elements-header.md'
    with open(home_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    information_elements_csv = str(relpath) + 'data/output/mids-master-list.csv'
    information_elements_df = pd.read_csv(information_elements_csv, encoding='utf8')

    mappings_csv = str(relpath) + 'data/output/mids-mappings.csv'
    mappings_df = pd.read_csv(mappings_csv, encoding='utf8')

    levels_csv = str(relpath) + 'data/output/mids-levels.csv'
    levels_df = pd.read_csv(levels_csv, encoding='utf8')

    information_elements_df = information_elements_df.sort_values(by=['class_name', 'term_local_name'])

    levels = levels_df.sort_values(by=['term_local_name'])

    grpdict2 = information_elements_df.groupby('class_name')[
        ['term_ns_name', 'term_local_name', 'namespace', 'compound_name', 'term_version_iri', 'term_modified']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    information_elements_by_level = []

    for i in grpdict2:
        information_elements_by_level.append({
            'class': i,
            'informationElementList': grpdict2[i]
        })

    return render_template('information-elements.html',
                           headerMarkdown=Markup(marked_text),
                           pageTitle='Information Elements',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['links']['landing_page'],
                           githubRepo=meta['links']['github_repository'],
                           slug='information-elements',
                           levels=levels,
                           informationElements=information_elements_df,
                           mappings=mappings_df,
                           informationElementsByLevel=information_elements_by_level
                           )

@app.route('/mappings/')
def mappings():
    home_mdfile = str(relpath) + 'md/mappings-header.md'
    with open(home_mdfile, encoding="utf8") as f:
        marked_text = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

    master_list_csv = str(relpath) + 'data/output/mids-master-list.csv'
    master_list_df = pd.read_csv(master_list_csv, encoding='utf8')

    mappings_csv = str(relpath) + 'data/output/mids-mappings.csv'
    mappings_df = pd.read_csv(mappings_csv, encoding='utf8')

    return render_template('mappings.html',
                           home_markdown=Markup(marked_text),
                           pageTitle='MIDS Mappings',
                           title=meta['title'],
                           acronym=meta['acronym'],
                           landingPage=meta['links']['landing_page'],
                           githubRepo=meta['links']['github_repository'],
                           slug='mappings',
                           mappings=mappings_df,
                           )

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)