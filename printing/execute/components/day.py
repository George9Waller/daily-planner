from escpos.printer import Usb

from printing.data.dataclasses import Day


def print_day(p: Usb, print_data: Day):
    p.set_with_default(align="center")
    p.textln(print_data.day)
