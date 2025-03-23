# syntax=docker/dockerfile:1

FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    gettext \
    build-essential \
    libpq-dev \
    libusb-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN bash /app/scripts/translations

RUN chmod +x /app/scripts/start-hosted
RUN chmod +x /app/scripts/migrate
RUN chmod +x /app/scripts/listen-for-print

# https://python-escpos.readthedocs.io/en/latest/user/installation.html
# Create the udev rule for the USB printer
RUN echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="04b8", ATTRS{idProduct}=="0e02", MODE="0664", GROUP="dialout"' > /etc/udev/rules.d/99-escpos.rules

# Reload udev rules
RUN udevadm control --reload-rules && udevadm trigger

# Add the user to the dialout group
RUN usermod -aG dialout root

# Ensure udev runs in the container (required for USB device detection)
CMD ["udevadm", "control", "--reload"]
