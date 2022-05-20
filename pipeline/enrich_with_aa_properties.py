from utils import get_amino_acid_properties


def enrich_with_amino_acid_properties(mutagenesis_data):
    new_mutagenesis_data = []

    for residue in mutagenesis_data:
        new_substitutions = [{**s, 'properties': get_amino_acid_properties(s.get('substitution'))} for s in residue.get('substitutions')]
        new_mutagenesis_data.append({
            **residue,
            'substitutions': new_substitutions,
            'properties': get_amino_acid_properties(residue.get('wt_amino_acid'))
        })

    return new_mutagenesis_data
