# autoLoginAtRUB

## What this script does

periodically check for the internet connection. If there's no internet connection, the script performs a login to the RUB login site to active the router. After correct setup it will run forever and start automatically upon boot/reboot ofd the raspbery pi.

## How to use

this is only for installing on a raspberry pi that's connected to the router/network. It **doesn't work on Windows PC or any device other than raspberry pi**

## Setup

1. pull repro into desired directory
2. use nano (or similar text editor) to ediut autoLogin.py to change these lines of code:
```
LOGINID = "ab12345@w-hs.de"  # change ab12345 with your ZA credentials
PASSWORD = "password"        # change password to your actual ZA password
IPADDRESS = ""               # LEAVE EMPTY unless you know what you're doing
```
and do **not change anything else** *(unless you know what you're doing)* <br>
3. make this run on raspberry startup (as service file) <br>
&ensp;3.1. Create a service file:
```
sudo nano /etc/systemd/system/autologin.service
```
&ensp;3.2. Paste content and change `/path/to/autoLogin.py` to the actual path of the script:
```
[Unit]
Description=Auto Login Script
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/autoLogin.py
User=p1
Restart=always

[Install]
WantedBy=multi-user.target
```
&ensp;3.3 Save and Reload systemd, enable and start the service:
```
sudo systemctl daemon-reload
sudo systemctl enable autologin.service
sudo systemctl start autologin.service
```

## Control the script

if you want to change your pasword, use systemctl commands to stop and start the script.
```
sudo systemctl stop autologin.service
```
edit the autoLogin.py to change the password
```
sudo systemctl start autologin.service
```

## Dependencies

1. Python: `Version 3.6` or higher
2. Built-in Python libraries (no installation needed): `time`, `subprocess`
3. External Python libraries: `requests`
4. System utilities: `ping` (usually pre-installed on most systems)
5. Permissions: Ability to make outgoing network connections, Permission to execute the ping command<br>

### Checking dependencies

1. Ensure Python 3.6+ and pip is installed:
```
python3 --version
pip --version
```
2. Install `requests` library:
```
pip install requests
```
3. Verify `ping` is available:
```
which ping
```
