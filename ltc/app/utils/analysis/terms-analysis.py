from pathlib import Path
import pandas as pd
import shutil
import numpy as np

# Analysis of CSV Files produced by the transformations scripts

current_dir = Path().absolute()
path = current_dir.parent.parent

# -------------------------------------------------------
# Read CSV and Create Dataframes
terms_csv = str(path)+'/data/output/ltc-termlist.csv'
working_csv = str(path)+'/utils/analysis/output/ltc-working-terms.csv'
translations_csv = str(path)+'/data/output/latimer-translations.csv'
shutil.copy(terms_csv, working_csv)

ltc_df = pd.read_csv(working_csv, encoding="utf8")
translations_df = pd.read_csv(translations_csv, encoding="utf8")
translations_df.rename(columns={'term_localName': 'term_local_name'}, inplace=True)
# ------------------------------------
# Analysis

#ltc_df.sort_values(by='term_local_name', axis='index', inplace=True, na_position='last')
#ltc_df.to_csv('output/sorted.csv', encoding='utf8', mode='w+' )
print(len(ltc_df.index))

# Add Class Name to definition is duplicate row
#sorted_df['definition'] = np.where(sorted_df[selectCols].duplicated(subset=['term_local_name'], keep=False), sorted_df['definition']+' ('+sorted_df['class_name'].astype(str)+')',sorted_df['definition'])
#selectCols = ['class_name', 'namespace', 'term_local_name', 'rdf_type', 'term_created', 'term_modified', 'namespace_iri', 'term_iri', 'term_ns_name', 'term_version_iri', 'datatype']
#groupCols = ['namespace', 'term_local_name', 'rdf_type', 'term_created', 'term_modified', 'namespace_iri', 'term_iri', 'term_ns_name', 'term_version_iri', 'datatype']
#unique_df = ltc_df[selectCols].groupby(groupCols)['class_name'].agg([('class_name', ', '.join)]).reset_index()

# Reduce columns and return only unique values
term_df = ltc_df[['term_local_name','rdf_type']]
unique_df = term_df.drop_duplicates()
unique_df.to_csv('output/unique.csv', index=False, encoding='utf8', mode='w+' )

# Return value in term_local_name in term_df not in translations_df
diff_df = term_df[~term_df["term_local_name"].isin(translations_df["term_local_name"])]

print(diff_df.shape[0])

