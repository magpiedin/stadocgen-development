import pandas as pd
import shutil
import datetime
from pathlib import Path
import os

today = datetime.date.today()
ts = today.strftime("%Y%m%d")

namespace = 'mids'

# -------------------------------------------------------
# Paths
currentPath = Path().absolute()
projectPath = currentPath.parent.parent.parent
# Source Files Path
sourceFile = str(projectPath) + '/app/data/source/mids-repo/information_elements.tsv'
examplesSource = str(projectPath) + '/app/data/source/mids-repo/examples.tsv'


# Timestamped output path
# Create timestamped folder for working files (works in progress)
targetPath = str(projectPath) + '/app/data/output'
targetFile = str(targetPath) + '/information-elements.tsv'
examplesTarget = str(targetPath) + '/examples.tsv'

# Create timestamped folder if it doesn't exist
if not os.path.isdir(targetPath):
    os.mkdir(targetPath)

# -------------------------------------------------------
# Create copies
# term_src > sourceFile
# term_csv > targetFile
shutil.copy(sourceFile, targetFile)
shutil.copy(examplesSource, examplesTarget)

# -------------------------------------------------------
# Process
# ltc_df > target_df
# Read
df = pd.read_csv(targetFile, encoding="utf8",sep='\t')

# Renamez
df.rename(columns={'MIDSLevel_localName': 'class_name',
                    'informationElement_localName': 'term_local_name',
                    'usage': 'purpose',
                    'recommendations': 'usage_note',
                   'term_added': 'term_created'
                   }, inplace=True)

# RDF Type
df['rdf_type'] = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'

# Qualified Term
df['term_ns_name'] = 'mids:' + df['term_local_name']

df["term_created"] = pd.to_datetime(df["term_created"], format='%d/%m/%Y')
df["term_modified"] = pd.to_datetime(df["term_modified"], format='%d/%m/%Y')

# Resave
df.to_csv(targetFile, encoding="utf8",sep='\t',index=False)

# Process Examples ------------------------------------------- */
df_examples = pd.read_csv(examplesTarget, encoding="utf8",sep='\t')
df_examples.rename(columns={'informationElement_localName': 'term_local_name'}, inplace=True)

