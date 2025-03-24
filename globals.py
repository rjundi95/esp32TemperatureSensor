from machine import Pin
import time

# Global variables
#led = Pin(21, Pin.OUT)
button = Pin(0, Pin.IN, Pin.PULL_UP)
led_board = Pin(2, Pin.OUT)

# Function to check if the button is pressed for 2 seconds
def reset_to_main_loop():
    if button.value() == 0:  # Button pressed
        press_start = time.ticks_ms()
        while button.value() == 0:  # Keep checking while pressed
            if time.ticks_diff(time.ticks_ms(), press_start) >= 2000:  # 2 seconds
                print("Button held for 2 seconds!")
                return True  # Indicate the button was held
    return False  # Button not held long enough

def led_error_internet():
    #pisca 3 vezes = problema de conexao com internet
    print("Problema de conexao com a internet")
    i = 1
    while i < 3:
        led_board.value(1)
        time.sleep(1)
        led_board.value(0)
        time.sleep(1)
        i += 1

def led_error_time():
    #pisca 5 vezes = problema de sincronizacao de relogio
    print("Problema de sincronizacao de horario")
    i = 1
    while i < 5:
        led_board.value(1)
        time.sleep(1)
        led_board.value(0)
        time.sleep(1)
        i += 1
