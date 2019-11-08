#!/usr/bin/env python3

from ISStreamer.Streamer import Streamer

ACCESS_KEY = "ist_Zz199NmUJzRKcJivg5cv1L91akhuC9hB"
BUCKET_KEY = "FEAKDV6SDUBV"
BUCKET_NAME = "Weather"

# create a Streamer instance
streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

# send some data
streamer.log("myNumber", 7)

# flush and close the stream
streamer.flush()