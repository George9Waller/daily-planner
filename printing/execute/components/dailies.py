from escpos.printer import Usb
from flask_babel import lazy_gettext as _

from printing.data.dataclasses import HabiticaTasks
from printing.execute.components.utils import center, print_habitica_tasks


def print_dailies(p: Usb, print_data: HabiticaTasks):
    p.set_with_default(bold=True)
    p.textln("")
    center(p, _("print.dailies"))
    print_habitica_tasks(p, print_data.dailies)
