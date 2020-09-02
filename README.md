# mac-changer [![Maintainability](https://api.codeclimate.com/v1/badges/fe37dada41aac61879f4/maintainability)](https://codeclimate.com/github/Sahil-Poonia/mac-changer/maintainability)
A simple python mac changer to change the mac address of network interfaces.

# Installation
make sure you are using linux and have following tool(s) installed on your system:
```bash
iproute2 (for Ubuntu / Debian) OR iproute (for CentOS / Fedora)
ethtool
```

Use the package manager pip to install all the requirements according to requirements.txt.
```bash
pip install -r requirements.txt
```

# Usage
```bash
python3 mac_changer.py -h
```

# Options
```bash
  -h, --help            show this help message and exit
  -i, --interface       name of network interface. (e.g:- wlan0, eth0, etc..)
  -m, --mac             desired mac address. (e.g:- 00:11:22:33:44:55)
  -a                    shows all interfaces
  -r, --reset           reset the mac address of specified network interfac
```
⚠️ the option 'show all interfaces' requires internet access to show their respective network interface's vendor. else, it'll show an unknown vendor.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
