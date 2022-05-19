from statistics import mean


def filter_high_affinity_substitutions(mutagenesis_data, threshold=3, method='mean'):
    def _filter(s):
        hsr1 = s.get('high_sort_rep_1')
        hsr2 = s.get('high_sort_rep_2')

        if method == 'mean':
            avg_hsr = mean([hsr1, hsr2])
            return avg_hsr >= threshold or avg_hsr <= -threshold
        else:
            return any([hsr1 >= threshold, hsr2 >= threshold, hsr1 <= -threshold, hsr2 <= -threshold])

    new_mutagenesis_data = []

    for m in mutagenesis_data:
        new_m = m
        new_m['substitutions'] = list(filter(_filter, m.get('substitutions')))

        if len(new_m['substitutions']) > 0:
            new_mutagenesis_data.append(new_m)

    return new_mutagenesis_data
