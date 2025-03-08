import network
import time

# Connect to Wi-Fi
ssid = '<enter_your_ssid>'
password = '<enter_your_wifi_password>'

def do_connect():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    # Wait for connection
    while not station.isconnected():
        print("Connecting...")
        time.sleep(3)

    print('Connection successful!')
    print(station.ifconfig())  # Displays IP address
