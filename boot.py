import connect2wifi as wifi
import thread_1 as t1
import thread_2 as t2
from machine import Pin
import time
import ntptime
import _thread
import socket
import os
import network

# Connect to WiFi using the function in connect2wifi
wifi.do_connect()
station = network.WLAN(network.STA_IF)
print(station.ifconfig()[0])

# Sync time with NTP

attempts = 0
while attempts < 5:
    try:
        ntptime.settime()  # Sync ESP32 clock
        print("Time synchronized:", time.localtime())
        break
    except Exception as e:
        attempts += 1
        print(f"Attempt {attempts} failed. Error {e}")
        time.sleep(2)
'''
try:
    ntptime.settime()  # Sync ESP32 clock
    print("Time synchronized:", time.localtime())
except:
    print("Failed to sync time")
'''
'''Funcao para o Thread 1 - responsavel por pegar dados dos sensores, manipular e gravar como csv'''
def thread_sensor_data():
    while True:
        try:
            temp = t1.get_sensor_data()[0]
            hum = t1.get_sensor_data()[1]
            timestamp = t1.get_formatted_time()  #get current timestamp
            t1.log_csv_data(temp, hum, timestamp)
            print(f"Logged: {timestamp}, {temp}°C, {hum}%\n")
            
        except Exception as e:
            print("Sensor error: ", e)
        time.sleep(600)  # Wait 600s (10min) before next reading

'''Funcao para o Thread 2 - responsavel por gerar o servidor e mandar os dados do csv para a web'''
def thread_web_server():
    # Create socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", 80))  # Listen on port 80
    server_socket.listen(5)

    print("Server is listening on port 80...")

    # Main loop to accept connections
    while True:
        client, addr = server_socket.accept()  # Accept new client
        print("New client connected:", addr)
        t2.handle_client(client)  # Handle request

# Start threads
_thread.start_new_thread(thread_sensor_data, ())
_thread.start_new_thread(thread_web_server, ())

#Erase all the data from csv file by pressing "boot" button
def reset_csv(pin):
    time.sleep_ms(200)  # Debounce delay
    if pin.value() == 0:
        try:
            with open("data.csv", "w") as f:
                f.write("")  # Clear the file
            print("data.csv has been reset.")
            #lights on the blue led for 3s straight
            led_blue.value(1)
            time.sleep(3)
            led_blue.value(0)
        except Exception as e:
            print("Error resetting file:", e)

# Set up GPIO0 (BOOT) as input with pull-up
led_blue = Pin(2, Pin.OUT)
button = Pin(0, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=reset_csv)

# Keep the main thread alive
while True:
    time.sleep(1)
