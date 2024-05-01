# Flashing Firmware

Hold the BOOTSEL button on the Pico and plug it into your computer. The Pico will show up as a USB drive. Drag and drop the `.uf2` file onto the Pico drive. The Pico will reboot and the firmware will be flashed.

If you are flashing Meshtastic firmware you are not able to connect to the Pico via the CLI or browser. You will need to unplug the Pico and plug it back in to connect to it again.

# Flash Nuke

If you brick the Meshtastic Pico with a bad configuration you can flash nuke the Pico to restore it to factory settings. Hold the BOOTSEL button on the Pico and plug it into your computer. The Pico will show up as a USB drive. Drag and drop the [`flash_nuke.uf2`](https://datasheets.raspberrypi.com/soft/flash_nuke.uf2) file onto the Pico drive. The Pico will reboot and the firmware will be flashed.

# Listing USB Devices

To list the USB devices connected to your computer run the following command:

```bash
ls /dev/{tty,cu}.*
```
