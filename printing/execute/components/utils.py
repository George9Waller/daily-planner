import math
from typing import List

from escpos.printer import Usb
from PIL import Image

from printing.data.dataclasses import HabiticaTask


def divider(p: Usb, character="-"):
    assert len(character) == 1
    p.textln(character * p.profile.get_columns("a"))


def center(p: Usb, text, font="a", padding_character="-"):
    assert len(padding_character) == 1
    columns = p.profile.get_columns(font)
    text_columns = len(text)
    padding = padding_character * math.floor((columns - text_columns - 2) / 2)
    p.set(align="center")
    p.textln(padding + " " + text + " " + padding)


def transform_rgba_monochrome(image: Image):
    pixels = list(image.getdata())
    new_pixels = [(255, 255, 255) if pixel[3] == 0 else (0, 0, 0) for pixel in pixels]
    monochrome = Image.new("RGB", image.size)
    monochrome.putdata(new_pixels)
    return monochrome


def print_habitica_tasks(p: Usb, tasks: List[HabiticaTask]):
    p.set_with_default()
    for task in tasks:
        p.textln(f"[] {task.text}")
        if task.notes:
            p.set_with_default(font="b")
            p.textln(task.notes)
            p.set_with_default()
        for step in task.checklist:
            p.textln(f"  [] {step}")
