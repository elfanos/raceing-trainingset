
def static_dataset_columns(prefix: str):
    columns = [
        prefix + "_starts",
        prefix + "_earnings",
        prefix + "_placement_1",
        prefix + "_placement_2",
        prefix + "_placement_3",
        prefix + "_winPercentage"
    ]
    return columns


def statistic_dataset(data, prefix: str):
    features = []
    columns = []
    if data is None:
        return features, columns

    for (year, stats) in data.items():
        print(stats)
        starts = stats["starts"]
        earnings = stats["earnings"]
        placements = stats["placement"]
        win_percentage = stats["winPercentage"]
        #
        # # Create a feature vector
        feature_vector = [
            year,
            starts,
            earnings,
            placements["1"],
            placements["2"],
            placements["3"],
            win_percentage
        ]
        print(feature_vector)
        #
        columns.append([prefix + "_year", prefix + "_starts", prefix + "_earnings", prefix +
                       "_placement_1", prefix + "_placement_2", prefix + "_placement_3", prefix + "_winPercentage"])
        features.append(feature_vector)

    return features, columns


def statistic_df(data, prefix: str):
    return statistic_dataset(data, prefix)
