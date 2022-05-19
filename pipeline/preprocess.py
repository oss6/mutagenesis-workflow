import csv

def _get_substitution_item(row):
    return {
        'substitution': row[2],
        'reads_in_naive_lib': row[3],
        'high_sort_rep_1': float(row[4]),
        'high_sort_rep_2': float(row[5]),
        'type': row[6]
    }

def pre_process_mutagenesis_data(source_file):
    with open(source_file, newline='') as mutagenesis_data_file:
        mutagenesis_data_reader = csv.reader(mutagenesis_data_file)
        mutagenesis_data = []
        current_residue = {}

        for index, row in enumerate(mutagenesis_data_reader):
            if index == 0:
                continue

            if row[0] != '':
                if current_residue:
                    mutagenesis_data.append(current_residue)

                current_residue = {}
                current_residue['residue'] = int(row[0])
                current_residue['wt_amino_acid'] = row[1]
                current_residue['substitutions'] = [_get_substitution_item(row)]
            else:
                current_residue['substitutions'].append(_get_substitution_item(row))

        mutagenesis_data.append(current_residue)

    return mutagenesis_data
