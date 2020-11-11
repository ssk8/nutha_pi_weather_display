import time
import urllib.request
import urllib.parse
from ST7789 import ST7789
from weather_graphics import Weather_Graphics
from os import environ

LAT, LON = "39.571", "-97.662"
DATA_SOURCE_URL = "http://api.openweathermap.org/data/2.5/weather"

params = {"lat": LAT, "lon": LON, "appid": environ['OPEN_WEATHER_TOKEN']}
data_source = DATA_SOURCE_URL + "?" + urllib.parse.urlencode(params)
print(data_source)

display = ST7789()
display.Init()
display.clear()

gfx = Weather_Graphics(display, am_pm=True, celsius=False)
weather_refresh = None

while True:
    # only query the weather every 10 minutes (and on first run)
    if (not weather_refresh) or (time.monotonic() - weather_refresh) > 600:
        response = urllib.request.urlopen(data_source)
        if response.getcode() == 200:
            value = response.read()
            print("Response is", value)
            gfx.display_weather(value)
            weather_refresh = time.monotonic()
        else:
            print("Unable to retrieve data at {}".format(url))

    gfx.update_time()
    time.sleep(300)  # wait 5 minutes before updating anything again
