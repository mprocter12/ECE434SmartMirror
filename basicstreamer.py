#!/usr/bin/env python2

from ISStreamer.Streamer import Streamer
from datetime import datetime
import requests

ACCESS_KEY = "ist_Zz199NmUJzRKcJivg5cv1L91akhuC9hB"
BUCKET_KEY = "FEAKDV6SDUBV"
BUCKET_NAME = "Weather"

# wjdata = requests.get('https://api.weather.gov/gridpoints/TOP/17,53').json()
# print (wjdata['properties']['temperature']['values'][0])

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

# create a Streamer instance
streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

# send some data
streamer.log("time", current_time)
streamer.log("myNumber", 9)
streamer.log("myLocation", "39.48291665,-87.32413881427742")

# flush and close the stream
streamer.flush()
