import pandas as pd
import shutil
from datetime import date
from pathlib import Path
import os
import numpy as np

today = date.today()
ts = today.strftime("%Y%m%d")


# -------------------------------------------------------
# Paths
currentPath = Path().absolute()
projectPath = currentPath.parent.parent.parent
# Source Files Path
sourceFile = str(projectPath) + '/app/data/output/examples.tsv'
masterSourceFile = str(projectPath) + '/app/data/output/master-list.tsv'
targetFile = str(projectPath) + '/app/data/output/master-list.tsv'

df2 = pd.read_csv(masterSourceFile, encoding="utf8",sep='\t')
#df2 = df2.drop('compound_name', axis=1)
#df2 = df2.drop('examples_list', axis=1)


df = pd.read_csv(sourceFile, encoding="utf8",sep='\t')
# Group examples tsv by term_local_name
df_grouped = df.groupby("term_local_name").agg({'example':lambda x: list(x)})

#Merged Examples with master list
merged_df = pd.merge(df_grouped, df2, on='term_local_name', how='right')

# Convert examples lists to string with pipes
merged_df['example'] = merged_df['example'].apply(lambda x: str(x).replace('[','').replace(']','').replace('\', \'', '|').replace('\'', ''))
# Rename
merged_df.rename(columns={'example': 'examples'}, inplace=True)
# Write to file
merged_df.to_csv(targetFile, index=False, encoding='utf8',sep='\t')

# Read Target File Again to Drop NAN
df3 = pd.read_csv(targetFile, encoding="utf8",sep='\t')
df3.dropna(how='all')

df3 = df3[['term_local_name', 'namespace', 'term_ns_name', 'label', 'definition', 'usage', 'rdf_type',
       'term_version_iri', 'purpose', 'alt_label', 'level', 'class_name', 'class_pref_label', 'examples',
       'isRequiredBy', 'term_uri', 'term_iri', 'namespace_iri', 'term_created', 'term_modified']]
df3.to_csv(targetFile, index=False, encoding='utf8',sep='\t')
