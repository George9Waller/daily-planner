from escpos.printer import Usb
from flask_babel import lazy_gettext as _

from printing.data.dataclasses import HabiticaTasks
from printing.execute.components.utils import center, divider


def print_reflection(p: Usb, print_data: HabiticaTasks):
    p.textln("")
    p.set_with_default(align="center", double_height=True, double_width=True, bold=True, font="b")
    p.textln(_("print.Reflection"))
    p.set_with_default(align="center")
    divider(p, "░")
    p.textln(_("print.whatwentwell"))
    for _count in range(7):
        p.textln("")
    divider(p, "▒")
    p.textln(_("print.whatcouldbebetter"))
    for _count in range(7):
        p.textln("")
    divider(p, "▓")
