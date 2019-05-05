from .providers.parking import ParkingProvider
from .providers.aircondition import AirConditionProvider
from .providers.playgrounds import PlaygroundsProvider

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
    {
        'title': 'Health',
        'icon': 'ni ni-favourite-28',
        'weight': 1,
        'providers': [
            {
                'id': 'aircondition',
                'title': 'Air Condition',
                'handler': AirConditionProvider(),
                'weight': 1,
            }
        ],
    },
    {
        'title': 'Places',
        'icon': 'ni ni-shop',
        'weight': 1,
        'providers': [
            {
                'id': 'places-playgrounds',
                'title': 'Playgrounds',
                'handler': PlaygroundsProvider(),
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
                'score': [],
            },
            'categories': [],
        }

        for category in categories:
            providers = []
            scores = []

            for provider in category['providers']:
                partial = provider['handler'].provide(lat, lon)
                scores.append(partial['summary']['score'] * provider['weight'])

                partial['id'] = provider['id']
                partial['title'] = provider['title']
                providers.append(partial)

            score = sum(scores) / len(scores)

            result['categories'].append({
                'title': category['title'],
                'icon': category['icon'],

                'summary': {
                    'score': score,
                    'grade': this.scoreToGrade(score),
                },

                'providers': providers,
            })

            result['summary']['score'].append(score * category['weight'])

        result['summary']['score'] = sum(result['summary']['score']) / len(result['summary']['score'])
        result['summary']['grade'] = this.scoreToGrade(result['summary']['score'])
        return result

    def scoreToGrade(this, score):
        if score > 70:
            return 'good'
        elif score > 40:
            return 'okay'
        return 'bad'
