from time import sleep

import dht
import utime
from machine import ADC, UART, Pin

uart = UART(0, 38400, tx=Pin(0), rx=Pin(1))
temp_sensor = dht.DHT22(Pin(2))
trigger = Pin(21, Pin.OUT)
echo = Pin(20, Pin.IN)


def get_soil_moisture():
    soil = ADC(Pin(26))
    min_moisture = 20000
    max_moisture = 65535
    moisture = (max_moisture - soil.read_u16()) * 100 / (max_moisture - min_moisture)
    # print("moisture: " + "%.2f" % moisture +"% (adc: "+str(soil.read_u16())+")")
    return moisture


def get_temp_and_hum():
    temp_sensor.measure()
    temp = temp_sensor.temperature()
    hum = temp_sensor.humidity()
    temp_f = temp * (9 / 5) + 32.0

    # print('Temperature: %3.1f C' %temp)
    # print('Temperature: %3.1f F' %temp_f)
    # print('Humidity: %3.1f %%' %hum)
    return (temp_f, hum)


def get_distance():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()

    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    # print(distance, "cm")
    return distance


def get_payload():
    temp, hum = get_temp_and_hum()
    return "|".join(
        map(str, (round(temp, 2), hum, get_soil_moisture(), round(get_distance(), 2)))
    )


# print("start")
# for i in range(10):
#   t = "ping," + str(i)
#   uart.write(bytes(t, "ascii"))
#    print(t)
#    sleep(1)

#
while True:
    # get_temp_and_hum()
    # get_soil_moisture()
    # get_distance()
    p = get_payload()
    print(p)
    uart.write(bytes(p, "ascii"))
    utime.sleep(5)
