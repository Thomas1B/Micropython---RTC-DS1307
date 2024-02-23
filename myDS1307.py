'''
Written 2024, Thomas Bourgeois

This module is written for the DS1307 RTC module using micropython on the Pi Pico.
Extension Module to https://github.com/brainelectronics/micropython-ds1307


Notes:
    1. Day of week is 0-6, monday being 0.
    2  Day of year is 1-366, 1 is Jan 1st, 366 is Dec 31st.
'''


from DS1307 import DS1307

from machine import I2C, Pin
import time


RTC_ADDR = 0x68  # default DS1307 address


# Program Parameters

day_names = ['Monday', 'Tuesday', 'Wednesday',
             'Thrusday', 'Friday', 'Saturday', 'Sunday']
day_names_abbr = ['Mon', 'Tu', 'Wed', 'Th', 'Fri', 'Sat', 'Sun']

month_names = ['January', 'Febuary', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
month_names_abbr = [month[:3] if len(
    month) > 4 else month for month in month_names]


class RTC(DS1307):
    '''
    Class for the DS1307 RTC.

    Paramteres:
        id: identifies particular i2c device.
        SCL: pin used for SCL.
        SDA: pin used for SDA.
        freq: i2c communication frequency (default 800_000).
        addr: DS1307 Address in hex code (default 0x68).


    This class uses super() in invoke the class methods of DS1307.
    '''

    def __init__(self, id: int, SCL: int, SDA: int, freq=800_000, addr=RTC_ADDR) -> None:

        self.i2c = I2C(id, scl=Pin(SCL), sda=Pin(SDA), freq=freq)
        self._rtc = DS1307(addr, self.i2c)

        super().__init__(RTC_ADDR, self.i2c)

    def set_time(self,
                 year: int,
                 month: int,
                 day: int,
                 hour: int,
                 minutes: int,
                 seconds: int,
                 day_of_week: int,
                 day_of_year: int) -> None:
        '''
        Function that reset the rtc's time to a given time.

        Should only be called once before implementing RTC module into a project
        or when updating the time...

        Parameters:
            year: what year it is.
            month: month in number, Jan -> 1, Feb -> 2, ...
            day: day of the month.
            hour: hour in 24hrs.
            minutes: how many minutes.
            seconds: how many seconds.
            day_of_week: day of the week, 0 is monday, ...
            day_of_year: day of the year, Jan 1st is day 1.
        '''

        self._rtc.datetime(year, month, day, hour, minutes,
                              seconds, day_of_week, day_of_year)
        print(f"New RTC time: {self._rtc.datetime}")

    def breakdown_print(self) -> None:
        '''
        Function to print a breakdown of datetime for easier viewing.
        '''
        categories = ['Year', 'Month', 'Day', 'Hours', 'Minutes',
                      'Seconds', 'Day of Week', 'Day of Year']
        # Calculate the maximum length of the category names for alignment
        max_category_length = len(categories[-1])

        values = self._rtc.datetime

        for category in categories:
            print(f"{category:^{max_category_length}}", end=" | ")
        print()  # Move to the next line after printing header

        for val in values:
            print(f"{val:^{max_category_length}}", end=" | ")
        print()

    def current_time_str(self, format=24, meridiem=False) -> str:
        '''
        Function to return a formatted string of the current time.

        Parameters:
            format: 12hr or 24hr format time, (default 24).
            meridiem: add 'am' or 'pm' to string, (default false).

        Returns: str
                hours/minutes/seconds 
        '''
        hrs, mins, secs = self._rtc.datetime[3:6]

        # checks if 'format' is the correct type and values.
        if type(format) is not int:
            raise TypeError("Parameter \"format\" must be an integer type.")
        elif format not in [12, 24]:
            raise ValueError("Parameter \"format\" must be 12 or 24.")

        if format == 24:  # 24 hour format
            return "{:02d}:{:02d}:{:02d}".format(hrs, mins, secs)
        elif format == 12:  # 12 hour format
            if meridiem:
                meridiem = 'PM' if hrs >= 12 else 'AM'
            hrs %= 12
            hrs = 12 if hrs == 0 else hrs
            if meridiem:
                return "{:02d}:{:02d}:{:02d} {}".format(hrs, mins, secs, meridiem)
            else:
                return "{:02d}:{:02d}:{:02d}".format(hrs, mins, secs)

    def date_str(self) -> str:
        '''
        Function to return the date as a formated string.

        Parameters:
            none

        Returns: str
            YYYY/MM/DD
        '''
        year, month, date = self._rtc.datetime[:3]

        return '{:02d}/{:02d}/{:02d}'.format(year, month, date)

    def name_weekday(self, full=True) -> str:
        '''
        Function to get the name of the current day as a string.

        Parameters:
            full: True - full name, False - abbr name (default True).

        Returns: str
            name of current week day.
        '''

        day = self._rtc.datetime[6]-1
        if full:
            return day_names[day]
        else:
            return day_names_abbr[day]

    def name_month(self, full=True) -> str:
        '''
        Function to get the name of the current month as a string.

        Parameters:
            full: True - full name, False - abbr name (default True).

        Returns: str
            name of current month.
        '''

        cur_month = self._rtc.datetime[1]

        if full:
            return month_names[cur_month-1]
        else:
            return month_names_abbr[cur_month-1]

    def raw(self) -> tuple:
        return self._rtc.datetime


def example(rtc):
    rtc.breakdown_print()
    print()

    print(rtc.current_time_str())  # calling in default mode, 24hrs format

    # 12 hour Format
    print(rtc.current_time_str(format=12), end=', ')
    # 12hr and showing am/pm
    print(rtc.current_time_str(format=12, meridiem=True), '\n')

    # showing date
    print(rtc.date_str(), '\n')

    # showing weekday name
    print(rtc.name_weekday(), end=', ')
    print(rtc.name_weekday(False), '\n')

    # showing month name
    print(rtc.name_month(), end=', ')
    print(rtc.name_month(False))


if __name__ == '__main__':

    # # creating rtc object
    rtc = RTC(1, SCL=19, SDA=18)

    # Setting time

    # example(rtc)
    # print(rtc._rtc.weekday_start)
