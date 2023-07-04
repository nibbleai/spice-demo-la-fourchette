import numpy as np

from src.schemas import TaxiColumn
from src.invariants import HOURS_IN_DAY
from spice import Registry
import pandas as pd

from src.utils import cyclical

registry = Registry("registry_adrien")


@registry.register(name="pickupTime")
def pickup_time(data):
    return data[TaxiColumn.PICKUP_TIME]


@registry.register(depends=("pickupTime",))
def pickup_date(pickup_time):
    return pickup_time.dt.date


@registry.register(depends=("pickupTime",))
def pickup_hour(pickup_time):
    return pickup_time.dt.hour

@registry.register(depends=("pickup_hour",))
def cyclical_pickup_hour(pickup_hour):
    return cyclical(pickup_hour, HOURS_IN_DAY)

@registry.register(depends=('pickup_hour',))
class QuantileBinHour:
    def fit(self, pickup_hour):
        hours_bins = pd.qcut(pickup_hour, q=4)
        self.bins_ = hours_bins.cat.categories
        return self
    def transform(self, pickup_hour):
        quantile_bins_hour = pd.cut(pickup_hour, bins=self.bins_)
        hours_bins_labels = np.arange(4) + 1
        return quantile_bins_hour.cat.rename_categories(hours_bins_labels)