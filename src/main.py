from spice import Generator

from src.data import get_dataset, get_target, train_test_split
from src.features.registry import registry
from src.preprocessing import preprocess
from src.resources import get_resources


def main():
    data = get_dataset()
    target = get_target(data)
    data, target = preprocess(data, target)

    train_data, test_data = train_test_split(data)

    feature_generator = Generator(
        registry,
        resources=get_resources(),
        features=[
            "cyclical_pickup_hour",
            "quantile_bin_hour",
            "is_raining",
            "euclidean_distance",
            "manhattan_distance",
        ]
    )
    train_features = feature_generator.fit_transform(train_data)
    test_features = feature_generator.transform(test_data)


if __name__ == '__main__':
    main()
