from pathlib import Path
import pandas as pd
import shutil
import globals
import glob
import yaml
from datetime import date

today = date.today()
formatted_date = today.strftime("%Y-%m-%d")

namespace = 'minext'
current_dir = Path().absolute()
path = current_dir.parent.parent

# -------------------------------------------------------
# Create copies
term_src = str(path)+'/data/sources/minext-term-list.csv'
term_csv = str(path)+'/data/output/minext-termlist.csv'
shutil.copy(term_src, term_csv)

ns_src = str(path)+'/data/sources/namespaces.csv'
ns_csv = str(path)+'/data/output/minext-namespaces.csv'
shutil.copy(ns_src, ns_csv)

# Target
target_csv = str(path)+'/data/output/minext-target.csv'
#---------------------------------------------------------------------------
# Terms
minext_df = pd.read_csv(term_csv, encoding="utf8")
# Rename Columns
minext_df.rename(columns={'term': 'term_local_name',
                          'organized_in_class': 'class_name'}, inplace=True)
# Create compound name column to uniquely identify each record
minext_df['compound_name'] = minext_df[["class_name", "term_local_name"]].apply(".".join, axis=1)
# Resave
minext_df.to_csv(term_csv, index=False, encoding='utf8')
# -------------------------------------------------------
# Revise namespaces file
ns_df = pd.read_csv(ns_csv, encoding="utf8")
ns_df['namespace'] = ns_df['namespace'].astype(str) + ':'
ns_df.to_csv(ns_csv, index=False, encoding='utf8')

# --------------------------------------------------------------------------
# Combine namespaces and terms
ns_df = pd.read_csv(ns_csv, encoding="utf8")
terms_df = pd.read_csv(term_csv, encoding="utf8")

minext_df = pd.merge(terms_df, ns_df[['namespace', 'namespace_iri']], on='namespace', how='inner')

# Create namespaces columns in merged file
minext_df['term_iri'] = minext_df['namespace_iri'].astype(str) + minext_df['term_local_name']
minext_df['term_ns_name'] = minext_df['namespace'].astype(str) + minext_df['term_local_name']
#minext_df['term_version_iri'] = 'http://rs.tdwg.org/mineralogy/terms/' + minext_df["term_local_name"] + '-' + minext_df["term_modified"]

# Write results
minext_df.to_csv(target_csv, index=False, encoding='utf8')

minext_df['term_modified'] = formatted_date

#minext_df.sort_values(by='term_local_name', axis='index', inplace=True, na_position='last')

# Data cleanup
minext_df['examples'] = minext_df['examples'].str.replace('"', '')
minext_df['definition'] = minext_df['definition'].str.replace('"', '')
minext_df['usage_note'] = minext_df['usage_note'].str.replace('"', '')
minext_df['notes'] = minext_df['notes'].str.replace('"', '')

# Resave terms file
minext_df.to_csv(term_csv, index=False, encoding='utf8')
