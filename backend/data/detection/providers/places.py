from urllib.request import urlopen, Request
import json


class PlaygroundsProvider():

    def provide(self, lat, lon):
        p_range = 500
        with open('api_key.txt', 'r') as f:
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'x-api-key': f.readlines()[0].strip(),
            }
        request = Request(f'https://api.mojepraha.eu/v3/playgrounds/?latlng={str(lat)},{str(lon)}&range={p_range}', headers=headers)

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
            score = 45
        elif len(data) == 2:
            score = 80
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


class GardensProvider():

    def provide(self, lat, lon):
        p_range = 1000
        with open('api_key.txt', 'r') as f:
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'x-api-key': f.readlines()[0].strip(),
            }
        request = Request(f'https://api.mojepraha.eu/v3/gardens/?latlng={str(lat)},{str(lon)}&range={p_range}', headers=headers)

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


class LibrariesProvider():

    def provide(self, lat, lon):
        p_range = 750
        with open('api_key.txt', 'r') as f:
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'x-api-key': f.readlines()[0].strip(),
            }
        request = Request(f'https://api.mojepraha.eu/v3/municipal-libraries/?latlng={str(lat)},{str(lon)}&range={p_range}', headers=headers)

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
            score = 70
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
