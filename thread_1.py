'''
Thread 1
    -Pega os dados de temperatura do sensor
    -Pega os dados de hora e dia e formata
    -Grava esses dados no arquivo csv

'''
from machine import Pin, SoftI2C
import BME280
import os
import time

def get_sensor_data():
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
    bme = BME280.BME280(i2c=i2c)
    temp = bme.temperature[:4]
    hum = bme.humidity[:4]
     
    return [temp, hum]

# Retorna os dados de tempo no formato yyyy-mm-dd HH:mm:ss
# Adjust this according to your timezone (for GMT-4)
GMT_OFFSET = -4 * 3600  # Convert hours to seconds
def get_formatted_time():
    utc_time = time.time()  # Get current UTC timestamp
    tm = time.localtime(utc_time + GMT_OFFSET)  # Adjust to local time
    
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        tm[0], tm[1], tm[2], tm[3], tm[4], tm[5]
    )

# Function to write data to a CSV file
def log_csv_data(temperature, humidity,  timestamp):
    with open("data.csv", "a") as file:
        file.write(f"{timestamp},{temperature},{humidity}\n")
