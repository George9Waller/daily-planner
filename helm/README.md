# Configure values for USB pass through
- Use the corresponding path for the controller e.g. `hiddev0` in `hid-generic 0003:8089:0007.0004: input,hiddev0,hidraw1: USB HID v1.11 Mouse [SayoDevice SayoDevice M3K RGB] on usb-0000:00:14.0-7/input1`
- Use the corresponding vendor and product IDs from the dmesg output e.g. `New USB device found, idVendor=8089, idProduct=0007, bcdDevice= 8.90`

## Receipt printer
```
lsusb
sudo dmesg | grep -i usb
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="04b8", ATTRS{idProduct}=="0e02", MODE="0664", GROUP="lp"' > sudo nano /etc/udev/rules.d/99-escpos.rules
sudo udevadm control --reload
sudo groupadd lp

```

## Keyboard
```
lsusb
sudo dmesg | grep -i usb

# get keyboard
ls -l /dev/input/by-id/

sudo chown root:input /dev/usb/hiddev0
sudo chmod 660 /dev/usb/hiddev0
sudo nano /etc/udev/rules.d/99-usb-hid.rules > SUBSYSTEM=="usb", ATTRS{idVendor}=="8089", ATTRS{idProduct}=="0007", MODE="0666", GROUP="input"
sudo udevadm control --reload
sudo groupadd input
sudo udevadm trigger
```
