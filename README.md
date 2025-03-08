# esp32TemperatureSensor
Program to set an esp32 wroom connected to a Temperature sensor. 
The main code is written in MicroPython.
  -First it connects to a wifi via network library to set the actual ntptime
  -One thread is responsable for get the temperature from the sensor and save it in a csv format file 
  -The other thread will create a server using socket method and load the html file

## Table of Contents

- [Installation] It uses a BME280 temperature sensor, but feel free to use any other sensor
- [Usage] IoT created to measure and dispose the graph of the temperature of a chick shed 

## Installation

Step-by-step instructions on how to install and set up your project.

## Usage

Instructions and examples on how to use your project.


## Acknowledgments

- Resource 1
- Resource 2
- Resource 3
