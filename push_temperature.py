#!/usr/bin/env python

import argparse
import datetime
import os
import re
import requests
import subprocess
import time
import xively

DEBUG = os.environ["DEBUG"] or false

def read_temperature(from_file):
  if DEBUG:
    print "Reading temperature from file: %s" % from_file

  temperature = None

  with open(from_file, 'r') as f:
    crc = f.readline()
    reading = f.readline()

    matches = re.search('t=(\d+)', reading)
    if matches:
      temperature = float(matches.group(1)) / 1000.0
  return temperature

def get_datastream(feed, name):
  try:
    datastream = feed.datastreams.get(name)

    if DEBUG:
      print "Found existing datastream"

    return datastream
  except:
    if DEBUG:
      print "Creating new datastream"

    datastream = feed.datastreams.create(name, tags="units=celsius")

    return datastream

def run():
  parser = argparse.ArgumentParser(description = 'Push a metric to Xively')
  parser.add_argument('--feed', type=str, required=True, help='your Xively feed ID')
  parser.add_argument('--key', type=str, required=True, help='your Xively API key')
  parser.add_argument('--name', type=str, default='temperature0', help='your Xively datastream name')
  parser.add_argument('--file', type=str, required=True, help='the file from which to read the temperature')

  args = parser.parse_args()

  api = xively.XivelyAPIClient(args.key)
  feed = api.feeds.get(args.feed)

  datastream = get_datastream(feed, args.name)
  datastream.max_value = None
  datastream.min_value = None

  while True:
    temperature = read_temperature(args.file)

    if DEBUG:
      print "Updating Xively feed with value: %s" % temperature

    datastream.current_value = temperature
    datastream.at = datetime.datetime.utcnow()

    try:
      datastream.update()
    except requests.HTTPError as e:
      print "HTTPError({0}): {1}".format(e.errno, e.strerror)

    print "Updated Xively feed, sleeping..."
    time.sleep(60)

run()
