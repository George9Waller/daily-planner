from datetime import date

from flask_babel import format_date

from printing.data.dataclasses import Day, PrintDataContext
from printing.data.decorators import returns_data_as


@returns_data_as(Day)
def get_day(*, print_data_context: PrintDataContext, **kwargs):
    parsed_date = date.fromisoformat(print_data_context.date)
    return {"day": format_date(parsed_date, format="full")}
