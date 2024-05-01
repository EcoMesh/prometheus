# prometheus

Firmware

# Development

Make sure you have a cable capable of power and data transfer when plugging
the Pico into your computer.

Use VS Code and install the @recommended extensions.

THe Pico W Go extension will allow you to easily upload the project
firmware to the Pico and execute the files for testing within the Pico.

## macOs

Use `brew install minicom` to install the minicom terminal emulator.

## Linux

Use `sudo apt install minicom` to install the minicom terminal emulator.

All the python tools can be installed with Poetry. To setup the poetry environment run `poetry install`.

To activate the poetry environment run `poetry shell`.

# Setup

## Hardware

One uplink node with WiFi capability is required to transmit data to the monitoring server. All the other nodes
can be simple Pico's without WiFi capability. The variable `n` refers to the number of nodes that do not have WiFi. We
need `2n` Pico's since it takes a pair to create a sensor node. One is used to control the LoRa module and the other
is used to control the sensors. They communicate via UART.

- 1 x [Raspberry Pi Pico WH](https://www.pishop.us/product/raspberry-pi-pico-wh-pre-soldered-headers/)
- (2n) x [Raspberry Pi Pico H](https://www.pishop.us/product/raspberry-pi-pico-h-pre-soldered-headers/)
- (1 + n) x [Pico LoRa SX1262](https://www.waveshare.com/pico-lora-sx1262-868m.htm)

### Meshtastic Nodes

Connect the Picos to the LoRa modules as shown in the following image.

![Meshtastic Node](https://www.waveshare.com/w/upload/6/6a/Pico-LoRa-SX1262-868M_Spec_03.jpg)

Make sure the antenna is connected to the LoRa module before powering it on or you may damage the module.

More information about the LoRa module can be found [here](https://www.waveshare.com/wiki/Pico-LoRa-SX1262).

## MQTT Server

You will need to set up an MQTT server to receive the data from the LoRa network. You can use [Mosquitto](https://mosquitto.org/). You can also use a cloud service like [CloudMQTT](https://www.cloudmqtt.com/).

Configure the MQTT server to allow anonymous connections by adding the following to the `mosquitto.conf` file and restart the server.

```bash
listener 1883 0.0.0.0
allow_anonymous true
```

TODO: Add instructions for setting up Mosquitto.

## Firmware

For each Pico connected to a LoRa module you will need to flash the [Meshtaic firmware](https://github.com/meshtastic/firmware/releases/tag/v2.2.16.1c6acfd). The link references version 2.2.16 but newer versions may also be suitable. See [Flashing Firmware](./APPENDIX.md#flashing-firmware).

Depending on the Pico, you'll want to run the following commands after flashing the firmware. Make sure the Pico is plugged in to computer.

### Pico H

```bash
meshtastic --configure meshtastic-pico-w.yaml
```

### Pico WH

You'll need to modify the network SSID and password in the `meshtastic-pico-wh.yaml` file and set the MQTT server address.

```bash
meshtastic --configure meshtastic-pico-wh.yaml
```

## Serial Connection

Wire pins 11-13 on the Pico to the LoRa module to pins 1-3 respectively. The pinout for the Pico is shown below.

| Sensor Pico Pin | LoRa Pico Pin |
| --------------- | ------------- |
| 11 (TX)         | 2 (RX)        |
| 12 (RX)         | 1 (TX)        |
| 13 (GND)        | 3 (GND)       |

This configuration will allow the Pico to communicate with the LoRa module via UART. The Pico will send data to the LoRa module on pin 11 and receive data from the LoRa module on pin 12. The Pico and LoRa module share a common ground on pin 13. These messages will then be transmitted over the LoRa network.

![Pico Pinout](https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2023/05/Raspberry-Pi-Pico-W-Pinout.png?w=861&quality=100&strip=all&ssl=1)

# Testing

You can run serial.py on the sensor pico to test the serial connection to the LoRa module. You can run the following command to run the script. If you monitor the MQTT server you should see the messages being published.

You can monitor all MQTT topics with the following command.

```bash
mosquitto_sub -v -t \#
```
