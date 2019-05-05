from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist

from datetime import time
from os import listdir
from xml.etree import ElementTree as ET

from .models import *
from .detection.detector import Detector

import json


def test(request):
    tests = Test.objects.all()
    return JsonResponse(serialize('json', tests), safe=False)


# Datum a cas; Parkoviste; Obsazenost; Kapacita
def analyze_data():
    with open('data3.txt', 'r') as f:
        data = {}
        for line in f.readlines():
            temp = line.split(';')

            timeblock = temp[0].split()[1].split(':')
            timeblock = time(int(timeblock[0]), int(timeblock[1]), 0)
            if timeblock >= time(21):
                timeslot = 'night'
            elif timeblock >= time(18):
                timeslot = 'evening'
            elif timeblock >= time(15):
                timeslot = 'afternoon'
            elif timeblock >= time(13):
                timeslot = 'noon'
            elif timeblock >= time(10):
                timeslot = 'forenoon'
            elif timeblock >= time(6):
                timeslot = 'morning'
            else:
                timeslot = 'night'

            name = temp[1][4:]
            full = int(temp[2])
            capacity = int(temp[3])

            try:
                usage = data[name]['usage']
            except(KeyError):
                usage = {}
                data[name] = {
                    'capacity': capacity,
                    'usage': {}
                }

            try:
                usage[timeslot][0] += full
                usage[timeslot][1] += 1
            except(KeyError):
                usage[timeslot] = [full, 1]

            data[name]['usage'] = usage

    for parking in data:
        p = Parking.objects.create(
            name=parking,
            capacity=data[parking]['capacity'],
        )

        for usage in data[parking]['usage']:
            t = Timeslot.objects.get(name=usage)
            Usage.objects.create(
                parking=p,
                timeslot=t,
                full=data[parking]['usage'][usage][0],
                weight=data[parking]['usage'][usage][1],
            )


def analyze_chmi():
    # List of all possible sensors
    sensors = ['SO2', 'NO2', 'CO', 'O3', 'PM10']

    sources = listdir('_chmi')
    processedSources = 0

    stations = {}

    # Iterate over each data source - snapshot of hourly data
    for source in sources:
        root = ET.parse('_chmi/' + source).getroot()

        # Iterate over each station in that particular snapshot
        for station in root.findall('Data/station'):
            stationCode = station.find('code').text

            # Make sure to register station if it does not exist
            if stationCode not in stations:
                stations[stationCode] = {
                    'code': stationCode,
                    'name': station.find('name').text,
                    'latitude': station.find('wgs84_latitude').text,
                    'longitude': station.find('wgs84_longitude').text,
                }

            measurements = {}

            # Read partial data and choose the best possible value
            # This weird iteration is necessary - XML structure is horrendous
            for component, averagedTime in zip(station.findall('measurement/component'), station.findall('measurement/averaged_time')):
                sensor = component.text
                value = averagedTime.find('value').text
                period = averagedTime.find('averaged_hours').text

                if sensor not in sensors:
                    continue

                # In case other averaged data from the same sensor exist,
                # choose the one measured over smaller period of time
                if (sensor in measurements and period < measurements[sensor]['period']) or (sensor not in measurements):
                    measurements[sensor] = {
                        'sensor': sensor,
                        'value': value,
                        'period': period,
                    }

            # Commit measurements to station
            for name in measurements:
                measurement = measurements[name]
                # Make sure sensor's array exists
                if name not in stations[stationCode]:
                    stations[stationCode][name] = []
                stations[stationCode][name].append(measurement['value'])

        processedSources += 1
        print('Source processed. ' + str(processedSources) + '/' + str(len(sources)))

    # Average, finalize and save all data
    for stationCode in stations:
        station = stations[stationCode]

        # Finalize data in sensors
        for sensor in sensors:
            if sensor in station:
                data = station[sensor]
                summary = 0
                for value in data:
                    summary += float(value)
                station[sensor] = summary / len(data)
            else:
                station[sensor] = None

        # Commit to database
        AirStation.objects.create(
            name=station['name'],
            code=station['code'],

            latitude=station['latitude'],
            longitude=station['longitude'],

            CO=station['CO'],
            NO2=station['NO2'],
            O3=station['O3'],
            PM10=station['PM10'],
            SO2=station['SO2']
        )


def detect(request, lat, lon):
    detector = Detector()
    result = detector.detect(lat, lon)
    return JsonResponse(result, safe=False)
