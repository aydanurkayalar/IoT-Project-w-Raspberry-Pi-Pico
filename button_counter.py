import usys, uos
import machine
import utime
import time


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

#System Starts
print(usys.implementation[0], uos.uname()[3],
      "\nrun on", uos.uname()[4])
print("------------------------------------")

uart_pico =machine.UART(0, timeout=1000)



def pico_send_wait_response(cmd, uart=uart_pico, timeout=8000, targetResp="OK"):
    print(color.MAGENTA + cmd + color.END)
    uart.write(cmd)
    return pico_wait_response(uart, timeout, targetResp)


def pico_wait_response(uart=uart_pico, timeout=8000, targetResp="OK"):
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
            utime.sleep(0.1)
            count += 1
            print(count)
            pico_send_wait_response('AT#SD=1,0,80,\"api.thingspeak.com",0,0\r\n')
            pico_send_wait_response('GET https://api.thingspeak.com/update?api_key=################&field1='+ str(count) +'\r\n')
            time.sleep(12)
        

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


button_value_func()
