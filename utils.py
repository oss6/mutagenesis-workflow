import json
from os import path
from pathlib import Path

def save_mutagenesis_data(output_directory, postfix, mutagenesis_data):
    Path(output_directory).mkdir(exist_ok=True)
    with open(path.join(output_directory, 'mutagenesis_data_' + postfix + '.json'), 'w') as mutagenesis_data_json:
            json.dump(mutagenesis_data, mutagenesis_data_json)

def delete_keys_from_dict(data, keys):
    for key in keys:
        data.pop(key, None)

def get_amino_acid_properties(residue):
    properties = {
        'A': ['nonpolar'],
        'G': ['nonpolar'],
        'V': ['nonpolar'],
        'L': ['nonpolar'],
        'I': ['nonpolar'],
        'M': ['nonpolar'],
        'P': ['nonpolar'],
        'F': ['aromatic'],
        'W': ['aromatic'],
        'Y': ['aromatic'],
        'S': ['polar'],
        'T': ['polar'],
        'C': ['polar'],
        'B': ['polar'],
        'Q': ['polar'],
        'N': ['polar'],
        'D': ['acidic'],
        'E': ['acidic'],
        'K': ['basic'],
        'R': ['basic'],
        'H': ['basic']
    }

    properties_descriptions = {
        'nonpolar': 'The R groups in this class of amino acids are nonpolar and hydrophobic.',
        'aromatic': 'Amino acids with aromatic side chains are relatively nonpolar (hydrophobic). All can participate in hydrophobic interactions.',
        'polar': 'The R groups of these amino acids are more soluble in water, or more hydrophilic, than those of the nonpolar amino acids, because they contain functional groups that form hydrogen bonds with water.',
        'acidic': 'Amino acids in which R-group is acidic or negatively charged.',
        'basic': 'Amino acids in which R-group is basic or positively charged.'
    }

    return [{'name': property_name, 'description': properties_descriptions.get(property_name)} for property_name in properties.get(residue, [])]
