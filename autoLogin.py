"""
This module handles automatic login to the RUB network by periodically
checking connectivity and initiating a login process when necessary.
"""

import time
import subprocess
import requests

LOGINID = "ab12345@w-hs.de"  # change ab12345 with your ZA credentials
PASSWORD = "password"  # change password to your actual ZA password
IPADDRESS = ""  # LEAVE EMPTY unless you know what you're doing

LOGIN_PAGE = "login.ruhr-uni-bochum.de"
LOGIN_URL = "https://login.ruhr-uni-bochum.de/cgi-bin/laklogin"
WEBSITES_TO_PING = ["google.com", "wikipedia.org", "youtube.com", "deutschland.de"]

SLEEP_TIME = 500  # seconds

def ping_website(website):
    """
    Attempt to ping a website.
    
    :param website: The website to ping
    :return: True if ping is successful, False otherwise
    """
    try:
        subprocess.run(
            ["ping", "-c", "3", "-W", "5", website],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False

def check_login_page():
    """
    Check if the login page is reachable.
    
    :return: True if login page is reachable, False otherwise
    """
    if ping_website(LOGIN_PAGE):
        print(f"Ping to {LOGIN_PAGE} successful")
        return True
    else:
        print(f"{LOGIN_PAGE} cannot be reached at the moment")
        return False

def check_connectivity():
    """
    Check connectivity by pinging a list of websites.
    
    :return: True if any website is reachable, False otherwise
    """
    for website in WEBSITES_TO_PING:
        if ping_website(website):
            print(f"Ping to {website} successful")
            return True
    return False

def login():
    """
    Attempt to log in to the network.
    
    :return: True if login is successful, False otherwise
    """
    try:
        response = requests.post(
            LOGIN_URL,
            data={
                "code": "1",
                "loginid": LOGINID,
                "password": PASSWORD,
                "ipaddr": IPADDRESS,
                "action": "Login"
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=10
        )
        print(response.text)  # Print the response for debugging
        return "Authentisierung gelungen" in response.text
    except requests.RequestException as e:
        print(f"Login attempt failed: {e}")
        return False

def main():
    """
    Main loop to check connectivity and manage login attempts.
    """
    while True:
        if not check_login_page() or not check_connectivity():
            print("Connection failed, attempting login")
            if login():
                print("Login successful")
            else:
                print("Login failed")
        else:
            print("Connection is active")

        print(f"Sleeping for {SLEEP_TIME} seconds")
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    main()
