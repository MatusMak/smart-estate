from .providers.parking import ParkingProvider

categories = [
    {
        'title': 'Transport',
        'icon': 'ni ni-bus-front-12',
        'weight': 1,
        'providers': [
            {
                'id': 'parking',
                'title': 'Parking',
                'handler': ParkingProvider(),
                'weight': 1,
            }
        ],
    },
]


class Detector():
    def detect(this, lat, lon):
        lat = float(lat)
        lon = float(lon)

        result = {
            'summary': {
                'grade': None,
                'score': 0,
            },
            'categories': [],
        }

        for category in categories:
            providers = []
            score = 0

            for provider in category['providers']:
                partial = provider['handler'].provide(lat, lon)
                score += partial['summary']['score'] * provider['weight']

                partial['title'] = provider['title']
                providers.append(partial)

            result['categories'].append({
                'title': category['title'],
                'icon': category['icon'],

                'summary': {
                    'score': score,
                    'grade': this.scoreToGrade(score),
                },

                'providers': providers,
            })

            result['summary']['score'] += score * category['weight']

        result['summary']['grade'] = this.scoreToGrade(result['summary']['score'])
        return result

    def scoreToGrade(this, score):
        if score > 70:
            return 'good'
        elif score > 40:
            return 'okay'
        return 'bad'
