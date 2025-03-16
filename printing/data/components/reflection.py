from printing.data.dataclasses import Reflection
from printing.data.decorators import returns_data_as


@returns_data_as(Reflection)
def get_reflection(*args, **kwargs):
    return {"data": "no-data"}
