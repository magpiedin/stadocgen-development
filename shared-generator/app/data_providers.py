# This module contains functions that provide complex data to the templates.
# Each function corresponds to a 'data_provider' string in the YAML config.

import pandas as pd
import os
import yaml

def get_terms_data(app):
    """
    Provides the data needed for the LtC Term List page.
    This is extracted from the original ltc/app/routes.py.
    """
    data_path = os.path.join(app.root_path, 'data', 'output')

    terms_csv = os.path.join(data_path, 'ltc-translations-termlist.csv')
    terms_df = pd.read_csv(terms_csv, encoding='utf-8')

    sssom_csv = os.path.join(data_path, 'ltc-sssom.csv')
    sssom_df = pd.read_csv(sssom_csv, encoding='utf-8')

    terms_skos_df = pd.merge(
        terms_df, sssom_df[['compound_name', 'predicate_label', 'object_id', 'object_category', 'object_label', 'mapping_justification']],
        on=['compound_name'], how='left'
    )
    terms = terms_skos_df.sort_values(by=['class_name','term_local_name'])
    ltcCls = terms_df['class_name'].dropna().unique()

    grpdict2 = terms_df.groupby('class_name')[['term_ns_name', 'term_local_name', 'namespace', 'compound_name','term_version_iri','term_modified']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    termsByClass = []
    for i in grpdict2:
        termsByClass.append({
            'class': i,
            'termlist': grpdict2[i]
        })

    return {
        'ltcCls': ltcCls,
        'terms': terms,
        'sssom': sssom_df,
        'termsByClass': termsByClass,
        'uniqueTerms': terms,
    }

def get_quick_reference_data(app):
    """
    Provides the data needed for the LtC Quick Reference page.
    """
    data_path = os.path.join(app.root_path, 'data', 'output')
    terms_csv = os.path.join(data_path, 'ltc-termlist.csv')

    df = pd.read_csv(terms_csv, encoding='utf-8')
    df['examples'] = df['examples'].str.replace(r'"', '')
    df['definition'] = df['definition'].str.replace(r'"', '')
    df['usage_note'] = df['usage_note'].str.replace(r'"', '')
    df['notes'] = df['notes'].str.replace(r'"', '')

    grpdict = df.fillna(-1).groupby('class_name')[['namespace', 'term_local_name', 'label', 'definition',
                                                   'usage_note', 'notes', 'examples', 'rdf_type', 'class_name',
                                                   'is_required', 'is_repeatable', 'compound_name',
                                                   'datatype', 'term_ns_name', 'term_iri', 'term_version_iri','term_modified']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    grplists = []
    for i in grpdict:
        grplists.append({
            'class': i,
            'termlist': grpdict[i]
        })

    terms_df = df[['namespace', 'term_local_name', 'label', 'class_name',
                   'is_required', 'rdf_type', 'compound_name']].sort_values(by=['class_name'])
    required_df = terms_df.loc[(terms_df['is_required'] == True) &
                               (terms_df['rdf_type'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property')]
    required_classes_df = terms_df.loc[(terms_df['is_required'] == True) &
                           (terms_df['rdf_type'] == 'http://www.w3.org/2000/01/rdf-schema#Class')]

    return {
        'grplists': grplists,
        'requiredTerms': required_df,
        'requiredClasses': required_classes_df,
    }

def get_mids_information_elements_data(app):
    """
    Provides data for the MIDS Information Elements page.
    """
    data_path = os.path.join(app.root_path, 'data', 'output')

    info_elems_df = pd.read_csv(os.path.join(data_path, 'master-list.tsv'), sep='\t', encoding='utf-8')
    info_elems_df = info_elems_df.sort_values(by=['class_name', 'term_local_name'])

    levels_df = pd.read_csv(os.path.join(data_path, 'levels.tsv'), sep='\t', encoding='utf-8')
    levels = levels_df.sort_values(by=['term_local_name'])

    mappings_df = pd.read_csv(os.path.join(data_path, 'mappings.tsv'), sep='\t', encoding='utf-8', skipinitialspace=True)

    examples_df = pd.read_csv(os.path.join(data_path, 'examples.tsv'), sep='\t', encoding='utf-8')
    examples_df = examples_df.replace('\n', '', regex=True)
    df2 = examples_df.groupby('term_local_name')['example'].apply(list).reset_index(name="examples_list")
    df2['examples_list'] = df2['examples_list'].apply(lambda x: "|".join(map(str, x)))

    merged_df = pd.merge(info_elems_df, df2[['term_local_name', 'examples_list']], on="term_local_name", how="left")
    merged_df.rename(columns={'examples_list_y': 'examples_list'}, inplace=True)

    grpdict2 = info_elems_df.groupby('class_pref_label')[
        ['term_ns_name', 'term_local_name', 'namespace', 'compound_name', 'term_version_iri', 'term_modified']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    info_elems_by_level = []
    for i in grpdict2:
        info_elems_by_level.append({
            'class': i,
            'informationElementList': grpdict2[i]
        })

    return {
        'levels': levels,
        'informationElements': merged_df,
        'mappings': mappings_df,
        'informationElementsByLevel': info_elems_by_level,
        'examples': examples_df
    }

def get_mids_mappings_data(app):
    """
    Provides data for the MIDS Mappings page.
    """
    data_path = os.path.join(app.root_path, 'data', 'output')
    mappings_df = pd.read_csv(os.path.join(data_path, 'mappings.tsv'), sep='\t', encoding='utf-8', skipinitialspace=True)
    mappings_df = mappings_df.fillna('')
    return {'mappings': mappings_df}

def get_mids_resources_data(app):
    """
    Provides data for the MIDS Resources page.
    """
    md_path = os.path.join(app.root_path, 'md')
    with open(os.path.join(md_path, 'tools.yml')) as tools_yml:
        tools_meta = yaml.safe_load(tools_yml)
    with open(os.path.join(md_path, 'glossary.yml')) as glossary_yml:
        glossary_meta = yaml.safe_load(glossary_yml)

    return {
        'tools_metadata': tools_meta,
        'glossary_metadata': glossary_meta
    }

def get_minext_terms_data(app):
    data_path = os.path.join(app.root_path, 'data', 'output')
    meta_df = pd.read_csv(os.path.join(data_path, 'metadata-terms.csv'), encoding='utf-8')
    terms_df = pd.read_csv(os.path.join(data_path, 'minext-termlist.csv'), encoding='utf-8')
    terms = terms_df.sort_values(by=['class_name','term_local_name'])
    termsCls = terms_df['class_name'].dropna().unique()
    grpdict2 = terms_df.fillna(-1).groupby('class_name')[['term_ns_name', 'term_local_name', 'namespace', 'compound_name', 'rdf_type']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    termsByClass = []
    for i in grpdict2:
        termsByClass.append({
            'class': i,
            'termlist': grpdict2[i]
        })
    return {
        'metadataTerms': meta_df,
        'termsCls': termsCls,
        'terms': terms,
        'termsByClass': termsByClass,
        'uniqueTerms': terms
    }

def get_minext_quick_reference_data(app):
    data_path = os.path.join(app.root_path, 'data', 'output')
    df = pd.read_csv(os.path.join(data_path, 'minext-termlist.csv'), encoding='utf-8')
    df['examples'] = df['examples'].str.replace(r'"', '')
    df['definition'] = df['definition'].str.replace(r'"', '')
    df['usage_note'] = df['usage_note'].str.replace(r'"', '')
    df['notes'] = df['notes'].str.replace(r'"', '')
    grpdict = df.fillna(-1).groupby('class_name')[['namespace', 'term_local_name', 'label', 'definition',
                                                   'usage_note', 'notes', 'examples', 'rdf_type', 'class_name',
                                                   'is_required', 'compound_name',
                                                   'datatype', 'term_ns_name', 'term_iri', 'term_modified']].apply(
        lambda g: list(map(tuple, g.values.tolist()))).to_dict()
    grplists = []
    for i in grpdict:
        grplists.append({
            'class': i,
            'termlist': grpdict[i]
        })
    terms_df = df[['namespace', 'term_local_name', 'label', 'class_name',
                   'is_required', 'rdf_type', 'compound_name']].sort_values(by=['class_name'])
    required_df = terms_df.loc[(terms_df['is_required'] == True) &
                               (terms_df['rdf_type'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property')]
    required_classes_df = terms_df.loc[(terms_df['is_required'] == True) &
                           (terms_df['rdf_type'] == 'http://www.w3.org/2000/01/rdf-schema#Class')]
    return {
        'grplists': grplists,
        'requiredTerms': required_df,
        'requiredClasses': required_classes_df
    }

def get_minext_term_scopes_data(app):
    data_path = os.path.join(app.root_path, 'data', 'output')
    terms_df = pd.read_csv(os.path.join(data_path, 'minext-termlist.csv'), encoding='utf-8')
    terms = terms_df.sort_values(by=['class_name', 'term_local_name'])
    return {'terms': terms}
