# Latimer Core Transformation Scripts
Sequence of csv transformations for the purposes of generating documentation from source csv files

## Sequence
Scripts must be run in a specific order to produce production files
sssom_transformations.py > terms_transformations.py > translation_transformations.py

### SKOS and SSSOM Mappings
Transforms both mapping files
Script:skos_transformations.py

| Mapping Type | Type   | Path                                     |
| ------------ |--------| ---------------------------------------- |
| SKOS         | Source | ltc-source/mapping/ltc_skos_mapping.csv  |
| SKOS         | Target | ltc-docs/ltc-skos.csv                    |
| SSSOM        | Source | ltc-source/mapping/ltc_sssom_mapping.csv |
| SSSOM        | Target | ltc-docs/ltc-sssom.csv                   |


### Terms
Script: terms_transformations.py
