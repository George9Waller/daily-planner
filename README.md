# Setup
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

# Configure printer on linux
```
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="04b8", ATTRS{idProduct}=="0e02", MODE="0664", GROUP="lp"' > sudo nano /etc/udev/rules.d/99-escpos.rules
sudo udevadm control --reload
sudo groupadd lp

```

# Env vars
- `BABEL_DEFAULT_LOCALE` "fr_FR" or "en_GB"
- `DATABASE_URL`
- `OPEN_WEATHER_API_KEY`
- `HABITICA_USER_ID`
- `HABITICA_API_TOKEN`