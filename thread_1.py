'''
Thread 1
    -Pega os dados de temperatura do sensor
    -Pega os dados de hora e dia e formata
    -Grava esses dados no arquivo csv

'''
import machine
import random #pode retirar depois que comecar a usar o sensor propriamente
import os
import time
import dht 		#sensor

# Initialize DHT sensor (connected to GPIO4)
#sensor = dht.DHT22(machine.Pin(4))

# A function to simulate data from this pin
# retorna a temperatura em °C
def get_sensor_data():  #function to simulate sensor data
    temp = random.randint(20, 40)
    #print(temp)
    return temp

# Retorna os dados de tempo no formato AAA-MM-DD HH:mm:ss
# Adjust this according to your timezone (e.g., -4 for GMT-4)
GMT_OFFSET = -4 * 3600  # Convert hours to seconds
def get_formatted_time():
    utc_time = time.time()  # Get current UTC timestamp
    tm = time.localtime(utc_time + GMT_OFFSET)  # Adjust to local time
    
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        tm[0], tm[1], tm[2], tm[3], tm[4], tm[5]
    )

# Function to write data to a CSV file
def log_csv_data(temperature, timestamp):
    with open("data.csv", "a") as file:
        file.write(f"{timestamp},{temperature}\n")

