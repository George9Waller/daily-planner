from flask_babel import force_locale
from pydantic import ValidationError

from printing import COMPONENTS
from printing.data.components import (
    get_day,
    get_greeting,
    get_habitica_tasks,
    get_reflection,
    get_weather,
)
from printing.data.dataclasses import GetPrintDataResponse, PrintData, PrintDataContext

COMPONENT_TO_METHOD = {
    "day": get_day,
    "greeting": get_greeting,
    "weather": get_weather,
    "todos": get_habitica_tasks,
    "dailies": get_habitica_tasks,
    "habits": get_habitica_tasks,
    "reflection": get_reflection,
}


def get_print_data(print_data_context: PrintDataContext) -> GetPrintDataResponse:
    is_fatal = False
    print_data = {}
    errors = {}
    with force_locale(print_data_context.locale):
        for component in COMPONENTS:
            try:
                print_data_method = COMPONENT_TO_METHOD[component]
                value = print_data_method(print_data_context=print_data_context)
                print_data[component] = value
                errors[component] = None
            except ValidationError as e:
                print_data[component] = None
                errors[component] = e.errors()
            except Exception as e:
                print_data[component] = None
                errors[component] = str(e)

    try:
        PrintData.validate(print_data)
    except ValidationError as e:
        errors["_"] = e.errors()
        is_fatal = True

    return GetPrintDataResponse(print_data=print_data, errors=errors, is_fatal=is_fatal)
