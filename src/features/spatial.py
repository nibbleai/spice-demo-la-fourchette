import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from src.config import config
from src.features.registry import registry
from src.schemas import TaxiColumn


@registry.register(name="pickup_lon")
def pickup_longitude(data):
    """Longitude of pickup position."""
    return data[TaxiColumn.PICKUP_LON]


@registry.register(name="pickup_lat")
def pickup_latitude(data):
    """Latitude of pickup position."""
    return data[TaxiColumn.PICKUP_LAT]


@registry.register(name="dropoff_lon")
def dropoff_longitude(data):
    """Longitude of dropoff position."""
    return data[TaxiColumn.DROPOFF_LON]


@registry.register(name="dropoff_lat")
def dropoff_latitude(data):
    """Latitude of dropoff position."""
    return data[TaxiColumn.DROPOFF_LAT]


@registry.register(
    name="euclidean_distance",
    depends=["pickup_lon", "pickup_lat", "dropoff_lon", "dropoff_lat"]
)
def euclidean_distance(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
    """Euclidean distance between pickup & dropoff positions."""
    return np.sqrt(
        abs(pickup_lon - dropoff_lon) ** 2 + abs(pickup_lat - dropoff_lat) ** 2
    )

@registry.register(
    name="manhattan_distance",
    depends=["pickup_lon", "pickup_lat", "dropoff_lon", "dropoff_lat"]
)
def manhattan_distance(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
    """Manhattan distance between pickup & dropoff positions."""
    return (abs(pickup_lon - dropoff_lon) + abs(pickup_lat - dropoff_lat))


@registry.register(name="pickup_cluster", depends=["pickup_lon", "pickup_lat"])
class PickupCluster:
    """Kmeans cluster from pickup coordinates."""

    def fit(self, pickup_lon, pickup_lat):
        self.kmeans_ = KMeans(n_clusters=config.features.pickup_n_clusters)
        pickup_coords = pd.concat([pickup_lon, pickup_lat], axis=1)
        self.kmeans_.fit(pickup_coords)
        return self

    def transform(self, pickup_lon, pickup_lat):
        pickup_coords = pd.concat([pickup_lon, pickup_lat], axis=1)
        return self.kmeans_.predict(pickup_coords)


@registry.register(
    name="dropoff_cluster", depends=["dropoff_lon", "dropoff_lat"]
)
class DropoffCluster:
    """Kmeans cluster from dropoff coordinates."""

    def fit(self, dropoff_lon, dropoff_lat):
        self.kmeans_ = KMeans(n_clusters=config.features.dropoff_n_clusters)
        dropoff_coords = pd.concat([dropoff_lon, dropoff_lat], axis=1)
        self.kmeans_.fit(dropoff_coords)
        return self

    def transform(self, dropoff_lon, dropoff_lat):
        dropoff_coords = pd.concat([dropoff_lon, dropoff_lat], axis=1)
        return self.kmeans_.predict(dropoff_coords)
