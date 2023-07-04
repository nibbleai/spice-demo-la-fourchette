import logging

from spice import Generator
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

from src.data import get_dataset, get_target, train_test_split
from src.features.registry import registry
from src.preprocessing import preprocess
from src.resources import get_resources


def main():
    data = get_dataset()
    target = get_target(data)
    data, target = preprocess(data, target)

    train_data, test_data = train_test_split(data)
    train_target = target.loc[train_data.index]
    test_target = target.loc[test_data.index]

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
    train_features = feature_generator.fit_transform(train_data).to_pandas()
    test_features = feature_generator.transform(test_data).to_pandas()

    model = RandomForestRegressor().fit(train_features, train_target)

    predicted = model.predict(test_features)
    m2_score = mean_squared_error(test_target, predicted)
    logging.info(f"M2 score is {m2_score}")


if __name__ == '__main__':
    main()
