import requests

from utils import delete_keys_from_dict


UNIPROT_API_BASE_URL = 'https://www.ebi.ac.uk/proteins/api'

def _set_variation_features(residue, protein):
    rest_url = UNIPROT_API_BASE_URL + '/variation/' + protein
    response = requests.get(rest_url + '?location=' + str(residue.get('residue')))
    variation_features = []

    if response.status_code == 200:
        variation_features = response.json().get('features')

    new_substitutions = []

    for s in residue.get('substitutions'):
        variation = next((f for f in variation_features if f.get('alternativeSequence') == s.get('substitution')), None)

        if variation is not None:
            delete_keys_from_dict(variation, [
                'type',
                'alternativeSequence',
                'begin',
                'end',
                'cytogeneticBand',
                'wildType',
                'mutatedType'
            ])

        new_substitutions.append({
            **s,
            'variation': variation
        })

    return new_substitutions

def _set_mutagenesis_details(residue, protein):
    rest_url = UNIPROT_API_BASE_URL + '/mutagenesis/' + protein
    response = requests.get(rest_url + '?location=' + str(residue.get('residue')))
    mutagenesis_details = []

    if response.status_code == 200:
        mutagenesis_details = response.json().get('features')

    new_substitutions = []

    for s in residue.get('substitutions'):
        mutagenesis = next((f for f in mutagenesis_details if f.get('alternativeSequence') == s.get('substitution')), None)

        if mutagenesis is not None:
            delete_keys_from_dict(mutagenesis, [
                'type',
                'alternativeSequence',
                'begin',
                'end'
            ])

        new_substitutions.append({
            **s,
            'mutagenesis': mutagenesis
        })

    return new_substitutions

def enrich_with_uniprot_information(mutagenesis_data, protein):
    new_mutagenesis_data = []

    for residue in mutagenesis_data:
        n_residue = {
            **residue,
            'substitutions': _set_variation_features(residue, protein)
        }

        n_residue = {
            **n_residue,
            'substitutions': _set_mutagenesis_details(n_residue, protein)
        }

        new_mutagenesis_data.append(n_residue)


    return new_mutagenesis_data
