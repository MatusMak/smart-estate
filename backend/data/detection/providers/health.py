from urllib.request import urlopen, Request
import json

from data.models import AirStation


class AirConditionProvider():

    def provide(self, lat, lon):
        station = self.get_nearest(lat, lon)
        conditions = self.get_conditions()

        scores = {}

        for code in conditions:
            if getattr(station, code) is None:
                continue
            score = 0
            for level in conditions[code]:
                if getattr(station, code) <= level['limit']:
                    score = level['score']
                    break
            scores[code] = score

        scoreSum = 0
        for code in scores:
            scoreSum += scores[code]
        score = scoreSum / len(scores)

        data = []
        for code in scores:
            data.append({
                'code': code,
                'level': getattr(station, code),
                'score': scores[code],
            })

        return {
            'summary': {
                'grade': self.scoreToGrade(score),
                'score': score,
            },
            'data': data,
        }


    def scoreToGrade(self, score):
        if score > 80:
            return 'good'
        elif score > 60:
            return 'okay'
        return 'bad'

    def get_nearest(self, lat, lon):
        parkings = AirStation.objects.all()
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

    def get_conditions(self):
        return {
            'SO2': [
                {
                    'limit': 20,
                    'score': 100,
                },
                {
                    'limit': 50,
                    'score': 80,
                },
                {
                    'limit': 120,
                    'score': 60,
                },
                {
                    'limit': 350,
                    'score': 30,
                },
                {
                    'limit': 500,
                    'score': 10,
                },
            ],
            'NO2': [
                {
                    'limit': 20,
                    'score': 100,
                },
                {
                    'limit': 50,
                    'score': 80,
                },
                {
                    'limit': 100,
                    'score': 60,
                },
                {
                    'limit': 200,
                    'score': 30,
                },
                {
                    'limit': 400,
                    'score': 10,
                },
            ],
            'CO': [
                {
                    'limit': 1000,
                    'score': 100,
                },
                {
                    'limit': 2000,
                    'score': 80,
                },
                {
                    'limit': 4000,
                    'score': 60,
                },
                {
                    'limit': 10000,
                    'score': 30,
                },
                {
                    'limit': 30000,
                    'score': 10,
                },
            ],
            'O3': [
                {
                    'limit': 33,
                    'score': 100,
                },
                {
                    'limit': 65,
                    'score': 80,
                },
                {
                    'limit': 120,
                    'score': 60,
                },
                {
                    'limit': 180,
                    'score': 30,
                },
                {
                    'limit': 240,
                    'score': 10,
                },
            ],
            'PM10': [
                {
                    'limit': 20,
                    'score': 100,
                },
                {
                    'limit': 40,
                    'score': 80,
                },
                {
                    'limit': 70,
                    'score': 60,
                },
                {
                    'limit': 90,
                    'score': 30,
                },
                {
                    'limit': 180,
                    'score': 10,
                },
            ],
        }


class MedicalInstitutionsProvider():

    def provide(self, lat, lon):
        p_range = 500
        with open('api_key.txt', 'r') as f:
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'x-api-key': f.readlines()[0].strip(),
            }
        request = Request(f'https://api.mojepraha.eu/v3/medical-institutions/?latlng={str(lat)},{str(lon)}&range={p_range}', headers=headers)

        response = urlopen(request).read().decode('utf8').replace("'", '"')
        response_data = json.loads(response)['features']

        data = []
        for x in response_data:
            data.append({
                'title': x['properties']['name'],
                'address': x['properties']['address'],
                'latitude': x['geometry']['coordinates'][0],
                'longitude': x['geometry']['coordinates'][1],
            })
        if len(data) == 0:
            score = 0
        elif len(data) == 1:
            score = 40
        elif len(data) == 2:
            score = 65
        elif len(data) == 3:
            score = 85
        elif len(data) == 4:
            score = 95
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
