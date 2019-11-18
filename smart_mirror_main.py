#!/usr/bin/env python2

# Authors: Andy Barbour and Mark Proctor
# Last Updated: 18 November 2019
# Class: ECE434 Embedded Linux

from ISStreamer.Streamer import Streamer
from datetime import datetime
import urllib2
import json
import webbrowser
import subprocess
import time
import pynput
from pynput.keyboard import Key, Controller
import blynklib
import threading

BUCKET_NAME = "Weather"
ACCESS_KEY = "ist_Zz199NmUJzRKcJivg5cv1L91akhuC9hB"
BUCKET_KEY = "FEAKDV6SDUBV"

DARK_SKY_API = "d112efc2c468c79899a1ca27d72b144c"
COORDINATES = "39.48291665,-87.32413881427742"

BLYNK_AUTH = "TubKCRtgU0RJ8JsTTS4fm4mEuT55kR80"

UPDATE_RATE = 30.0

# Initlalize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

# Retrieve current weather conditions from DarkSky
def get_current_conditions():
	api_conditions_url = "https://api.darksky.net/forecast/" + DARK_SKY_API + "/" + COORDINATES + "?units=auto"
	try:
		f = urllib2.urlopen(api_conditions_url)
	except:
		return []
	json_currently = f.read()
	f.close()
	return json.loads(json_currently)

# Convert weather status into appropriate icon to display
def weather_icon(ds_icon):
	icon = {
		"clear-day"            	: ":sunny:",
		"clear-night"           : ":new_moon_with_face:",
		"rain"         			: ":umbrella:",
		"snow"              	: ":snowflake:",
		"sleet"             	: ":sweat_drops: :snowflake:",
		"wind"     				: ":wind_blowing_face:",
		"fog"      				: ":fog:",
		"cloudy"     			: ":cloud:",
		"partly-cloudy-day"		: ":partly_sunny:",
		"partly-cloudy-night"   : ":new_moon_with_face:",
		"unknown"          		: ":sun_with_face:",
	}
	return icon.get(ds_icon,":sun_with_face:")

# Update widget data by streaming new temperatures, fortune, etc. to the data bucket
def stream_data():
	print('Updating Widgets ...')

	# create a Streamer instance
	streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

	# Retrieve weather data
	curr_conditions = get_current_conditions()

	# Retrieve new fortune
	fortune = json.load(urllib2.urlopen('http://fortunecookieapi.herokuapp.com/v1/cookie'))

	# Retrieve date and time
	date = json.dumps(json.load(urllib2.urlopen('http://worldtimeapi.org/api/timezone/America/Indianapolis'))['utc_datetime'])
	year = date.split('-')[0].split('"')[1]
	month = date.split('-')[1]
	day = date.split('-')[2].split('T')[0]
	current_date = month + "/" + day + "/" + year

	# Stream data to data bucket
	streamer.log("myLocation", "39.48291665,-87.32413881427742")
	streamer.log("Temperature",curr_conditions['currently']['temperature'])
	streamer.log("Current Forecast",weather_icon(curr_conditions['currently']['icon']))
	streamer.log("Today's Feels Like",curr_conditions['currently']['apparentTemperature'])
	streamer.log("Wind Speed",curr_conditions['currently']['windSpeed'])
	streamer.log("Today's Fortune",fortune[0]['fortune']['message'])
	streamer.log("Today's Date",current_date)

	# Create new timer to stream updated data
	new_timer = threading.Timer(UPDATE_RATE, stream_data) 
	new_timer.start()

# Handle toggling of monitor display using Blynk
@blynk.handle_event('write V0')
def write_virtual_pin_handler(pin, value):
	if("{}".format(value) == "[u'0']"):
		print('Turning Off Monitor ...')
		subprocess.call('xset dpms force off', shell=True) # Turns off the HDMI port
	elif("{}".format(value) == "[u'1']"):
		print('Turning On Monitor ...')
		subprocess.call('xset dpms force on', shell=True) # Turns on the HDMI port

def main():
	# Open dashboard file and wait two minutes for it to open completely in browser
	url = 'file:///home/debian/ECE434SmartMirror/dashboard.html'
	webbrowser.open(url)
	time.sleep(120)

	# Simulate F11 keypress to make Chromium window fullscreen and wait 15 seconds for operation to complete
	keyboard = Controller()
	keyboard.press(Key.f11)
	keyboard.release(Key.f11)
	time.sleep(15)

	# Create timer to stream updated data
	timer = threading.Timer(UPDATE_RATE, stream_data)
	timer.start()	

	# Run Blynk process
	while True:
		blynk.run()

	# Flush and close the stream
	streamer.flush()

if __name__ == "__main__":
	main()
