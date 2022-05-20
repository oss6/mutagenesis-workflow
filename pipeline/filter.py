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

    high_affinity_mutagenesis_data = []
    neutral_affinity_mutagenesis_data = []

    for m in mutagenesis_data:
        hm = {**m, 'substitutions': []}
        nm = {**m, 'substitutions': []}

        for s in m.get('substitutions'):
            if _filter(s):
                hm['substitutions'].append(s)
            else:
                nm['substitutions'].append(s)

        # hm['substitutions'] = list(filter(_filter, m.get('substitutions')))

        # if len(hm['substitutions']) > 0:
        #     high_affinity_mutagenesis_data.append(hm)

        if len(hm['substitutions']) > 0:
            high_affinity_mutagenesis_data.append(hm)

        if len(nm['substitutions']) > 0:
            neutral_affinity_mutagenesis_data.append(nm)

    return high_affinity_mutagenesis_data, neutral_affinity_mutagenesis_data
