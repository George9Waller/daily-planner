import logging

from escpos.exceptions import DeviceNotFoundError
from escpos.printer import Usb
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)
from usb.core import USBError

from printing import COMPONENTS
from printing.data.dataclasses import PrintData
from printing.execute.components import (
    print_dailies,
    print_day,
    print_greeting,
    print_habits,
    print_reflection,
    print_todos,
    print_weather,
)
from printing.execute.print_to_html import HTMLPrinter

logger = logging.getLogger(__name__)

COMPONENT_TO_METHOD = {
    "dailies": print_dailies,
    "day": print_day,
    "greeting": print_greeting,
    "habits": print_habits,
    "todos": print_todos,
    "weather": print_weather,
    "reflection": print_reflection,
}


@retry(
    stop=stop_after_attempt(3),
    retry=retry_if_exception(USBError),
    wait=wait_exponential_jitter(initial=1, max=5),
)
def get_printer():
    return Usb(idVendor=0x04B8, idProduct=0x0E02, profile="TM-T88V")


def get_printer_online_status():
    try:
        p = get_printer()
        return p.is_online()
    except (DeviceNotFoundError, USBError):
        return False


def print_label(print_data: dict):
    parsed_print_data = PrintData(**print_data)

    # TODO: configure printer from db
    try:
        p = get_printer()
        _print_label(p, parsed_print_data)
        return True
    except (DeviceNotFoundError, USBError):
        logger.warning("No printer found")
        return False


def print_label_as_html(print_data: dict):
    parsed_print_data = PrintData(**print_data)
    p = HTMLPrinter()
    _print_label(p, parsed_print_data)
    return p.render()


def _print_label(p, print_data: PrintData):
    for component in COMPONENTS:
        print_component = COMPONENT_TO_METHOD[component]
        component_data = getattr(print_data, component, None)
        if component_data:
            print_component(p, component_data)
            p.set_with_default()

    p.cut()
    # TODO: move this to only connect and close once in batch prints
    p.close()
