#!/usr/bin/env python2

from ISStreamer.Streamer import Streamer
from datetime import datetime
import urllib2
import json

ACCESS_KEY = "ist_Zz199NmUJzRKcJivg5cv1L91akhuC9hB"
COORDINATES = "39.48291665,-87.32413881427742"
DARK_SKY_API = "d112efc2c468c79899a1ca27d72b144c"
BUCKET_KEY = "FEAKDV6SDUBV"
BUCKET_NAME = "Weather"

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

def main():

	# create a Streamer instance
	streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

	curr_conditions = get_current_conditions()

	date = json.dumps(json.load(urllib2.urlopen('http://worldtimeapi.org/api/timezone/America/Indianapolis'))['utc_datetime'])
	year = date.split('-')[0].split('"')[1]
	month = date.split('-')[1]
	day = date.split('-')[2].split('T')[0]
	

	# send some data
	streamer.log("myLocation", "39.48291665,-87.32413881427742")
	streamer.log("Temperature",curr_conditions['currently']['temperature'])
	streamer.log("Current Forecast",weather_icon(curr_conditions['currently']['summary']))
	streamer.log("Today's Feels Like",curr_conditions['currently']['apparentTemperature'])
	streamer.log("Wind Speed",curr_conditions['currently']['windSpeed'])

	# flush and close the stream
	streamer.flush()

if __name__ == "__main__":
	main()