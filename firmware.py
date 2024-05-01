import gc

import dht
import utime
from machine import ADC, UART, Pin

uart = UART(0, 38400, tx=Pin(0), rx=Pin(1))
temp_sensor = dht.DHT22(Pin(2))
trigger = Pin(21, Pin.OUT)
echo = Pin(20, Pin.IN)
led = Pin(25, Pin.OUT)
soil = ADC(Pin(26))


def get_soil_moisture():
    min_moisture = 20000
    max_moisture = 65535
    moisture_percent = (
        (max_moisture - soil.read_u16()) * 100 / (max_moisture - min_moisture)
    )
    return moisture_percent


def get_temp_and_hum():
    try:
        temp_sensor.measure()
    except Exception:  # should be Exception("checksum error")
        led.toggle()
        utime.sleep(0.1)
        get_temp_and_hum()
        return (1000, 1000)
    temp = temp_sensor.temperature()
    hum = temp_sensor.humidity()
    temp_f = temp * (9 / 5) + 32.0
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

    time_passed = signalon - signaloff
    distance_cm = (time_passed * 0.0343) / 2  # cm
    return distance_cm


def get_payload():
    temp, hum = get_temp_and_hum()
    return "|".join(
        map(str, (round(temp, 2), hum, get_soil_moisture(), round(get_distance(), 2)))
    )


try:
    while True:
        utime.sleep(5)
        led.on()
        p = get_payload()
        uart.write(bytes(p, "ascii"))
        led.off()
        gc.collect()
except Exception as e:
    uart.write(bytes(repr(e), "ascii"))
    while True:
        led.toggle()
        utime.sleep(1)
