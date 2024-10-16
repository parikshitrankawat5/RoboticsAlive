"""Implements a HD44780 character LCD connected via ESP32 GPIO pins."""
import ntptime
from machine import Pin
import machine
from esp32_gpio_lcd import GpioLcd
from utime import sleep_ms, ticks_ms
import time
import network
import urequests
net = network.WLAN(network.STA_IF)
net.active(True)
net.connect("Wokwi-GUEST","")
while not net.isconnected():
    pass
lcd = GpioLcd(rs_pin=Pin(4),
                  enable_pin=Pin(17),
                  d4_pin=Pin(5),
                  d5_pin=Pin(18),
                  d6_pin=Pin(21),
                  d7_pin=Pin(22),
                  num_lines=2, num_columns=20)

def showText(txt):
    lcd.clear()
    lcd.putstr(txt)
def getDt(dt):#2024-10-14T15:54:07.304102+05:30
    x = []
    dt = dt[:dt.rindex("+")+1]
    x.append(int(dt[:dt.index("-")]))
    x.append(int(dt[dt.index("-")+1:dt.rindex("-")]))
    x.append(int(dt[dt.rindex("-")+1:dt.rindex("T")]))
    x.append(int(dt[dt.rindex("T")+1:dt.index(":")]))
    x.append(int(dt[dt.index(":")+1:dt.rindex(":")]))
    x.append(int(dt[dt.rindex(":")+1:dt.rindex(".")]))
    x.append(int(dt[dt.rindex(":")+1:dt.rindex(".")]))
    x.append(0)
    return x
showText("Getting Data......")
while True:
    try:
        getdata = urequests.get("http://worldtimeapi.org/api/timezone/Asia/Kolkata")
        break
    except Exception as error:
        print(error)
        print(net.ifconfig())
        continue
print(getdata.json())





tms = getDt(getdata.json()["datetime"])
print(tms)
rtc = machine.RTC()
rtc.datetime(tuple(tms))


sec = ntptime.time()
timezone_hour = 5.50
timezone_sec = timezone_hour * 3600
sec = int(sec + timezone_sec)
(year, month, day, hours, minutes, seconds, weekday, yearday) = time.localtime(sec)
print ("IST Time: ")
print((year, month, day, hours, minutes, seconds))
rtc.datetime((year, month, day, 0, hours, minutes, seconds, 0))
while True:
    dts = list(rtc.datetime())
    print(dts)
    showtxt = f"{dts[2]}-{dts[1]}-{dts[0]}             {dts[4]}:{dts[5]}"
    print(showtxt)
    showText(showtxt)
    time.sleep_ms(1000)




