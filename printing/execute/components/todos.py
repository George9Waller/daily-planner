from escpos.printer import Usb
from flask_babel import lazy_gettext as _

from printing.data.dataclasses import HabiticaTasks
from printing.execute.components.utils import center, print_habitica_tasks


def print_todos(p: Usb, print_data: HabiticaTasks):
    p.textln("")
    p.set_with_default(double_height=True, double_width=True, bold=True, font="b")
    p.textln(_("print.whatson"))
    p.set_with_default(bold=True)
    center(p, _("print.todos"))

    print_habitica_tasks(p, print_data.todos)
    p.set_with_default()
    for _count in range(5):
        p.textln("[]")
