import json
from pathlib import Path

def save_mutagenesis_data(postfix, mutagenesis_data):
    Path('out').mkdir(exist_ok=True)
    with open('out/mutagenesis_data_' + postfix + '.json', 'w') as mutagenesis_data_json:
            json.dump(mutagenesis_data, mutagenesis_data_json)


def delete_keys_from_dict(data, keys):
    for key in keys:
        data.pop(key, None)
