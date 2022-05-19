def set_residue_features(mutagenesis_data, uniprotkb_data):
    def _only_important_features(feature):
        feature_type = feature.get('type')

        return feature_type not in ['Chain', 'Signal', 'Mutagenesis', 'Alternative sequence']

    new_mutagenesis_data = []

    for residue in mutagenesis_data:
        residue_position = residue.get('residue')
        features = []

        for feature in filter(_only_important_features, uniprotkb_data.get('features')):
            feature_start = feature.get('location').get('start').get('value')
            feature_end = feature.get('location').get('end').get('value')

            if residue_position >= feature_start and residue_position <= feature_end:
                features.append(feature)

        new_mutagenesis_data.append({
            **residue,
            'features': features
        })

    return new_mutagenesis_data
