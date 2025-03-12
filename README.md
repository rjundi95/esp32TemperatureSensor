# esp32TemperatureSensor
IoT module programmed in an ESP32 WROOM-32 that reads the ambient temperature and humidity via BME280 sensor and posts the readings in a local web service in a graph format.
The main code is written in MicroPython.
First it connects to a wifi via 'network' library to set the actual time.
One thread is responsable for get the sensor data and save it in a csv format file.
The other thread will create a server using socket method and load the html file.

## Table of Contents

- [Installation](#installation) It uses a BME280 temperature sensor, but feel free to use any other sensor
- [Usage](#usage) IoT created to measure and dispose the graph of the temperature and humidity in a chick shed 
- [Acknowledgments](#acknowledgments)
  
## Installation

Step-by-step instructions on how to install and set up your project.

## Usage

Instructions and examples on how to use your project.


## Acknowledgments

- Resource 1
- Resource 2
- Resource 3
