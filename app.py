import re
import time
import os
import sqlite3
import telnetlib
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
load_dotenv()

vendor_cache = {}

app = Flask(__name__)
app.secret_key = os.getenv('appseckey')

USERNAME = os.getenv('routeruser')
PASSWORD = os.getenv('routerpass')

TELNET_USER = os.getenv('teluser')
TELNET_PASSWORD = os.getenv('telpass')
TELNET_PORT = 23

def is_valid_mac(mac):
    return re.match(r"^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$", mac) is not None

def is_valid_ip(ip):
    return re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip) is not None

def get_mac_vendor(mac):
    prefix = mac.replace(":", "").replace("-", "").upper()[:6]
    if prefix in vendor_cache:
        return vendor_cache[prefix]

    try:
        conn = sqlite3.connect("vendors.db")
        cursor = conn.cursor()
        cursor.execute("SELECT vendor FROM vendors WHERE prefix = ?", (prefix,))
        result = cursor.fetchone()
        conn.close()

        if result:
            vendor = result[0]
            vendor_cache[prefix] = vendor
            return vendor
    except Exception as e:
        print("SQLite Error:", e)

    return "Unknown vendor"

def fetch_hostnames_telnet(router_ip):
    try:
        tn = telnetlib.Telnet(router_ip, TELNET_PORT, timeout=10)

        tn.read_until(b"login: ")
        tn.write(TELNET_USER.encode('ascii') + b"\n")

        tn.read_until(b"Password: ")
        tn.write(TELNET_PASSWORD.encode('ascii') + b"\n")

        tn.write(b"cd /tmp\n")
        tn.read_until(b"$", timeout=3)

        tn.write(b"cat hosts\n")
        hosts_output = tn.read_until(b"#", timeout=5).decode('ascii')

        tn.write(b"exit\n")
        tn.close()

        host_dict = {}
        for line in hosts_output.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = re.split(r'\s+', line)
            if len(parts) >= 2:
                ip = parts[0]
                hostname = parts[1]
                host_dict[ip] = hostname

        return host_dict

    except Exception as e:
        print(f"Telnet Error: {e}")
        return {}

def fetch_dhcp_clients(router_ip):
    chrome_options = Options()
    chrome_bin = os.getenv("CHROME_BIN")
    # added .env and now need to define the chrome_bin location
    if chrome_bin:
        chrome_options.binary_location = chrome_bin

    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])


    driver = webdriver.Chrome(options=chrome_options)

    try:
        url = f"http://{router_ip}/"
        dhcp_url = f"http://{router_ip}/admin/dhcptbl.asp"

        driver.get(url)
        time.sleep(2)

        driver.find_element(By.ID, "username").clear()
        driver.find_element(By.ID, "username").send_keys(USERNAME)

        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys(PASSWORD)

        driver.find_element(By.ID, "submitBtn").click()
        time.sleep(3)

        driver.get(dhcp_url)
        time.sleep(3)

        table = None
        for t in driver.find_elements(By.TAG_NAME, "table"):
            if t.get_attribute("border") == "1":
                table = t
                break

        if not table:
            return []

        clients = []
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 2:
                ip = cols[0].text.strip()
                mac = cols[1].text.strip()
                if not (is_valid_ip(ip) and is_valid_mac(mac)):
                    continue
                vendor = get_mac_vendor(mac)
                clients.append((ip, mac, vendor))
                time.sleep(0.3)

        return clients

    except Exception as e:
        print("Selenium Error:", e)
        return []

    finally:
        driver.quit()

def fetch_dhcp_clients_with_hostnames(router_ip):
    hostnames = fetch_hostnames_telnet(router_ip)
    dhcp_clients = fetch_dhcp_clients(router_ip)

    clients_with_hostnames = []
    for ip, mac, vendor in dhcp_clients:
        hostname = hostnames.get(ip, "Unknown")
        clients_with_hostnames.append((ip, mac, vendor, hostname))

    return clients_with_hostnames

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        router_ip = request.form.get("router_ip")
        if is_valid_ip(router_ip):
            vendors = fetch_dhcp_clients_with_hostnames(router_ip)
            session["vendors"] = vendors
            session["current_ip"] = router_ip
        else:
            session["vendors"] = []
            session["current_ip"] = None
        return redirect(url_for("index"))

    vendors = session.pop("vendors", [])
    current_ip = session.pop("current_ip", None)
    return render_template("index.html", vendors=vendors, current_ip=current_ip)

@app.route("/clear")
def clear():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5055, debug=True)
