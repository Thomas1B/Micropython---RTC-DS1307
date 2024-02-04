# Micropython Module for the the RTC DS1307

This module is written for the DS1307 RTC module using micropython on the Pi Pico.
Extension Module to https://github.com/brainelectronics/micropython-ds1307

## Class Description

```py
rtc = RTC(id=1, SCL=19, SDA=18, freq=800_000, addr=0x68)
```
- `id`: Identifies particular I2C device.
- `SCL`: Pin used for the SCL connection.
- `SDA`: Pin used for the SDA connection.
- `freq`: Maximum frequency for SCL, (default 800_000).
- `addr`: Address to the I2C (default 0x68).

