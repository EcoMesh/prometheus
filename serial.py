from time import sleep

from machine import UART, Pin

uart = UART(0, 38400, tx=Pin(0), rx=Pin(1))

print("start")
for i in range(10):
    t = "ping," + str(i)
    uart.write(bytes(t, "ascii"))
    print(t)
    sleep(1)