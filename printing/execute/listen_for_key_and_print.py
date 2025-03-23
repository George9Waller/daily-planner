import logging
import os
import subprocess

from evdev import categorize, ecodes, InputDevice

logger = logging.getLogger(__name__)


def _get_device_path():
    with open("/config/keyboard_path", "r") as f:
        device_path = f.read().strip()

    if not device_path:
        raise ValueError("Keyboard path not found")

    return device_path


def listen_for_key_and_print():
    trigger_key = os.environ.get("TRIGGER_KEY") or "KEY_P"
    device_path = _get_device_path()
    device = InputDevice(device_path)

    logger.info(f"Listening for key events from '{device_path}'")
    logger.info(f"Trigger key: '{trigger_key}'")
    for event in device.read_loop():
        logger.info(f"Received event: {event}")
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            logger.info(f"- Key Event: {key_event}")
            if key_event.keystate == key_event.key_down:
                if key_event.keycode == trigger_key:
                    logger.info("Trigger key pressed, printing")
                    try:
                        subprocess.run(["flask", "print-now"])
                    except Exception as e:
                        logger.error(f"Error printing: {e}")


if __name__ == "__main__":
    listen_for_key_and_print()
