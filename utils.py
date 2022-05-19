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
