from .providers.transport import ParkingProvider
from .providers.health import AirConditionProvider, MedicalInstitutionsProvider
from .providers.places import PlaygroundsProvider, GardensProvider, LibrariesProvider

categories = [
    {
        'title': 'Transport',
        'icon': 'ni ni-bus-front-12',
        'weight': 1,
        'providers': [
            {
                'id': 'parking-availibility',
                'title': 'Parking Availability',
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
                'id': 'places-medicine',
                'title': 'Medical Institutions',
                'handler': MedicalInstitutionsProvider(),
                'weight': 1,
            },
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
            },
            {
                'id': 'places-gardens',
                'title': 'Gardens',
                'handler': GardensProvider(),
                'weight': 1,
            },
            {
                'id': 'places-libraries',
                'title': 'Libraries',
                'handler': LibrariesProvider(),
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
                scores.append({
                    'score': partial['summary']['score'],
                    'weight': provider['weight']
                })

                partial['id'] = provider['id']
                partial['title'] = provider['title']
                providers.append(partial)

            score = this.avgScore(scores)

            result['categories'].append({
                'title': category['title'],
                'icon': category['icon'],

                'summary': {
                    'score': score,
                    'grade': this.scoreToGrade(score),
                },

                'providers': providers,
            })

            result['summary']['score'].append({
                'score': score,
                'weight': category['weight']
            })

        result['summary']['score'] = this.avgScore(result['summary']['score'])
        result['summary']['grade'] = this.scoreToGrade(result['summary']['score'])
        return result

    def scoreToGrade(this, score):
        if score > 70:
            return 'good'
        elif score > 40:
            return 'okay'
        return 'bad'

    def avgScore(this, scores):
        scoreSum = 0
        lenSum = 0

        for partial in scores:
            scoreSum += partial['score'] * partial['weight']
            lenSum += partial['weight']

        return scoreSum / lenSum
