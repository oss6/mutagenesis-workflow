import argparse
import json
from pipeline.enrich_with_aa_properties import enrich_with_amino_acid_properties
from pipeline.enrich_with_uniprot import enrich_with_uniprot_information
from pipeline.filter import filter_high_affinity_substitutions
from pipeline.preprocess import pre_process_mutagenesis_data
from pipeline.enrich_with_residue_features import enrich_with_residue_features
from utils import save_mutagenesis_data, save_session_input

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mutagenesis_file', help='the mutagenesis csv file')
    parser.add_argument('-p', '--protein', type=str, default='Q9BYF1', help='the uniprot protein id')
    parser.add_argument('-s', '--steps', nargs='*', help='specify the steps to run (filter, uniprot_enrich, residue_features, aa_props)')
    parser.add_argument('-t', '--filter-threshold', type=int, default=3, help='filtering threshold')
    parser.add_argument('-m', '--filter-method', type=str, default='mean', help='filtering method')
    parser.add_argument('-o', '--output', type=str, default='out', help='output directory name')
    parser.add_argument('-c', '--compact', action='store_true', default=False, help='whether to get compact output files')
    args = parser.parse_args()

    should_run_all = args.steps is None or args.steps[0] == 'all' or args.steps[0] == '*'

    # TODO: this should be an API call
    uniprotkb_data = None
    with open('examples/uniprotkb_Q9BYF1.json') as json_file:
        uniprotkb_data = json.load(json_file)

    print('Preprocessing data...')
    mutagenesis_data = pre_process_mutagenesis_data(args.mutagenesis_file)
    save_mutagenesis_data(args.output, 'initial', mutagenesis_data, args.compact)
    print('Done.\n')

    if should_run_all or 'filter' in args.steps:
        high_affinity_threshold = args.filter_threshold
        filtering_method = args.filter_method
        print(f'Filtering with high affinity threshold = {high_affinity_threshold} and filtering method = \'{filtering_method}\'...')
        mutagenesis_data, n_mutagenesis_data = filter_high_affinity_substitutions(mutagenesis_data, threshold=high_affinity_threshold, method=filtering_method)
        save_mutagenesis_data(args.output, 'high_affinity', mutagenesis_data, args.compact)
        print(f'Done. Found {len(mutagenesis_data)} high affinity residues and {len(n_mutagenesis_data)} neutral residues.\n')

    if should_run_all or 'uniprot_enrich' in args.steps:
        print(f'Enriching with UniProt information for protein {args.protein}...')
        mutagenesis_data = enrich_with_uniprot_information(mutagenesis_data, args.protein)
        save_mutagenesis_data(args.output, 'uniprot_info', mutagenesis_data, args.compact)
        print('Done.\n')

    if should_run_all or 'residue_features' in args.steps:
        print('Enriching with residue features...')
        mutagenesis_data = enrich_with_residue_features(mutagenesis_data, uniprotkb_data)
        n_mutagenesis_data = enrich_with_residue_features(n_mutagenesis_data, uniprotkb_data)
        save_mutagenesis_data(args.output, 'residue_features', mutagenesis_data, args.compact)
        print('Done.\n')

    if should_run_all or 'aa_props' in args.steps:
        print('Enriching with amino acid properties...')
        mutagenesis_data = enrich_with_amino_acid_properties(mutagenesis_data)
        n_mutagenesis_data = enrich_with_amino_acid_properties(n_mutagenesis_data)
        save_mutagenesis_data(args.output, 'aa_props', mutagenesis_data, args.compact)
        print('Done.\n')

    save_mutagenesis_data(args.output, 'summary', mutagenesis_data, args.compact)
    save_mutagenesis_data(args.output, 'summary_neutral', n_mutagenesis_data, args.compact)
    save_session_input(args)
    print(f'Results saved in {args.output}')
    print('Pipeline executed successfully.')

if __name__ == '__main__':
    main()
