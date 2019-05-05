from urllib.request import urlopen, Request
import json

from data.models import Parking, Usage


class ParkingProvider():

    def provide(self, lat, lon):
        p_range = 500
        with open('api_key.txt', 'r') as f:
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'x-api-key': f.readlines()[0].strip(),
            }
        request = Request(f'https://api.mojepraha.eu/v3/parkings/?latlng={str(lat)},{str(lon)}&range={p_range}', headers=headers)

        response = urlopen(request).read().decode('utf8').replace("'", '"')
        response_data = json.loads(response)['features']

        data = []
        if x['properties']['parking_type']['id'] == 1:
            typ = 'Park & Ride'
        elif x['properties']['parking_type']['id'] == 2:
            typ = 'Paid'
        else:
            typ = 'Free'
        for x in response_data:
            data.append({
                'title': x['properties']['name'],
                'address': x['properties']['address'],
                'capacity': x['properties']['total_num_of_places'],
                'type': typ,
                'latitude': x['geometry']['coordinates'][0],
                'longitude': x['geometry']['coordinates'][1],
            })
        if len(data) == 0:
            score = 0
        elif len(data) == 1:
            score = 45
        elif len(data) == 2:
            score = 70
        elif len(data) == 3:
            score = 85
        else:
            score = 100

        return {
            'summary': {
                'grade': self.scoreToGrade(score),
                'score': score,
            },
            'data': data,
        }

        return response

    def scoreToGrade(this, score):
        if score > 70:
            return 'good'
        elif score > 40:
            return 'okay'
        return 'bad'


class ParkingAvailabilityProvider():

    def provide(self, lat, lon):
        parking = self.get_nearest(lat, lon)
        usages = Usage.objects.filter(parking=parking)

        data = []
        for u in usages:
            data.append({
                'title': u.timeslot.name[0].upper()+u.timeslot.name[1:].lower(),
                'relative': int(round(100*(parking.capacity-u.full//u.weight)/parking.capacity, 0)),
                'absolute': parking.capacity-u.full//u.weight,
                'capacity': parking.capacity,
            })
        score = int(round(400*max((((parking.capacity-u.full//u.weight)/parking.capacity)**(1/6)-0.75), 0), 0))

        return {
            'summary': {
                'grade': self.scoreToGrade(score),
                'score': score,
            },
            'data': data,
        }

    def scoreToGrade(self, score):
        if score > 70:
            return 'good'
        elif score > 40:
            return 'okay'
        return 'bad'

    def get_nearest(self, lat, lon):
        parkings = Parking.objects.all()
        best = [
            parkings[0],
            (float(parkings[0].latitude) - lat)**2+(float(parkings[0].longitude) - lon)**2,
        ]

        for p in parkings[1:]:
            temp = [
                p,
                (float(p.latitude) - lat)**2+(float(p.longitude) - lon)**2,
            ]
            if temp[1] < best[1]:
                best = temp

        return best[0]
