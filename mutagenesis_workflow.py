import argparse
import json
from pipeline.enrich_with_uniprot import extract_uniprot_information
from pipeline.filter import filter_high_affinity_substitutions
from pipeline.preprocess import pre_process_mutagenesis_data
from pipeline.set_residue_features import set_residue_features
from utils import save_mutagenesis_data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mutagenesis_file', help='the mutagenesis csv file')
    parser.add_argument('-p', '--protein', type=str, default='Q9BYF1', help='the uniprot protein id')
    parser.add_argument('-s', '--steps', nargs='*', help='specify the steps to run')
    parser.add_argument('-t', '--filter-threshold', type=int, default=3, help='filtering threshold')
    parser.add_argument('-m', '--filter-method', type=str, default='mean', help='filtering method')
    parser.add_argument('-o', '--output', type=str, default='out', help='output directory name')
    args = parser.parse_args()

    should_run_all = args.steps is None or args.steps[0] == 'all' or args.steps[0] == '*'

    # TODO: this should be an API call
    uniprotkb_data = None
    with open('examples/uniprotkb_Q9BYF1.json') as json_file:
        uniprotkb_data = json.load(json_file)

    print('Preprocessing data...')
    mutagenesis_data = pre_process_mutagenesis_data(args.mutagenesis_file)
    save_mutagenesis_data(args.output, '1_initial', mutagenesis_data)
    print('Data processed successfully.\n')

    if should_run_all or 'filter' in args.steps:
        high_affinity_threshold = args.filter_threshold
        filtering_method = args.filter_method
        print(f'Filtering with high affinity threshold = {high_affinity_threshold} and filtering method = \'{filtering_method}\'...')
        mutagenesis_data = filter_high_affinity_substitutions(mutagenesis_data, threshold=high_affinity_threshold, method=filtering_method)
        save_mutagenesis_data(args.output, '2_high_affinity', mutagenesis_data)
        print(f'Filtering done. Found {len(mutagenesis_data)} residues.\n')

    if should_run_all or 'uniprot_enrich' in args.steps:
        print(f'Extracting UniProt information for protein {args.protein}...')
        mutagenesis_data = extract_uniprot_information(mutagenesis_data, args.protein)
        save_mutagenesis_data(args.output, '3_uniprot_info', mutagenesis_data)
        print('Extraction done.\n')

    if should_run_all or 'residue_features' in args.steps:
        print('Combining residue features...')
        mutagenesis_data = set_residue_features(mutagenesis_data, uniprotkb_data)
        save_mutagenesis_data(args.output, '4_summary', mutagenesis_data)
        print('Combination of residues done.\n')

    print('Pipeline executed successfully.')

if __name__ == '__main__':
    main()
