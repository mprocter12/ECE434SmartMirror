#!/usr/bin/env python2

from ISStreamer.Streamer import Streamer
from datetime import datetime
import requests
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

# wjdata = requests.get('https://api.weather.gov/gridpoints/TOP/17,53').json()
# print (wjdata['properties']['temperature']['values'][0])

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

# create a Streamer instance
streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

curr_conditions = get_current_conditions()

# send some data
streamer.log("time", current_time)
streamer.log("myNumber", 9)
streamer.log("myLocation", "39.48291665,-87.32413881427742")
streamer.log("Temperature",curr_conditions['currently']['temperature'])

# flush and close the stream
streamer.flush()
