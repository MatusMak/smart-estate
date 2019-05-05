from urllib.request import urlopen, Request
import json


class PlaygroundsProvider():

    def provide(self, lat, lon):
        p_range = 500
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-api-key': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiaGFja2F0aG9uNSIsInJvbGVzIjpbInVzZXIiXSwiaWF0IjoxNTM5MzU2NjUxfQ.XJWj-xHzQxPBtS-ZlXIYVPNdk6zB6jX0wkfuiGb9ivvK5Oo10wEx9lwwCoUqd4fhQZyFZJku6tnAZXaYU6TCXw'
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
        score = min(len(data)*34, 100)

        return {
            'summary': {
                'grade': self.scoreToGrade(score),
                'score': score,
            },
            'data': data,
        }

        return response

    def binary_to_dict(self, the_binary):
        jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
        d = json.loads(jsn)
        return d

    def scoreToGrade(this, score):
        if score > 70:
            return 'good'
        elif score > 40:
            return 'okay'
        return 'bad'
