from src.schemas import TaxiColumn
from spice import Registry


registry = Registry("registry_adrien")


@registry.register(name="pickupTime")
def pickup_time(data):
    return data[TaxiColumn.PICKUP_TIME]


@registry.register(depends=("pickupTime",))
def pickup_date(pickup_time):
    return pickup_time.dt.date