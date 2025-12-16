# RogueHostapd - Python 3.13+ Edition

Roguehostapd is a fork of hostapd, the famous user space software access point. It provides Python ctypes bindings and additional attack features. Originally developed for the Wifiphisher project, this version has been modernized by **idenroad** for Python 3.13+ with improved network interface management for modern Linux distributions.

## What's New v1.2.0

- ✅ **Full Python 3.13+ support** (minimum 3.8)
- ✅ **WPA3-SAE support** for modern security
- ✅ **Automatic interface cleanup** on shutdown
- ✅ **Recovery script** to restore NetworkManager
- ✅ **Modern pyproject.toml** for standardized installation
- ✅ **Fixed network crashes** on recent distributions (CachyOS, Arch, etc.)
- ✅ **GitHub Actions CI/CD** for automated testing

## Installation

```bash
git clone https://github.com/idenroad/roguehostapd.git
cd roguehostapd
python3 setup.py install
```

Or with pip (development mode):
```bash
pip install -e .
```

## System Dependencies

On Arch/CachyOS:
```bash
sudo pacman -S libnl iw
```

On Debian/Ubuntu:
```bash
sudo apt-get install libnl-3-dev libnl-genl-3-dev libssl-dev iw
```

## Usage

### Launch Open AP
```bash
python3 run.py -i wlan0 -ssid MyAP
```

### Launch WPA2 AP
```bash
python3 run.py -i wlan0 -ssid MyAP -pK password123
```

### Launch WPA3 AP (SAE)
```bash
python3 run.py -i wlan0 -ssid MySecureAP -pK3 SecurePass2025
```

### Launch KARMA Attack
```bash
python3 run.py -i wlan0 -ssid MyAP -kA
```

### Programmatic Usage
```python
from roguehostapd.apctrl import Hostapd

HOSTAPD_CONFIG = {
    'ssid': 'MyAP',
    'interface': 'wlan0',
    'karma_enable': 1
}

HOSTAPD_OPTIONS = {
    'debug_verbose': False
}

hostapd = Hostapd()
hostapd.start(HOSTAPD_CONFIG, HOSTAPD_OPTIONS)

# Clean shutdown:
hostapd.stop()  # Automatically cleans interface and restores managed mode
```

## Network Connection Issues After Crash?

If your WiFi connection stops working after a roguehostapd crash:

### Quick Fix
```bash
sudo python3 cleanup_interface.py -i wlan0
```

### Auto-cleanup All Interfaces
```bash
sudo python3 cleanup_interface.py -a
```

### What the cleanup script does:
1. Kills all remaining hostapd processes
2. Restores interface to "managed" mode
3. Restarts NetworkManager
4. Unblocks WiFi (rfkill)

## Command Line Options

| Option | Long Form | Description |
|--------|-----------|-------------|
| `-h` | `--help` | Show help message |
| `-ssid SSID` | `--ssid SSID` | Set the AP SSID |
| `-c CHANNEL` | `--channel CHANNEL` | Set the channel (1-14) |
| `-bI BEACON_INT` | `--beacon_int BEACON_INT` | Set beacon interval in ms |
| `-i INTERFACE` | `--interface INTERFACE` | Interface to use (e.g., wlan0) |
| `-pK PASSWORD` | `--wpa_passphrase PASSWORD` | WPA2/WPA password (8-64 chars) |
| `-pK3 PASSWORD` | `--wpa3_passphrase PASSWORD` | WPA3-SAE password (8-64 chars) |
| `-kA` | | Enable KARMA attack |
| `-dV` | `--debug-verbose` | Enable verbose debug logging |
| `-K` | `--key_data` | Include key data in debug messages |
| `-t` | `--timestamp` | Include timestamps in debug messages |
| `-v` | `--version` | Show hostapd version |

## Modern Distribution Improvements

This version specifically fixes issues on modern systems:

1. **Automatic cleanup**: Interface automatically restored to "managed" mode on shutdown
2. **Improved NetworkManager handling**: Clean service restart
3. **Crash recovery**: Dedicated script to restore connectivity
4. **Modern Python**: Full compatibility Python 3.8 to 3.13+

## License

BSD License - See LICENSE.txt

## Credits

- Original Wifiphisher project authors
- **idenroad** - Python 3.13+ modernization and NetworkManager fixes

---

**Important Note**: Use this tool responsibly and only on networks you own or have explicit permission to test.
