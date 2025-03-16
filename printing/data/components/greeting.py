from random import choice

from flask_babel import lazy_gettext as _

from printing.data.dataclasses import Greeting
from printing.data.decorators import returns_data_as

GREETINGS = [
    _("printing.greeting.1"),
    _("printing.greeting.2"),
    _("printing.greeting.3"),
]


@returns_data_as(Greeting)
def get_greeting(*args, **kwargs):
    return {"greeting": str(choice(GREETINGS))}
