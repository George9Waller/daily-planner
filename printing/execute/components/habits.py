from escpos.printer import Usb
from flask_babel import lazy_gettext as _

from printing.data.dataclasses import HabiticaTasks
from printing.execute.components.utils import center, print_habitica_tasks


def print_habits(p: Usb, print_data: HabiticaTasks):
    p.set_with_default(bold=True)
    p.textln("")
    center(p, _("print.habits"))

    print_habitica_tasks(p, print_data.habits)
