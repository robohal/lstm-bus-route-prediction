#!/usr/bin/env python

import os
import sys
import csv
import json
import time
from datetime import datetime,timedelta
import urllib.request as ur

bus_num = '83'
bus_id = '1170'

# MetLinkAPIv1StopDeparturesUrl = "https://www.metlink.org.nz/api/v1/StopDepartures/" + stop_code
MetLinkAPIv1BusStopUrl = "https://www.metlink.org.nz/api/v1/ServiceLocation/" + bus_num

# look for updates to bus data
def refreshData():
    response = ur.urlopen(MetLinkAPIv1BusStopUrl)
    raw_json = response.read()
    raw_json = raw_json.decode()
    bus_departures = json.loads(raw_json)
    return bus_departures
# print(bus_departures[0])

# get data for first bus in the list returned from the API.
def getBusData():
    busList = []
    for bus in refreshData()['Services']:
        # filter for a bus that has already started its route
        if bus['HasStarted'] == False:
            break
        # print(bus)
        return bus
        break

def followBus():
    # follow the bus to the end of its route
    pingData = getBusData()
    pingTime = (datetime.strptime(pingData['RecordedAtTime'].split("+")[0], '%Y-%m-%dT%H:%M:%S'))
    print(str(pingTime),pingData['VehicleRef'],pingData['VehicleFeature'],pingData['Bearing'],pingData['DelaySeconds'],pingData['Lat'],pingData['Long'],pingData['Direction'],pingData['OriginStopID'])
    with open('bus.csv', 'a', newline='') as csvfile:
        # write out to the CSV file
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow([str(pingTime),pingData['VehicleRef'],pingData['VehicleFeature'],pingData['Bearing'],pingData['DelaySeconds'],pingData['Lat'],pingData['Long'],pingData['Direction']])
    if getBusData()['HasStarted'] == True:
        print('following bus...')
        pingData = getBusData()
        direction = pingData['Direction']
        try:
            while getBusData()['HasStarted'] == True:
                # keep recording the pings until the bus finishes its route
                pingData = getBusData()
                lastPing = (datetime.strptime(pingData['RecordedAtTime'].split("+")[0], '%Y-%m-%dT%H:%M:%S'))
                time.sleep(30)
                pingData = getBusData()
                newPing = (datetime.strptime(pingData['RecordedAtTime'].split("+")[0], '%Y-%m-%dT%H:%M:%S'))
                # print(pingData)
                if str(newPing) != str(lastPing):
                    print(str(newPing),pingData['VehicleRef'],pingData['VehicleFeature'],pingData['Bearing'],pingData['DelaySeconds'],pingData['Lat'],pingData['Long'],pingData['Direction'],pingData['OriginStopID'])
                    with open('bus.csv', 'a', newline='') as csvfile:
                        csvwriter = csv.writer(csvfile, delimiter=',')
                        csvwriter.writerow([str(newPing),pingData['VehicleRef'],pingData['VehicleFeature'],pingData['Bearing'],pingData['DelaySeconds'],pingData['Lat'],pingData['Long'],pingData['Direction'],pingData['OriginStopID']])
                if direction != pingData['Direction']:
                    print('bus finished its route...')
                    break
        except TypeError:
            print('waiting for a bus...')

# main function that tries every 30 seconds
while True: 
    try:
        followBus()
        time.sleep(30)
    except TypeError:
        time.sleep(30)
        print('waiting for a bus...')