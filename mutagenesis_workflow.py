import json
from pipeline.enrich_with_uniprot import extract_uniprot_information
from pipeline.filter import filter_high_affinity_substitutions
from pipeline.preprocess import pre_process_mutagenesis_data
from pipeline.set_residue_features import set_residue_features
from utils import save_mutagenesis_data

def main():
    # TODO: this should be an API call
    uniprotkb_data = None
    with open('examples/uniprotkb_Q9BYF1.json') as json_file:
        uniprotkb_data = json.load(json_file)

    print('Preprocessing data...')
    mutagenesis_data = pre_process_mutagenesis_data('examples/GSE147194_ACE2_deep_mutagenesis.csv')
    save_mutagenesis_data('1_initial', mutagenesis_data)
    print('Data processed successfully.\n')

    high_affinity_threshold = 3
    filtering_method = 'mean'
    print(f'Filtering with high affinity threshold = {high_affinity_threshold} and filtering method = \'{filtering_method}\'...')
    mutagenesis_data = filter_high_affinity_substitutions(mutagenesis_data, threshold=high_affinity_threshold, method=filtering_method)
    save_mutagenesis_data('2_high_affinity', mutagenesis_data)
    print(f'Filtering done. Found {len(mutagenesis_data)} residues.\n')

    protein = 'Q9BYF1'
    print(f'Extracting UniProt information for protein {protein}...')
    mutagenesis_data = extract_uniprot_information(mutagenesis_data, protein)
    save_mutagenesis_data('3_uniprot_info', mutagenesis_data)
    print('Extraction done.\n')

    print('Combining residue features...')
    mutagenesis_data = set_residue_features(mutagenesis_data, uniprotkb_data)
    save_mutagenesis_data('4_summary', mutagenesis_data)
    print('Combination of residues done.\n')

    print('Pipeline executed successfully.')

if __name__ == '__main__':
    main()
