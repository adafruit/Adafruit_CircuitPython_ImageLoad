# SPDX-FileCopyrightText: 2021 Tim C for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
imageload example for esp32s2 that loads an image fetched via
adafruit_requests using BytesIO
"""

from io import BytesIO
from os import getenv

import adafruit_connection_manager
import adafruit_requests as requests
import board
import displayio
import wifi

import adafruit_imageload

# Get WiFi details, ensure these are setup in settings.toml
ssid = getenv("CIRCUITPY_WIFI_SSID")
password = getenv("CIRCUITPY_WIFI_PASSWORD")

wifi.radio.connect(ssid, password)

print("My IP address is", wifi.radio.ipv4_address)

pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
https = requests.Session(pool, ssl_context)

url = "https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_ImageLoad/main/examples/images/4bit.bmp"

print(f"Fetching text from {url}")
response = https.get(url)
print("GET complete")

bytes_img = BytesIO(response.content)
image, palette = adafruit_imageload.load(bytes_img)
tile_grid = displayio.TileGrid(image, pixel_shader=palette)

group = displayio.Group(scale=1)
group.append(tile_grid)
board.DISPLAY.root_group = group

response.close()

while True:
    pass
