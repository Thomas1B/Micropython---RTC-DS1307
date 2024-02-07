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

## Class Methods

1. `set_time(year: int, month: int, day: int, hour: int, minutes: int, seconds: int, day_of_week: int, day_of_year: int)`
   
    Function to set the time of the RTC.
    - `year`: what year it is.
    - `month`: month in number, Jan -> 1, Feb -> 2, ...
    - `day`: day of the month.
    - `hour`: hour in 24hrs.
    - `minutes`: how many minutes.
    - `seconds`: how many seconds.
    - `day_of_week`: day of the week, 0 is monday, ...
    - `day_of_year`: day of the year, Jan 1st is day 1.

2. `breakdown()`
   
   Function to print a breakdown of datetime for easier viewing.

3. `current_time_str(format=24, meridiem=False)`
   
   Function to return the current time as a string, in either 12/24 format and also adding 'am/pm'

   - `format`: 12hr or 24hr format, integer value '12' or '24', (default 24).
   - `meridiem`: add 'am' or 'pm' to string, (default false).
  
4. `date_str()`
   
   Function to return the date as a string, YYYY/MM/DD.

5. `name_weekday(full=True)`
   
   Function to get the name of the current day as a string.
   - `full` True - full name, False - abbr name (default True).

6. `name_month(full=True)`
   
   Function to get the name of the current month as a string.
   - `full`  True - full name, False - abbr name (default True).


## Examples

```py
    from myDS1307 import RTC

    rtc = RTC(1, 19, 18)

    rtc.breakdown()
    print()

    print(rtc.current_time_str())  # calling in default mode, 24hrs format

    # 12 hour Format
    print(rtc.current_time_str(format=12), end=', ')
    # showing am/pm
    print(rtc.current_time_str(format=12, meridiem=True))

    # showing date YYYY/MM/DD
    print(rtc.date_str())

    # showing weekday name
    print(rtc.name_weekday(), end=', ')
    print(rtc.name_weekday(False))

    # showing month name
    print(rtc.name_month(), end=', ')
    print(rtc.name_month(False))
```
