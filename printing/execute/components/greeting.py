from escpos.printer import Usb

from printing.data.dataclasses import Greeting


def print_greeting(p: Usb, print_data: Greeting):
    p.set_with_default(
        align="center",
        bold=True,
        custom_size=True,
        width=3,
        height=3,
        invert=True,
        smooth=True,
    )
    p.textln(" " + print_data.greeting + " ")
    p.set_with_default()
    p.textln("")
