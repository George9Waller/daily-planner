# Configure values for USB pass through
- Use the corresponding vendor and product IDs from the dmesg output e.g. `New USB device found, idVendor=8089, idProduct=0007, bcdDevice= 8.90`

## Receipt printer
```
lsusb
sudo dmesg | grep -i usb
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="04b8", ATTRS{idProduct}=="0e02", MODE="0664", GROUP="lp"' > sudo nano /etc/udev/rules.d/99-escpos.rules
sudo udevadm control --reload
sudo groupadd lp

```
