#!/usr/bin/env python2

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


ACCESS_KEY = "ist_Zz199NmUJzRKcJivg5cv1L91akhuC9hB"
COORDINATES = "39.48291665,-87.32413881427742"
DARK_SKY_API = "d112efc2c468c79899a1ca27d72b144c"
BLYNK_AUTH = "0SBmcHeg3zIyJEr08uRW1DouR0HC2W2P"
BUCKET_KEY = "FEAKDV6SDUBV"
BUCKET_NAME = "Weather"
UPDATE_RATE = 15

# Initlalize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

def get_current_conditions():
	api_conditions_url = "https://api.darksky.net/forecast/" + DARK_SKY_API + "/" + COORDINATES + "?units=auto"
	try:
		f = urllib2.urlopen(api_conditions_url)
	except:
		return []
	json_currently = f.read()
	f.close()
	return json.loads(json_currently)

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

# Virtual Pin Handler
@blynk.handle_event('write V0')
def write_virtual_pin_handler(pin, value):
	print("In event handler")
	if(value[0] == 0):
		subprocess.call("./turnOffMonitor.sh") # Turns off the HDMI port and is turned back on with a keypress
		print('Turning Off Monitor ...')
	else:
		keyboard.press('a') # Random keypress to turn the monitor back on
		keyboard.release('a')
		print('Turning On Monitor ...')
	

def main():
	url = 'file:///home/debian/ECE434SmartMirror/dashboard.html'
	#webbrowser.open(url)
	#time.sleep(120)

	keyboard = Controller() # Using simulated Keypresses, we can make the chrome window fullscreen
	#keyboard.press(Key.f11)
	#keyboard.release(Key.f11)
	#time.sleep(30)
	
	print('Running Blynk ...')
	while True:
		blynk.run()

	while True:
		# create a Streamer instance
		streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

		curr_conditions = get_current_conditions()

		fortune = json.load(urllib2.urlopen('http://fortunecookieapi.herokuapp.com/v1/cookie'))

		date = json.dumps(json.load(urllib2.urlopen('http://worldtimeapi.org/api/timezone/America/Indianapolis'))['utc_datetime'])
		year = date.split('-')[0].split('"')[1]
		month = date.split('-')[1]
		day = date.split('-')[2].split('T')[0]
		current_date = month + "/" + day + "/" + year

		# send some data
		streamer.log("myLocation", "39.48291665,-87.32413881427742")
		streamer.log("Temperature",curr_conditions['currently']['temperature'])
		streamer.log("Current Forecast",weather_icon(curr_conditions['currently']['icon']))
		streamer.log("Today's Feels Like",curr_conditions['currently']['apparentTemperature'])
		streamer.log("Wind Speed",curr_conditions['currently']['windSpeed'])
		streamer.log("Today's Fortune",fortune[0]['fortune']['message'])
		streamer.log("Today's Date",current_date)

		time.sleep(UPDATE_RATE)

	# flush and close the stream
	streamer.flush()

if __name__ == "__main__":
	main()