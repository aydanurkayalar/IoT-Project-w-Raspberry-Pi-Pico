import usys, uos
import machine
import utime
import time
import json
import _thread
from neopixel import Neopixel
import random

class color:
    BLACK =   '\033[1;30;48m'
    RED =     '\033[1;31;48m'
    GREEN =   '\033[1;32;48m'
    YELLOW =  '\033[1;33;48m'
    BLUE =    '\033[1;34;48m'
    MAGENTA = '\033[1;35;48m'
    CYAN =    '\033[1;36;48m'
    END =    '\033[1;37;0m'
    
    
button_value = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
led = machine.Pin(25, machine.Pin.OUT)

global status

#Neopixel configurations
numpix = 2
strip = Neopixel(numpix, 0, 22, "RGB")

red = (255, 0, 0)
orange = (255, 50, 0)
yellow = (255, 100, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (100, 0, 90)
violet = (200, 0, 100)
colors_rgb = [red, orange, yellow, green, blue, indigo, violet]

delay = 5
strip.brightness(42)
blank = (0,0,0)


#System Starts
print(usys.implementation[0], uos.uname()[3],
      "\nrun on", uos.uname()[4])
print("------------------------------------")

uart_pico = machine.UART(0, timeout=1000)


def pico_send_wait_response(cmd, uart=uart_pico, timeout=2000, targetResp="OK"):
    print(color.MAGENTA + cmd + color.END)
    uart.write(cmd)
    return pico_wait_response(uart, timeout, targetResp)


def pico_wait_response(uart=uart_pico, timeout=2000, targetResp="OK"):
    targetCatched = False
    prvMills = utime.ticks_ms()
    print(color.BLUE)
    while (utime.ticks_diff(utime.ticks_ms(), prvMills))<timeout:
        line=uart.readline()
        if line is not None:
            try:
                line_decoded = line.strip().decode()
                if line_decoded == targetResp:
                    print(color.GREEN + line_decoded)
                    targetCatched = True
                    break
                
                elif line_decoded == "OK":
                    print(color.GREEN + line_decoded)
                    break
                elif line_decoded == "ERROR":
                    print(color.RED + line_decoded)
                    break
                
                elif line_decoded == "SEND OK":
                    print(color.GREEN + line_decoded)
                    break
                elif line_decoded == "SEND FAIL":
                    print(color.RED + line_decoded)
                    break
                else:
                    print(line_decoded)
            except UnicodeError:
                print(line)
    print(color.END)
    return targetCatched


def pico_send_wait_response_button(cmd, uart=uart_pico, timeout=10000, targetResp="OK"):
    print(color.MAGENTA + cmd + color.END)
    uart.write(cmd)
    return pico_wait_response_button(uart, timeout, targetResp)


def pico_wait_response_button(uart=uart_pico, timeout=10000, targetResp="OK"):
    targetCatched = False
    prvMills = utime.ticks_ms()
    print(color.BLUE)
    while (utime.ticks_diff(utime.ticks_ms(), prvMills))<timeout:
        line=uart.readline()
        if line is not None:
            try:
                line_decoded = line.strip().decode()
                if line_decoded == targetResp:
                    print(color.GREEN + line_decoded)
                    targetCatched = True
                    break
                
                elif line_decoded == "OK":
                    print(color.GREEN + line_decoded)
                    break
                elif line_decoded == "ERROR":
                    print(color.RED + line_decoded)
                    break
                
                elif line_decoded == "SEND OK":
                    print(color.GREEN + line_decoded)
                    break
                elif line_decoded == "SEND FAIL":
                    print(color.RED + line_decoded)
                    break
                
                else:
                    print(line_decoded)
            except UnicodeError:
                print(line)
        else:
            print(line)
    
    print(color.END)
    return targetCatched

def pico_send_wait_response_json(cmd, uart=uart_pico, timeout=10000, targetResp="OK"):
    print(color.MAGENTA + cmd + color.END)
    uart.write(cmd)
    return pico_wait_response_json(uart, timeout, targetResp)

def pico_wait_response_json(uart=uart_pico, timeout=10000, targetResp="OK"):
    targetCatched = False
    prvMills = utime.ticks_ms()
    print(color.BLUE)
    while (utime.ticks_diff(utime.ticks_ms(), prvMills))<timeout:
        line=uart.readline()
        if line is not None:
            try:
                new_line = str(line)
                cutted_line = new_line[2:-5]
                line_decoded = line.strip().decode()
                #To avoid mingling two responses
                if ( len(cutted_line) > 4 ):
                    try:
                        json_object = json.loads(cutted_line)
                        status = json_object['feeds'][1]['field2']
                        print(status)
                        #Json response controls the Neopixel led
                        if status == "1" or "0":
                            neopixel(status)
                        else:
                            print("No Status Response")
                    except ValueError as e:
                        print("No Json Response")
                else:
                    print("Button Response Detected")
            
                if line_decoded == targetResp:
                    print(color.GREEN + line_decoded)
                    targetCatched = True
                    break
                
                elif line_decoded == "OK":
                    print(color.GREEN + line_decoded)
                    break
                elif line_decoded == "ERROR":
                    print(color.RED + line_decoded)
                    break
                
                elif line_decoded == "SEND OK":
                    print(color.GREEN + line_decoded)
                    break
                elif line_decoded == "SEND FAIL":
                    print(color.RED + line_decoded)
                    break
                
                else:
                    print(line_decoded)
            except UnicodeError:
                print(line)
        else:
            print(line)
    print(color.END)
    return targetCatched
    
       

def pico_waitDummyResp(uart=uart_pico, timeout=2000):
    pico_wait_response(uart=uart_pico, timeout=2000)


def pico_dummyMonitor(uart=uart_pico):
    while True:
        line=uart.readline()
        if line is not None:
            try:
                line_decoded = line.strip().decode()
                print(line_decoded)
            except UnicodeError:
                print(line)


def button_value_func(button=button_value):
    count=0
    while True:
        first = button.value()
        time.sleep(0.01)
        second = button.value()
        #XOR the button values to check button status
        if not first and second:
            print("Entered into the second Thread")
            count += 1
            print(count)
            pico_send_wait_response('AT#SD=2,0,80,\"api.thingspeak.com",0,0\r\n')
            pico_send_wait_response_button('GET https://api.thingspeak.com/update?api_key=################&field1='+ str(count) +'\r\n')
        
        
def neopixel(status):
    if status == "1":
        print("led on")
        for i in range(3):
            strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
            strip.show()
            strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
    elif status == "0":
        print("led off")
        for i in range(2):
            strip.show()
            strip.fill((0,0,0))
    else:
        print("Error Value")
        for i in range(2):
            strip.show()
            strip.fill((0,0,0))



print("=== Start ===")

pico_waitDummyResp()
pico_send_wait_response('AT\r\n')

#--------Configuration of Telit ME910C1---------

# reset command
#pico_send_wait_response('AT+CFUN=1,1\r\n')

pico_send_wait_response('AT&K0\r\n')
pico_send_wait_response('AT+CREG?\r\n')
pico_send_wait_response('AT+CGDCONT=1,"IP","super"\r\n')
pico_send_wait_response('AT+CGDCONT?\r\n')
pico_send_wait_response('AT#SGACT=1,1\r\n')
pico_send_wait_response('AT#SGACT?\r\n')

#pico_send_wait_response('AT#SD=1,0,80,\"api.thingspeak.com",0,0\r\n')

#-------Multi Threading---------

#Second thread counts the button value
second_thread = _thread.start_new_thread(button_value_func, ())

#Main thread controls the status of the Neopixel button to on or off the led
while True:
    print("Entered into the first Thread")
    utime.sleep(0.1)
    pico_send_wait_response('AT#SD=2,0,80,\"api.thingspeak.com",0,0\r\n')
    pico_send_wait_response_json('GET https://api.thingspeak.com/channels/1725260/feeds.json?api_key=################&results=2\r\n')
    
    
