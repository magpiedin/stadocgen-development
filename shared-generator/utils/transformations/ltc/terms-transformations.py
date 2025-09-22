import pandas as pd
import os
import shutil

# --- Configuration ---
# Get the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

# Define source and destination paths relative to the project root
source_dir = os.path.join(project_root, 'utils', 'sources', 'ltc')
output_dir = os.path.join(project_root, 'shared-generator', 'app', 'data', 'output')
os.makedirs(output_dir, exist_ok=True)

# --- File Paths ---
term_src_path = os.path.join(source_dir, 'ltc_terms_source.csv')
term_dest_path = os.path.join(output_dir, 'ltc-termlist.csv')
ns_src_path = os.path.join(source_dir, 'ltc_namespaces.csv')
ns_dest_path = os.path.join(output_dir, 'ltc-namespaces.csv')
dt_src_path = os.path.join(source_dir, 'ltc_datatypes.csv')
dt_dest_path = os.path.join(output_dir, 'ltc-datatypes.csv')

# --- Main Transformation Logic ---
print("Running ltc/terms-transformations...")
shutil.copy(term_src_path, term_dest_path)
shutil.copy(ns_src_path, ns_dest_path)
shutil.copy(dt_src_path, dt_dest_path)

ltc_df = pd.read_csv(term_dest_path, encoding="utf8")
ltc_df.rename(columns={'term_localName': 'term_local_name',
                       'tdwgutility_organizedInClass': 'class_uri',
                       'tdwgutility_required': 'is_required',
                       'tdwgutility_repeatable': 'is_repeatable'}, inplace=True)
ltc_df['is_required'] = ltc_df['is_required'].replace({'Yes': 'True', 'No': 'False'})
ltc_df['is_repeatable'] = ltc_df['is_repeatable'].replace({'Yes': 'True', 'No': 'False'})
ltc_df['class_name'] = ltc_df['class_uri'].str.replace('http://rs.tdwg.org/dwc/terms/attributes/', '')
ltc_df['compound_name'] = ltc_df[["class_name", "term_local_name"]].apply(".".join, axis=1)
ltc_df.to_csv(term_dest_path, index=False, encoding='utf8')

ns_df = pd.read_csv(ns_dest_path, encoding="utf8")
ns_df.rename(columns={'curie': 'namespace', 'value': 'namespace_iri'}, inplace=True)
ns_df['namespace'] = ns_df['namespace'].astype(str) + ':'
if 'ltc:' not in ns_df['namespace'].values:
    ltc_row = {"namespace": "ltc:", "namespace_iri": "http://rs.tdwg.org/ltc/terms/"}
    ns_df = pd.concat([ns_df, pd.DataFrame([ltc_row])], ignore_index=True)
ns_df.to_csv(ns_dest_path, index=False, encoding='utf8')

ltc_df = pd.read_csv(term_dest_path, encoding="utf8")
ns_df = pd.read_csv(ns_dest_path, encoding="utf8")
ltc_df = pd.merge(ltc_df, ns_df[['namespace', 'namespace_iri']], on='namespace', how='inner')
ltc_df['term_iri'] = ltc_df['namespace_iri'].astype(str) + ltc_df['term_local_name']
ltc_df['term_ns_name'] = ltc_df['namespace'].astype(str) + ltc_df['term_local_name']
ltc_df['term_version_iri'] = 'http://rs.tdwg.org/ltc/terms/' + ltc_df["term_local_name"] + '-' + ltc_df["term_modified"]
ltc_df.sort_values(by='term_local_name', axis='index', inplace=True, na_position='last')
ltc_df['examples'] = ltc_df['examples'].str.replace('"', '')
ltc_df['definition'] = ltc_df['definition'].str.replace('"', '')
ltc_df['usage'] = ltc_df['usage'].str.replace('"', '')
ltc_df['notes'] = ltc_df['notes'].str.replace('"', '')
ltc_df.to_csv(term_dest_path, index=False, encoding='utf8')

dt_df = pd.read_csv(dt_dest_path, encoding='utf8')
dt_df.rename(columns={'term_localName': 'term_local_name','tdwgutility_organizedInClass': 'class_name'}, inplace=True)
dt_df['compound_name'] = dt_df[["class_name", "term_local_name"]].apply(".".join, axis=1)
dt_df.to_csv(dt_dest_path, index=False, encoding='utf8')

ltc_df = pd.merge(ltc_df, dt_df[['compound_name', 'datatype']], on='compound_name', how='left')
ltc_df.to_csv(term_dest_path, index=False, encoding='utf8')

print("ltc/terms-transformations complete.")
