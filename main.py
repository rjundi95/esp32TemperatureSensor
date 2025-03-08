import connect2wifi as wifi
import thread_1 as t1
import thread_2 as t2

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
try:
    ntptime.settime()  # Sync ESP32 clock
    print("Time synchronized:", time.localtime())
except:
    print("Failed to sync time")

'''Funcao para o Thread 1 - responsavel por pegar dados dos sensores, manipular e gravar como csv'''
def thread_sensor_data():
    while True:
        try:
            temp = t1.get_sensor_data()
            timestamp = t1.get_formatted_time()  #get current timestamp
            t1.log_csv_data(temp, timestamp)
            print(f"Logged: {timestamp}, {temp}°C")
            
        except Exception as e:
            print("Sensor error: ", e)
        time.sleep(15)  # Wait 15 seconds before next reading

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

# Keep the main thread alive
while True:
    time.sleep(1)
